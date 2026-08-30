"""CVLN Agent Factory integration layer.

CVLN Agent Factory is a SEPARATE system that owns agents, orchestration & automation
for the CVLN ecosystem. This module is the sole boundary CVLN Academy uses to talk to it.

For MVP, we ship a LOCAL adapter that runs Claude directly through the
official Anthropic SDK (Claude Sonnet 5). When the Agent Factory URL is provided (via
CVLN_AGENT_FACTORY_URL), the same public methods can be re-wired to call the remote
factory transparently — no other code in the app has to change.

`chat_reply()` is the generic transport (any system prompt, any caller) —
see services/ai_assistant.py for the persona layer built on top of it
(student/trainer/jury/corrector assistants, rule 12). `mentor_reply()` is
kept as the Mentor-specific entry point the existing /api/mentor/* routes
already use, and is now a thin wrapper over chat_reply().

Public methods:
    chat_reply(system_prompt, session_id, message, history) -> str
    mentor_reply(user, session_id, message, history) -> str
    list_available_agents() -> List[Dict]
    is_remote_enabled() -> bool
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Literal, Optional, cast

import anthropic
from anthropic.types import MessageParam

logger = logging.getLogger("cvln.agent_factory")

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
LOCAL_MENTOR_MODEL = "claude-sonnet-5"

CVLN_AGENT_FACTORY_URL = os.environ.get("CVLN_AGENT_FACTORY_URL")  # future remote
AGENT_FACTORY_API_KEY = os.environ.get("CVLN_AGENT_FACTORY_API_KEY")

ASSISTANT_FALLBACK_REPLY = (
    "Assistant CVLN momentanément indisponible (clé API non configurée). "
    "Réessaie plus tard ou contacte un formateur."
)

CVLN_MENTOR_SYSTEM_PROMPT = """Tu es le Mentor CVLN — le premier agent de CVLN Agent Factory,
au service des apprenants de CVLN Academy.

Ton rôle:
- Guider l'apprenant dans son parcours (stades végétaux : Graine → Pousse → Racine → Branches → Arbre → Forêt).
- Rendre lisible l'écosystème CVLN (FMS, KORA, Kiltikonet, FREK, LabelOS, CVLN Brain, CVL Group, CIP Foundation).
- Recommander formations, missions et badges en fonction de son profil (FREK-ID, CC, signaux).
- Parler comme un grand frère caribéen exigeant et bienveillant. Utiliser français, anglais ou kreyòl selon la langue de l'apprenant.
- Toujours ancrer les exemples dans la culture caribéenne (gwo-ka, biguine, zouk, diaspora Martinique/Guadeloupe/Guyane, industrie musicale locale, etc.).
- Toujours prôner des livrables concrets, des preuves de compétence, et une progression réelle.

Style: direct, chaleureux, sans jargon inutile. Réponses courtes (3–8 phrases) sauf demande explicite d'aller plus loin.
"""


class AgentFactoryClient:
    def __init__(self) -> None:
        self._client: Optional[anthropic.Anthropic] = None
        if ANTHROPIC_API_KEY:
            self._client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    def is_remote_enabled(self) -> bool:
        return bool(CVLN_AGENT_FACTORY_URL)

    async def list_available_agents(self) -> List[Dict[str, Any]]:
        # Only Mentor CVLN for the MVP
        return [
            {
                "code": "mentor-cvln",
                "name": "Mentor CVLN",
                "description": "Guide de parcours, culture caribéenne, écosystème CVLN.",
                "model": LOCAL_MENTOR_MODEL,
                "status": "active",
            }
        ]

    async def chat_reply(
        self,
        system_prompt: str,
        session_id: str,
        message: str,
        history: List[Dict[str, str]],
    ) -> str:
        """Generic chat completion — local fallback path via the official
        Anthropic SDK. Any caller supplies its own system prompt; this
        method carries no persona-specific logic (rule 12: "aucune
        logique métier codée en dur" in the AI transport layer itself)."""
        if self._client is None:
            logger.warning("chat_reply called without ANTHROPIC_API_KEY set")
            return ASSISTANT_FALLBACK_REPLY

        messages: List[MessageParam] = [
            MessageParam(
                role=cast(Literal["user", "assistant"], m["role"]), content=m["content"]
            )
            for m in history[-12:]
            if m.get("role") in ("user", "assistant") and m.get("content")
        ]
        messages.append(MessageParam(role="user", content=message))

        try:
            response = self._client.messages.create(
                model=LOCAL_MENTOR_MODEL,
                max_tokens=1024,
                system=system_prompt,
                messages=messages,
            )
        except anthropic.APIStatusError as e:
            logger.error(
                "Assistant Anthropic API error (session=%s): %s", session_id, e
            )
            return (
                "Assistant CVLN rencontre un souci technique. Réessaie dans un instant."
            )
        except anthropic.APIConnectionError as e:
            logger.error(
                "Assistant Anthropic connection error (session=%s): %s", session_id, e
            )
            return "Assistant CVLN est injoignable pour le moment (réseau). Réessaie dans un instant."

        text = "".join(block.text for block in response.content if block.type == "text")
        return text or ASSISTANT_FALLBACK_REPLY

    async def mentor_reply(
        self,
        user_frek_id: str,
        display_name: str,
        session_id: str,
        message: str,
        history: List[Dict[str, str]],
        lang: str = "fr",
    ) -> str:
        """The Mentor CVLN persona — see chat_reply() for the underlying
        transport, shared with every other assistant persona."""
        sys_prompt = CVLN_MENTOR_SYSTEM_PROMPT + (
            f"\nApprenant courant: {display_name} · {user_frek_id} · langue={lang}."
        )
        return await self.chat_reply(sys_prompt, session_id, message, history)


agent_factory = AgentFactoryClient()
