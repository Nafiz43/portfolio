"""Run with: python3 -m uvicorn server.app:app --host 127.0.0.1 --port 5000 --no-proxy-headers"""
import asyncio
import json
import os
import re
import secrets
import time
from collections import OrderedDict, defaultdict, deque
from contextlib import asynccontextmanager, suppress
from datetime import datetime
from typing import Annotated
from urllib.parse import urlparse

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from server.knowledge import KnowledgeGraph, ROOT
from server.audit import audit, AuditMiddleware, conversation_id
from server.prompts import load_prompt
from server.guardrails import inspect_input, refusal, scope_redirect, ungrounded_response, output_leaks_prompt

MODEL = os.getenv("OLLAMA_MODEL", "qwen3:8b")
OLLAMA = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")
BOOKING_URL = os.getenv("BOOKING_URL", "https://calendar.app.google/bNG7fkvhgRykj2Ba7")
PUBLIC_URL = "https://cattle-scratch-parlor.ngrok-free.dev"
if urlparse(BOOKING_URL).scheme != "https":
    raise ValueError("BOOKING_URL must use HTTPS")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", ",".join([
    "https://nafiz43.github.io", PUBLIC_URL, "http://localhost:5000", "http://127.0.0.1:5000",
])).split(",")
graph = KnowledgeGraph()


@asynccontextmanager
async def lifespan(app):
    _, prompt_version = load_prompt()
    audit.record("server_started", model=MODEL, graph_fingerprint=graph.graph["fingerprint"], prompt_version=prompt_version)
    async def expire_sessions():
        while True:
            await asyncio.sleep(30)
            harness.expire()
    task = asyncio.create_task(expire_sessions())
    yield
    task.cancel()
    with suppress(asyncio.CancelledError):
        await task
    audit.record("server_stopped")


app = FastAPI(title="Portfolio assistant", lifespan=lifespan, docs_url=None, redoc_url=None, openapi_url=None)
app.add_middleware(CORSMiddleware, allow_origins=ALLOWED_ORIGINS,
                   allow_methods=["GET", "POST", "OPTIONS"],
                   allow_headers=["Content-Type", "ngrok-skip-browser-warning"], max_age=600)


class RequestLimits:
    """Bound the request body before JSON parsing."""
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        headers = dict(scope.get("headers", []))
        origin = headers.get(b"origin", b"").decode()
        if origin and origin not in ALLOWED_ORIGINS:
            return await JSONResponse({"detail": "Origin not allowed."}, status_code=403)(scope, receive, send)
        total = 0
        chunks = []
        while True:
            event = await receive()
            if event["type"] == "http.disconnect":
                return
            total += len(event.get("body", b""))
            if total > 16384:
                return await JSONResponse({"detail": "Message is too large."}, status_code=413)(scope, receive, send)
            chunks.append(event)
            if not event.get("more_body", False):
                break

        async def replay():
            return chunks.pop(0) if chunks else await receive()

        async def secure_send(event):
            if event["type"] == "http.response.start":
                event.setdefault("headers", []).extend([
                    (b"x-content-type-options", b"nosniff"),
                    (b"referrer-policy", b"strict-origin-when-cross-origin"),
                    (b"cache-control", b"no-store"),
                ])
            await send(event)
        await self.app(scope, replay, secure_send)


app.add_middleware(RequestLimits)
app.add_middleware(AuditMiddleware)


class ChatRequest(BaseModel):
    message: Annotated[str, Field(min_length=1, max_length=2000)]
    session_id: Annotated[str | None, Field(max_length=100)] = None


