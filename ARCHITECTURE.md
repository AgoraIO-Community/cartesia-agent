# Cartesia Voice Agent Architecture

## Topology

```text
Browser -> Next.js /api/* rewrites -> FastAPI -> Agora Conversational AI
   |                                      |
   +------------- RTC + RTM --------------+
```

- `web/` owns the UI, RTC microphone/audio, RTM transcript and state events, and `/api/*` fetch helpers.
- `web/next.config.ts` rewrites `/api/*` to `AGENT_BACKEND_URL`.
- `server/` owns token generation, vendor secrets, fixed pipeline construction, and start/stop lifecycle.

## Fixed Pipeline

```text
User audio -> SarvamSTT(language=SARVAM_LANGUAGE or en-IN)
           -> managed OpenAI(model=gpt-4o-mini)
           -> CartesiaTTS(model=sonic-3.6, wss://api.cartesia.ai, en, 24000 Hz)
           -> RTC agent audio
```

There is no runtime provider selection. `POST /startAgent` contains channel and UID data only, and `Agent.start` imports and constructs only `SarvamSTT`, `OpenAI`, and `CartesiaTTS`.

## Session Flow

1. The browser requests `GET /api/get_config`.
2. FastAPI generates a one-hour RTC+RTM token for a concrete non-zero UID.
3. The browser calls `POST /api/startAgent`, logs into RTM, subscribes to the channel, and joins RTC.
4. FastAPI starts the fixed voice pipeline and returns `agent_id`.
5. The browser receives audio over RTC and transcript/state/metrics over RTM.
6. `POST /api/stopAgent` stops the active session; the browser releases RTC and RTM resources.

## Security Boundary

`AGORA_APP_CERTIFICATE`, `SARVAM_API_KEY`, `CARTESIA_API_KEY`, and `CARTESIA_VOICE_ID` stay in FastAPI. The browser receives only scoped Agora tokens. Restrict the sample's permissive CORS and add authentication/rate limiting before a public production deployment.
