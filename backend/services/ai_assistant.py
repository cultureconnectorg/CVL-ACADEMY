"""Common AI assistant interface (rule 12) — one transport
(agent_factory.chat_reply), N personas, all defined as data.

Every persona (student/trainer/jury/corrector) is a system-prompt config
entry, not a code branch — adding a fifth persona means adding a
dictionary entry, not an if/elif. This is what "aucune logique métier
codée en dur" means in practice here.
"""

from __future__ import annotations

from typing import Dict, List, TypedDict

from db import db, utc_now_iso
from models import User
from services.agent_factory import agent_factory

AssistantPersona = str  # "student" | "trainer" | "jury" | "corrector"


class PersonaConfig(TypedDict):
    label: str
    description: str
    system_prompt: str
    allowed_roles: tuple


ASSISTANT_PERSONAS: Dict[str, PersonaConfig] = {
    "student": {
        "label": "Assistant Étudiant",
        "description": "Guide de parcours pour les apprenants — voir Mentor CVLN.",
        "system_prompt": (
            "Tu es l'Assistant Étudiant de CVLN Academy. Aide l'apprenant à comprendre "
            "un module, se débloquer sur un livrable, ou se préparer à un quiz/certification. "
            "Style direct, chaleureux, ancré dans la culture caribéenne. Ne donne jamais "
            "directement les réponses d'un quiz ou d'une évaluation."
        ),
        "allowed_roles": (
            "student",
            "trainer",
            "corrector",
            "jury",
            "admin",
            "super_admin",
            "founder",
        ),
    },
    "trainer": {
        "label": "Assistant Formateur",
        "description": "Aide à la correction, au suivi de cohorte, à la pédagogie.",
        "system_prompt": (
            "Tu es l'Assistant Formateur de CVLN Academy. Aide le formateur à analyser la "
            "progression d'une cohorte, à formuler un feedback constructif sur un livrable, "
            "ou à adapter un module. Style professionnel, concis, orienté action."
        ),
        "allowed_roles": ("trainer", "admin", "super_admin", "founder"),
    },
    "jury": {
        "label": "Assistant Jury",
        "description": "Aide à la notation et à la rédaction de commentaires de jury.",
        "system_prompt": (
            "Tu es l'Assistant Jury de CVLN Academy. Aide le membre du jury à structurer une "
            "grille de notation, à rédiger un commentaire de certification factuel et "
            "actionnable, ou à comparer une prestation à un référentiel. Reste neutre — tu "
            "n'attribues jamais de note toi-même, tu aides à formuler le jugement du jury."
        ),
        "allowed_roles": ("jury", "admin", "super_admin", "founder"),
    },
    "corrector": {
        "label": "Assistant Correcteur",
        "description": "Aide à la correction de livrables et quiz.",
        "system_prompt": (
            "Tu es l'Assistant Correcteur de CVLN Academy. Aide le correcteur à repérer les "
            "points forts et les lacunes d'un livrable, en te basant sur les critères fournis. "
            "Style précis, bienveillant, toujours constructif."
        ),
        "allowed_roles": ("corrector", "admin", "super_admin", "founder"),
    },
}


def get_persona(persona: str) -> PersonaConfig:
    if persona not in ASSISTANT_PERSONAS:
        raise KeyError(persona)
    return ASSISTANT_PERSONAS[persona]


def can_use_persona(user: User, persona: str) -> bool:
    config = ASSISTANT_PERSONAS.get(persona)
    if config is None:
        return False
    return user.role in config["allowed_roles"]


async def assistant_reply(
    persona: str, user: User, session_id: str, message: str
) -> str:
    config = get_persona(persona)
    doc = await db.assistant_conversations.find_one(
        {"user_id": user.id, "persona": persona, "session_id": session_id}, {"_id": 0}
    )
    history: List[Dict[str, str]] = (doc or {}).get("messages", [])

    sys_prompt = (
        config["system_prompt"] + f"\nUtilisateur : {user.display_name} ({user.role})."
    )
    reply = await agent_factory.chat_reply(
        sys_prompt, f"{persona}-{session_id}", message, history
    )

    new_messages = history + [
        {"role": "user", "content": message, "ts": utc_now_iso()},
        {"role": "assistant", "content": reply, "ts": utc_now_iso()},
    ]
    await db.assistant_conversations.update_one(
        {"user_id": user.id, "persona": persona, "session_id": session_id},
        {
            "$set": {
                "user_id": user.id,
                "persona": persona,
                "session_id": session_id,
                "messages": new_messages,
                "updated_at": utc_now_iso(),
            }
        },
        upsert=True,
    )
    return reply
