# Fixed Agent Config

> Read this when changing the prompt, VAD, model, voice, session options, or fixed voice pipeline.

All agent configuration lives in `server/src/agent.py`. The browser sends `{ channelName, rtcUid, userUid, parameters? }` to `POST /startAgent`; no provider field is accepted.

## Pipeline

```python
from agora_agent.agentkit.vendors import CartesiaTTS, OpenAI, SarvamSTT

agent = (
    AgoraAgent(...)
    .with_stt(SarvamSTT(api_key=sarvam_key, language="en-IN"))
    .with_llm(OpenAI(model="gpt-4o-mini", ...))
    .with_tts(CartesiaTTS(
        api_key=cartesia_key,
        voice_id=cartesia_voice_id,
        model_id="sonic-2",
        base_url="wss://api.cartesia.ai",
        language="en",
        sample_rate=24000,
    ))
)
```

- `SARVAM_LANGUAGE` overrides the STT language; default is `en-IN`.
- `CARTESIA_MODEL_ID` overrides the TTS model; default is `sonic-2`.
- Managed OpenAI needs no browser or server OpenAI API key.
- `SARVAM_API_KEY`, `CARTESIA_API_KEY`, and `CARTESIA_VOICE_ID` are required during `Agent` initialization.

## Agent And Session Options

- Edit `ADA_PROMPT` for behavior and `AGENT_GREETING` for the first utterance.
- VAD settings live under `AgoraAgent(turn_detection={"config": ...})`.
- RTM events require `advanced_features.enable_rtm`, `parameters.data_channel="rtm"`, `enable_error_message`, and `enable_metrics`.
- Sessions use numeric UIDs, a 30-second idle timeout, and a one-hour expiry.
- Active sessions are held in `Agent._sessions` so `/stopAgent` can stop them directly before falling back to `client.stop_agent`.

## Response

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "agent_id": "string",
    "channel_name": "string",
    "status": "started"
  }
}
```

## Verify

```bash
bun run verify:backend
bun run verify:web:api
cd server && pytest tests -v
```
