"""Legal operations for CVLN Academy P0 requirements.

Implements a legal matter registry, explicit review-policy decisions, contract
lifecycle and evidence-backed signer authorization. It records evidence and authority;
it never fabricates a legal conclusion, signature or jurisdictional rule.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso


LEGAL_MATTER_STATES = {"OPEN", "IN_REVIEW", "WAITING_EXTERNAL", "RESOLVED", "ARCHIVED"}
CONTRACT_STATES = {
    "DRAFT",
    "IN_REVIEW",
    "APPROVED",
    "SIGNED",
    "ACTIVE",
    "EXPIRED",
    "TERMINATED",
    "RENEWED",
    "SUPERSEDED",
}
CONTRACT_TRANSITIONS = {
    "DRAFT": {"IN_REVIEW"},
    "IN_REVIEW": {"DRAFT", "APPROVED"},
    "APPROVED": {"SIGNED"},
    "SIGNED": {"ACTIVE"},
    "ACTIVE": {"EXPIRED", "TERMINATED", "RENEWED", "SUPERSEDED"},
    "EXPIRED": {"RENEWED", "SUPERSEDED"},
    "TERMINATED": set(),
    "RENEWED": {"SUPERSEDED"},
    "SUPERSEDED": set(),
}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


async def create_legal_matter(
    *,
    actor_id: str,
    title: str,
    matter_type: str,
    jurisdiction: Optional[str] = None,
    case_id: Optional[str] = None,
    owner_id: Optional[str] = None,
    risk_ids: Iterable[str] = (),
    evidence_refs: Iterable[str] = (),
) -> Dict[str, Any]:
    row = {
        "id": _id("LMAT"),
        "title": title,
        "matter_type": matter_type.upper(),
        "jurisdiction": jurisdiction,
        "case_id": case_id,
        "owner_id": owner_id,
        "risk_ids": list(dict.fromkeys(risk_ids)),
        "evidence_refs": list(dict.fromkeys(evidence_refs)),
        "status": "OPEN",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }
    await db.legal_matters.insert_one(dict(row))
    return row


async def transition_legal_matter(
    *, actor_id: str, matter_id: str, status: str
) -> Dict[str, Any]:
    target = status.upper()
    if target not in LEGAL_MATTER_STATES:
        raise ValueError("invalid legal matter state")
    row = await db.legal_matters.find_one({"id": matter_id}, {"_id": 0})
    if not row:
        raise LookupError("legal matter not found")
    now = utc_now_iso()
    await db.legal_matters.update_one(
        {"id": matter_id},
        {"$set": {"status": target, "updated_at": now, "updated_by": actor_id}},
    )
    return {**row, "status": target, "updated_at": now, "updated_by": actor_id}


async def record_review_policy_decision(
    *,
    actor_id: str,
    matter_id: str,
    external_review_required: bool,
    rationale: str,
    policy_ref: str,
    evidence_refs: Iterable[str] = (),
) -> Dict[str, Any]:
    if not await db.legal_matters.find_one({"id": matter_id}):
        raise LookupError("legal matter not found")
    if not policy_ref.strip():
        raise ValueError("policy_ref is required")
    if not rationale.strip():
        raise ValueError("rationale is required")
    row = {
        "id": _id("LREV"),
        "matter_id": matter_id,
        "external_review_required": bool(external_review_required),
        "rationale": rationale,
        "policy_ref": policy_ref,
        "evidence_refs": list(dict.fromkeys(evidence_refs)),
        "decided_by": actor_id,
        "decided_at": utc_now_iso(),
    }
    await db.legal_review_decisions.insert_one(dict(row))
    if external_review_required:
        await db.legal_matters.update_one(
            {"id": matter_id},
            {"$set": {"status": "WAITING_EXTERNAL", "updated_at": utc_now_iso()}},
        )
    return row


async def create_contract(
    *,
    actor_id: str,
    title: str,
    contract_type: str,
    counterparty: str,
    matter_id: Optional[str] = None,
    jurisdiction: Optional[str] = None,
    starts_at: Optional[str] = None,
    ends_at: Optional[str] = None,
    renewal_at: Optional[str] = None,
    document_id: Optional[str] = None,
    evidence_refs: Iterable[str] = (),
) -> Dict[str, Any]:
    if matter_id and not await db.legal_matters.find_one({"id": matter_id}):
        raise LookupError("legal matter not found")
    row = {
        "id": _id("CTR"),
        "title": title,
        "contract_type": contract_type.upper(),
        "counterparty": counterparty,
        "matter_id": matter_id,
        "jurisdiction": jurisdiction,
        "starts_at": starts_at,
        "ends_at": ends_at,
        "renewal_at": renewal_at,
        "document_id": document_id,
        "evidence_refs": list(dict.fromkeys(evidence_refs)),
        "status": "DRAFT",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }
    await db.legal_contracts.insert_one(dict(row))
    return row


async def transition_contract(
    *,
    actor_id: str,
    contract_id: str,
    status: str,
    evidence_refs: Iterable[str] = (),
) -> Dict[str, Any]:
    target = status.upper()
    if target not in CONTRACT_STATES:
        raise ValueError("invalid contract state")
    row = await db.legal_contracts.find_one({"id": contract_id}, {"_id": 0})
    if not row:
        raise LookupError("contract not found")
    current = row["status"]
    if target not in CONTRACT_TRANSITIONS[current]:
        raise ValueError(f"invalid contract transition {current}->{target}")
    refs = list(dict.fromkeys(evidence_refs))
    if target in {"SIGNED", "TERMINATED", "RENEWED", "SUPERSEDED"} and not refs:
        raise ValueError(f"{target.lower()} transition requires evidence")
    now = utc_now_iso()
    update = {
        "status": target,
        "updated_at": now,
        "updated_by": actor_id,
        "last_transition_evidence_refs": refs,
    }
    await db.legal_contracts.update_one({"id": contract_id}, {"$set": update})
    await db.legal_contract_events.insert_one(
        {
            "id": _id("CTREV"),
            "contract_id": contract_id,
            "from": current,
            "to": target,
            "evidence_refs": refs,
            "actor_id": actor_id,
            "created_at": now,
        }
    )
    return {**row, **update}


async def authorize_contract_signer(
    *,
    actor_id: str,
    contract_id: str,
    signer_user_id: str,
    signer_frek_id: str,
    signer_role: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    """Authorize one Academy/FREK identity to attest signing intent.

    Authorization is never inferred from the counterparty display name. At least one
    evidence reference is mandatory so the authority decision remains auditable.
    """
    contract = await db.legal_contracts.find_one({"id": contract_id}, {"_id": 0})
    if not contract:
        raise LookupError("contract not found")
    if contract.get("status") not in {"IN_REVIEW", "APPROVED"}:
        raise ValueError("signer authorization requires IN_REVIEW or APPROVED contract")
    refs = list(dict.fromkeys(evidence_refs))
    if not refs:
        raise ValueError("signer authorization requires evidence")
    if not signer_user_id.strip() or not signer_frek_id.strip():
        raise ValueError("signer user and FREK identities are required")

    existing = await db.contract_signer_authorizations.find_one(
        {
            "contract_id": contract_id,
            "signer_user_id": signer_user_id,
            "signer_frek_id": signer_frek_id,
        },
        {"_id": 0},
    )
    now = utc_now_iso()
    if existing:
        update = {
            "signer_role": signer_role,
            "evidence_refs": refs,
            "status": "AUTHORIZED",
            "authorized_by": actor_id,
            "updated_at": now,
        }
        await db.contract_signer_authorizations.update_one(
            {"id": existing["id"]}, {"$set": update}
        )
        return {**existing, **update}

    row = {
        "id": _id("SIGAUTH"),
        "contract_id": contract_id,
        "signer_user_id": signer_user_id,
        "signer_frek_id": signer_frek_id,
        "signer_role": signer_role,
        "evidence_refs": refs,
        "status": "AUTHORIZED",
        "authorized_by": actor_id,
        "created_at": now,
        "updated_at": now,
    }
    await db.contract_signer_authorizations.insert_one(dict(row))
    return row


async def revoke_contract_signer(
    *, actor_id: str, authorization_id: str, evidence_refs: Iterable[str]
) -> Dict[str, Any]:
    row = await db.contract_signer_authorizations.find_one(
        {"id": authorization_id}, {"_id": 0}
    )
    if not row:
        raise LookupError("signer authorization not found")
    refs = list(dict.fromkeys(evidence_refs))
    if not refs:
        raise ValueError("revocation requires evidence")
    now = utc_now_iso()
    update = {
        "status": "REVOKED",
        "revocation_evidence_refs": refs,
        "revoked_by": actor_id,
        "updated_at": now,
    }
    await db.contract_signer_authorizations.update_one(
        {"id": authorization_id}, {"$set": update}
    )
    return {**row, **update}
