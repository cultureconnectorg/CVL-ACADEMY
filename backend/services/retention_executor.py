"""Retention Executor (XCP-003 / PRI-008).

Deterministic retention scheduling from the canonical Data Classification Engine,
Privacy retention rules and immutable RETENTION policy versions.

Important semantics:
- SCHEDULING is not execution.
- A dry-run never mutates source data.
- A destructive action cannot complete without a concrete adapter receipt/evidence.
- Legal holds block execution.
- Due time is enforced.
- Failed work can be retried; verified work may only be replayed as a new job with
  explicit evidence, preserving the original proof trail.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import policy_registry
from services import professional_governance as governance

ACTIONS = {"DELETE", "ANONYMIZE", "ARCHIVE", "REVIEW"}
EXECUTABLE_STATES = {"SCHEDULED", "EXECUTION_FAILED"}
TERMINAL_STATES = {"VERIFIED_EXECUTED"}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _dedupe(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(str(value).strip() for value in values if str(value).strip()))


async def _active_hold(resource_record_id: str) -> Optional[Dict[str, Any]]:
    return await db.retention_legal_holds.find_one(
        {"resource_record_id": resource_record_id, "status": "ACTIVE"}, {"_id": 0}
    )


async def create_legal_hold(
    *, actor_id: str, resource_record_id: str, reason: str, evidence_refs: Iterable[str]
) -> Dict[str, Any]:
    if not await db.classification_resources.find_one({"id": resource_record_id}):
        raise LookupError("classification resource not found")
    refs = _dedupe(evidence_refs)
    if not reason.strip() or not refs:
        raise ValueError("legal hold requires reason and evidence")
    existing = await _active_hold(resource_record_id)
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
    refs = _dedupe(evidence_refs)
    if not refs:
        raise ValueError("legal hold release requires evidence")
    now = utc_now_iso()
    result = await db.retention_legal_holds.update_one(
        {"id": hold_id, "status": "ACTIVE"},
        {
            "$set": {
                "status": "RELEASED",
                "released_at": now,
                "released_by": actor_id,
                "release_evidence_refs": refs,
            }
        },
    )
    if result.modified_count != 1:
        raise ValueError("legal hold changed concurrently")
    await governance.audit_event(
        event_type="retention.legal_hold.released",
        actor_id=actor_id,
        resource_type="classification_resource",
        resource_id=hold["resource_record_id"],
        payload={"hold_id": hold_id, "evidence_refs": refs},
    )
    return {
        **hold,
        "status": "RELEASED",
        "released_at": now,
        "released_by": actor_id,
        "release_evidence_refs": refs,
    }


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
            "replay_of_job_id": None,
        },
        {"_id": 0},
    )
    if existing:
        return existing

    hold = await _active_hold(resource_record_id) if rule.get("legal_hold_blocks", True) else None
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
        "attempt_count": 0,
        "retry_count": 0,
        "replay_of_job_id": None,
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "last_attempt_at": None,
        "execution": None,
    }
    await db.retention_jobs.insert_one(dict(row))
    await governance.audit_event(
        event_type="retention.job.scheduled",
        actor_id=actor_id,
        resource_type="retention_job",
        resource_id=row["id"],
        payload={
            "action": row["action"],
            "due_at": row["due_at"],
            "status": row["status"],
            "policy_version_id": policy["id"],
        },
    )
    return row


async def refresh_job(job_id: str) -> Dict[str, Any]:
    job = await db.retention_jobs.find_one({"id": job_id}, {"_id": 0})
    if not job:
        raise LookupError("retention job not found")
    if job["status"] == "BLOCKED_HOLD":
        active = await _active_hold(job["resource_record_id"])
        if not active:
            await db.retention_jobs.update_one(
                {"id": job_id, "status": "BLOCKED_HOLD"},
                {"$set": {"status": "SCHEDULED", "blocking_hold_id": None}},
            )
            return {**job, "status": "SCHEDULED", "blocking_hold_id": None}
    elif job["status"] in EXECUTABLE_STATES:
        hold = await _active_hold(job["resource_record_id"])
        if hold:
            await db.retention_jobs.update_one(
                {"id": job_id, "status": job["status"]},
                {"$set": {"status": "BLOCKED_HOLD", "blocking_hold_id": hold["id"]}},
            )
            return {**job, "status": "BLOCKED_HOLD", "blocking_hold_id": hold["id"]}
    return job


async def dry_run_job(job_id: str) -> Dict[str, Any]:
    """Return deterministic execution intent without changing source or job state."""
    job = await refresh_job(job_id)
    due = policy_registry.parse_instant(job["due_at"])
    hold = await _active_hold(job["resource_record_id"])
    executable = (
        job["status"] in EXECUTABLE_STATES
        and hold is None
        and due <= _now()
    )
    return {
        "job_id": job["id"],
        "dry_run": True,
        "action": job["action"],
        "resource_record_id": job["resource_record_id"],
        "classification_id": job["classification_id"],
        "policy_version_id": job["policy_version_id"],
        "due_at": job["due_at"],
        "due": due <= _now(),
        "blocked_by_hold": hold is not None,
        "blocking_hold_id": hold["id"] if hold else None,
        "executable": executable,
    }


async def list_due_jobs(*, limit: int = 200) -> list[Dict[str, Any]]:
    """Scheduled-worker query. It does not execute destructive actions by itself."""
    now = _now().isoformat()
    rows = await db.retention_jobs.find(
        {
            "status": {"$in": sorted(EXECUTABLE_STATES)},
            "due_at": {"$lte": now},
        },
        {"_id": 0},
    ).sort("due_at", 1).to_list(max(1, min(limit, 1000)))
    result = []
    for row in rows:
        refreshed = await refresh_job(row["id"])
        if refreshed["status"] in EXECUTABLE_STATES:
            result.append(refreshed)
    return result


async def begin_execution(*, actor_id: str, job_id: str) -> Dict[str, Any]:
    job = await refresh_job(job_id)
    if job["status"] == "BLOCKED_HOLD":
        raise ValueError("retention execution blocked by legal hold")
    if job["status"] in TERMINAL_STATES:
        return job
    if job["status"] not in EXECUTABLE_STATES:
        raise ValueError("retention job is not executable")
    if policy_registry.parse_instant(job["due_at"]) > _now():
        raise ValueError("retention job is not due yet")

    now = utc_now_iso()
    result = await db.retention_jobs.update_one(
        {"id": job_id, "status": job["status"]},
        {
            "$set": {"status": "EXECUTING", "last_attempt_at": now},
            "$inc": {"attempt_count": 1},
        },
    )
    if result.modified_count != 1:
        raise ValueError("retention job execution claim lost race")
    await governance.audit_event(
        event_type="retention.execution.started",
        actor_id=actor_id,
        resource_type="retention_job",
        resource_id=job_id,
        payload={"action": job["action"], "due_at": job["due_at"]},
    )
    return {
        **job,
        "status": "EXECUTING",
        "last_attempt_at": now,
        "attempt_count": int(job.get("attempt_count", 0)) + 1,
    }


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

    if job["status"] != "EXECUTING":
        job = await begin_execution(actor_id=actor_id, job_id=job_id)

    execution = {
        "adapter": adapter.strip(),
        "evidence_ref": evidence_ref.strip(),
        "outcome": normalized,
        "details": details or {},
        "recorded_by": actor_id,
        "recorded_at": utc_now_iso(),
        "attempt_number": int(job.get("attempt_count", 1)),
    }
    status = "VERIFIED_EXECUTED" if normalized == "SUCCESS" else "EXECUTION_FAILED"
    result = await db.retention_jobs.update_one(
        {"id": job_id, "status": "EXECUTING"},
        {"$set": {"status": status, "execution": execution}},
    )
    if result.modified_count != 1:
        raise ValueError("retention execution completion lost race")
    await governance.audit_event(
        event_type="retention.execution.recorded",
        actor_id=actor_id,
        resource_type="retention_job",
        resource_id=job_id,
        payload={
            "status": status,
            "adapter": adapter,
            "evidence_ref": evidence_ref,
            "attempt_number": execution["attempt_number"],
        },
    )
    return {**job, "status": status, "execution": execution}


async def retry_failed_job(
    *, actor_id: str, job_id: str, evidence_refs: Iterable[str]
) -> Dict[str, Any]:
    refs = _dedupe(evidence_refs)
    if not refs:
        raise ValueError("retention retry requires evidence")
    job = await db.retention_jobs.find_one(
        {"id": job_id, "status": "EXECUTION_FAILED"}, {"_id": 0}
    )
    if not job:
        raise ValueError("only failed retention jobs can be retried")
    hold = await _active_hold(job["resource_record_id"])
    status = "BLOCKED_HOLD" if hold else "SCHEDULED"
    now = utc_now_iso()
    result = await db.retention_jobs.update_one(
        {"id": job_id, "status": "EXECUTION_FAILED"},
        {
            "$set": {
                "status": status,
                "blocking_hold_id": hold["id"] if hold else None,
                "retry_authorized_at": now,
                "retry_authorized_by": actor_id,
                "retry_evidence_refs": refs,
            },
            "$inc": {"retry_count": 1},
        },
    )
    if result.modified_count != 1:
        raise ValueError("retention retry lost race")
    await governance.audit_event(
        event_type="retention.execution.retry_authorized",
        actor_id=actor_id,
        resource_type="retention_job",
        resource_id=job_id,
        payload={"evidence_refs": refs, "status": status},
    )
    return {
        **job,
        "status": status,
        "retry_count": int(job.get("retry_count", 0)) + 1,
        "retry_evidence_refs": refs,
    }


async def replay_verified_job(
    *, actor_id: str, job_id: str, reason: str, evidence_refs: Iterable[str]
) -> Dict[str, Any]:
    """Create a new auditable replay job; never mutate a verified original."""
    refs = _dedupe(evidence_refs)
    if not reason.strip() or not refs:
        raise ValueError("retention replay requires reason and evidence")
    original = await db.retention_jobs.find_one(
        {"id": job_id, "status": "VERIFIED_EXECUTED"}, {"_id": 0}
    )
    if not original:
        raise ValueError("only verified retention jobs can be replayed")
    hold = await _active_hold(original["resource_record_id"])
    now = utc_now_iso()
    replay = {
        **{key: value for key, value in original.items() if key not in {"id", "execution"}},
        "id": _id("RETJOB"),
        "status": "BLOCKED_HOLD" if hold else "SCHEDULED",
        "blocking_hold_id": hold["id"] if hold else None,
        "attempt_count": 0,
        "retry_count": 0,
        "replay_of_job_id": original["id"],
        "replay_reason": reason.strip(),
        "replay_evidence_refs": refs,
        "created_by": actor_id,
        "created_at": now,
        "last_attempt_at": None,
        "execution": None,
    }
    await db.retention_jobs.insert_one(dict(replay))
    await governance.audit_event(
        event_type="retention.job.replayed",
        actor_id=actor_id,
        resource_type="retention_job",
        resource_id=replay["id"],
        payload={
            "replay_of_job_id": original["id"],
            "reason": replay["replay_reason"],
            "evidence_refs": refs,
        },
    )
    return replay


async def execution_gate() -> Dict[str, Any]:
    blockers = await db.retention_jobs.find(
        {
            "status": {
                "$in": ["BLOCKED_HOLD", "EXECUTION_FAILED", "EXECUTING"]
            }
        },
        {"_id": 0},
    ).to_list(5000)
    overdue = await list_due_jobs(limit=1000)
    return {
        "pass": len(blockers) == 0 and len(overdue) == 0,
        "blocking_count": len(blockers) + len(overdue),
        "blocking_jobs": blockers,
        "overdue_jobs": overdue,
    }
