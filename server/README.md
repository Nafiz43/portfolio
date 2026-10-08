# Portfolio conversation server

The GitHub Pages chat widget calls `https://cattle-scratch-parlor.ngrok-free.dev/api/chat`.
Ngrok forwards to this Mac's `127.0.0.1:5000`. The server retrieves an entity/relationship
subgraph, adds server-owned conversation history, and calls local Ollama (`qwen3:8b`).
Answers include verified source links. Meeting requests open
[Nafiz's Google Calendar booking page](https://calendar.app.google/bNG7fkvhgRykj2Ba7).
The visitor selects a time and confirms there; the assistant has no calendar write access.

## Start and stop

Python 3.10+ and Node.js are required. From the repository root:

The operator must provide the private prompt at `server/.private/assistant.txt`
or set `PORTFOLIO_PROMPT_FILE` to a file outside the repository. It must include
`{{date}}` and `{{context}}` substitution markers. The exact production prompt is
deliberately not distributed in Git; a fresh clone needs its own local prompt.

```sh
python3 -m venv .venv
.venv/bin/pip install -r server/requirements.txt
ollama serve  # only if the Ollama app/service is not already running
ollama pull qwen3:8b  # only if the model is not already installed
.venv/bin/python -m server.manage start
.venv/bin/python -m server.manage status
ngrok http 5000 --url https://cattle-scratch-parlor.ngrok-free.dev
```

Reuse an existing ngrok tunnel for this domain/port; do not start a second one.
The server runs in the background and logs startup/errors to `server/.runtime/server.log`.
It does not auto-start after a reboot. Stop it with `python3 -m server.manage stop`.
The Python installation used to start it must contain the dependencies.
For foreground development:

```sh
python3 -m uvicorn server.app:app --host 127.0.0.1 --port 5000 --no-proxy-headers --no-access-log
```

Visit `http://127.0.0.1:5000/` to preview the complete site. The Mac must remain awake,
with Ollama, this server, and the tunnel running for visitors to receive AI answers.
The booking link continues to work when the server is offline.

Environment variables (set before starting):

| Variable | Default |
| --- | --- |
| `OLLAMA_MODEL` | `qwen3:8b` |
| `OLLAMA_URL` | `http://127.0.0.1:11434` |
| `BOOKING_URL` | Google Calendar URL above |
| `ALLOWED_ORIGINS` | GitHub Pages origin, ngrok origin, localhost:5000 and 127.0.0.1:5000 |
| `PORTFOLIO_PROMPT_FILE` | `server/.private/assistant.txt` (gitignored) |
| `AUDIT_DIR` | `~/Documents/Portfolio Chat Logs` |

Changing the booking URL also requires updating the offline fallback in `js/chat.js`.
No API keys, Google credentials, or browser secrets are required.

## Knowledge graph and harness

`knowledge.py` ingests only seven explicitly named public portfolio files. It extracts
the profile, education, news, publications, roles, organizations, projects, awards,
activities, teaching, patents, and contact information. Relations include `authored`,
`held_role`, `at_organization`, `advised_by`, `describes_project`, and `about_topic`.
Topic tags are deterministic keyword classifications, not independent factual claims.

The generated `server/knowledge_graph.json` is ignored by Git. A fingerprint check
rebuilds it on startup when the source files change. After updating/pulling content,
restart the server; or rebuild explicitly with `python3 -m server.knowledge`.
The original `graphify-out` code graph is not used for biography answers.

Retrieval ranks entity text and expands along one-hop relationships. The bounded
harness supplies these entities, relationships, and recent turns to Ollama's
[native chat API](https://docs.ollama.com/api/chat), with schema-constrained output.
It filters citations against retrieved sources and returns only the configured
booking action. This is a retrieval and action-routing harness, not an unrestricted
shell/browser agent. No model-controlled filesystem, network or calendar tools exist.

Sessions use random tokens and stay in memory, retaining up to 12 recent messages.
Idle sessions expire after one hour (cleaned every 30 seconds); restarting clears all.
The UI stores its session token in memory only, and New chat starts an isolated session.
The working memory limit does not delete the persistent audit archive described below.

## Audit archive

All new chat requests are recorded in `~/Documents/Portfolio Chat Logs/`:

- `YYYY-MM-DD.md`: readable visitor/assistant transcripts, with request IDs, sources and actions.
- `YYYY-MM-DD.jsonl`: timestamped request/response events, model input (including the private
  prompt and retrieved graph), raw model output, graph/prompt fingerprints, errors,
  guardrail decisions, elapsed time, and server start/stop events. Dates are UTC.

Records are appended and flushed to disk before a successful response is sent. Requests
fail with HTTP 503 if recording is unavailable, rather than silently losing transcripts.
`response_ready` records what the server prepared; `response_sent` means the server handed
the response to its transport, not proof that a visitor read it. Interrupted requests may
have only the initial events. Oversized requests are limited to the first 16 KB, and
rejected origins may have no consumed body. No attempt is made to recover pre-feature chats.

The directory is created with owner-only access (0700); new files use 0600. Logs are
outside the repository, are not served over HTTP, and have no automatic deletion.
Conversation IDs are SHA-256 hashes of session tokens; live session tokens are removed
from structured audit bodies. These files contain private prompts and visitor messages:
keep them local. The archive is append-only at the application level, not tamper-proof.
The browser discloses transcript storage before a visitor sends a message.

Booking-link clicks and New chat actions are recorded through `POST /api/events` when
the server is reachable. They are visitor-reported events, not proof of an appointment;
offline/blocked client telemetry cannot be guaranteed. Actual bookings remain in Google
Calendar. Ngrok's traffic inspection is managed independently of this application.

## Guardrails and personality

Deterministic checks block common instruction overrides, prompt extraction, private-data
requests and attempts to operate the host before inference. The model also classifies
scope; unrelated answers are redirected and factual answers without a retrieved citation
are replaced by an explicit uncertainty response. Long verbatim prompt leaks are blocked.
These checks reduce risk; keyword rules and model classification are not a guarantee
against every adversarial phrasing or factual error. Booking confirmations remain outside
the model's control. The exact tone/personality instructions live only in the private
prompt file, loaded on each request, and its hash is included in the local audit trail.

Messages are limited to 2,000 characters and requests to 16 KB. One generation runs
at a time, with per-client/global rate limits, bounded session storage, a model timeout,
and an explicit browser origin allowlist. Rate limits are local to this single worker;
do not run multiple workers without shared state. CORS is not authentication: this is
an intentionally public endpoint. Only public static directories are served.
The widget renders model/visitor content with `textContent`, includes keyboard controls,
and uses the documented [ngrok interstitial bypass header](https://ngrok.com/docs/pricing-limits/free-plan-limits#using-headers).

## Validation

```sh
python3 -m unittest discover -s server/tests -v
node --check js/chat.js
curl http://127.0.0.1:5000/api/health
curl -H 'ngrok-skip-browser-warning: 1' https://cattle-scratch-parlor.ngrok-free.dev/api/health
```

`GET /api/config` returns the booking link. `POST /api/chat` accepts
`{"message":"What does Nafiz research?","session_id":null}` and returns `answer`,
`session_id`, `sources`, and `actions`. Pass the returned session ID for follow-ups.
Health distinguishes server reachability from whether the configured model is installed;
it does not run an inference request. Tests stub inference; real-model/browser smoke
tests should also be run after changing models or prompts.
