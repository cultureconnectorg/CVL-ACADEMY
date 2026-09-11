"""CVLN CareOps core: support, claims, incidents and maintenance routing."""

from __future__ import annotations

import hashlib
import re
import secrets
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Literal

from db import db, utc_now_iso

TicketKind = Literal["support", "claim", "payment", "security", "access", "maintenance"]
Priority = Literal["P0", "P1", "P2", "P3"]


@dataclass(frozen=True)
class Classification:
    kind: TicketKind
    priority: Priority
    queue: str
    sensitive: bool = False


def _contains(text: str, terms: Iterable[str]) -> bool:
    normalized = text.casefold()
    return any(term.casefold() in normalized for term in terms)


def classify_message(message: str) -> Classification:
    if _contains(message, ("pirat", "hack", "fraude", "phishing", "compte volé")):
        return Classification("security", "P0", "security", True)
    if _contains(message, ("réclamation", "reclamation", "conteste", "remboursement", "litige")):
        return Classification("claim", "P1", "claims", True)
    if _contains(message, ("paiement", "facture", "invoice", "prélev", "prelev", "stripe")):
        return Classification("payment", "P2", "billing", True)
    if _contains(message, ("connexion", "connecter", "login", "accès", "acces", "mot de passe", "ne s'ouvre")):
        return Classification("access", "P2", "support")
    if _contains(message, ("bug", "erreur", "error", "cassé", "casse", "indisponible", "ne fonctionne", "500", "timeout")):
        return Classification("maintenance", "P2", "maintenance")
    return Classification("support", "P3", "support")


def make_fingerprint(product: str, kind: str, message: str) -> str:
    normalized = re.sub(r"[^a-z0-9à-ÿ]+", " ", message.casefold())
    normalized = " ".join(normalized.split())[:240]
    return hashlib.sha256(f"{product}|{kind}|{normalized}".encode()).hexdigest()[:24]


def autonomy_policy(classification: Classification) -> Dict[str, Any]:
    return {
        "mode": "policy_guarded" if classification.sensitive else "autonomous",
        "can_auto_close": not classification.sensitive,
        "review_queue": classification.queue if classification.sensitive else None,
        "founder_required": False,
    }


def _ticket_id() -> str:
    return f"CVLN-{secrets.token_hex(5).upper()}"


async def create_ticket(*, user_id: str, message: str, product: str = "academy", channel: str = "academy") -> Dict[str, Any]:
    classification = classify_message(message)
    now = utc_now_iso()
    ticket = {
        "ticket_id": _ticket_id(),
        "user_id": user_id,
        "product": product,
        "channel": channel,
        "source": "laurentia",
        "kind": classification.kind,
        "priority": classification.priority,
        "queue": classification.queue,
        "status": "triaged",
        "message": message.strip(),
        "fingerprint": make_fingerprint(product, classification.kind, message),
        "incident_id": None,
        "autonomy": autonomy_policy(classification),
        "created_at": now,
        "updated_at": now,
        "events": [{"type": "ticket.created", "actor": "laurentia", "ts": now}],
    }
    await db.careops_tickets.insert_one(ticket.copy())
    return await db.careops_tickets.find_one({"ticket_id": ticket["ticket_id"]}, {"_id": 0}) or ticket


async def list_user_tickets(user_id: str, limit: int = 50) -> list[Dict[str, Any]]:
    limit = max(1, min(limit, 100))
    cursor = db.careops_tickets.find({"user_id": user_id}, {"_id": 0}).sort("created_at", -1).limit(limit)
    return await cursor.to_list(length=limit)