class Harness:
    def __init__(self):
        self.sessions = OrderedDict()
        self.rates = defaultdict(deque)
        self.global_rate = deque()
        self.lock = asyncio.Lock()

    def check_rate(self, client):
        now = time.monotonic()
        for key in list(self.rates):
            if not self.rates[key] or self.rates[key][-1] < now - 60:
                del self.rates[key]
        queue = self.rates[client]
        for q in [queue, self.global_rate]:
            while q and q[0] < now - 60:
                q.popleft()
        if len(queue) >= 10 or len(self.global_rate) >= 30:
            raise HTTPException(429, "Too many messages. Please try again in a minute.")
        queue.append(now)
        self.global_rate.append(now)

    def expire(self):
        now = time.monotonic()
        for key in list(self.sessions):
            if self.sessions[key]["updated"] < now - 3600:
                del self.sessions[key]

    def session(self, identifier):
        self.expire()
        now = time.monotonic()
        if identifier not in self.sessions:
            identifier = secrets.token_urlsafe(32)
            self.sessions[identifier] = {"history": [], "updated": now}
        self.sessions.move_to_end(identifier)
        while len(self.sessions) > 200:
            self.sessions.popitem(last=False)
        self.sessions[identifier]["updated"] = now
        return identifier, self.sessions[identifier]

    async def chat(self, message, identifier):
        if self.lock.locked():
            raise HTTPException(429, "The assistant is answering another visitor. Please try again shortly.")
        async with self.lock:
            identifier, session = self.session(identifier)
            history = session["history"][-10:]
            reason = inspect_input(message)
            if reason:
                audit.model_event("guardrail_blocked", reason=reason, conversation_id=conversation_id(identifier))
                return {"answer": refusal(reason), "session_id": identifier, "sources": [], "actions": []}
            # Include preceding user turns to resolve conversational follow-ups.
            preceding = " ".join(m["content"] for m in history[-4:] if m["role"] == "user")
            nodes, edges = graph.search(message + " " + preceding)
            context = {"publication_count": graph.graph["publication_count"],
                       "entities": [{**n, "text": n["text"][:2200]} for n in nodes], "relationships": edges}
            template, prompt_version = load_prompt()
            system = template.replace("{{date}}", datetime.now().date().isoformat()).replace(
                "{{context}}", json.dumps(context, ensure_ascii=False))
            schema = {"type": "object", "properties": {
                "answer": {"type": "string"},
                "source_ids": {"type": "array", "items": {"type": "string"}},
                "offer_booking": {"type": "boolean"},
                "scope": {"type": "string", "enum": ["portfolio", "greeting", "booking", "unknown", "out_of_scope"]},
            }, "required": ["answer", "source_ids", "offer_booking", "scope"], "additionalProperties": False}
            payload = {"model": MODEL, "messages": [{"role": "system", "content": system}, *history,
                        {"role": "user", "content": message}], "stream": False, "think": False,
                       "format": schema, "keep_alive": "15m",
                       "options": {"temperature": 0.55, "num_ctx": 8192, "num_predict": 700}}
            audit.model_event("model_request", conversation_id=conversation_id(identifier),
                              graph_fingerprint=graph.graph["fingerprint"], prompt_version=prompt_version, payload=payload)
            try:
                async with httpx.AsyncClient(timeout=100, trust_env=False) as client:
                    response = await client.post(OLLAMA + "/api/chat", json=payload)
                    response.raise_for_status()
                    model_response = response.json()
                    audit.model_event("model_response", conversation_id=conversation_id(identifier), payload=model_response)
                    result = json.loads(model_response["message"]["content"])
                if not isinstance(result, dict) or not isinstance(result.get("answer"), str) or not result["answer"].strip():
                    raise ValueError("Empty model response")
            except (httpx.HTTPError, ValueError, KeyError, TypeError) as error:
                audit.model_event("model_error", conversation_id=conversation_id(identifier), error_type=type(error).__name__)
                raise HTTPException(503, "The assistant is temporarily unavailable. Please try again, or use Schedule a meeting.") from None
            # Only the server's verified source URLs and booking URL reach the UI.
            ids = result.get("source_ids", [])
            sources, seen = [], set()
            for node in nodes:
                if isinstance(ids, list) and node["id"] in ids and node["source"] not in seen:
                    if urlparse(node["source"]).scheme == "https":
                        sources.append({"title": node["label"], "url": node["source"]})
                        seen.add(node["source"])
            meeting_intent = bool(re.search(r"\b(meet(?:ing)?|book(?:ing)?|schedul\w*|availability|appointment|calendar)\b", message, re.I))
            offer_booking = result.get("offer_booking") is True or meeting_intent
            answer = result["answer"].strip()[:6000]
            scope = result.get("scope", "portfolio")
            reason = None
            if output_leaks_prompt(answer, template):
                reason, answer = "prompt_leak", refusal("prompt_extraction")
            elif scope == "out_of_scope":
                reason, answer = "out_of_scope", scope_redirect()
            elif scope == "unknown" or (scope == "portfolio" and not sources and not offer_booking):
                reason, answer = "missing_evidence", ungrounded_response()
            if reason:
                audit.model_event("guardrail_blocked", reason=reason, conversation_id=conversation_id(identifier))
                sources = []
                offer_booking = False
            # Booking facts are deterministic, not a language model's claim.
            if offer_booking:
                answer = "Let’s turn the conversation into a calendar event—without the scheduling email tennis. Open Nafiz’s Google Calendar booking page below, choose an available time, and complete your booking there. This chat does not reserve or confirm a time."
                sources = []
            session["history"] = [*history, {"role": "user", "content": message},
                                  {"role": "assistant", "content": answer}][-12:]
            session["updated"] = time.monotonic()
            return {"answer": answer, "session_id": identifier, "sources": sources[:4],
                    "actions": [{"type": "booking", "label": "Choose a meeting time", "url": BOOKING_URL}] if offer_booking else []}


