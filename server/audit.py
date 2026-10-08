"""Durable, append-only JSONL audit records, outside the public repository."""
import contextvars
import hashlib
import json
import os
import secrets
import threading
from datetime import datetime, timezone
from pathlib import Path

from starlette.responses import JSONResponse

request_id = contextvars.ContextVar("audit_request_id", default=None)


def conversation_id(token):
    # Correlate conversations without saving their live bearer/session tokens.
    return hashlib.sha256(token.encode()).hexdigest() if isinstance(token, str) and token else None


class AuditLog:
    def __init__(self, directory=None):
        self.directory = Path(directory or os.getenv("AUDIT_DIR", str(Path.home() / "Documents/Portfolio Chat Logs")))
        self.lock = threading.Lock()

    @staticmethod
    def append(path, data):
        fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
        try:
            view = memoryview(data)
            while view:
                written = os.write(fd, view)
                if written == 0:
                    raise OSError("Audit write made no progress")
                view = view[written:]
            os.fsync(fd)
        finally:
            os.close(fd)

    def record(self, event, **fields):
        now = datetime.now(timezone.utc)
        record = {"version": 1, "timestamp": now.isoformat(), "event_id": secrets.token_hex(16),
                  "request_id": request_id.get(), "event": event, **fields}
        data = (json.dumps(record, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")
        with self.lock:
            self.directory.mkdir(parents=True, exist_ok=True, mode=0o700)
            path = self.directory / (now.strftime("%Y-%m-%d") + ".jsonl")
            self.append(path, data)
            if event in {"request_received", "response_ready"}:
                body = fields.get("body", {})
                role = "Visitor" if event == "request_received" else "Assistant / server"
                if isinstance(body, dict):
                    text = body.get("message") if event == "request_received" else body.get("answer", body.get("detail"))
                    if text is None:
                        text = json.dumps(body, ensure_ascii=False)
                else:
                    text = json.dumps(body, ensure_ascii=False)
                if not isinstance(text, str):
                    text = json.dumps(text, ensure_ascii=False)
                lines = "\n".join("    " + line for line in text.splitlines())
                readable = f"\n## {now.isoformat()} — {role}\n\nRequest: {record['request_id']}\n\n{lines}\n"
                if isinstance(body, dict):
                    metadata = {k: body[k] for k in ["conversation_id", "sources", "actions"] if body.get(k)}
                    if metadata:
                        readable += "\n    " + json.dumps(metadata, ensure_ascii=False) + "\n"
                self.append(path.with_suffix(".md"), readable.encode("utf-8"))
        return record

    def model_event(self, event, **fields):
        if request_id.get():
            self.record(event, **fields)


audit = AuditLog()


def sanitized_body(raw):
    try:
        value = json.loads(raw)
    except (ValueError, UnicodeDecodeError):
        return {"raw_body": raw.decode("utf-8", errors="replace")}
    def redact(item):
        if isinstance(item, dict):
            return {("conversation_id" if key == "session_id" else key):
                    (conversation_id(val) if key == "session_id" else redact(val)) for key, val in item.items()}
        if isinstance(item, list):
            return [redact(i) for i in item]
        return item
    return redact(value)


class AuditMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or scope.get("path") not in {"/api/chat", "/api/events"} or scope.get("method") != "POST":
            return await self.app(scope, receive, send)
        import asyncio
        import time
        started = time.monotonic()
        token = request_id.set(secrets.token_hex(16))
        received, response_body = bytearray(), bytearray()
        request_logged = False
        response_started = False
        response_finished = False
        response_start = None

        def log_request():
            nonlocal request_logged
            if not request_logged:
                headers = dict(scope.get("headers", []))
                audit.record("request_received", path=scope["path"],
                             origin=headers.get(b"origin", b"").decode(errors="replace"),
                             body=sanitized_body(bytes(received)),
                             body_limit_bytes=16384)
                request_logged = True

        async def audited_receive():
            event = await receive()
            if event["type"] == "http.request":
                received.extend(event.get("body", b"")[:max(0, 16384 - len(received))])
                if not event.get("more_body", False) or len(received) >= 16384:
                    log_request()
            elif event["type"] == "http.disconnect":
                log_request()
                audit.record("client_disconnected")
            return event

        async def audited_send(event):
            nonlocal response_start, response_started, response_finished
            if event["type"] == "http.response.start":
                response_start = event
                return
            if event["type"] == "http.response.body":
                response_body.extend(event.get("body", b""))
                if event.get("more_body", False):
                    return
                log_request()
                audit.record("response_ready", status=response_start["status"],
                             elapsed_ms=round((time.monotonic() - started) * 1000),
                             body=sanitized_body(bytes(response_body)))
                await send(response_start)
                response_started = True
                await send({"type": "http.response.body", "body": bytes(response_body)})
                response_finished = True
                audit.record("response_sent", status=response_start["status"])

        try:
            await self.app(scope, audited_receive, audited_send)
        except OSError:
            # Never return an unrecorded successful chat if the disk is unavailable.
            if not response_started:
                headers = dict(scope.get("headers", []))
                origin = headers.get(b"origin", b"").decode(errors="replace")
                from server.app import ALLOWED_ORIGINS
                cors = {"Access-Control-Allow-Origin": origin, "Vary": "Origin"} if origin in ALLOWED_ORIGINS else {}
                await JSONResponse({"detail": "Chat recording is temporarily unavailable. Please try again later."},
                                   status_code=503, headers=cors)(scope, receive, send)
            else:
                raise
        except BaseException as error:
            log_request()
            audit.record("request_cancelled" if isinstance(error, asyncio.CancelledError) else "request_failed",
                         error_type=type(error).__name__, response_finished=response_finished)
            raise
        finally:
            request_id.reset(token)
