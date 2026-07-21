"""CVLN Agent Factory integration layer.

CVLN Agent Factory is a SEPARATE system that owns agents, orchestration & automation
for the CVLN ecosystem. This module is the sole boundary CVLN Academy uses to talk to it.

For MVP, we ship a LOCAL adapter that runs the AI Mentor agent directly through the
Emergent LLM key (Claude Sonnet 4.6). When the Agent Factory URL is provided (via
CVLN_AGENT_FACTORY_URL), the same public methods can be re-wired to call the remote
factory transparently — no other code in the app has to change.

Public methods:
    mentor_reply(user, session_id, message, history) -> str
    list_available_agents() -> List[Dict]
"""
from __future__ import annotations

import os
from typing import List, Dict, Any, Optional

from emergentintegrations.llm.chat import LlmChat, UserMessage

EMERGENT_LLM_KEY = os.environ.get("EMERGENT_LLM_KEY")
CVLN_AGENT_FACTORY_URL = os.environ.get("CVLN_AGENT_FACTORY_URL")  # future remote
AGENT_FACTORY_API_KEY = os.environ.get("CVLN_AGENT_FACTORY_API_KEY")


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
    def is_remote_enabled(self) -> bool:
        return bool(CVLN_AGENT_FACTORY_URL)

    async def list_available_agents(self) -> List[Dict[str, Any]]:
        # Only Mentor CVLN for the MVP
        return [
            {
                "code": "mentor-cvln",
                "name": "Mentor CVLN",
                "description": "Guide de parcours, culture caribéenne, écosystème CVLN.",
                "model": "anthropic/claude-sonnet-4-6",
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

        Even though this uses `send_message` (non-streaming) for MVP simplicity,
        the signature is designed to be swapped for a streaming remote factory call.
        """
        # Personalized system prompt
        sys = CVLN_MENTOR_SYSTEM_PROMPT + (
            f"\nApprenant courant: {display_name} · {user_frek_id} · langue={lang}."
        )
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message=sys,
        ).with_model("anthropic", "claude-sonnet-4-6")

        # Re-inject the conversation history so multi-turn works even
        # when clients are stateless.
        for m in history[-12:]:
            if m.get("role") == "user":
                await chat.send_message(UserMessage(text=m["content"]))
            # assistant turns are already tracked by the underlying chat via send_message

        reply = await chat.send_message(UserMessage(text=message))
        return reply if isinstance(reply, str) else str(reply)


agent_factory = AgentFactoryClient()
