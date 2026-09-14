"""Quality evidence core for CVLN Academy.

Implements Academy-side evidence and workflow primitives. It records who carries
quality responsibility and the evidence required for delivery; it does not claim
that a partner's external certification or regulatory status is validated unless
explicit evidence is attached.

P0 quality rules intentionally reuse the canonical Evidence Graph and Incident Core:
quality packs reference source evidence, and escalated complaints project from one
canonical incident instead of creating separate Legal/Privacy/Security/Risk truths.
"""

from __future__ import annotations

import uuid
from collections import Counter
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import evidence_graph, incident_core


COMPLAINT_STATES = {"OPEN", "ACKNOWLEDGED", "INVESTIGATING", "RESOLVED", "ESCALATED", "CLOSED"}
IMPROVEMENT_STATES = {"OPEN", "IN_PROGRESS", "VERIFIED", "CLOSED"}
QUALITY_LEVELS = {"Q1_INFORMATION", "Q2_SERVICE", "Q3_QUALITY", "Q4_RIGHTS", "Q5_LEGAL_SAFETY"}


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
    refs = list(dict.fromkeys(evidence_refs))
    row = {
        "id": _id("QPART"),
        "name": name,
        "organisation": organisation,
        "claimed_certifications": sorted(set(claimed_certifications)),
        "evidence_refs": refs,
        # Evidence presence proves only that evidence was attached. It does not let
        # Academy assert the external certification itself without human/external review.
        "verification_status": "EVIDENCE_ATTACHED" if refs else "UNVERIFIED",
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
    if not await db.quality_partners.find_one({"id": partner_id, "status": "ACTIVE"}):
        raise LookupError("active quality partner not found")
    refs = list(dict.fromkeys(evidence_refs))
    if not refs:
        raise ValueError("quality scope assignment requires contractual/authority evidence")
    existing = await db.quality_scopes.find_one(
        {
            "partner_id": partner_id,
            "formation_code": formation_code,
            "cohort_id": cohort_id,
            "status": "ACTIVE",
        },
        {"_id": 0},
    )
    if existing:
        return existing
    row = {
        "id": _id("QSCOPE"),
        "partner_id": partner_id,
        "formation_code": formation_code,
        "cohort_id": cohort_id,
        "evidence_refs": refs,
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
    if signed_at and not evidence_ref:
        raise ValueError("signed attendance requires evidence_ref")
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
    """Backward-compatible raw aggregate; never makes a governance decision."""
    rows = await db.quality_satisfaction.find(
        {"formation_code": formation_code}, {"_id": 0}
    ).to_list(10000)
    if not rows:
        return {"formation_code": formation_code, "responses": 0, "average": None}
    avg = sum(row["score"] for row in rows) / len(rows)
    return {"formation_code": formation_code, "responses": len(rows), "average": round(avg, 2)}


async def satisfaction_analysis(formation_code: str) -> Dict[str, Any]:
    """Expose multi-signal quality data without inventing a pass/fail threshold."""
    rows = await db.quality_satisfaction.find(
        {"formation_code": formation_code}, {"_id": 0}
    ).sort("recorded_at", 1).to_list(10000)
    distribution = Counter(int(row["score"]) for row in rows)
    average = None if not rows else round(sum(row["score"] for row in rows) / len(rows), 2)
    first_half = rows[: max(1, len(rows) // 2)] if rows else []
    second_half = rows[max(1, len(rows) // 2) :] if len(rows) > 1 else []
    trend = None
    if first_half and second_half:
        before = sum(row["score"] for row in first_half) / len(first_half)
        after = sum(row["score"] for row in second_half) / len(second_half)
        trend = round(after - before, 2)
    return {
        "formation_code": formation_code,
        "responses": len(rows),
        "average": average,
        "distribution": {str(score): distribution.get(score, 0) for score in range(1, 6)},
        "trend_delta": trend,
        "governance_decision": None,
        "note": "Metrics are evidence inputs; no single satisfaction threshold governs quality.",
    }


async def create_complaint(
    *,
    actor_id: str,
    user_id: Optional[str],
    formation_code: Optional[str],
    category: str,
    description: str,
    severity: str,
    quality_level: Optional[str] = None,
) -> Dict[str, Any]:
    level = quality_level.upper() if quality_level else "UNCLASSIFIED"
    if quality_level and level not in QUALITY_LEVELS:
        raise ValueError("invalid quality complaint level")
    row = {
        "id": _id("COMP"),
        "user_id": user_id,
        "formation_code": formation_code,
        "category": category.upper(),
        "description": description,
        "severity": severity.upper(),
        "quality_level": level,
        "canonical_incident_id": None,
        "status": "OPEN",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }
    await db.quality_complaints.insert_one(dict(row))
    return row


async def classify_and_escalate_complaint(
    *,
    actor_id: str,
    complaint_id: str,
    quality_level: str,
    evidence_refs: Iterable[str],
    projection_domains: Iterable[str] = (),
) -> Dict[str, Any]:
    complaint = await db.quality_complaints.find_one({"id": complaint_id}, {"_id": 0})
    if not complaint:
        raise LookupError("quality complaint not found")
    level = quality_level.upper()
    if level not in QUALITY_LEVELS:
        raise ValueError("invalid quality complaint level")
    refs = list(dict.fromkeys(evidence_refs))
    if not refs:
        raise ValueError("complaint classification requires evidence")

    domains = sorted({item.upper() for item in projection_domains})
    incident = None
    if level in {"Q4_RIGHTS", "Q5_LEGAL_SAFETY"}:
        if not domains:
            raise ValueError("Q4/Q5 complaint escalation requires explicit projection_domains")
        if level == "Q5_LEGAL_SAFETY" and not any(
            item in {"LEGAL", "SECURITY", "PRIVACY", "RISK"} for item in domains
        ):
            raise ValueError("Q5 complaint requires a legal/safety-related projection domain")
        if complaint.get("canonical_incident_id"):
            incident = await db.incidents.find_one(
                {"id": complaint["canonical_incident_id"]}, {"_id": 0}
            )
        if not incident:
            incident = await incident_core.create_incident(
                actor_id=actor_id,
                title=f"Quality complaint escalation — {complaint['id']}",
                description=complaint["description"],
                severity=complaint["severity"],
                domains=domains,
                evidence_refs=[complaint["id"], *refs],
                metadata={"source_type": "QUALITY_COMPLAINT", "source_id": complaint["id"], "quality_level": level},
            )
    now = utc_now_iso()
    update = {
        "quality_level": level,
        "classification_evidence_refs": refs,
        "canonical_incident_id": incident["id"] if incident else None,
        "status": "ESCALATED" if incident else complaint["status"],
        "updated_at": now,
        "last_actor_id": actor_id,
    }
    await db.quality_complaints.update_one({"id": complaint_id}, {"$set": update})
    return {**complaint, **update}


async def transition_complaint(
    *, actor_id: str, complaint_id: str, state: str, resolution: Optional[str] = None
) -> Dict[str, Any]:
    target = state.upper()
    if target not in COMPLAINT_STATES:
        raise ValueError("invalid complaint state")
    row = await db.quality_complaints.find_one({"id": complaint_id}, {"_id": 0})
    if not row:
        raise LookupError("complaint not found")
    if target in {"RESOLVED", "CLOSED"} and not resolution:
        raise ValueError(f"{target.lower()} complaint requires resolution evidence/statement")
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
    refs = list(dict.fromkeys(source_refs))
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


async def create_quality_audit_pack(
    *,
    actor_id: str,
    partner_id: str,
    formation_code: str,
    cohort_id: Optional[str],
    node_ids: Iterable[str],
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    """QLT-013: compose canonical evidence references for an assigned quality scope."""
    scope = await db.quality_scopes.find_one(
        {
            "partner_id": partner_id,
            "formation_code": formation_code,
            "cohort_id": cohort_id,
            "status": "ACTIVE",
        },
        {"_id": 0},
    )
    if not scope:
        raise PermissionError("quality partner has no active scope for formation/cohort")
    refs = list(dict.fromkeys(evidence_refs))
    if not refs:
        raise ValueError("quality audit pack requires composition evidence")
    pack = await evidence_graph.create_pack(
        actor_id=actor_id,
        title=f"Quality audit pack — {formation_code}" + (f" / {cohort_id}" if cohort_id else ""),
        consumer="QUALITY",
        node_ids=node_ids,
        purpose="Quality audit / partner review",
        evidence_refs=[scope["id"], *refs],
    )
    await db.quality_audit_packs.insert_one(
        {
            "id": _id("QPACK"),
            "partner_id": partner_id,
            "formation_code": formation_code,
            "cohort_id": cohort_id,
            "scope_id": scope["id"],
            "evidence_pack_id": pack["id"],
            "created_by": actor_id,
            "created_at": utc_now_iso(),
        }
    )
    return pack


async def quality_partner_workspace(partner_id: str) -> Dict[str, Any]:
    """QLT-014 data boundary: only records reachable through partner scopes."""
    partner = await db.quality_partners.find_one({"id": partner_id, "status": "ACTIVE"}, {"_id": 0})
    if not partner:
        raise LookupError("active quality partner not found")
    scopes = await db.quality_scopes.find(
        {"partner_id": partner_id, "status": "ACTIVE"}, {"_id": 0}
    ).to_list(1000)
    scoped_records = []
    for scope in scopes:
        query: Dict[str, Any] = {"formation_code": scope["formation_code"]}
        if scope.get("cohort_id"):
            query["cohort_id"] = scope["cohort_id"]
        scoped_records.append(
            {
                "scope": scope,
                "learner_evidence": await db.quality_learner_evidence.find(query, {"_id": 0}).to_list(5000),
                "attendance": await db.quality_attendance.find(query, {"_id": 0}).to_list(5000),
                "satisfaction": await db.quality_satisfaction.find(
                    {"formation_code": scope["formation_code"]}, {"_id": 0}
                ).to_list(5000),
                "complaints": await db.quality_complaints.find(
                    {"formation_code": scope["formation_code"]}, {"_id": 0}
                ).to_list(5000),
            }
        )
    return {"partner": partner, "scopes": scoped_records, "global_access": False}
