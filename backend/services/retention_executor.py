"""Retention Executor control plane (XCP-003).

Creates deterministic retention jobs from the canonical classification + retention
rule, blocks them on legal hold, and records execution proof. It deliberately does
not pretend a generic service can erase arbitrary storage: DELETE/ANONYMIZE/ARCHIVE
become VERIFIED only after a concrete adapter reports an evidence reference.
"""

from __future__ import annotations

import uuid
from datetime import timedelta
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import policy_registry
from services import professional_governance as governance

ACTIONS = {"DELETE", "ANONYMIZE", "ARCHIVE", "REVIEW"}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


async def create_legal_hold(
    *, actor_id: str, resource_record_id: str, reason: str, evidence_refs: Iterable[str]
) -> Dict[str, Any]:
    if not await db.classification_resources.find_one({"id": resource_record_id}):
        raise LookupError("classification resource not found")
    refs = list(dict.fromkeys(evidence_refs))
    if not reason.strip() or not refs:
        raise ValueError("legal hold requires reason and evidence")
    existing = await db.retention_legal_holds.find_one(
        {"resource_record_id": resource_record_id, "status": "ACTIVE"}, {"_id": 0}
    )
    if existing:
        return existing
    row = {
        "id": _id("HOLD"),
        "resource_record_id": resource_record_id,
        "reason": reason.strip(),
        "evidence_refs": refs,
        "status": "ACTIVE",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "released_at": None,
    }
    await db.retention_legal_holds.insert_one(dict(row))
    await governance.audit_event(
        event_type="retention.legal_hold.created",
        actor_id=actor_id,
        resource_type="classification_resource",
        resource_id=resource_record_id,
        payload={"hold_id": row["id"], "evidence_refs": refs},
    )
    return row


async def release_legal_hold(
    *, actor_id: str, hold_id: str, evidence_refs: Iterable[str]
) -> Dict[str, Any]:
    hold = await db.retention_legal_holds.find_one({"id": hold_id}, {"_id": 0})
    if not hold:
        raise LookupError("legal hold not found")
    if hold["status"] == "RELEASED":
        return hold
    refs = list(dict.fromkeys(evidence_refs))
    if not refs:
        raise ValueError("legal hold release requires evidence")
    now = utc_now_iso()
    result = await db.retention_legal_holds.update_one(
        {"id": hold_id, "status": "ACTIVE"},
        {"$set": {"status": "RELEASED", "released_at": now, "released_by": actor_id, "release_evidence_refs": refs}},
    )
    if result.modified_count != 1:
        raise ValueError("legal hold changed concurrently")
    return {**hold, "status": "RELEASED", "released_at": now, "released_by": actor_id, "release_evidence_refs": refs}