harness = Harness()


@app.get("/api/health")
async def health():
    ready = False
    try:
        async with httpx.AsyncClient(timeout=3, trust_env=False) as client:
            response = await client.get(OLLAMA + "/api/tags")
            ready = any(m.get("name") == MODEL for m in response.json().get("models", []))
    except (httpx.HTTPError, ValueError):
        pass
    return {"status": "ok" if ready else "degraded", "model_ready": ready,
            "graph_nodes": len(graph.nodes), "graph_edges": len(graph.graph["edges"])}


@app.get("/api/config")
async def config():
    return {"booking_url": BOOKING_URL, "booking_mode": "google_calendar", "session_ttl_seconds": 3600,
            "transcripts_saved": True, "transcript_retention": "Until deleted by the site owner"}


class VisitorEvent(BaseModel):
    event: Annotated[str, Field(pattern=r"^(booking_opened|new_chat)$")]
    session_id: Annotated[str | None, Field(max_length=100)] = None


@app.post("/api/events")
async def visitor_event(body: VisitorEvent, request: Request):
    # AuditMiddleware persists this visitor-reported action. A click is not a booking.
    harness.check_rate(client_address(request))
    return {"recorded": True}


def client_address(request):
    client = request.client.host if request.client else "unknown"
    # ngrok connects locally and appends the real client address. Ignore a supplied
    # chain's earlier entries, and never trust proxy headers from remote peers.
    if client in {"127.0.0.1", "::1"}:
        client = request.headers.get("x-forwarded-for", client).split(",")[-1].strip()
    return client


@app.post("/api/chat")
async def chat(body: ChatRequest, request: Request):
    message = body.message.strip()
    if not message:
        raise HTTPException(422, "Please enter a message.")
    harness.check_rate(client_address(request))
    return await harness.chat(message, body.session_id)


@app.get("/")
async def homepage():
    return FileResponse(ROOT / "index.html")


# Explicit public assets only. Never mount the repository root (which includes .git).
for directory in ["css", "js", "img", "vendor"]:
    app.mount("/" + directory, StaticFiles(directory=ROOT / directory), name=directory)


@app.get("/data/publications.json")
async def publications():
    return FileResponse(ROOT / "data/publications.json")
