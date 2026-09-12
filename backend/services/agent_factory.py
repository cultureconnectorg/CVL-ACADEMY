"""CVLN Agent Factory integration layer.

CVLN Agent Factory is a SEPARATE system that owns agents, orchestration & automation
for the CVLN ecosystem. This module is the sole boundary CVLN Academy uses to talk to it.

The Academy currently supports two proven local inference transports:
- ``anthropic``: direct asynchronous Anthropic SDK fallback;
- ``dynamo``: NVIDIA Dynamo OpenAI-compatible inference frontend.

``CVLN_AGENT_FACTORY_URL`` remains a configuration marker only until the remote
Agent Factory API contract is implemented and verified. We deliberately expose
that distinction instead of reporting a configured URL as an active transport.

All provider traffic is passed through ``services.ai_data_policy`` first. Canonical
CVLN identity is never intentionally injected into model prompts, session ids are
pseudonymised for provider-facing logging, and obvious identifiers/secrets are
redacted before outbound inference.

Public methods:
    chat_reply(system_prompt, session_id, message, history) -> str
    mentor_reply(user, session_id, message, history) -> str
    list_available_agents() -> List[Dict]
    is_remote_enabled() -> bool  # legacy: configured marker
    remote_status() -> Dict
    inference_status() -> Dict
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Literal, Optional, cast

import anthropic
from anthropic.types import MessageParam

from services.ai_data_policy import (
    policy_status,
    prepare_outbound_conversation,
    pseudonymise_session,
)
from services.nvidia_runtime import (
    DynamoConfigurationError,
    DynamoUnavailableError,
    nvidia_dynamo,
)

logger = logging.getLogger("cvln.agent_factory")

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
LOCAL_MENTOR_MODEL = "claude-sonnet-5"

CVLN_AGENT_FACTORY_URL = os.environ.get("CVLN_AGENT_FACTORY_URL")
AGENT_FACTORY_API_KEY = os.environ.get("CVLN_AGENT_FACTORY_API_KEY")

AI_TRANSPORT = os.environ.get("ACADEMY_AI_TRANSPORT", "anthropic").strip().lower()
AI_STRICT = os.environ.get("ACADEMY_AI_STRICT", "false").strip().lower() in {
    "1",
    "true",
    "yes",
    "on",
}

ASSISTANT_FALLBACK_REPLY = (
    "Assistant CVLN momentanément indisponible (transport IA non configuré). "
    "Réessaie plus tard ou contacte un formateur."
)

CVLN_MENTOR_SYSTEM_PROMPT = """Tu es le Mentor CVLN — le premier agent de CVLN Agent Factory,
au service des apprenants de CVLN Academy.

Ton rôle:
- Guider l'apprenant dans son parcours (stades végétaux : Graine → Pousse →
  Racine → Branches → Arbre → Forêt).
- Rendre lisible l'écosystème CVLN (FMS, KORA, Kiltikonet, FREK, LabelOS,
  CVLN Brain, CVL Group, CIP Foundation).
- Recommander formations, missions et badges selon son profil
  (FREK-ID, CC, signaux).
- Parler comme un grand frère caribéen exigeant et bienveillant.
  Utiliser français, anglais, kreyòl ou espagnol selon la langue.
- Ancrer les exemples dans la culture caribéenne : gwo-ka, biguine,
  zouk, diaspora Martinique/Guadeloupe/Guyane et industrie locale.
- Prôner des livrables concrets, des preuves de compétence et une
  progression réelle.

