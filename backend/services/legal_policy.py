"""Policy-driven legal review requirement (LEG-007 / FD-L03 / FD-L04).

The canonical Authority Policy Engine decides whether an Academy legal matter can
remain internally reviewed (ALLOW) or must be escalated to an external legal
expert (ESCALATE). A DENY never becomes an implicit business decision.

Approval provenance is stored separately from matter lifecycle so
INTERNAL_APPROVED and EXTERNAL_LEGAL_APPROVED can never be conflated.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import authority_policy
from services import professional_governance as governance


APPROVAL_KINDS = {"INTERNAL_APPROVED", "EXTERNAL_LEGAL_APPROVED"}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


async def decide_review_requirement(
    *,
    actor_id: str,
    actor_role: str,
    authority_level: str,
    matter_id: str,
    policy_version_id: str,
    risk_level: str,
    context: Optional[Dict[str, Any]] = None,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    refs = list(dict.fromkeys(str(ref) for ref in evidence_refs if str(ref)))
    if not refs:
        raise ValueError("legal review decision requires evidence")
    matter = await db.legal_matters.find_one({"id": matter_id}, {"_id": 0})
    if not matter:
        raise LookupError("legal matter not found")

    decision = await authority_policy.evaluate_authority(
        actor_id=actor_id,
        actor_role=actor_role,
        action="LEGAL_REVIEW_DECIDE",
        context={
            "domain": "LEGAL",
            "jurisdiction": matter.get("jurisdiction"),
            "authority_level": authority_level,
            "risk_level": str(risk_level or "").upper(),
            "resource_type": matter.get("matter_type"),
            **(context or {}),
        },
        policy_version_id=policy_version_id,
    )
    if decision["policy_key"] != "LEGAL_REVIEW_REQUIREMENT":
        raise ValueError("legal review decision requires LEGAL_REVIEW_REQUIREMENT policy")
    if decision["decision"] == "DENY":
        raise PermissionError("legal review policy denied the decision")

    external_required = decision["decision"] == "ESCALATE"
    row = {
        "id": _id("LREV"),
        "matter_id": matter_id,
        "external_review_required": external_required,
        "risk_level": str(risk_level or "").upper(),
        "context": context or {},
        "authority_decision_id": decision["id"],
        "policy_version_id": decision["policy_version_id"],
        "policy_content_hash": decision["policy_content_hash"],
        "evidence_refs": refs,
        "decided_by": actor_id,
        "decided_at": utc_now_iso(),
    }
    await db.legal_review_decisions.insert_one(dict(row))
    update = {
        "external_review_required": external_required,
        "legal_review_decision_id": row["id"],
        "updated_at": utc_now_iso(),
    }
    if external_required:
        update["status"] = "WAITING_EXTERNAL"
    await db.legal_matters.update_one({"id": matter_id}, {"$set": update})
    await governance.audit_event(
        event_type="legal.review.requirement_decided",
        actor_id=actor_id,
        resource_type="legal_matter",
        resource_id=matter_id,
        payload={
            "review_decision_id": row["id"],
            "external_review_required": external_required,
            "authority_decision_id": decision["id"],
            "policy_version_id": decision["policy_version_id"],
            "evidence_refs": refs,
        },
    )
    return {**row, "authority": decision}


async def record_approval(
    *,
    actor_id: str,
    actor_role: str,
    authority_level: str,
    matter_id: str,
    approval_kind: str,
    policy_version_id: str,
    rationale: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    kind = str(approval_kind or "").upper()
    if kind not in APPROVAL_KINDS:
        raise ValueError("invalid legal approval kind")
    refs = list(dict.fromkeys(str(ref) for ref in evidence_refs if str(ref)))
    rationale = str(rationale or "").strip()
    if not refs or not rationale:
        raise ValueError("legal approval requires rationale and evidence")
    matter = await db.legal_matters.find_one({"id": matter_id}, {"_id": 0})
    if not matter:
        raise LookupError("legal matter not found")

    action = (
        "LEGAL_INTERNAL_APPROVE"
        if kind == "INTERNAL_APPROVED"
        else "LEGAL_EXTERNAL_APPROVE"
    )
    decision = await authority_policy.evaluate_authority(
        actor_id=actor_id,
        actor_role=actor_role,
        action=action,
        context={
            "domain": "LEGAL",
            "jurisdiction": matter.get("jurisdiction"),
            "authority_level": authority_level,
            "resource_type": matter.get("matter_type"),
        },
        policy_version_id=policy_version_id,
    )
    if decision["decision"] != "ALLOW":
        raise PermissionError(f"authority policy did not allow {kind}")

    if kind == "INTERNAL_APPROVED":
        if decision["policy_key"] != "LEGAL_INTERNAL_APPROVAL":
            raise ValueError("internal approval requires LEGAL_INTERNAL_APPROVAL policy")
    elif decision["policy_key"] != "LEGAL_EXTERNAL_APPROVAL":
        raise ValueError("external approval requires LEGAL_EXTERNAL_APPROVAL policy")

    row = {
        "id": _id("LAPP"),
        "matter_id": matter_id,
        "approval_kind": kind,
        "rationale": rationale,
        "evidence_refs": refs,
        "authority_decision_id": decision["id"],
        "policy_version_id": decision["policy_version_id"],
        "policy_content_hash": decision["policy_content_hash"],
        "approved_by": actor_id,
        "approved_at": utc_now_iso(),
        "status": "ACTIVE",
    }
    await db.legal_approvals.insert_one(dict(row))
    await governance.audit_event(
        event_type="legal.approval.recorded",
        actor_id=actor_id,
        resource_type="legal_matter",
        resource_id=matter_id,
        payload={
            "approval_id": row["id"],
            "approval_kind": kind,
            "authority_decision_id": decision["id"],
            "policy_version_id": decision["policy_version_id"],
            "evidence_refs": refs,
        },
    )
    return {**row, "authority": decision}


async def approval_state(matter_id: str) -> Dict[str, Any]:
    if not await db.legal_matters.find_one({"id": matter_id}):
        raise LookupError("legal matter not found")
    approvals = await db.legal_approvals.find(
        {"matter_id": matter_id, "status": "ACTIVE"}, {"_id": 0}
    ).sort("approved_at", 1).to_list(100)
    kinds = {row["approval_kind"] for row in approvals}
    return {
        "matter_id": matter_id,
        "internal_approved": "INTERNAL_APPROVED" in kinds,
        "external_legal_approved": "EXTERNAL_LEGAL_APPROVED" in kinds,
        "approvals": approvals,
    }