async def schedule_job(
    *,
    actor_id: str,
    resource_record_id: str,
    trigger: str,
    trigger_at: str,
    policy_version_id: str,
) -> Dict[str, Any]:
    resource = await db.classification_resources.find_one(
        {"id": resource_record_id, "classification_status": "CLASSIFIED"}, {"_id": 0}
    )
    if not resource:
        raise ValueError("resource must be explicitly classified before retention scheduling")
    classification = await db.resource_classifications.find_one(
        {"id": resource["current_classification_id"], "status": "CURRENT"}, {"_id": 0}
    )
    if not classification:
        raise ValueError("current resource classification not found")

    policy = await policy_registry.require_effective_version(policy_version_id)
    if policy.get("policy_key") != "RETENTION":
        raise ValueError("policy version is not a RETENTION policy")

    normalized_trigger = trigger.strip().upper()
    rule = await db.privacy_retention_rules.find_one(
        {
            "data_class": classification["data_class_code"],
            "trigger": normalized_trigger,
            "status": "ACTIVE",
        },
        {"_id": 0},
    )
    if not rule:
        raise LookupError("active retention rule not found")
    if rule["action"] not in ACTIONS:
        raise ValueError("retention rule action is invalid")

    start = policy_registry.parse_instant(trigger_at)
    due = start + timedelta(days=int(rule["retention_days"]))
    existing = await db.retention_jobs.find_one(
        {
            "resource_record_id": resource_record_id,
            "trigger": normalized_trigger,
            "trigger_at": trigger_at,
            "rule_id": rule["id"],
        },
        {"_id": 0},
    )
    if existing:
        return existing

    hold = None
    if rule.get("legal_hold_blocks", True):
        hold = await db.retention_legal_holds.find_one(
            {"resource_record_id": resource_record_id, "status": "ACTIVE"}, {"_id": 0}
        )
    row = {
        "id": _id("RETJOB"),
        "resource_record_id": resource_record_id,
        "classification_id": classification["id"],
        "data_class_code": classification["data_class_code"],
        "rule_id": rule["id"],
        "action": rule["action"],
        "trigger": normalized_trigger,
        "trigger_at": trigger_at,
        "due_at": due.isoformat(),
        "policy_version_id": policy["id"],
        "policy_hash": policy["content_hash"],
        "status": "BLOCKED_HOLD" if hold else "SCHEDULED",
        "blocking_hold_id": hold["id"] if hold else None,
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "execution": None,
    }
    await db.retention_jobs.insert_one(dict(row))
    await governance.audit_event(
        event_type="retention.job.scheduled",
        actor_id=actor_id,
        resource_type="retention_job",
        resource_id=row["id"],
        payload={"action": row["action"], "due_at": row["due_at"], "status": row["status"]},
    )
    return row


async def refresh_job(job_id: str) -> Dict[str, Any]:
    job = await db.retention_jobs.find_one({"id": job_id}, {"_id": 0})
    if not job:
        raise LookupError("retention job not found")
    if job["status"] == "BLOCKED_HOLD":
        active = await db.retention_legal_holds.find_one(
            {"id": job.get("blocking_hold_id"), "status": "ACTIVE"}, {"_id": 0}
        )
        if not active:
            await db.retention_jobs.update_one(
                {"id": job_id, "status": "BLOCKED_HOLD"},
                {"$set": {"status": "SCHEDULED", "blocking_hold_id": None}},
            )
            return {**job, "status": "SCHEDULED", "blocking_hold_id": None}
    return job


async def record_execution(
    *,
    actor_id: str,
    job_id: str,
    adapter: str,
    evidence_ref: str,
    outcome: str,
    details: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    job = await refresh_job(job_id)
    if job["status"] == "BLOCKED_HOLD":
        raise ValueError("retention execution blocked by legal hold")
    if job["status"] == "VERIFIED_EXECUTED":
        return job
    if not adapter.strip() or not evidence_ref.strip():
        raise ValueError("execution adapter and evidence_ref are required")
    normalized = outcome.strip().upper()
    if normalized not in {"SUCCESS", "FAILED"}:
        raise ValueError("outcome must be SUCCESS or FAILED")
    execution = {
        "adapter": adapter.strip(),
        "evidence_ref": evidence_ref.strip(),
        "outcome": normalized,
        "details": details or {},
        "recorded_by": actor_id,
        "recorded_at": utc_now_iso(),
    }
    status = "VERIFIED_EXECUTED" if normalized == "SUCCESS" else "EXECUTION_FAILED"
    await db.retention_jobs.update_one(
        {"id": job_id}, {"$set": {"status": status, "execution": execution}}
    )
    await governance.audit_event(
        event_type="retention.execution.recorded",
        actor_id=actor_id,
        resource_type="retention_job",
        resource_id=job_id,
        payload={"status": status, "adapter": adapter, "evidence_ref": evidence_ref},
    )
    return {**job, "status": status, "execution": execution}


async def execution_gate() -> Dict[str, Any]:
    blockers = await db.retention_jobs.find(
        {"status": {"$in": ["BLOCKED_HOLD", "EXECUTION_FAILED"]}}, {"_id": 0}
    ).to_list(5000)
    return {"pass": len(blockers) == 0, "blocking_count": len(blockers), "blocking_jobs": blockers}
