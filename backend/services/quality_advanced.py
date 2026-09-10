"""Advanced quality evidence controls (QLT-004/005/006/009/010/012/014/015).

The Quality Core remains the canonical operational source for partner scopes,
learner evidence, attendance, satisfaction, complaints and improvement actions.
This module composes existing records and XCP primitives; it does not claim external
Qualiopi/regulatory validation from self-entered data.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import evidence_graph, expert_access, policy_registry, quality_core


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _refs(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(str(v).strip() for v in values if str(v).strip()))


async def record_needs_assessment(
    *,
    actor_id: str,
    user_id: str,
    formation_code: str,
    needs: Iterable[str],
    prerequisites: Iterable[str],
    accommodations: Iterable[str] = (),
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    refs = _refs(evidence_refs)
    need_list = _refs(needs)
    prereq_list = _refs(prerequisites)
    if not refs or (not need_list and not prereq_list):
        raise ValueError("needs assessment requires needs/prerequisites and evidence")
    row = {
        "id": _id("QNEED"),
        "user_id": user_id,
        "formation_code": formation_code,
        "needs": need_list,
        "prerequisites": prereq_list,
        "accommodations": _refs(accommodations),
        "evidence_refs": refs,
        "status": "RECORDED",
        "recorded_by": actor_id,
        "recorded_at": utc_now_iso(),
    }
    await db.quality_needs_assessments.insert_one(dict(row))
    await quality_core.record_learner_quality_evidence(
        actor_id=actor_id,
        user_id=user_id,
        formation_code=formation_code,
        cohort_id=None,
        evidence_type="NEEDS_PREREQUISITES",
        evidence_ref=row["id"],
        metadata={"evidence_refs": refs},
    )
    return row


async def record_attendance_proof(
    *,
    actor_id: str,
    user_id: str,
    formation_code: str,
    session_id: str,
    mode: str,
    attended: bool,
    evidence_ref: str,
    signature_attestation_id: Optional[str] = None,
    signature_verification_id: Optional[str] = None,
) -> Dict[str, Any]:
    """QLT-005: a signed attendance is accepted only with verified native proof."""
    if not evidence_ref.strip():
        raise ValueError("attendance requires evidence_ref")
    signed_at = None
    if signature_attestation_id or signature_verification_id:
        if not signature_attestation_id or not signature_verification_id:
            raise ValueError("signed attendance requires attestation and verification ids")
        verification = await db.native_signature_verifications.find_one(
            {"id": signature_verification_id, "attestation_id": signature_attestation_id},
            {"_id": 0},
        )
        if not verification or verification.get("status") not in {
            "VERIFIED_FREK",
            "VERIFIED_FREK_BTC",
        }:
            raise ValueError("attendance signature is not independently verified")
        signed_at = verification["verified_at"]
    row = await quality_core.record_attendance(
        actor_id=actor_id,
        user_id=user_id,
        formation_code=formation_code,
        session_id=session_id,
        mode=mode,
        attended=attended,
        signed_at=signed_at,
        evidence_ref=evidence_ref,
    )
    extension = {
        "signature_attestation_id": signature_attestation_id,
        "signature_verification_id": signature_verification_id,
        "signature_verified": bool(signature_verification_id),
    }
    await db.quality_attendance.update_one({"id": row["id"]}, {"$set": extension})
    return {**row, **extension}


async def compose_learning_evidence(
    *,
    actor_id: str,
    user_id: str,
    formation_code: str,
    cohort_id: Optional[str],
    evidence_node_ids: Iterable[str],
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    """QLT-006: compose learning proofs by reference via XCP-004."""
    pack = await evidence_graph.create_pack(
        actor_id=actor_id,
        title=f"Learner quality evidence — {user_id} / {formation_code}",
        consumer="QUALITY",
        node_ids=evidence_node_ids,
        purpose="Learning, assessment, attendance and completion evidence",
        evidence_refs=evidence_refs,
    )
    await quality_core.record_learner_quality_evidence(
        actor_id=actor_id,
        user_id=user_id,
        formation_code=formation_code,
        cohort_id=cohort_id,
        evidence_type="EVIDENCE_GRAPH_PACK",
        evidence_ref=pack["id"],
        metadata={"composition_mode": "REFERENCE_ONLY"},
    )
    return pack


async def record_accessibility_review(
    *,
    actor_id: str,
    formation_code: str,
    scope: str,
    findings: Iterable[str],
    actions: Iterable[str],
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    refs = _refs(evidence_refs)
    if not scope.strip() or not refs:
        raise ValueError("accessibility review requires scope and evidence")
    row = {
        "id": _id("QACC"),
        "formation_code": formation_code,
        "scope": scope.strip(),
        "findings": _refs(findings),
        "actions": _refs(actions),
        "evidence_refs": refs,
        "status": "REVIEWED",
        "reviewed_by": actor_id,
        "reviewed_at": utc_now_iso(),
    }
    await db.quality_accessibility_reviews.insert_one(dict(row))
    return row


async def register_trainer_record(
    *,
    actor_id: str,
    trainer_id: str,
    display_name: str,
    competencies: Iterable[str],
    assigned_formations: Iterable[str],
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    refs = _refs(evidence_refs)
    skills = _refs(competencies)
    if not trainer_id.strip() or not display_name.strip() or not skills or not refs:
        raise ValueError("trainer record requires identity, competencies and evidence")
    row = {
        "id": _id("QTRAIN"),
        "trainer_id": trainer_id.strip(),
        "display_name": display_name.strip(),
        "competencies": skills,
        "assigned_formations": _refs(assigned_formations),
        "evidence_refs": refs,
        "verification_status": "EVIDENCE_ATTACHED_NOT_EXTERNAL_VALIDATED",
        "status": "ACTIVE",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.quality_trainers.update_one(
        {"trainer_id": row["trainer_id"]}, {"$set": row}, upsert=True
    )
    return row


async def quality_kpis(formation_code: str) -> Dict[str, Any]:
    satisfaction = await quality_core.satisfaction_analysis(formation_code)
    attendance = await db.quality_attendance.find(
        {"formation_code": formation_code}, {"_id": 0}
    ).to_list(10000)
    complaints = await db.quality_complaints.find(
        {"formation_code": formation_code}, {"_id": 0}
    ).to_list(10000)
    evidence = await db.quality_learner_evidence.find(
        {"formation_code": formation_code}, {"_id": 0}
    ).to_list(10000)
    attended = sum(1 for row in attendance if row.get("attended"))
    return {
        "formation_code": formation_code,
        "attendance_records": len(attendance),
        "attended_count": attended,
        "attendance_rate": round(attended / len(attendance), 4) if attendance else None,
        "satisfaction": satisfaction,
        "complaint_count": len(complaints),
        "open_complaint_count": sum(
            1 for row in complaints if row.get("status") not in {"RESOLVED", "CLOSED"}
        ),
        "evidence_record_count": len(evidence),
        "governance_decision": None,
        "status": "EVIDENCE_METRICS_ONLY",
    }


async def record_quality_retention_policy(
    *,
    actor_id: str,
    record_type: str,
    retention_days: int,
    policy_version_id: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    if retention_days < 0:
        raise ValueError("quality retention_days must be >= 0")
    refs = _refs(evidence_refs)
    policy = await policy_registry.require_effective_version(policy_version_id)
    if policy.get("policy_key") != "QUALITY_RETENTION":
        raise ValueError("quality retention requires QUALITY_RETENTION policy")
    if not refs:
        raise ValueError("quality retention requires evidence")
    row = {
        "id": _id("QRET"),
        "record_type": record_type.strip().upper(),
        "retention_days": retention_days,
        "policy_version_id": policy["id"],
        "policy_hash": policy["content_hash"],
        "evidence_refs": refs,
        "status": "ACTIVE",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.quality_retention_policies.update_one(
        {"record_type": row["record_type"]}, {"$set": row}, upsert=True
    )
    return row


async def get_quality_workspace(*, raw_key: str, case_id: str) -> Dict[str, Any]:
    """QLT-014: XCP-006 credential scoped to a QUALITY case."""
    context = await expert_access.authorize_case_scope(raw_key, case_id, "quality:case:read")
    case = await db.professional_cases.find_one({"id": case_id}, {"_id": 0})
    if not case:
        raise LookupError("professional case not found")
    if str(case.get("domain", "")).upper() != "QUALITY":
        raise PermissionError("quality workspace only exposes QUALITY cases")
    expert = context["expert"]
    if "QUALITY" not in {str(v).upper() for v in expert.get("domains", [])}:
        raise PermissionError("expert identity is not authorised for QUALITY domain")
    scope_ids = list((case.get("metadata") or {}).get("quality_scope_ids", []))
    scopes = await db.quality_scopes.find(
        {"id": {"$in": scope_ids}, "status": "ACTIVE"}, {"_id": 0}
    ).to_list(500)
    records = []
    for scope in scopes:
        query: Dict[str, Any] = {"formation_code": scope["formation_code"]}
        if scope.get("cohort_id"):
            query["cohort_id"] = scope["cohort_id"]
        records.append(
            {
                "scope": scope,
                "learner_evidence": await db.quality_learner_evidence.find(
                    query, {"_id": 0}
                ).to_list(5000),
                "attendance": await db.quality_attendance.find(query, {"_id": 0}).to_list(5000),
                "complaints": await db.quality_complaints.find(
                    {"formation_code": scope["formation_code"]}, {"_id": 0}
                ).to_list(5000),
            }
        )
    return {
        "case": case,
        "expert": {"id": expert["id"], "display_name": expert["display_name"]},
        "granted_scope": context["assignment"].get("scope", []),
        "scopes": records,
        "global_access": False,
    }
