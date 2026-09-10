"""Privacy operations for CVLN Academy.

Implements operational P0 primitives from the Academy master: retention rules,
delete-request workflow, processor/vendor registry and privacy-incident to risk
cascade. These are control-plane records; destructive erasure is never silently
performed by this module. A verified execution step must explicitly record each
erasure/anonymisation action and its evidence.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import assurance_core


DELETION_STATES = {
    "OPEN",
    "IDENTITY_VERIFIED",
    "IMPACT_ASSESSED",
    "APPROVED",
    "EXECUTING",
    "COMPLETED",
    "REJECTED",
}
PROCESSOR_STATES = {"PROPOSED", "APPROVED", "SUSPENDED", "RETIRED"}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


async def create_retention_rule(
    *,
    actor_id: str,
    data_class: str,
    retention_days: int,
    trigger: str,
    action: str,
    legal_hold_blocks: bool = True,
    evidence_refs: Iterable[str] = (),
) -> Dict[str, Any]:
    if retention_days < 0:
        raise ValueError("retention_days must be >= 0")
    target_action = action.upper()
    if target_action not in {"DELETE", "ANONYMIZE", "ARCHIVE", "REVIEW"}:
        raise ValueError("invalid retention action")
    row = {
        "id": _id("RET"),
        "data_class": data_class.upper(),
        "retention_days": retention_days,
        "trigger": trigger.upper(),
        "action": target_action,
        "legal_hold_blocks": legal_hold_blocks,
        "evidence_refs": list(evidence_refs),
        "status": "ACTIVE",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }
    await db.privacy_retention_rules.update_one(
        {"data_class": row["data_class"], "trigger": row["trigger"]},
        {"$set": row},
        upsert=True,
    )
    return row


async def register_processor(
    *,
    actor_id: str,
    name: str,
    service: str,
    data_classes: Iterable[str],
    regions: Iterable[str],
    dpa_evidence_ref: Optional[str] = None,
    subprocessor_url: Optional[str] = None,
) -> Dict[str, Any]:
    row = {
        "id": _id("PROC"),
        "name": name,
        "service": service,
        "data_classes": sorted({x.upper() for x in data_classes}),
        "regions": sorted(set(regions)),
        "dpa_evidence_ref": dpa_evidence_ref,
        "subprocessor_url": subprocessor_url,
        "status": "PROPOSED",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }
    await db.privacy_processors.insert_one(dict(row))
    return row


async def transition_processor(
    *, actor_id: str, processor_id: str, status: str
) -> Dict[str, Any]:
    target = status.upper()
    if target not in PROCESSOR_STATES:
        raise ValueError("invalid processor status")
    row = await db.privacy_processors.find_one({"id": processor_id}, {"_id": 0})
    if not row:
        raise LookupError("processor not found")
    if target == "APPROVED" and not row.get("dpa_evidence_ref"):
        raise ValueError("processor cannot be approved without DPA evidence")
    now = utc_now_iso()
    await db.privacy_processors.update_one(
        {"id": processor_id},
        {"$set": {"status": target, "updated_at": now, "last_actor_id": actor_id}},
    )
    return {**row, "status": target, "updated_at": now}


async def create_deletion_request(
    *,
    actor_id: str,
    user_id: str,
    reason: str,
) -> Dict[str, Any]:
    row = {
        "id": _id("DEL"),
        "user_id": user_id,
        "reason": reason,
        "status": "OPEN",
        "impact": None,
        "execution_log": [],
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }
    await db.privacy_deletion_requests.insert_one(dict(row))
    return row


async def transition_deletion_request(
    *,
    actor_id: str,
    request_id: str,
    status: str,
    impact: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    target = status.upper()
    if target not in DELETION_STATES:
        raise ValueError("invalid deletion status")
    row = await db.privacy_deletion_requests.find_one({"id": request_id}, {"_id": 0})
    if not row:
        raise LookupError("deletion request not found")
    allowed = {
        "OPEN": {"IDENTITY_VERIFIED", "REJECTED"},
        "IDENTITY_VERIFIED": {"IMPACT_ASSESSED", "REJECTED"},
        "IMPACT_ASSESSED": {"APPROVED", "REJECTED"},
        "APPROVED": {"EXECUTING"},
        "EXECUTING": {"COMPLETED"},
        "COMPLETED": set(),
        "REJECTED": set(),
    }
    if target not in allowed[row["status"]]:
        raise ValueError(f"invalid deletion transition {row['status']}->{target}")
    if target == "IMPACT_ASSESSED" and not impact:
        raise ValueError("impact assessment required")
    now = utc_now_iso()
    update: Dict[str, Any] = {
        "status": target,
        "updated_at": now,
        "last_actor_id": actor_id,
    }
    if impact is not None:
        update["impact"] = impact
    await db.privacy_deletion_requests.update_one({"id": request_id}, {"$set": update})
    return {**row, **update}


async def record_deletion_execution(
    *,
    actor_id: str,
    request_id: str,
    resource_type: str,
    action: str,
    evidence_ref: str,
) -> Dict[str, Any]:
    request = await db.privacy_deletion_requests.find_one(
        {"id": request_id}, {"_id": 0}
    )
    if not request:
        raise LookupError("deletion request not found")
    if request["status"] != "EXECUTING":
        raise ValueError("deletion request must be EXECUTING")
    entry = {
        "id": _id("DELEX"),
        "resource_type": resource_type,
        "action": action.upper(),
        "evidence_ref": evidence_ref,
        "actor_id": actor_id,
        "executed_at": utc_now_iso(),
    }
    await db.privacy_deletion_requests.update_one(
        {"id": request_id}, {"$push": {"execution_log": entry}}
    )
    return entry


async def cascade_privacy_incident_to_risk(
    *,
    actor_id: str,
    incident_id: str,
    impact: int,
    probability: int,
    owner: Optional[str] = None,
    mitigation: Optional[str] = None,
    deadline: Optional[str] = None,
    evidence_refs: Iterable[str] = (),
) -> Dict[str, Any]:
    incident = await db.privacy_incidents.find_one({"id": incident_id}, {"_id": 0})
    if not incident:
        raise LookupError("privacy incident not found")
    existing = await db.risks.find_one(
        {"source_type": "PRIVACY_INCIDENT", "source_id": incident_id}, {"_id": 0}
    )
    if existing:
        return existing
    risk = await assurance_core.create_risk(
        actor_id=actor_id,
        title=f"Privacy incident: {incident['title']}",
        domain="PRIVACY",
        impact=impact,
        probability=probability,
        owner=owner,
        mitigation=mitigation,
        deadline=deadline,
        evidence_refs=[incident_id, *list(evidence_refs)],
    )
    await db.risks.update_one(
        {"id": risk["id"]},
        {"$set": {"source_type": "PRIVACY_INCIDENT", "source_id": incident_id}},
    )
    return {**risk, "source_type": "PRIVACY_INCIDENT", "source_id": incident_id}
