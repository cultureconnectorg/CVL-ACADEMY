"""Operational privacy controls for CVLN Academy.

This module owns the existing canonical operational records for retention rules,
processor/vendor registry and deletion workflow. Cross-cutting classification,
retention execution and incident orchestration remain in XCP-002/XCP-003/XCP-005;
this module references those primitives instead of duplicating them.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import assurance_core, data_classification
from services import professional_governance as governance


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


def _refs(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(str(value).strip() for value in values if str(value).strip()))


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
    refs = _refs(evidence_refs)
    row = {
        "id": _id("RET"),
        "data_class": data_class.upper(),
        "retention_days": retention_days,
        "trigger": trigger.upper(),
        "action": target_action,
        "legal_hold_blocks": legal_hold_blocks,
        "evidence_refs": refs,
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
    await governance.audit_event(
        event_type="privacy.retention_rule.registered",
        actor_id=actor_id,
        resource_type="privacy_retention_rule",
        resource_id=row["id"],
        payload={
            "data_class": row["data_class"],
            "trigger": row["trigger"],
            "action": target_action,
            "retention_days": retention_days,
            "evidence_refs": refs,
        },
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
    purpose: Optional[str] = None,
    legal_entity: Optional[str] = None,
    transfer_mechanism: Optional[str] = None,
) -> Dict[str, Any]:
    """PRI-011: register provider and declare it into XCP-002 as UNCLASSIFIED.

    Approval is intentionally separate. A provider cannot become APPROVED until it
    has DPA evidence and its provider resource is explicitly classified.
    """
    processor_id = _id("PROC")
    class_codes = sorted({x.upper() for x in data_classes if str(x).strip()})
    region_list = sorted({str(x).strip().upper() for x in regions if str(x).strip()})
    row = {
        "id": processor_id,
        "name": name.strip(),
        "legal_entity": (legal_entity or name).strip(),
        "service": service.strip(),
        "purpose": (purpose or service).strip(),
        "data_classes": class_codes,
        "regions": region_list,
        "dpa_evidence_ref": dpa_evidence_ref,
        "dpa_state": "EVIDENCED" if dpa_evidence_ref else "MISSING",
        "subprocessor_url": subprocessor_url,
        "transfer_mechanism": transfer_mechanism,
        "classification_resource_id": None,
        "status": "PROPOSED",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }
    if not row["name"] or not row["service"] or not row["purpose"]:
        raise ValueError("processor requires name, service and purpose")
    if not class_codes or not region_list:
        raise ValueError("processor requires data_classes and regions")
    await db.privacy_processors.insert_one(dict(row))

    classification_resource = await data_classification.declare_resource(
        actor_id=actor_id,
        resource_kind="PROVIDER",
        resource_type="PRIVACY_PROCESSOR",
        resource_id=processor_id,
        owner="PRIVACY",
        source="ACADEMY",
        metadata={
            "processor_name": row["name"],
            "legal_entity": row["legal_entity"],
            "service": row["service"],
            "purpose": row["purpose"],
            "data_classes": class_codes,
            "regions": region_list,
        },
    )
    await db.privacy_processors.update_one(
        {"id": processor_id},
        {"$set": {"classification_resource_id": classification_resource["id"]}},
    )
    await governance.audit_event(
        event_type="privacy.processor.registered",
        actor_id=actor_id,
        resource_type="privacy_processor",
        resource_id=processor_id,
        payload={
            "classification_resource_id": classification_resource["id"],
            "data_classes": class_codes,
            "regions": region_list,
            "dpa_state": row["dpa_state"],
        },
    )
    return {**row, "classification_resource_id": classification_resource["id"]}


async def transition_processor(
    *, actor_id: str, processor_id: str, status: str
) -> Dict[str, Any]:
    target = status.upper()
    if target not in PROCESSOR_STATES:
        raise ValueError("invalid processor status")
    row = await db.privacy_processors.find_one({"id": processor_id}, {"_id": 0})
    if not row:
        raise LookupError("processor not found")

    allowed = {
        "PROPOSED": {"APPROVED", "RETIRED"},
        "APPROVED": {"SUSPENDED", "RETIRED"},
        "SUSPENDED": {"APPROVED", "RETIRED"},
        "RETIRED": set(),
    }
    if target == row["status"]:
        return row
    if target not in allowed.get(row["status"], set()):
        raise ValueError(f"invalid processor transition {row['status']}->{target}")

    if target == "APPROVED":
        if not row.get("dpa_evidence_ref"):
            raise ValueError("processor cannot be approved without DPA evidence")
        resource_id = row.get("classification_resource_id")
        resource = await db.classification_resources.find_one(
            {"id": resource_id}, {"_id": 0}
        )
        if not resource or resource.get("classification_status") != "CLASSIFIED":
            raise ValueError("processor cannot be approved while provider is unclassified")
        classification = await db.resource_classifications.find_one(
            {"id": resource.get("current_classification_id"), "status": "CURRENT"},
            {"_id": 0},
        )
        if not classification:
            raise ValueError("processor current provider classification is missing")

    now = utc_now_iso()
    result = await db.privacy_processors.update_one(
        {"id": processor_id, "status": row["status"]},
        {"$set": {"status": target, "updated_at": now, "last_actor_id": actor_id}},
    )
    if result.modified_count != 1:
        raise ValueError("processor transition lost race")
    await governance.audit_event(
        event_type="privacy.processor.state_changed",
        actor_id=actor_id,
        resource_type="privacy_processor",
        resource_id=processor_id,
        payload={"from": row["status"], "to": target},
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
    await governance.audit_event(
        event_type="privacy.deletion.created",
        actor_id=actor_id,
        resource_type="privacy_deletion_request",
        resource_id=row["id"],
        payload={"user_id": user_id},
    )
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
        "IMPACT_ASSESSED": {"REJECTED"},
        "APPROVED": set(),
        "EXECUTING": set(),
        "COMPLETED": set(),
        "REJECTED": set(),
    }
    if target not in allowed[row["status"]]:
        if target == "APPROVED":
            raise ValueError("APPROVED requires policy-driven privacy compliance approval")
        if target in {"EXECUTING", "COMPLETED"}:
            raise ValueError(f"{target} requires XCP-003 retention execution workflow")
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
    result = await db.privacy_deletion_requests.update_one(
        {"id": request_id, "status": row["status"]}, {"$set": update}
    )
    if result.modified_count != 1:
        raise ValueError("deletion transition lost race")
    await governance.audit_event(
        event_type="privacy.deletion.state_changed",
        actor_id=actor_id,
        resource_type="privacy_deletion_request",
        resource_id=request_id,
        payload={"from": row["status"], "to": target},
    )
    return {**row, **update}


async def record_deletion_execution(
    *,
    actor_id: str,
    request_id: str,
    resource_type: str,
    action: str,
    evidence_ref: str,
) -> Dict[str, Any]:
    """Legacy/manual evidence hook; does not complete the canonical request.

    PRI-007 completion is controlled by privacy_compliance and XCP-003 retention jobs.
    """
    request = await db.privacy_deletion_requests.find_one(
        {"id": request_id}, {"_id": 0}
    )
    if not request:
        raise LookupError("deletion request not found")
    if request["status"] != "EXECUTING":
        raise ValueError("deletion request must be EXECUTING")
    if not evidence_ref.strip():
        raise ValueError("deletion execution requires evidence_ref")
    entry = {
        "id": _id("DELEX"),
        "resource_type": resource_type,
        "action": action.upper(),
        "evidence_ref": evidence_ref,
        "actor_id": actor_id,
        "executed_at": utc_now_iso(),
        "canonical_completion": False,
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
    """Legacy projection helper for already-existing privacy projections.

    New incidents must originate in XCP-005 via privacy_compliance.open_privacy_incident.
    """
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
