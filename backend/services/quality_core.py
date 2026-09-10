"""Quality evidence core for CVLN Academy.

Implements Academy-side evidence and workflow primitives. It records who
carries quality responsibility and the evidence required for delivery; it does
not claim that a partner's external certification or regulatory status is
validated unless explicit evidence is attached.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso


COMPLAINT_STATES = {"OPEN", "ACKNOWLEDGED", "INVESTIGATING", "RESOLVED", "ESCALATED", "CLOSED"}
IMPROVEMENT_STATES = {"OPEN", "IN_PROGRESS", "VERIFIED", "CLOSED"}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


async def register_partner(
    *,
    actor_id: str,
    name: str,
    organisation: str,
    evidence_refs: Iterable[str] = (),
    claimed_certifications: Iterable[str] = (),
) -> Dict[str, Any]:
    row = {
        "id": _id("QPART"),
        "name": name,
        "organisation": organisation,
        "claimed_certifications": sorted(set(claimed_certifications)),
        "evidence_refs": list(evidence_refs),
        "verification_status": "VERIFIED" if list(evidence_refs) else "UNVERIFIED",
        "status": "ACTIVE",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.quality_partners.insert_one(dict(row))
    return row


async def assign_formation_scope(
    *,
    actor_id: str,
    partner_id: str,
    formation_code: str,
    cohort_id: Optional[str] = None,
    evidence_refs: Iterable[str] = (),
) -> Dict[str, Any]:
    if not await db.quality_partners.find_one({"id": partner_id}):
        raise LookupError("quality partner not found")
    row = {
        "id": _id("QSCOPE"),
        "partner_id": partner_id,
        "formation_code": formation_code,
        "cohort_id": cohort_id,
        "evidence_refs": list(evidence_refs),
        "assigned_by": actor_id,
        "assigned_at": utc_now_iso(),
        "status": "ACTIVE",
    }
    await db.quality_scopes.insert_one(dict(row))
    return row


async def record_learner_quality_evidence(
    *,
    actor_id: str,
    user_id: str,
    formation_code: str,
    cohort_id: Optional[str],
    evidence_type: str,
    evidence_ref: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    row = {
        "id": _id("QEVID"),
        "user_id": user_id,
        "formation_code": formation_code,
        "cohort_id": cohort_id,
        "evidence_type": evidence_type.upper(),
        "evidence_ref": evidence_ref,
        "metadata": metadata or {},
        "recorded_by": actor_id,
        "recorded_at": utc_now_iso(),
    }
    await db.quality_learner_evidence.insert_one(dict(row))
    return row


async def learner_quality_file(user_id: str, formation_code: Optional[str] = None) -> Dict[str, Any]:
    query: Dict[str, Any] = {"user_id": user_id}
    if formation_code:
        query["formation_code"] = formation_code
    evidence = await db.quality_learner_evidence.find(query, {"_id": 0}).to_list(5000)
    attendance = await db.quality_attendance.find(query, {"_id": 0}).to_list(5000)
    satisfaction = await db.quality_satisfaction.find(query, {"_id": 0}).to_list(5000)
    return {
        "user_id": user_id,
        "formation_code": formation_code,
        "evidence": evidence,
        "attendance": attendance,
        "satisfaction": satisfaction,
    }


async def record_attendance(
    *,
    actor_id: str,
    user_id: str,
    formation_code: str,
    session_id: str,
    mode: str,
    attended: bool,
    signed_at: Optional[str] = None,
    evidence_ref: Optional[str] = None,
) -> Dict[str, Any]:
    row = {
        "id": _id("ATT"),
        "user_id": user_id,
        "formation_code": formation_code,
        "session_id": session_id,
        "mode": mode.upper(),
        "attended": attended,
        "signed_at": signed_at,
        "evidence_ref": evidence_ref,
        "recorded_by": actor_id,
        "recorded_at": utc_now_iso(),
    }
    await db.quality_attendance.insert_one(dict(row))
    return row


async def record_satisfaction(
    *,
    user_id: str,
    formation_code: str,
    score: int,
    comment: Optional[str] = None,
) -> Dict[str, Any]:
    if not 1 <= score <= 5:
        raise ValueError("satisfaction score must be 1..5")
    row = {
        "id": _id("SAT"),
        "user_id": user_id,
        "formation_code": formation_code,
        "score": score,
        "comment": comment,
        "recorded_at": utc_now_iso(),
    }
    await db.quality_satisfaction.insert_one(dict(row))
    return row


async def satisfaction_summary(formation_code: str) -> Dict[str, Any]:
    rows = await db.quality_satisfaction.find(
        {"formation_code": formation_code}, {"_id": 0}
    ).to_list(10000)
    if not rows:
        return {"formation_code": formation_code, "responses": 0, "average": None}
    avg = sum(row["score"] for row in rows) / len(rows)
    return {"formation_code": formation_code, "responses": len(rows), "average": round(avg, 2)}


async def create_complaint(
    *,
    actor_id: str,
    user_id: Optional[str],
    formation_code: Optional[str],
    category: str,
    description: str,
    severity: str,
) -> Dict[str, Any]:
    row = {
        "id": _id("COMP"),
        "user_id": user_id,
        "formation_code": formation_code,
        "category": category.upper(),
        "description": description,
        "severity": severity.upper(),
        "status": "OPEN",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }
    await db.quality_complaints.insert_one(dict(row))
    return row


async def transition_complaint(
    *, actor_id: str, complaint_id: str, state: str, resolution: Optional[str] = None
) -> Dict[str, Any]:
    target = state.upper()
    if target not in COMPLAINT_STATES:
        raise ValueError("invalid complaint state")
    row = await db.quality_complaints.find_one({"id": complaint_id}, {"_id": 0})
    if not row:
        raise LookupError("complaint not found")
    update = {"status": target, "updated_at": utc_now_iso(), "last_actor_id": actor_id}
    if resolution is not None:
        update["resolution"] = resolution
    await db.quality_complaints.update_one({"id": complaint_id}, {"$set": update})
    return {**row, **update}


async def create_improvement_action(
    *,
    actor_id: str,
    title: str,
    source_refs: Iterable[str],
    owner: str,
    due_at: Optional[str] = None,
) -> Dict[str, Any]:
    refs = list(source_refs)
    if not refs:
        raise ValueError("improvement action requires at least one source signal")
    row = {
        "id": _id("QACT"),
        "title": title,
        "source_refs": refs,
        "owner": owner,
        "due_at": due_at,
        "status": "OPEN",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }
    await db.quality_improvement_actions.insert_one(dict(row))
    return row
