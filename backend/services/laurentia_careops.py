"""Laurentia adapter for the CVLN CareOps service desk."""

from __future__ import annotations

from typing import Any, Dict

from models import User
from services.agent_factory import agent_factory
from services.careops import create_ticket

LAURENTIA_CAREOPS_PROMPT = """Tu es Laurentia, agent opérationnel du groupe CVLN.
Pour le support, le service client et les réclamations, un ticket CareOps est déjà créé
avant ta réponse. Tu ne promets jamais une action non enregistrée. Tu confirmes le numéro
du dossier, expliques brièvement la prochaine étape et restes concise. Tu ne demandes pas
au fondateur d'intervenir. Les cas sensibles sont routés vers la file spécialisée prévue
par la politique CareOps. Ne prétends jamais qu'un remboursement, un correctif ou une
action externe est terminé si l'état du ticket ne le prouve pas.
"""


async def handle_with_laurentia(
    *,
    user: User,
    session_id: str,
    message: str,
    product: str = "academy",
    channel: str = "academy",
) -> Dict[str, Any]:
    ticket = await create_ticket(
        user_id=user.id,
        message=message,
        product=product,
        channel=channel,
    )
    context = (
        f"Ticket={ticket['ticket_id']} kind={ticket['kind']} "
        f"priority={ticket['priority']} queue={ticket['queue']} "
        f"status={ticket['status']}.\nDemande client: {message}"
    )
    reply = await agent_factory.chat_reply(
        LAURENTIA_CAREOPS_PROMPT,
        f"careops-{session_id}",
        context,
        [],
    )
    return {"ticket": ticket, "reply": reply}