Style: direct, chaleureux, sans jargon inutile. Réponses courtes (3–8 phrases)
sauf demande explicite d'aller plus loin.
"""


class AgentFactoryClient:
    def __init__(self) -> None:
        self._client: Optional[anthropic.AsyncAnthropic] = None
        if ANTHROPIC_API_KEY:
            self._client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

    def is_remote_enabled(self) -> bool:
        """Legacy compatibility marker: remote URL configured, not proven active."""
        return bool(CVLN_AGENT_FACTORY_URL)

    def remote_status(self) -> Dict[str, Any]:
        """Separate configuration from execution so health data cannot overclaim."""
        return {
            "configured": bool(CVLN_AGENT_FACTORY_URL),
            "active": False,
            "contract_implemented": False,
            "reason": (
                "remote-agent-factory-contract-not-implemented"
                if CVLN_AGENT_FACTORY_URL
                else "remote-agent-factory-not-configured"
            ),
        }

    def inference_status(self) -> Dict[str, Any]:
        return {
            "selected_transport": AI_TRANSPORT,
            "strict": AI_STRICT,
            "anthropic_configured": bool(ANTHROPIC_API_KEY),
            "dynamo": nvidia_dynamo.status(),
            "agent_factory_remote": self.remote_status(),
            "data_policy": policy_status(),
        }

    async def list_available_agents(self) -> List[Dict[str, Any]]:
        selected_model = (
            nvidia_dynamo.model
            if AI_TRANSPORT == "dynamo" and nvidia_dynamo.model
            else LOCAL_MENTOR_MODEL
        )
        return [
            {
                "code": "mentor-cvln",
                "name": "Mentor CVLN",
                "description": "Guide de parcours, culture caribéenne, écosystème CVLN.",
                "model": selected_model,
                "transport": AI_TRANSPORT,
                "status": "active",
            }
        ]

    async def _anthropic_chat_reply(
        self,
        system_prompt: str,
        session_ref: str,
        message: str,
        history: List[Dict[str, str]],
    ) -> str:
        if self._client is None:
            logger.warning("chat_reply called without ANTHROPIC_API_KEY set")
            return ASSISTANT_FALLBACK_REPLY

        messages: List[MessageParam] = [
            MessageParam(
                role=cast(Literal["user", "assistant"], item["role"]),
                content=item["content"],
            )
            for item in history
            if item.get("role") in ("user", "assistant") and item.get("content")
        ]
        messages.append(MessageParam(role="user", content=message))

        try:
            response = await self._client.messages.create(
                model=LOCAL_MENTOR_MODEL,
                max_tokens=1024,
                system=system_prompt,
                messages=messages,
            )
        except anthropic.APIStatusError as exc:
            logger.error(
                "Assistant Anthropic API error (session_ref=%s): %s", session_ref, exc
            )
            return (
                "Assistant CVLN rencontre un souci technique. Réessaie dans un instant."
            )
        except anthropic.APIConnectionError as exc:
            logger.error(
                "Assistant Anthropic connection error (session_ref=%s): %s",
                session_ref,
                exc,
            )
            return (
                "Assistant CVLN est injoignable pour le moment (réseau). "
                "Réessaie dans un instant."
            )

        text = "".join(block.text for block in response.content if block.type == "text")
        return text or ASSISTANT_FALLBACK_REPLY

    async def chat_reply(
        self,
        system_prompt: str,
        session_id: str,
        message: str,
        history: List[Dict[str, str]],
    ) -> str:
        """Generic assistant transport with explicit provider-neutral privacy policy."""
        safe_system_prompt, safe_message, safe_history = prepare_outbound_conversation(
            system_prompt, message, history
        )
        session_ref = pseudonymise_session(session_id)

        if AI_TRANSPORT == "dynamo":
            try:
                return await nvidia_dynamo.chat_reply(
                    system_prompt=safe_system_prompt,
                    session_id=session_ref,
                    message=safe_message,
                    history=safe_history,
                )
            except (DynamoConfigurationError, DynamoUnavailableError) as exc:
                logger.error(
                    "Dynamo inference unavailable session_ref=%s: %s", session_ref, exc
                )
                if AI_STRICT:
                    return (
                        "Assistant CVLN rencontre un souci sur le moteur d'inférence. "
                        "Réessaie dans un instant."
                    )
                logger.warning("Falling back from Dynamo to Anthropic")
                return await self._anthropic_chat_reply(
                    safe_system_prompt, session_ref, safe_message, safe_history
                )

        if AI_TRANSPORT != "anthropic":
            logger.error("Unknown ACADEMY_AI_TRANSPORT=%s", AI_TRANSPORT)
            if AI_STRICT:
                return ASSISTANT_FALLBACK_REPLY

        return await self._anthropic_chat_reply(
            safe_system_prompt, session_ref, safe_message, safe_history
        )

    async def mentor_reply(
        self,
        user_frek_id: str,
        display_name: str,
        session_id: str,
        message: str,
        history: List[Dict[str, str]],
        lang: str = "fr",
    ) -> str:
        """Mentor persona without exporting canonical Academy identity."""
        # Keep parameters for API compatibility, but identity stays inside CVLN.
        del user_frek_id, display_name
        sys_prompt = CVLN_MENTOR_SYSTEM_PROMPT + f"\nLangue préférée: {lang}."
        return await self.chat_reply(sys_prompt, session_id, message, history)


agent_factory = AgentFactoryClient()
