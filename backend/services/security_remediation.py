"""Security remediation protocol (SEC-011/SEC-012/SEC-30..32).

Academy owns authorization, evidence and verification state. Real execution dispatch is
sent to CVLN Agent Factory; Command Center receives the operational mirror. Neither
external system is treated as successful without its real API returning a concrete id.

AUTONOMOUS_FIX != AUTONOMOUS_TRUST: an agent may execute an authorised change,
but verification evidence is required before the remediation can be marked VERIFIED.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import authority_policy
from services import professional_governance as governance
from services import remediation_dispatch


STATES = {
    "REQUESTED",
    "AUTHORIZED",
    "EXECUTING",
    "TESTING",
    "VERIFIED",
    "FAILED",
    "ROLLBACK_REQUIRED",
    "ROLLED_BACK",
    "CANCELLED",
}
TRANSITIONS = {
    "REQUESTED": {"AUTHORIZED", "CANCELLED"},
    "AUTHORIZED": {"EXECUTING", "CANCELLED"},
    "EXECUTING": {"TESTING", "FAILED", "ROLLBACK_REQUIRED"},
    "TESTING": {"VERIFIED", "FAILED", "ROLLBACK_REQUIRED"},
    "FAILED": {"AUTHORIZED", "ROLLBACK_REQUIRED", "CANCELLED"},
    "ROLLBACK_REQUIRED": {"ROLLED_BACK"},
    "VERIFIED": set(),
    "ROLLED_BACK": set(),
    "CANCELLED": set(),
}
AUTHORIZATION_ACTIONS = {
    "SECURITY_REMEDIATION_AUTHORIZE",
    "SECURITY_AUTONOMOUS_FIX",
}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


async def create_remediation(
    *,
    actor_id: str,
    finding_id: Optional[str] = None,
    threat_id: Optional[str] = None,
    title: str,
    proposed_change: str,
    target_system: str,
    rollback_plan: str,
    test_plan: Iterable[str],
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    if bool(finding_id) == bool(threat_id):
        raise ValueError("exactly one of finding_id or threat_id is required")
    if finding_id and not await db.security_findings.find_one({"id": finding_id}):
        raise LookupError("security finding not found")
    if threat_id and not await db.security_threats.find_one({"id": threat_id}):
        raise LookupError("security threat not found")
    tests = list(dict.fromkeys(test_plan))
    refs = list(dict.fromkeys(evidence_refs))
    if not tests or not refs or not rollback_plan.strip():
        raise ValueError("test_plan, rollback_plan and evidence_refs are required")

    row = {
        "id": _id("REMED"),
        "finding_id": finding_id,
        "threat_id": threat_id,
        "title": title.strip(),
        "proposed_change": proposed_change.strip(),
        "target_system": target_system.strip().upper(),
        "rollback_plan": rollback_plan.strip(),
        "test_plan": tests,
        "evidence_refs": refs,
        "status": "REQUESTED",
        "authority_decision_ref": None,
        "external_dispatch": {
            "status": "PENDING_EXTERNAL_CONTRACT",
            "execution_dispatch_confirmed": False,
            "operations_mirror_confirmed": False,
            "results": {},
        },
        "execution_evidence_refs": [],
        "test_evidence_refs": [],
        "rollback_evidence_refs": [],
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }
    await db.security_remediations.insert_one(dict(row))
    await governance.audit_event(
        event_type="security.remediation.requested",
        actor_id=actor_id,
        resource_type="security_remediation",
        resource_id=row["id"],
        payload={
            "finding_id": finding_id,
            "threat_id": threat_id,
            "target_system": row["target_system"],
        },
    )
    return row


async def _require_allow_authority(remediation: Dict[str, Any], decision_id: str) -> Dict[str, Any]:
    if not decision_id.strip():
        raise ValueError("authority decision reference is required")
    decision = await authority_policy.get_decision(decision_id.strip())
    if decision.get("decision") != "ALLOW":
        raise PermissionError("security remediation requires an ALLOW authority decision")
    if str(decision.get("action", "")).upper() not in AUTHORIZATION_ACTIONS:
        raise ValueError("authority decision action does not authorize security remediation")
    context = decision.get("context") or {}
    if str(context.get("domain", "")).upper() != "SECURITY":
        raise ValueError("authority decision must be scoped to SECURITY domain")
    bound_id = context.get("remediation_id")
    if bound_id != remediation["id"]:
        raise ValueError("authority decision is not bound to this remediation")
    target = context.get("target_system")
    if target and str(target).upper() != remediation["target_system"]:
        raise ValueError("authority decision target_system does not match remediation")
    return decision


async def authorize_remediation(
    *, actor_id: str, remediation_id: str, authority_decision_ref: str
) -> Dict[str, Any]:
    row = await db.security_remediations.find_one({"id": remediation_id}, {"_id": 0})
    if not row:
        raise LookupError("security remediation not found")
    if row["status"] not in {"REQUESTED", "FAILED"}:
        raise ValueError("only REQUESTED or FAILED remediation can be authorized")
    decision = await _require_allow_authority(row, authority_decision_ref)
    now = utc_now_iso()
    update = {
        "status": "AUTHORIZED",
        "authority_decision_ref": decision["id"],
        "authority_decision_hash": decision.get("decision_hash"),
        "authority_policy_version_id": decision.get("policy_version_id"),
        "authorized_by": actor_id,
        "updated_at": now,
    }
    result = await db.security_remediations.update_one(
        {"id": remediation_id, "status": row["status"]}, {"$set": update}
    )
    if result.modified_count != 1:
        raise ValueError("remediation authorization changed concurrently")
    await governance.audit_event(
        event_type="security.remediation.authorized",
        actor_id=actor_id,
        resource_type="security_remediation",
        resource_id=remediation_id,
        payload={
            "authority_decision_ref": decision["id"],
            "authority_decision_hash": decision.get("decision_hash"),
            "authority_policy_version_id": decision.get("policy_version_id"),
        },
        result="AUTHORIZED",
    )
    return {**row, **update}


async def dispatch_authorized_remediation(
    *, actor_id: str, remediation_id: str
) -> Dict[str, Any]:
    """Perform the real CVLN dispatch after Academy authority approval.

    Agent Factory must return a real mission id before execution is considered
    dispatched. Command Center is mirrored independently and can leave the dispatch
    PARTIAL without hiding the fact. No status transition to EXECUTING occurs here.
    """
    row = await db.security_remediations.find_one({"id": remediation_id}, {"_id": 0})
    if not row:
        raise LookupError("security remediation not found")
    if row["status"] != "AUTHORIZED":
        raise ValueError("automatic dispatch requires AUTHORIZED remediation")
    await _require_allow_authority(row, str(row.get("authority_decision_ref") or ""))

    prior = row.get("external_dispatch") or {}
    if prior.get("execution_dispatch_confirmed"):
        return row

    dispatch = await remediation_dispatch.dispatch_remediation(row)
    now = utc_now_iso()
    result = await db.security_remediations.update_one(
        {"id": remediation_id, "status": "AUTHORIZED"},
        {"$set": {"external_dispatch": dispatch, "updated_at": now}},
    )
    if result.modified_count != 1:
        raise ValueError("remediation changed during automatic dispatch")
    await governance.audit_event(
        event_type="security.remediation.external_dispatch",
        actor_id=actor_id,
        resource_type="security_remediation",
        resource_id=remediation_id,
        payload={
            "status": dispatch["status"],
            "execution_dispatch_confirmed": dispatch["execution_dispatch_confirmed"],
            "operations_mirror_confirmed": dispatch["operations_mirror_confirmed"],
            "agent_factory_task_id": (
                dispatch.get("results", {}).get("agent_factory", {}).get("remote_task_id")
            ),
            "command_center_task_id": (
                dispatch.get("results", {}).get("command_center", {}).get("remote_task_id")
            ),
        },
    )
    return {**row, "external_dispatch": dispatch, "updated_at": now}


async def record_external_dispatch(
    *,
    actor_id: str,
    remediation_id: str,
    target: str,
    remote_task_id: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    """Legacy/manual adapter record, retained for non-CVLN external systems."""
    row = await db.security_remediations.find_one({"id": remediation_id}, {"_id": 0})
    if not row:
        raise LookupError("security remediation not found")
    if row["status"] not in {"AUTHORIZED", "EXECUTING", "TESTING"}:
        raise ValueError("external dispatch requires an authorized remediation")
    await _require_allow_authority(row, str(row.get("authority_decision_ref") or ""))
    normalized_target = target.strip().upper()
    if normalized_target != row["target_system"]:
        raise ValueError("dispatch target does not match remediation target_system")
    refs = list(dict.fromkeys(evidence_refs))
    if not remote_task_id.strip() or not refs:
        raise ValueError("real remote task id and dispatch evidence are required")
    dispatch = {
        "status": "CONFIRMED",
        "execution_dispatch_confirmed": True,
        "operations_mirror_confirmed": False,
        "results": {
            "manual_external": {
                "target": normalized_target,
                "status": "DISPATCHED_CONFIRMED",
                "remote_task_id": remote_task_id.strip(),
                "evidence_refs": refs,
                "recorded_by": actor_id,
                "recorded_at": utc_now_iso(),
            }
        },
    }
    result = await db.security_remediations.update_one(
        {"id": remediation_id, "status": row["status"]},
        {"$set": {"external_dispatch": dispatch, "updated_at": utc_now_iso()}},
    )
    if result.modified_count != 1:
        raise ValueError("remediation changed during external dispatch recording")
    return {**row, "external_dispatch": dispatch}


async def transition_remediation(
    *,
    actor_id: str,
    remediation_id: str,
    status: str,
    evidence_refs: Iterable[str] = (),
) -> Dict[str, Any]:
    row = await db.security_remediations.find_one({"id": remediation_id}, {"_id": 0})
    if not row:
        raise LookupError("security remediation not found")
    target = status.strip().upper()
    if target not in STATES or target not in TRANSITIONS[row["status"]]:
        raise ValueError(f"invalid remediation transition {row['status']}->{target}")
    refs = list(dict.fromkeys(evidence_refs))

    if target == "EXECUTING":
        await _require_allow_authority(row, str(row.get("authority_decision_ref") or ""))
        if not (row.get("external_dispatch") or {}).get("execution_dispatch_confirmed"):
            raise ValueError("execution requires confirmed Agent Factory/external dispatch")
    if target == "TESTING" and not refs:
        raise ValueError("testing transition requires execution evidence")
    if target == "VERIFIED":
        if not refs:
            raise ValueError("verified remediation requires test evidence")
        if row.get("status") != "TESTING":
            raise ValueError("remediation must be TESTING before verification")
    if target == "ROLLED_BACK" and not refs:
        raise ValueError("rollback completion requires evidence")

    now = utc_now_iso()
    update: Dict[str, Any] = {
        "status": target,
        "updated_at": now,
        "last_actor_id": actor_id,
    }
    if target == "TESTING":
        update["execution_evidence_refs"] = refs
    elif target == "VERIFIED":
        update["test_evidence_refs"] = refs
    elif target == "ROLLED_BACK":
        update["rollback_evidence_refs"] = refs

    result = await db.security_remediations.update_one(
        {"id": remediation_id, "status": row["status"]}, {"$set": update}
    )
    if result.modified_count != 1:
        raise ValueError("remediation state changed concurrently")
    await governance.audit_event(
        event_type="security.remediation.status_changed",
        actor_id=actor_id,
        resource_type="security_remediation",
        resource_id=remediation_id,
        payload={"from": row["status"], "to": target, "evidence_refs": refs},
    )
    return {**row, **update}


async def remediation_gate() -> Dict[str, Any]:
    blockers = await db.security_remediations.find(
        {"status": {"$nin": ["VERIFIED", "ROLLED_BACK", "CANCELLED"]}}, {"_id": 0}
    ).to_list(1000)
    return {
        "pass": len(blockers) == 0,
        "blocking_count": len(blockers),
        "blocking_remediations": blockers,
    }
