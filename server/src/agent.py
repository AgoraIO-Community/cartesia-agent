"""
Agent

High-level API for managing Agora Conversational AI Agents.
"""
import logging
import os
from typing import Any, Dict, Optional

from agora_agent import Area, AsyncAgora
from agora_agent.agentkit import Agent as AgoraAgent
from agora_agent.agentkit.vendors import CartesiaTTS, OpenAI, SarvamSTT

logger = logging.getLogger("uvicorn.error")

ADA_PROMPT = """You are Ada, an agentic developer advocate from Agora. You help developers understand and build with Agora's Conversational AI platform.

Agora is a real-time communications company. The product you represent is the Agora Conversational AI Engine.

If you do not know a specific fact about Agora, say so plainly and suggest checking docs.agora.io. Keep most replies to one or two sentences unless the user explicitly asks for more detail.
"""


def _configured_env(*names: str) -> Optional[str]:
    for name in names:
        value = os.getenv(name)
        if value and not value.startswith("your_"):
            return value
    return None


def get_agora_credentials() -> tuple[Optional[str], Optional[str]]:
    return (
        _configured_env("AGORA_APP_ID", "APP_ID"),
        _configured_env("AGORA_APP_CERTIFICATE", "APP_CERTIFICATE"),
    )


def _required_env(name: str) -> str:
    value = _configured_env(name)
    if not value:
        raise ValueError(f"{name} is required")
    return value


class Agent:
    """
    High-level wrapper for Agora Conversational AI Agent operations.
    
    Uses AgentSession for full lifecycle management (start/stop),
    which handles Token007 authentication automatically.
    """
    
    def __init__(self):
        self.app_id, self.app_certificate = get_agora_credentials()
        self.greeting = os.getenv(
            "AGENT_GREETING",
            "Hi there! I'm Ada, your virtual assistant from Agora. How can I help?",
        )

        if not self.app_id or not self.app_certificate:
            raise ValueError("Agora App ID and App Certificate are required")

        self.sarvam_api_key = _required_env("SARVAM_API_KEY")
        self.sarvam_language = os.getenv("SARVAM_LANGUAGE", "en-IN")
        self.cartesia_api_key = _required_env("CARTESIA_API_KEY")
        self.cartesia_voice_id = _required_env("CARTESIA_VOICE_ID")
        self.cartesia_model_id = os.getenv("CARTESIA_MODEL_ID", "sonic-2")

        self.client = AsyncAgora(
            area=Area.US,
            app_id=self.app_id,
            app_certificate=self.app_certificate,
        )

        # Track active sessions by agent_id
        self._sessions: Dict[str, Any] = {}

    async def start(
        self,
        channel_name: str,
        agent_uid: int,
        user_uid: int,
        output_audio_codec: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Start an agent with the fixed Sarvam, OpenAI, and Cartesia pipeline."""
        if not channel_name or not str(channel_name).strip():
            raise ValueError("channel_name is required and cannot be empty")
        if agent_uid <= 0:
            raise ValueError("agent_uid is required and cannot be empty")
        if user_uid <= 0:
            raise ValueError("user_uid is required and cannot be empty")
        llm = OpenAI(
            model="gpt-4o-mini",
            greeting_message=self.greeting,
            failure_message="Please wait a moment.",
            max_history=15,
            max_tokens=1024,
            temperature=0.7,
            top_p=0.95,
        )
        stt = SarvamSTT(
            api_key=self.sarvam_api_key,
            language=self.sarvam_language,
        )
        tts = CartesiaTTS(
            api_key=self.cartesia_api_key,
            voice_id=self.cartesia_voice_id,
            model_id=self.cartesia_model_id,
            base_url="wss://api.cartesia.ai",
            language="en",
            sample_rate=24000,
        )

        parameters = {
            "audio_scenario": "chorus",  # web client → ultra-low-latency chorus profile
            "data_channel": "rtm",
            "enable_error_message": True,
            "enable_metrics": True,
        }
        if isinstance(output_audio_codec, str) and output_audio_codec.strip():
            parameters["output_audio_codec"] = output_audio_codec.strip()

        agora_agent = AgoraAgent(
            client=self.client,
            instructions=ADA_PROMPT,
            greeting=self.greeting,
            failure_message="Please wait a moment.",
            max_history=50,
            turn_detection={
                "config": {
                    "speech_threshold": 0.5,
                    "start_of_speech": {
                        "mode": "vad",
                        "vad_config": {
                            "interrupt_duration_ms": 160,
                            "prefix_padding_ms": 300,
                        },
                    },
                    "end_of_speech": {
                        "mode": "vad",
                        "vad_config": {
                            "silence_duration_ms": 480,
                        },
                    },
                },
            },
            advanced_features={"enable_rtm": True, "enable_tools": True},
            parameters=parameters,
        )
        
        agora_agent = (
            agora_agent
            .with_stt(stt)
            .with_llm(llm)
            .with_tts(tts)
        )

        session = agora_agent.create_async_session(
            channel=channel_name,
            agent_uid=str(agent_uid),
            remote_uids=[str(user_uid)],
            enable_string_uid=False,
            idle_timeout=30,
            expires_in=3600,
        )

        logger.info(
            "Starting Cartesia voice agent channel=%s agent_uid=%s user_uid=%s",
            channel_name,
            agent_uid,
            user_uid,
        )

        try:
            agent_id = await session.start()
        except Exception:
            logger.exception(
                "Failed to start Agora agent channel=%s agent_uid=%s user_uid=%s",
                channel_name,
                agent_uid,
                user_uid,
            )
            raise

        # Save session for later stop
        self._sessions[agent_id] = session

        logger.info(
            "Started Agora agent agent_id=%s channel=%s agent_uid=%s user_uid=%s",
            agent_id,
            channel_name,
            agent_uid,
            user_uid,
        )
        
        return {
            "agent_id": agent_id,
            "channel_name": channel_name,
            "status": "started",
        }

    async def stop(self, agent_id: str) -> None:
        """Stop a running agent. Falls back to the stateless client path."""
        if not agent_id or not str(agent_id).strip():
            raise ValueError("agent_id is required and cannot be empty")

        session = self._sessions.pop(agent_id, None)
        if session:
            try:
                await session.stop()
                logger.info("Stopped Agora agent from active session agent_id=%s", agent_id)
                return
            except Exception:
                # Fall back to the stateless SDK path if the in-memory session is stale.
                logger.warning(
                    "Failed to stop Agora agent from active session; falling back to client.stop_agent agent_id=%s",
                    agent_id,
                    exc_info=True,
                )

        logger.info("Stopping Agora agent through client.stop_agent agent_id=%s", agent_id)
        await self.client.stop_agent(agent_id)
