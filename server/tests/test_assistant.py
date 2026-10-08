import asyncio
import json
import time
import unittest
from unittest.mock import AsyncMock, patch

import httpx
from fastapi import HTTPException
from server.app import app, Harness, graph, BOOKING_URL


class GraphTests(unittest.TestCase):
    def test_graph_covers_portfolio_and_relationships(self):
        self.assertGreaterEqual(graph.graph["publication_count"], 42)
        ids = set(graph.nodes)
        for edge in graph.graph["edges"]:
            self.assertIn(edge["source"], ids)
            self.assertIn(edge["target"], ids)
        self.assertTrue({"authored", "educated_at", "at_organization", "about_topic", "describes_project"}.issubset(
            {e["relation"] for e in graph.graph["edges"]}))

    def test_project_retrieval_follows_source_relationships(self):
        nodes, edges = graph.search("Tell me about AngioVision")
        self.assertTrue(any(n["label"] == "AngioVision" for n in nodes))
        self.assertTrue(any("multi-sequence DICOM" in n["text"] for n in nodes))
        self.assertTrue(any(e["relation"] == "describes_project" for e in edges))

    def test_dates_and_awards_available(self):
        nodes, _ = graph.search("BetterHelp internship")
        self.assertTrue(any("June 2026 - September 2026" in n["text"] for n in nodes))
        nodes, _ = graph.search("RepoWise award")
        self.assertTrue(any("Best Paper Award" in n["text"] for n in nodes))


class HarnessTests(unittest.IsolatedAsyncioTestCase):
    def model(self, answer, ids=None, booking=False):
        result = {"answer": answer, "source_ids": ids or [], "offer_booking": booking}
        client = AsyncMock()
        client.post.return_value = httpx.Response(200, json={"message": {"content": json.dumps(result)}},
                                                request=httpx.Request("POST", "http://ollama/api/chat"))
        client.__aenter__.return_value = client
        return client

    async def test_sources_cannot_be_invented_by_model(self):
        model = self.model("Nafiz is a researcher.", [graph.graph["person"], "https://evil.example", "made-up"])
        with patch("server.app.httpx.AsyncClient", return_value=model):
            result = await Harness().chat("Who is Nafiz?", None)
        self.assertEqual(len(result["sources"]), 1)
        self.assertEqual(result["sources"][0]["url"], "https://nafiz43.github.io/portfolio/#about")

    async def test_booking_cannot_falsely_confirm_event(self):
        model = self.model("Your meeting is confirmed for tomorrow.", booking=True)
        with patch("server.app.httpx.AsyncClient", return_value=model):
            result = await Harness().chat("Schedule a meeting tomorrow", None)
        self.assertIn("does not reserve or confirm", result["answer"])
        self.assertEqual(result["actions"][0]["url"], BOOKING_URL)

    async def test_conversation_history_is_server_owned_and_isolated(self):
        harness = Harness()
        model = self.model("An answer.")
        with patch("server.app.httpx.AsyncClient", return_value=model):
            one = await harness.chat("Tell me about AngioVision", None)
            await harness.chat("What is it for?", one["session_id"])
            payload = model.post.call_args.kwargs["json"]
            self.assertEqual(payload["messages"][1]["content"], "Tell me about AngioVision")
            two = await harness.chat("Hi", "visitor-selected-session")
            self.assertNotEqual(two["session_id"], "visitor-selected-session")
            self.assertNotEqual(two["session_id"], one["session_id"])
            self.assertEqual(len(model.post.call_args.kwargs["json"]["messages"]), 2)

    async def test_offline_model_returns_controlled_error(self):
        model = self.model("unused")
        model.post.side_effect = httpx.ConnectError("private host information")
        with patch("server.app.httpx.AsyncClient", return_value=model):
            with self.assertRaises(HTTPException) as error:
                await Harness().chat("Hi", None)
        self.assertEqual(error.exception.status_code, 503)
        self.assertNotIn("private", error.exception.detail)

    async def test_concurrent_generation_is_bounded(self):
        harness = Harness()
        async with harness.lock:
            with self.assertRaises(HTTPException) as error:
                await harness.chat("Hi", None)
        self.assertEqual(error.exception.status_code, 429)

    def test_session_expiry_and_rate_limit(self):
        harness = Harness()
        identifier, session = harness.session(None)
        session["updated"] = time.monotonic() - 3601
        other, _ = harness.session(identifier)
        self.assertNotEqual(identifier, other)
        self.assertNotIn(identifier, harness.sessions)
        for _ in range(10):
            harness.check_rate("client")
        with self.assertRaises(HTTPException):
            harness.check_rate("client")


class APITests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.client = httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test")

    async def asyncTearDown(self):
        await self.client.aclose()

    async def test_browser_cors_preflight(self):
        response = await self.client.options("/api/chat", headers={"Origin": "https://nafiz43.github.io",
            "Access-Control-Request-Method": "POST", "Access-Control-Request-Headers": "content-type,ngrok-skip-browser-warning"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["access-control-allow-origin"], "https://nafiz43.github.io")
        response = await self.client.post("/api/chat", headers={"Origin": "https://evil.example"}, json={"message": "Hi"})
        self.assertEqual(response.status_code, 403)

    async def test_rejects_oversized_and_invalid_messages(self):
        for data in [{"message": " "}, {"message": "x" * 2001}, {"message": 4}]:
            self.assertEqual((await self.client.post("/api/chat", json=data)).status_code, 422)
        response = await self.client.post("/api/chat", content=b"x" * 17000)
        self.assertEqual(response.status_code, 413)

    async def test_only_public_assets_exposed(self):
        for path in ["/.git/config", "/server/app.py", "/.env", "/server/knowledge_graph.json", "/data/publications.manual.json"]:
            self.assertEqual((await self.client.get(path)).status_code, 404)
        self.assertEqual((await self.client.get("/js/chat.js")).status_code, 200)
        self.assertEqual((await self.client.get("/api/config")).json()["booking_url"], BOOKING_URL)


if __name__ == "__main__":
    unittest.main()
