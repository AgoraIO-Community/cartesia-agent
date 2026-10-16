# Cartesia Voice Agent Service

FastAPI backend for the standalone Agora Cartesia voice agent.

## Pipeline

- STT: `SarvamSTT`, `SARVAM_LANGUAGE=en-IN` by default
- LLM: Agora-managed `OpenAI`, model `gpt-4o-mini`
- TTS: `CartesiaTTS`, `CARTESIA_MODEL_ID=sonic-3.6` by default, `wss://api.cartesia.ai`, language `en`, sample rate `24000`

The pipeline is fixed. `/startAgent` does not accept a provider or profile field.

## Configure

Required server variables are `AGORA_APP_ID`, `AGORA_APP_CERTIFICATE`, `SARVAM_API_KEY`, `CARTESIA_API_KEY`, and `CARTESIA_VOICE_ID`. Optional variables are documented in [`.env.example`](.env.example). Never expose these values to `web/`.

## Install And Run

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/server.py
```

The service binds `0.0.0.0:8001` unless `PORT` overrides it.

## API

```bash
curl http://localhost:8001/get_config

curl -X POST http://localhost:8001/startAgent \
  -H "Content-Type: application/json" \
  -d '{"channelName":"test-channel","rtcUid":123456,"userUid":789012}'

curl -X POST http://localhost:8001/stopAgent \
  -H "Content-Type: application/json" \
  -d '{"agentId":"returned-agent-id"}'
```

Run standalone tests with `pytest tests -v`. They use fake credentials and sessions and make no external calls.
