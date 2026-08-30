"""CVLN Agent Factory integration layer.

CVLN Agent Factory is a SEPARATE system that owns agents, orchestration & automation
for the CVLN ecosystem. This module is the sole boundary CVLN Academy uses to talk to it.

For MVP, we ship a LOCAL adapter that runs the AI Mentor agent directly through the
official Anthropic SDK (Claude Sonnet 5). When the Agent Factory URL is provided (via
CVLN_AGENT_FACTORY_URL), the same public methods can be re-wired to call the remote
factory transparently — no other code in the app has to change.

Public methods:
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

MENTOR_FALLBACK_REPLY = (
    "Mentor CVLN est momentanément indisponible (clé API non configurée). "
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

    async def mentor_reply(
        self,
        user_frek_id: str,
        display_name: str,
        session_id: str,
        message: str,
        history: List[Dict[str, str]],
        lang: str = "fr",
    ) -> str:
        """Return a single mentor reply.

        Local fallback path — calls Claude directly via the official Anthropic SDK.
        The signature is designed to be swapped for a remote Agent Factory call
        (streaming or not) without touching any caller.
        """
        if self._client is None:
            logger.warning("mentor_reply called without ANTHROPIC_API_KEY set")
            return MENTOR_FALLBACK_REPLY

        sys_prompt = CVLN_MENTOR_SYSTEM_PROMPT + (
            f"\nApprenant courant: {display_name} · {user_frek_id} · langue={lang}."
        )

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
                system=sys_prompt,
                messages=messages,
            )
        except anthropic.APIStatusError as e:
            logger.error("Mentor Anthropic API error: %s", e)
            return "Mentor CVLN rencontre un souci technique. Réessaie dans un instant."
        except anthropic.APIConnectionError as e:
            logger.error("Mentor Anthropic connection error: %s", e)
            return "Mentor CVLN est injoignable pour le moment (réseau). Réessaie dans un instant."

        text = "".join(block.text for block in response.content if block.type == "text")
        return text or MENTOR_FALLBACK_REPLY


agent_factory = AgentFactoryClient()
