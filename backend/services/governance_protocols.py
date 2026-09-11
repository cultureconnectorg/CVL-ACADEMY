"""Governance escalation protocol (GOV-13).

Escalations are evidence-bearing governance records linked to an existing canonical
case, incident, risk or legal matter. This module does not create parallel domain
stores. Acknowledgement requires an explicit ALLOW decision from the canonical
Authority Policy Engine bound to the exact escalation.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import authority_policy
from services import professional_governance as governance

SOURCE_COLLECTIONS = {
    "PROFESSIONAL_CASE": "professional_cases",
    "INCIDENT": "incidents",
    "RISK": "risks",
    "LEGAL_MATTER": "legal_matters",
}
SEVERITIES = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
STATES = {"OPEN", "ACKNOWLEDGED", "RESOLVED", "CANCELLED"}
TRANSITIONS = {
    "OPEN": {"ACKNOWLEDGED", "CANCELLED"},
    "ACKNOWLEDGED": {"RESOLVED", "CANCELLED"},
    "RESOLVED": set(),
    "CANCELLED": set(),
}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _refs(values: Iterable[str]) -> list[str]:
    return list(
        dict.fromkeys(str(value).strip() for value in values if str(value).strip())
    )


async def _source(source_type: str, source_id: str) -> Dict[str, Any]:
    kind = str(source_type or "").strip().upper()
    collection_name = SOURCE_COLLECTIONS.get(kind)
    if not collection_name:
        raise ValueError("unsupported escalation source_type")
    collection = getattr(db, collection_name)
    row = await collection.find_one({"id": source_id}, {"_id": 0})
    if not row:
        raise LookupError("escalation source not found")
    return row


async def create_escalation(
    *,
    actor_id: str,
    source_type: str,
    source_id: str,
    domain: str,
    severity: str,
    target_authority_level: str,
    reason: str,
    evidence_refs: Iterable[str],
    case_id: Optional[str] = None,
) -> Dict[str, Any]:
    source_kind = str(source_type or "").strip().upper()
    severity_key = str(severity or "").strip().upper()
    refs = _refs(evidence_refs)
    if severity_key not in SEVERITIES:
        raise ValueError("invalid escalation severity")
    if not domain.strip() or not target_authority_level.strip() or not reason.strip():
        raise ValueError("escalation requires domain, target authority and reason")
    if not refs:
        raise ValueError("escalation requires evidence")
    await _source(source_kind, source_id)
    if case_id:
        case = await db.professional_cases.find_one({"id": case_id}, {"_id": 0})
        if not case:
            raise LookupError("professional case not found")

    existing = await db.governance_escalations.find_one(
        {
            "source_type": source_kind,
            "source_id": source_id,
            "status": {"$in": ["OPEN", "ACKNOWLEDGED"]},
        },
        {"_id": 0},
    )
    if existing:
        return existing

    now = utc_now_iso()
    row = {
        "id": _id("ESC"),
        "source_type": source_kind,
        "source_id": source_id,
        "case_id": case_id,
        "domain": domain.strip().upper(),
        "severity": severity_key,
        "target_authority_level": target_authority_level.strip().upper(),
        "reason": reason.strip(),
        "evidence_refs": refs,
        "status": "OPEN",
        "authority_decision_id": None,
        "acknowledged_by": None,
        "acknowledged_at": None,
        "resolution": None,
        "created_by": actor_id,
        "created_at": now,
        "updated_at": now,
    }
    await db.governance_escalations.insert_one(dict(row))
    await governance.audit_event(
        event_type="governance.escalation.opened",
        actor_id=actor_id,
        resource_type="governance_escalation",
        resource_id=row["id"],
        after=row,
        reason=row["reason"],
        result="OPEN",
        payload={
            "source_type": source_kind,
            "source_id": source_id,
            "domain": row["domain"],
            "severity": severity_key,
            "target_authority_level": row["target_authority_level"],
            "evidence_refs": refs,
        },
    )
    return row


async def acknowledge_escalation(
    *,
    actor_id: str,
    escalation_id: str,
    authority_decision_id: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    row = await db.governance_escalations.find_one(
        {"id": escalation_id}, {"_id": 0}
    )
    if not row:
        raise LookupError("governance escalation not found")
    if row["status"] != "OPEN":
        raise ValueError("only OPEN escalation can be acknowledged")
    refs = _refs(evidence_refs)
    if not refs:
        raise ValueError("escalation acknowledgement requires evidence")

    decision = await authority_policy.get_decision(authority_decision_id)
    if decision.get("decision") != "ALLOW":
        raise PermissionError("escalation acknowledgement requires ALLOW authority")
    if str(decision.get("action", "")).upper() != "GOVERNANCE_ESCALATION_ACKNOWLEDGE":
        raise ValueError("authority decision action does not acknowledge escalation")
    context = decision.get("context") or {}
    if context.get("escalation_id") != escalation_id:
        raise ValueError("authority decision is not bound to this escalation")
    if str(context.get("domain", "")).upper() != row["domain"]:
        raise ValueError("authority decision domain does not match escalation")
    authority_level = str(context.get("authority_level", "")).upper()
    if authority_level != row["target_authority_level"]:
        raise ValueError("authority decision level does not match escalation target")

    now = utc_now_iso()
    update = {
        "status": "ACKNOWLEDGED",
        "authority_decision_id": decision["id"],
        "authority_decision_hash": decision.get("decision_hash"),
        "acknowledgement_evidence_refs": refs,
        "acknowledged_by": actor_id,
        "acknowledged_at": now,
        "updated_at": now,
    }
    result = await db.governance_escalations.update_one(
        {"id": escalation_id, "status": "OPEN"}, {"$set": update}
    )
    if result.modified_count != 1:
        raise ValueError("escalation changed concurrently")
    after = {**row, **update}
    await governance.audit_event(
        event_type="governance.escalation.acknowledged",
        actor_id=actor_id,
        resource_type="governance_escalation",
        resource_id=escalation_id,
        before=row,
        after=after,
        result="ACKNOWLEDGED",
        payload={
            "authority_decision_id": decision["id"],
            "evidence_refs": refs,
        },
    )
    return after


async def close_escalation(
    *,
    actor_id: str,
    escalation_id: str,
    status: str,
    resolution: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    row = await db.governance_escalations.find_one(
        {"id": escalation_id}, {"_id": 0}
    )
    if not row:
        raise LookupError("governance escalation not found")
    target = str(status or "").strip().upper()
    if target not in {"RESOLVED", "CANCELLED"}:
        raise ValueError("escalation can only close as RESOLVED or CANCELLED")
    if target not in TRANSITIONS.get(row["status"], set()):
        raise ValueError(f"invalid escalation transition {row['status']}->{target}")
    refs = _refs(evidence_refs)
    if not resolution.strip() or not refs:
        raise ValueError("escalation closure requires resolution and evidence")

    now = utc_now_iso()
    update = {
        "status": target,
        "resolution": resolution.strip(),
        "closure_evidence_refs": refs,
        "closed_by": actor_id,
        "closed_at": now,
        "updated_at": now,
    }
    result = await db.governance_escalations.update_one(
        {"id": escalation_id, "status": row["status"]}, {"$set": update}
    )
    if result.modified_count != 1:
        raise ValueError("escalation changed concurrently")
    after = {**row, **update}
    await governance.audit_event(
        event_type="governance.escalation.closed",
        actor_id=actor_id,
        resource_type="governance_escalation",
        resource_id=escalation_id,
        before=row,
        after=after,
        reason=resolution.strip(),
        result=target,
        payload={"evidence_refs": refs},
    )
    return after


async def escalation_gate(*, domain: Optional[str] = None) -> Dict[str, Any]:
    query: Dict[str, Any] = {"status": {"$in": ["OPEN", "ACKNOWLEDGED"]}}
    if domain:
        query["domain"] = domain.strip().upper()
    rows = await db.governance_escalations.find(query, {"_id": 0}).to_list(10000)
    blockers = [
        row
        for row in rows
        if row.get("severity") in {"HIGH", "CRITICAL"}
        and row.get("status") != "RESOLVED"
    ]
    return {
        "pass": not blockers,
        "blocking_count": len(blockers),
        "blocking_escalations": blockers,
        "open_count": len(rows),
    }
