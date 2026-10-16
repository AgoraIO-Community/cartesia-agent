# Agora Cartesia Voice Agent

A standalone Agora Conversational AI project with a fixed voice pipeline:

`Sarvam STT (en-IN by default) -> managed OpenAI gpt-4o-mini -> Cartesia Sonic 3.6 TTS (English, 24 kHz)`

The Next.js client provides RTC audio, RTM transcripts, agent state, metrics, and controls. The Python FastAPI service generates Agora tokens and owns the agent lifecycle and vendor credentials.

## Requirements

- Python 3.10+
- Bun
- An Agora project with Conversational AI enabled
- Sarvam and Cartesia credentials

## Configure

Use [`server/.env.example`](server/.env.example) as the variable reference. Keep actual values in an ignored local environment file or your deployment secret manager.

| Variable | Required | Default | Purpose |
| --- | :---: | --- | --- |
| `AGORA_APP_ID` | Yes | | Agora App ID |
| `AGORA_APP_CERTIFICATE` | Yes | | Server-only Agora App Certificate |
| `SARVAM_API_KEY` | Yes | | Sarvam STT authentication |
| `SARVAM_LANGUAGE` | No | `en-IN` | Sarvam recognition language |
| `CARTESIA_API_KEY` | Yes | | Cartesia TTS authentication |
| `CARTESIA_VOICE_ID` | Yes | | Cartesia voice identifier |
| `CARTESIA_MODEL_ID` | No | `sonic-3.6` | Cartesia model identifier |
| `AGENT_GREETING` | No | Built in | First agent utterance |
| `PORT` | No | `8001` | FastAPI port |
| `AGENT_BACKEND_URL` | Web deploy | | FastAPI URL used by Next rewrites |

No OpenAI API key is needed because the LLM stage uses Agora-managed OpenAI.

## Run

```bash
bun run setup
bun run doctor:local
bun run dev
```

- Web: `http://localhost:3000`
- FastAPI: `http://localhost:8001`
- API docs: `http://localhost:8001/docs`

The root development command sets `AGENT_BACKEND_URL=http://localhost:8001` for the web process. Set that variable explicitly when deploying `web` separately.

## Verify

```bash
bun run verify:backend
bun run verify:web:api
bun run verify:web:proxy
bun run verify:local:fastapi
cd server && pytest tests -v
cd ../web && bun test
```

The static contract and unit checks do not contact Agora, Sarvam, Cartesia, or OpenAI. `bun run verify:local:fastapi` requires the existing backend virtual environment created by `bun run setup`.

## API

- `GET /get_config`: returns RTC/RTM token, channel, user UID, and agent UID.
- `POST /startAgent`: accepts `{ channelName, rtcUid, userUid, parameters? }`.
- `POST /stopAgent`: accepts `{ agentId }`.

`/startAgent` has no provider fields. The server always creates the fixed Sarvam, managed OpenAI, and Cartesia pipeline.

## Deployment

Deploy `web` to a Next.js-compatible host and `server` as a reachable Python service. Keep all Agora, Sarvam, and Cartesia secrets on the FastAPI host. The backend and Docker image use port `8001` by default.

See [ARCHITECTURE.md](ARCHITECTURE.md), [server/README.md](server/README.md), and [AGENTS.md](AGENTS.md).
# cartesia-agent
# sarvam-agent
