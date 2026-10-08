import json
import stat
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

import httpx
from server.app import app, harness
from server.audit import audit, AuditLog, conversation_id


class AuditTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.directory = Path(self.temp.name) / "logs"
        self.patch = patch.object(audit, "directory", self.directory)
        self.patch.start()
        self.prompt_patch = patch("server.app.load_prompt", return_value=("Test configuration {{date}} {{context}}", "test-version"))
        self.prompt_patch.start()
        self.client = httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test")

    async def asyncTearDown(self):
        await self.client.aclose()
        self.patch.stop()
        self.prompt_patch.stop()
        self.temp.cleanup()

    def records(self):
        return [json.loads(line) for file in self.directory.glob("*.jsonl") for line in file.read_text().splitlines()]

    async def test_full_request_and_response_saved_without_session_token(self):
        response = {"answer": "Hello, visitor!", "session_id": "secret-session", "sources": [],
                    "actions": [{"type": "booking", "url": "https://calendar.app.google/test"}]}
        with patch.object(harness, "chat", AsyncMock(return_value=response)):
            result = await self.client.post("/api/chat", json={"message": "Hi\nUnicode: café", "session_id": "secret-session"})
        self.assertEqual(result.status_code, 200)
        records = self.records()
        self.assertEqual([r["event"] for r in records], ["request_received", "response_ready", "response_sent"])
        self.assertEqual(len({r["request_id"] for r in records}), 1)
        self.assertEqual(records[0]["body"]["message"], "Hi\nUnicode: café")
        self.assertEqual(records[1]["body"]["answer"], "Hello, visitor!")
        self.assertEqual(records[1]["body"]["conversation_id"], conversation_id("secret-session"))
        self.assertNotIn("secret-session", json.dumps(records))
        transcript = next(self.directory.glob("*.md")).read_text()
        self.assertIn("Unicode: café", transcript)
        self.assertIn("Hello, visitor!", transcript)
        self.assertIn("https://calendar.app.google/test", transcript)
        self.assertEqual(stat.S_IMODE(self.directory.stat().st_mode), 0o700)
        for file in self.directory.iterdir():
            self.assertEqual(stat.S_IMODE(file.stat().st_mode), 0o600)

    async def test_model_inputs_and_outputs_are_recorded(self):
        # Patch the existing HTTP client's post method only; API traffic uses ASGI.
        model = AsyncMock()
        model.__aenter__.return_value = model
        model.post.return_value = httpx.Response(200, request=httpx.Request("POST", "http://ollama/api/chat"),
            json={"message": {"content": json.dumps({"answer": "A researcher.", "source_ids": [], "offer_booking": False})},
                  "eval_count": 12})
        with patch("server.app.httpx.AsyncClient", return_value=model):
            result = await self.client.post("/api/chat", json={"message": "Who is Nafiz?"})
        self.assertEqual(result.status_code, 200)
        records = self.records()
        model_request = next(r for r in records if r["event"] == "model_request")
        self.assertIn('"entities":', model_request["payload"]["messages"][0]["content"])
        self.assertEqual(next(r for r in records if r["event"] == "model_response")["payload"]["eval_count"], 12)
        self.assertEqual(len({r["request_id"] for r in records}), 1)

    async def test_errors_and_visitor_actions_recorded(self):
        response = await self.client.post("/api/chat", json={"message": " "})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(next(r for r in self.records() if r["event"] == "response_ready")["status"], 422)
        response = await self.client.post("/api/events", json={"event": "booking_opened", "session_id": "token"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(r.get("body", {}).get("event") == "booking_opened" for r in self.records()))

    async def test_unwritable_audit_fails_closed(self):
        with patch.object(audit, "record", side_effect=OSError("disk full")), patch.object(harness, "chat", AsyncMock()) as model:
            response = await self.client.post("/api/chat", json={"message": "Hello"}, headers={"Origin": "https://nafiz43.github.io"})
        self.assertEqual(response.status_code, 503)
        self.assertIn("recording", response.json()["detail"])
        self.assertEqual(response.headers["access-control-allow-origin"], "https://nafiz43.github.io")
        model.assert_not_called()

    async def test_append_survives_new_logger_instance(self):
        AuditLog(self.directory).record("first")
        AuditLog(self.directory).record("second")
        self.assertEqual([r["event"] for r in self.records()], ["first", "second"])
        self.assertEqual((await self.client.get("/Portfolio%20Chat%20Logs/")).status_code, 404)


if __name__ == "__main__":
    unittest.main()
