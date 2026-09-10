"""Risk operations for Academy P0 controls.

Builds incident-to-risk linkage and evidence-first insurance review triggers.
It does not purchase insurance or claim coverage; those remain human/external
operations requiring verified provider documents.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import assurance_core


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


async def cascade_incident_to_risk(
    *,
    actor_id: str,
    incident_type: str,
    incident_id: str,
    title: str,
    domain: str,
    impact: int,
    probability: int,
    owner: Optional[str] = None,
    mitigation: Optional[str] = None,
    deadline: Optional[str] = None,
    evidence_refs: Iterable[str] = (),
) -> Dict[str, Any]:
    source_type = incident_type.upper()
    existing = await db.risks.find_one(
        {"source_type": source_type, "source_id": incident_id}, {"_id": 0}
    )
    if existing:
        return existing
    risk = await assurance_core.create_risk(
        actor_id=actor_id,
        title=title,
        domain=domain,
        impact=impact,
        probability=probability,
        owner=owner,
        mitigation=mitigation,
        deadline=deadline,
        evidence_refs=[incident_id, *list(evidence_refs)],
    )
    await db.risks.update_one(
        {"id": risk["id"]},
        {"$set": {"source_type": source_type, "source_id": incident_id}},
    )
    return {**risk, "source_type": source_type, "source_id": incident_id}


async def create_insurance_review_trigger(
    *,
    actor_id: str,
    risk_id: str,
    reason: str,
    coverage_types: Iterable[str],
    broker_or_provider: Optional[str] = None,
) -> Dict[str, Any]:
    risk = await db.risks.find_one({"id": risk_id}, {"_id": 0})
    if not risk:
        raise LookupError("risk not found")
    existing = await db.insurance_review_triggers.find_one(
        {"risk_id": risk_id, "status": {"$in": ["OPEN", "IN_REVIEW"]}}, {"_id": 0}
    )
    if existing:
        return existing
    row = {
        "id": _id("INSREV"),
        "risk_id": risk_id,
        "risk_level": risk.get("level"),
        "reason": reason,
        "coverage_types": sorted({item.upper() for item in coverage_types}),
        "broker_or_provider": broker_or_provider,
        "status": "OPEN",
        "coverage_confirmed": False,
        "evidence_refs": [],
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }
    await db.insurance_review_triggers.insert_one(dict(row))
    return row


async def record_insurance_review(
    *,
    actor_id: str,
    trigger_id: str,
    coverage_confirmed: bool,
    evidence_refs: Iterable[str],
    notes: Optional[str] = None,
) -> Dict[str, Any]:
    row = await db.insurance_review_triggers.find_one({"id": trigger_id}, {"_id": 0})
    if not row:
        raise LookupError("insurance review trigger not found")
    refs = list(evidence_refs)
    if coverage_confirmed and not refs:
        raise ValueError("coverage cannot be confirmed without evidence")
    now = utc_now_iso()
    status = "CLOSED" if refs else "IN_REVIEW"
    update = {
        "coverage_confirmed": coverage_confirmed,
        "evidence_refs": refs,
        "notes": notes,
        "status": status,
        "reviewed_by": actor_id,
        "updated_at": now,
    }
    await db.insurance_review_triggers.update_one({"id": trigger_id}, {"$set": update})
    return {**row, **update}


async def auto_insurance_review_for_critical_risk(
    *, actor_id: str, risk_id: str
) -> Optional[Dict[str, Any]]:
    risk = await db.risks.find_one({"id": risk_id}, {"_id": 0})
    if not risk:
        raise LookupError("risk not found")
    if int(risk.get("level", 0)) < 4:
        return None
    return await create_insurance_review_trigger(
        actor_id=actor_id,
        risk_id=risk_id,
        reason="Risk level requires insurance/transfer review",
        coverage_types=[risk.get("domain", "GENERAL")],
    )


async def cascade_privacy_incident(
    *,
    actor_id: str,
    incident_id: str,
    impact: int,
    probability: int,
    owner: Optional[str] = None,
    mitigation: Optional[str] = None,
    deadline: Optional[str] = None,
    jurisdiction: Optional[str] = None,
    evidence_refs: Iterable[str] = (),
) -> Dict[str, Any]:
    """Project one real privacy incident into Legal + Risk + Insurance review.

    Severity is intentionally *not* converted into impact/probability here: the
    Academy target does not define that mapping, so callers must provide the
    scored inputs explicitly instead of this service inventing policy.
    """
    incident = await db.privacy_incidents.find_one({"id": incident_id}, {"_id": 0})
    if not incident:
        raise LookupError("privacy incident not found")

    legal = await db.legal_documents.find_one(
        {"case_id": incident_id, "document_type": "PRIVACY_INCIDENT_CASE"}, {"_id": 0}
    )
    if not legal:
        legal = await assurance_core.create_legal_document(
            actor_id=actor_id,
            title=f"Privacy incident case — {incident.get('title', incident_id)}",
            document_type="PRIVACY_INCIDENT_CASE",
            case_id=incident_id,
            jurisdiction=jurisdiction,
            metadata={
                "source_type": "PRIVACY_INCIDENT",
                "source_id": incident_id,
                "severity": incident.get("severity"),
                "data_classes": incident.get("data_classes", []),
            },
        )

    risk = await cascade_incident_to_risk(
        actor_id=actor_id,
        incident_type="PRIVACY_INCIDENT",
        incident_id=incident_id,
        title=f"Privacy incident risk — {incident.get('title', incident_id)}",
        domain="PRIVACY",
        impact=impact,
        probability=probability,
        owner=owner,
        mitigation=mitigation,
        deadline=deadline,
        evidence_refs=[legal["id"], *list(evidence_refs)],
    )

    insurance_review = await auto_insurance_review_for_critical_risk(
        actor_id=actor_id, risk_id=risk["id"]
    )
    return {
        "incident": incident,
        "legal_case": legal,
        "risk": risk,
        "insurance_review": insurance_review,
    }
