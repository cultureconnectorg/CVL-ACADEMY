"""Professional review / decision workflow (GOV-006).

Makes preparation and authority states explicit. AI_PREPARED is never treated as an
approval; CVL_APPROVED and EXPERT_VALIDATED require separate evidence-bearing actions.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import authority_policy
from services import professional_governance as governance

STATES = {
    "DRAFT",
    "AI_PREPARED",
    "HUMAN_REVIEW",
    "CVL_APPROVED",
    "EXPERT_VALIDATED",
    "REJECTED",
    "SUPERSEDED",
}
TRANSITIONS = {
    "DRAFT": {"AI_PREPARED", "HUMAN_REVIEW", "REJECTED"},
    "AI_PREPARED": {"HUMAN_REVIEW", "REJECTED", "SUPERSEDED"},
    "HUMAN_REVIEW": {"CVL_APPROVED", "EXPERT_VALIDATED", "REJECTED", "SUPERSEDED"},
    "CVL_APPROVED": {"EXPERT_VALIDATED", "SUPERSEDED"},
    "EXPERT_VALIDATED": {"SUPERSEDED"},
    "REJECTED": {"SUPERSEDED"},
    "SUPERSEDED": set(),
}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _refs(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(str(v).strip() for v in values if str(v).strip()))


async def create_review(
    *,
    actor_id: str,
    case_id: str,
    subject: str,
    prepared_by: str,
    evidence_refs: Iterable[str],
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    case = await db.professional_cases.find_one({"id": case_id}, {"_id": 0})
    if not case:
        raise LookupError("professional case not found")
    refs = _refs(evidence_refs)
    if not refs:
        raise ValueError("review requires evidence")
    prepared = str(prepared_by or "").upper()
    if prepared not in {"HUMAN", "AI"}:
        raise ValueError("prepared_by must be HUMAN or AI")
    state = "AI_PREPARED" if prepared == "AI" else "DRAFT"
    row = {
        "id": _id("PREVIEW"),
        "case_id": case_id,
        "domain": case["domain"],
        "subject": subject.strip(),
        "state": state,
        "prepared_by": prepared,
        "evidence_refs": refs,
        "metadata": metadata or {},
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }
    if not row["subject"]:
        raise ValueError("review subject is required")
    await db.governance_reviews.insert_one(dict(row))
    await governance.audit_event(
        event_type="governance.review.created",
        actor_id=actor_id,
        resource_type="professional_review",
        resource_id=row["id"],
        payload={"case_id": case_id, "state": state, "prepared_by": prepared},
        after=row,
        reason="Professional review created",
        result=state,
    )
    return row


async def transition_review(
    *,
    actor_id: str,
    actor_role: str,
    authority_level: str,
    review_id: str,
    target_state: str,
    policy_version_id: Optional[str],
    rationale: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    review = await db.governance_reviews.find_one({"id": review_id}, {"_id": 0})
    if not review:
        raise LookupError("professional review not found")
    target = str(target_state or "").upper()
    if target not in STATES or target not in TRANSITIONS[review["state"]]:
        raise ValueError(f"invalid professional review transition {review['state']}->{target}")
    refs = _refs(evidence_refs)
    if not rationale.strip() or not refs:
        raise ValueError("review transition requires rationale and evidence")

    authority = None
    if target in {"CVL_APPROVED", "EXPERT_VALIDATED"}:
        if not policy_version_id:
            raise ValueError("approval/validation requires authority policy version")
        action = "PROFESSIONAL_REVIEW_CVL_APPROVE" if target == "CVL_APPROVED" else "PROFESSIONAL_REVIEW_EXPERT_VALIDATE"
        authority = await authority_policy.evaluate_authority(
            actor_id=actor_id,
            actor_role=actor_role,
            action=action,
            context={
                "domain": review["domain"],
                "authority_level": authority_level,
                "case_id": review["case_id"],
                "review_id": review_id,
            },
            policy_version_id=policy_version_id,
        )
        if authority["decision"] != "ALLOW":
            raise PermissionError("authority policy did not allow review transition")

    now = utc_now_iso()
    update = {
        "state": target,
        "last_rationale": rationale.strip(),
        "last_evidence_refs": refs,
        "authority_decision_id": authority["id"] if authority else None,
        "policy_version_id": authority["policy_version_id"] if authority else None,
        "updated_by": actor_id,
        "updated_at": now,
    }
    result = await db.governance_reviews.update_one(
        {"id": review_id, "state": review["state"]}, {"$set": update}
    )
    if result.modified_count != 1:
        raise ValueError("professional review changed concurrently")
    after = {**review, **update}
    await governance.audit_event(
        event_type="governance.review.state_changed",
        actor_id=actor_id,
        resource_type="professional_review",
        resource_id=review_id,
        payload={
            "from": review["state"],
            "to": target,
            "authority_decision_id": update["authority_decision_id"],
            "evidence_refs": refs,
        },
        before=review,
        after=after,
        reason=rationale.strip(),
        result=target,
    )
    return after
