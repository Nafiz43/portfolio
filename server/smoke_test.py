"""Opt-in real-model test through the public tunnel; does not book an appointment."""
import json
import time
import urllib.request

BASE = "https://cattle-scratch-parlor.ngrok-free.dev"


def request(path, data=None, method=None, extra_headers=None):
    headers = {"ngrok-skip-browser-warning": "1", "Origin": "https://nafiz43.github.io"}
    headers.update(extra_headers or {})
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE + path, data=json.dumps(data).encode() if data is not None else None,
                                 headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=110) as response:
        assert response.headers.get("Access-Control-Allow-Origin") == "https://nafiz43.github.io"
        body = response.read().decode()
        return json.loads(body) if body.startswith("{") else body


def main():
    assert request("/api/health")["model_ready"]
    request("/api/chat", method="OPTIONS", extra_headers={
        "Access-Control-Request-Method": "POST", "Access-Control-Request-Headers": "content-type,ngrok-skip-browser-warning"})
    session = None
    for question in ["Tell me about AngioVision.", "What kind of data does that project use?", "Can I schedule a meeting with Nafiz?"]:
        start = time.monotonic()
        result = request("/api/chat", {"message": question, "session_id": session})
        session = result["session_id"]
        assert result["answer"]
        if "meeting" in question:
            assert result["actions"][0]["url"] == "https://calendar.app.google/bNG7fkvhgRykj2Ba7"
            assert "does not reserve or confirm" in result["answer"]
        else:
            assert "DICOM" in result["answer"]
            assert result["sources"]
        print(f"PASS ({time.monotonic() - start:.1f}s): {question}\n{result['answer']}\n", flush=True)
    print("Public endpoint, CORS, real-model answers, conversation follow-up and booking action passed.")


if __name__ == "__main__":
    main()
