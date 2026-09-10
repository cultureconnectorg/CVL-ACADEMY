"""Policy-driven Privacy Core orchestration (PRI-002/003/004/005/007/011/013).

This module does not create parallel truth stores. It orchestrates and hardens the
existing Academy primitives:
- assurance_core collections for processing activities, consent and DSAR;
- XCP-008 policy_registry for immutable policy versions;
- XCP-001 authority_policy for approval authority;
- XCP-002 data_classification for provider/resource classification;
- XCP-003 retention_executor for actual retention/deletion execution records;
- XCP-005 incident_core for canonical privacy incidents.

Generated DSAR exports are assembled from canonical source records and only their
hash/manifest is persisted; the export payload is not copied into another database
collection.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import assurance_core, authority_policy, incident_core, policy_registry
from services import retention_executor
from services import professional_governance as governance


DSAR_SOURCE_QUERIES = {
    "users": lambda user_id: {"id": user_id},
    "progress": lambda user_id: {"user_id": user_id},
    "privacy_consents": lambda user_id: {"user_id": user_id},
    "privacy_dsar": lambda user_id: {"user_id": user_id},
    "privacy_deletion_requests": lambda user_id: {"user_id": user_id},
}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _refs(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(str(value).strip() for value in values if str(value).strip()))


def _hash(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


async def _require_policy(policy_version_id: str, key: str) -> Dict[str, Any]:
    policy = await policy_registry.require_effective_version(policy_version_id)
    if policy.get("policy_key") != key:
        raise ValueError(f"policy version is not a {key} policy")
    return policy


async def register_processing_activity(
    *,
    actor_id: str,
    name: str,
    purpose: str,
    data_classes: Iterable[str],
    legal_basis: str,
    processors: Iterable[str],
    regions: Iterable[str],
    controller: str,
    recipients: Iterable[str] = (),
    systems: Iterable[str] = (),
    retention_refs: Iterable[str] = (),
    transfer_mechanism: Optional[str] = None,
    evidence_refs: Iterable[str] = (),
) -> Dict[str, Any]:
    """PRI-002: create one operational RoPA row from registered canonical inputs."""
    classes = sorted({str(code).strip().upper() for code in data_classes if str(code).strip()})
    processor_ids = sorted({str(pid).strip() for pid in processors if str(pid).strip()})
    region_list = sorted({str(region).strip().upper() for region in regions if str(region).strip()})
    refs = _refs(evidence_refs)
    if not name.strip() or not purpose.strip() or not legal_basis.strip() or not controller.strip():
        raise ValueError("processing activity requires name, purpose, legal_basis and controller")
    if not classes or not refs:
        raise ValueError("processing activity requires data classes and evidence")

    known_classes = await db.privacy_data_classes.find(
        {"code": {"$in": classes}}, {"_id": 0, "code": 1}
    ).to_list(len(classes))
    known_codes = {row["code"] for row in known_classes}
    missing = sorted(set(classes) - known_codes)
    if missing:
        raise LookupError(f"unknown privacy data classes: {', '.join(missing)}")

    if processor_ids:
        known_processors = await db.privacy_processors.find(
            {"id": {"$in": processor_ids}}, {"_id": 0, "id": 1}
        ).to_list(len(processor_ids))
        known_ids = {row["id"] for row in known_processors}
        missing_processors = sorted(set(processor_ids) - known_ids)
        if missing_processors:
            raise LookupError(
                f"unknown privacy processors: {', '.join(missing_processors)}"
            )

    row = await assurance_core.register_processing_activity(
        actor_id=actor_id,
        name=name.strip(),
        purpose=purpose.strip(),
        data_classes=classes,
        legal_basis=legal_basis.strip(),
        processors=processor_ids,
        regions=region_list,
    )
    extension = {
        "controller": controller.strip(),
        "recipients": sorted({str(v).strip() for v in recipients if str(v).strip()}),
        "systems": sorted({str(v).strip() for v in systems if str(v).strip()}),
        "retention_refs": _refs(retention_refs),
        "transfer_mechanism": transfer_mechanism,
        "evidence_refs": refs,
        "ropa_complete": True,
        "updated_at": utc_now_iso(),
    }
    await db.privacy_processing_activities.update_one(
        {"id": row["id"]}, {"$set": extension}
    )
    await governance.audit_event(
        event_type="privacy.ropa.registered",
        actor_id=actor_id,
        resource_type="processing_activity",
        resource_id=row["id"],
        payload={
            "data_classes": classes,
            "processors": processor_ids,
            "regions": region_list,
            "evidence_refs": refs,
        },
    )
    return {**row, **extension}


async def register_consent_purpose(
    *,
    actor_id: str,
    purpose: str,
    required: bool,
    policy_version_id: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    """Defines whether a purpose is mandatory or self-service withdrawable."""
    policy = await _require_policy(policy_version_id, "CONSENT")
    refs = _refs(evidence_refs)
    key = purpose.strip().upper()
    if not key or not refs:
        raise ValueError("consent purpose requires purpose and evidence")
    row = {
        "id": _id("CPURP"),
        "purpose": key,
        "required": bool(required),
        "policy_version_id": policy["id"],
        "policy_hash": policy["content_hash"],
        "evidence_refs": refs,
        "status": "ACTIVE",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.privacy_consent_purposes.update_one(
        {"purpose": key, "status": "ACTIVE"}, {"$set": row}, upsert=True
    )
    await governance.audit_event(
        event_type="privacy.consent_purpose.registered",
        actor_id=actor_id,
        resource_type="consent_purpose",
        resource_id=row["id"],
        payload={"purpose": key, "required": bool(required), "policy_version_id": policy["id"]},
    )
    return row


async def record_consent(
    *,
    actor_id: str,
    user_id: str,
    purpose: str,
    granted: bool,
    policy_version_id: str,
    evidence_refs: Iterable[str],
    frek_evidence_ref: Optional[str] = None,
    source: str = "SELF_SERVICE",
) -> Dict[str, Any]:
    """PRI-003: append-only consent bound to immutable policy + evidence."""
    policy = await _require_policy(policy_version_id, "CONSENT")
    refs = _refs(evidence_refs)
    key = purpose.strip().upper()
    definition = await db.privacy_consent_purposes.find_one(
        {"purpose": key, "status": "ACTIVE"}, {"_id": 0}
    )
    if not definition:
        raise LookupError("active consent purpose not found")
    if definition["policy_version_id"] != policy["id"]:
        raise ValueError("consent purpose is bound to a different policy version")
    if not refs:
        raise ValueError("consent requires evidence")
    if not granted and definition.get("required"):
        raise PermissionError("required consent purpose cannot be withdrawn through preferences")

    evidence = {
        "evidence_refs": refs,
        "frek_evidence_ref": frek_evidence_ref,
        "source": source.strip().upper(),
        "policy_version_id": policy["id"],
        "policy_hash": policy["content_hash"],
    }
    row = await assurance_core.record_consent(
        actor_id=actor_id,
        user_id=user_id,
        purpose=key,
        policy_version=policy["id"],
        granted=granted,
        evidence=evidence,
    )
    extension = {
        "policy_version_id": policy["id"],
        "policy_hash": policy["content_hash"],
        "frek_evidence_ref": frek_evidence_ref,
        "source": evidence["source"],
    }
    await db.privacy_consents.update_one({"id": row["id"]}, {"$set": extension})
    return {**row, **extension}


async def consent_preferences(user_id: str) -> list[Dict[str, Any]]:
    definitions = await db.privacy_consent_purposes.find(
        {"status": "ACTIVE"}, {"_id": 0}
    ).sort("purpose", 1).to_list(1000)
    consents = await db.privacy_consents.find(
        {"user_id": user_id}, {"_id": 0}
    ).sort("recorded_at", 1).to_list(5000)
    current: Dict[str, Dict[str, Any]] = {}
    for row in consents:
        current[row["purpose"]] = row
    return [
        {
            "purpose": definition["purpose"],
            "required": bool(definition.get("required")),
            "granted": bool(current.get(definition["purpose"], {}).get("granted", False)),
            "last_consent_id": current.get(definition["purpose"], {}).get("id"),
            "policy_version_id": definition["policy_version_id"],
        }
        for definition in definitions
    ]


async def create_dsar(*, actor_id: str, user_id: str, request_type: str) -> Dict[str, Any]:
    row = await assurance_core.create_dsar(
        actor_id=actor_id, user_id=user_id, request_type=request_type
    )
    await db.privacy_dsar.update_one(
        {"id": row["id"]},
        {"$set": {"identity_verified": False, "identity_evidence_refs": []}},
    )
    return {**row, "identity_verified": False, "identity_evidence_refs": []}


async def verify_dsar_identity(
    *, actor_id: str, dsar_id: str, evidence_refs: Iterable[str]
) -> Dict[str, Any]:
    refs = _refs(evidence_refs)
    if not refs:
        raise ValueError("DSAR identity verification requires evidence")
    row = await db.privacy_dsar.find_one({"id": dsar_id}, {"_id": 0})
    if not row:
        raise LookupError("DSAR not found")
    if row.get("status") in {"COMPLETED", "REJECTED"}:
        raise ValueError("terminal DSAR cannot be identity-verified")
    now = utc_now_iso()
    await db.privacy_dsar.update_one(
        {"id": dsar_id},
        {
            "$set": {
                "identity_verified": True,
                "identity_verified_by": actor_id,
                "identity_verified_at": now,
                "identity_evidence_refs": refs,
                "status": "IDENTITY_CHECK",
                "updated_at": now,
            }
        },
    )
    await governance.audit_event(
        event_type="privacy.dsar.identity_verified",
        actor_id=actor_id,
        resource_type="dsar",
        resource_id=dsar_id,
        payload={"evidence_refs": refs},
    )
    return {**row, "identity_verified": True, "status": "IDENTITY_CHECK"}


async def build_dsar_export(*, actor_id: str, dsar_id: str) -> Dict[str, Any]:
    """PRI-005: assemble export from canonical sources; persist manifest/hash only."""
    dsar = await db.privacy_dsar.find_one({"id": dsar_id}, {"_id": 0})
    if not dsar:
        raise LookupError("DSAR not found")
    if not dsar.get("identity_verified"):
        raise PermissionError("DSAR export requires verified identity")
    if dsar.get("request_type") not in {"EXPORT", "ACCESS"}:
        raise ValueError("DSAR request type does not permit an export")

    user_id = dsar["user_id"]
    payload: Dict[str, Any] = {"user_id": user_id, "generated_at": utc_now_iso(), "sources": {}}
    counts: Dict[str, int] = {}
    for collection_name, query_factory in DSAR_SOURCE_QUERIES.items():
        collection = getattr(db, collection_name)
        rows = await collection.find(query_factory(user_id), {"_id": 0}).to_list(10000)
        payload["sources"][collection_name] = rows
        counts[collection_name] = len(rows)

    digest = _hash(payload)
    manifest = {
        "id": _id("DSAREX"),
        "dsar_id": dsar_id,
        "user_id": user_id,
        "payload_hash": digest,
        "source_counts": counts,
        "source_collections": sorted(DSAR_SOURCE_QUERIES),
        "generated_by": actor_id,
        "generated_at": payload["generated_at"],
        "payload_persisted": False,
    }
    await db.privacy_dsar_exports.insert_one(dict(manifest))
    await db.privacy_dsar.update_one(
        {"id": dsar_id},
        {
            "$set": {
                "status": "READY",
                "export_manifest_id": manifest["id"],
                "updated_at": utc_now_iso(),
            }
        },
    )
    await governance.audit_event(
        event_type="privacy.dsar.export_generated",
        actor_id=actor_id,
        resource_type="dsar",
        resource_id=dsar_id,
        payload={"manifest_id": manifest["id"], "payload_hash": digest, "source_counts": counts},
    )
    return {"manifest": manifest, "export": payload}


async def approve_deletion_request(
    *,
    actor_id: str,
    actor_role: str,
    authority_level: str,
    request_id: str,
    policy_version_id: str,
    evidence_refs: Iterable[str],
    exception_refs: Iterable[str] = (),
) -> Dict[str, Any]:
    """PRI-007: A4 policy gate before a deletion request may execute."""
    refs = _refs(evidence_refs)
    if not refs:
        raise ValueError("deletion approval requires evidence")
    request = await db.privacy_deletion_requests.find_one(
        {"id": request_id}, {"_id": 0}
    )
    if not request:
        raise LookupError("deletion request not found")
    if request["status"] != "IMPACT_ASSESSED":
        raise ValueError("deletion approval requires IMPACT_ASSESSED state")

    authority = await authority_policy.evaluate_authority(
        actor_id=actor_id,
        actor_role=actor_role,
        action="PRIVACY_DELETION_APPROVE",
        context={
            "domain": "PRIVACY",
            "authority_level": authority_level,
            "user_id": request["user_id"],
            "request_id": request_id,
        },
        policy_version_id=policy_version_id,
    )
    if authority["policy_key"] != "PRIVACY_DELETION":
        raise ValueError("deletion approval requires PRIVACY_DELETION policy")
    if authority["decision"] != "ALLOW":
        raise PermissionError("authority policy did not allow deletion")

    exceptions = _refs(exception_refs)
    now = utc_now_iso()
    update = {
        "status": "APPROVED",
        "authority_decision_id": authority["id"],
        "policy_version_id": authority["policy_version_id"],
        "policy_hash": authority["policy_content_hash"],
        "approval_evidence_refs": refs,
        "exception_refs": exceptions,
        "approved_by": actor_id,
        "approved_at": now,
        "updated_at": now,
    }
    result = await db.privacy_deletion_requests.update_one(
        {"id": request_id, "status": "IMPACT_ASSESSED"}, {"$set": update}
    )
    if result.modified_count != 1:
        raise ValueError("deletion approval lost race")
    await governance.audit_event(
        event_type="privacy.deletion.approved",
        actor_id=actor_id,
        resource_type="privacy_deletion_request",
        resource_id=request_id,
        payload={
            "authority_decision_id": authority["id"],
            "policy_version_id": authority["policy_version_id"],
            "evidence_refs": refs,
            "exception_refs": exceptions,
        },
    )
    return {**request, **update, "authority": authority}


async def schedule_deletion_retention_jobs(
    *,
    actor_id: str,
    request_id: str,
    resource_record_ids: Iterable[str],
    trigger_at: str,
    retention_policy_version_id: str,
) -> Dict[str, Any]:
    """Connect approved deletion to XCP-003; no direct/fake erasure occurs here."""
    request = await db.privacy_deletion_requests.find_one(
        {"id": request_id}, {"_id": 0}
    )
    if not request:
        raise LookupError("deletion request not found")
    if request["status"] != "APPROVED":
        raise ValueError("deletion request must be APPROVED before scheduling")
    ids = list(dict.fromkeys(resource_record_ids))
    if not ids:
        raise ValueError("deletion scheduling requires classified resources")

    jobs = []
    for resource_record_id in ids:
        job = await retention_executor.schedule_job(
            actor_id=actor_id,
            resource_record_id=resource_record_id,
            trigger="DELETION_APPROVED",
            trigger_at=trigger_at,
            policy_version_id=retention_policy_version_id,
        )
        jobs.append(job)
    now = utc_now_iso()
    await db.privacy_deletion_requests.update_one(
        {"id": request_id, "status": "APPROVED"},
        {
            "$set": {
                "status": "EXECUTING",
                "retention_job_ids": [job["id"] for job in jobs],
                "updated_at": now,
            }
        },
    )
    return {"request_id": request_id, "status": "EXECUTING", "jobs": jobs}


async def complete_deletion_from_retention(
    *, actor_id: str, request_id: str, evidence_refs: Iterable[str]
) -> Dict[str, Any]:
    refs = _refs(evidence_refs)
    request = await db.privacy_deletion_requests.find_one(
        {"id": request_id}, {"_id": 0}
    )
    if not request:
        raise LookupError("deletion request not found")
    if request["status"] != "EXECUTING":
        raise ValueError("deletion request must be EXECUTING")
    job_ids = request.get("retention_job_ids") or []
    if not job_ids:
        raise ValueError("deletion request has no retention execution jobs")
    jobs = await db.retention_jobs.find(
        {"id": {"$in": job_ids}}, {"_id": 0}
    ).to_list(len(job_ids))
    if len(jobs) != len(job_ids) or any(job.get("status") != "VERIFIED_EXECUTED" for job in jobs):
        raise ValueError("all deletion retention jobs must be VERIFIED_EXECUTED")
    if not refs:
        raise ValueError("deletion completion requires evidence")
    now = utc_now_iso()
    await db.privacy_deletion_requests.update_one(
        {"id": request_id, "status": "EXECUTING"},
        {
            "$set": {
                "status": "COMPLETED",
                "completion_evidence_refs": refs,
                "completed_by": actor_id,
                "completed_at": now,
                "updated_at": now,
            }
        },
    )
    await governance.audit_event(
        event_type="privacy.deletion.completed",
        actor_id=actor_id,
        resource_type="privacy_deletion_request",
        resource_id=request_id,
        payload={"retention_job_ids": job_ids, "evidence_refs": refs},
    )
    return {**request, "status": "COMPLETED", "completion_evidence_refs": refs}


async def open_privacy_incident(
    *,
    actor_id: str,
    title: str,
    description: str,
    severity: str,
    data_classes: Iterable[str],
    evidence_refs: Iterable[str],
    asset_id: Optional[str] = None,
) -> Dict[str, Any]:
    """PRI-013: privacy incidents originate in XCP-005, never a parallel source."""
    return await incident_core.create_incident(
        actor_id=actor_id,
        title=title,
        description=description,
        severity=severity,
        domains=["PRIVACY", "LEGAL", "RISK"],
        evidence_refs=evidence_refs,
        data_classes=data_classes,
        asset_id=asset_id,
        metadata={"origin": "PRIVACY_CORE"},
    )


async def project_privacy_incident(
    *,
    actor_id: str,
    incident_id: str,
    risk_impact: int,
    risk_probability: int,
    risk_owner: Optional[str] = None,
    risk_mitigation: Optional[str] = None,
    risk_deadline: Optional[str] = None,
    jurisdiction: Optional[str] = None,
) -> Dict[str, Any]:
    return await incident_core.project_incident(
        actor_id=actor_id,
        incident_id=incident_id,
        jurisdiction=jurisdiction,
        risk_impact=risk_impact,
        risk_probability=risk_probability,
        risk_owner=risk_owner,
        risk_mitigation=risk_mitigation,
        risk_deadline=risk_deadline,
    )
