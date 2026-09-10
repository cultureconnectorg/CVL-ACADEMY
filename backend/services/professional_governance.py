"""Professional Governance Core for CVLN Academy.

Implements the first P0 primitives from the Academy integration masters:
professional cases, scoped expert identities/assignments, document-version
registry, review/decision workflow, append-only audit trail and scoped expert
credential lifecycle.
"""

from __future__ import annotations

import hashlib
import json
import secrets
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso


TERMINAL_DECISION_STATES = {"APPROVED", "REJECTED", "SUPERSEDED"}
CASE_STATES = {"OPEN", "IN_REVIEW", "BLOCKED", "RESOLVED", "ARCHIVED"}
DECISION_STATES = {"DRAFT", "PROPOSED", "APPROVED", "REJECTED", "SUPERSEDED"}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _canonical_hash(payload: Dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _normalise_expiry(expires_at: str) -> str:
    raw = (expires_at or "").strip()
    if not raw:
        raise ValueError("expert credential expiry is required")
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("expires_at must be a valid ISO-8601 datetime") from exc
    if parsed.tzinfo is None:
        raise ValueError("expires_at must include a timezone")
    now = datetime.now(timezone.utc)
    if parsed.astimezone(timezone.utc) <= now:
        raise ValueError("expires_at must be in the future")
    return parsed.astimezone(timezone.utc).isoformat()


async def audit_event(
    *,
    event_type: str,
    actor_id: str,
    resource_type: str,
    resource_id: str,
    payload: Optional[Dict[str, Any]] = None,
    before: Optional[Dict[str, Any]] = None,
    after: Optional[Dict[str, Any]] = None,
    reason: Optional[str] = None,
    result: Optional[str] = None,
) -> Dict[str, Any]:
    """Write the single Academy governance audit envelope.

    Optional before/after/reason/result fields allow sensitive workflows to satisfy
    GOV-010 without inventing separate domain audit stores. Existing callers remain
    valid; the canonical payload hash covers the complete audit body.
    """
    body = {
        "data": payload or {},
        "before": before,
        "after": after,
        "reason": reason,
        "result": result,
    }
    event = {
        "id": _id("AUD"),
        "event_type": event_type,
        "actor_id": actor_id,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "payload": payload or {},
        "before": before,
        "after": after,
        "reason": reason,
        "result": result,
        "payload_hash": _canonical_hash(body),
        "created_at": utc_now_iso(),
    }
    await db.governance_audit_events.insert_one(dict(event))
    return event


async def create_case(
    *,
    actor_id: str,
    title: str,
    domain: str,
    description: str,
    sensitivity: str = "INTERNAL",
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    case = {
        "id": _id("CASE"),
        "title": title,
        "domain": domain.upper(),
        "description": description,
        "sensitivity": sensitivity.upper(),
        "status": "OPEN",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
        "metadata": metadata or {},
    }
    await db.professional_cases.insert_one(dict(case))
    await audit_event(
        event_type="governance.case.created",
        actor_id=actor_id,
        resource_type="professional_case",
        resource_id=case["id"],
        payload={"domain": case["domain"], "sensitivity": case["sensitivity"]},
        after=case,
        reason="Professional case created",
        result="CREATED",
    )
    return case


async def transition_case(*, case_id: str, status: str, actor_id: str) -> Dict[str, Any]:
    target = status.upper()
    if target not in CASE_STATES:
        raise ValueError("invalid case status")
    before = await db.professional_cases.find_one({"id": case_id}, {"_id": 0})
    if not before:
        raise LookupError("case not found")
    now = utc_now_iso()
    result = await db.professional_cases.update_one(
        {"id": case_id, "status": before["status"]},
        {"$set": {"status": target, "updated_at": now}},
    )
    if result.modified_count != 1:
        raise ValueError("case status changed concurrently")
    after = {**before, "status": target, "updated_at": now}
    await audit_event(
        event_type="governance.case.status_changed",
        actor_id=actor_id,
        resource_type="professional_case",
        resource_id=case_id,
        payload={"from": before["status"], "to": target},
        before=before,
        after=after,
        reason="Professional case lifecycle transition",
        result=target,
    )
    return after


async def create_expert(
    *,
    actor_id: str,
    display_name: str,
    email: str,
    domains: Iterable[str],
    organisation: Optional[str] = None,
) -> Dict[str, Any]:
    expert = {
        "id": _id("EXP"),
        "display_name": display_name,
        "email": email.lower(),
        "domains": sorted({d.upper() for d in domains}),
        "organisation": organisation,
        "status": "ACTIVE",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.governance_experts.insert_one(dict(expert))
    await audit_event(
        event_type="governance.expert.created",
        actor_id=actor_id,
        resource_type="expert",
        resource_id=expert["id"],
        payload={"domains": expert["domains"]},
        after={k: v for k, v in expert.items() if k != "email"},
        reason="Expert identity registered",
        result="CREATED",
    )
    return expert


async def assign_expert(
    *,
    actor_id: str,
    case_id: str,
    expert_id: str,
    scope: Iterable[str],
    authority_level: str = "A3_EXTERNAL_EXPERT",
) -> Dict[str, Any]:
    case = await db.professional_cases.find_one({"id": case_id}, {"_id": 0})
    expert = await db.governance_experts.find_one({"id": expert_id}, {"_id": 0})
    if not case or not expert:
        raise LookupError("case or expert not found")
    assignment = {
        "id": _id("ASN"),
        "case_id": case_id,
        "expert_id": expert_id,
        "scope": sorted(set(scope)),
        "authority_level": authority_level,
        "status": "ACTIVE",
        "assigned_by": actor_id,
        "assigned_at": utc_now_iso(),
        "revoked_at": None,
    }
    await db.governance_expert_assignments.insert_one(dict(assignment))
    await audit_event(
        event_type="governance.expert.assigned",
        actor_id=actor_id,
        resource_type="professional_case",
        resource_id=case_id,
        payload={
            "assignment_id": assignment["id"],
            "expert_id": expert_id,
            "scope": assignment["scope"],
        },
        after=assignment,
        reason="Expert assigned to explicit case scope",
        result="ASSIGNED",
    )
    return assignment


async def issue_expert_api_key(
    *, actor_id: str, assignment_id: str, expires_at: str
) -> tuple[str, Dict[str, Any]]:
    assignment = await db.governance_expert_assignments.find_one(
        {"id": assignment_id, "status": "ACTIVE"}, {"_id": 0}
    )
    if not assignment:
        raise LookupError("active assignment not found")
    expiry = _normalise_expiry(expires_at)
    raw = f"cvln_exp_{secrets.token_urlsafe(32)}"
    record = {
        "id": _id("KEY"),
        "assignment_id": assignment_id,
        "expert_id": assignment["expert_id"],
        "case_id": assignment["case_id"],
        "scope": assignment["scope"],
        "token_hash": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
        "status": "ACTIVE",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "expires_at": expiry,
        "revoked_at": None,
        "rotated_to_key_id": None,
        "last_used_at": None,
        "usage_count": 0,
    }
    await db.governance_api_keys.insert_one(dict(record))
    await audit_event(
        event_type="governance.expert_api_key.issued",
        actor_id=actor_id,
        resource_type="expert_assignment",
        resource_id=assignment_id,
        payload={
            "key_id": record["id"],
            "scope": record["scope"],
            "expires_at": expiry,
        },
        reason="Scoped external expert credential issued",
        result="ACTIVE",
    )
    public = {k: v for k, v in record.items() if k != "token_hash"}
    return raw, public


async def rotate_expert_api_key(
    *, actor_id: str, key_id: str, expires_at: str
) -> tuple[str, Dict[str, Any]]:
    old = await db.governance_api_keys.find_one(
        {"id": key_id, "status": "ACTIVE"}, {"_id": 0}
    )
    if not old:
        raise LookupError("active expert API key not found")
    raw, new = await issue_expert_api_key(
        actor_id=actor_id,
        assignment_id=old["assignment_id"],
        expires_at=expires_at,
    )
    now = utc_now_iso()
    result = await db.governance_api_keys.update_one(
        {"id": key_id, "status": "ACTIVE"},
        {
            "$set": {
                "status": "ROTATED",
                "revoked_at": now,
                "revoked_by": actor_id,
                "rotated_to_key_id": new["id"],
            }
        },
    )
    if result.modified_count != 1:
        await db.governance_api_keys.update_one(
            {"id": new["id"]},
            {"$set": {"status": "REVOKED", "revoked_at": now, "revoked_by": actor_id}},
        )
        raise ValueError("expert credential rotation lost race")
    await audit_event(
        event_type="governance.expert_api_key.rotated",
        actor_id=actor_id,
        resource_type="expert_api_key",
        resource_id=key_id,
        payload={"new_key_id": new["id"], "expires_at": new["expires_at"]},
        before={"id": old["id"], "status": old["status"]},
        after={"id": old["id"], "status": "ROTATED", "rotated_to_key_id": new["id"]},
        reason="Expert credential rotated",
        result="ROTATED",
    )
    return raw, new


async def register_document_version(
    *,
    actor_id: str,
    case_id: str,
    document_type: str,
    title: str,
    content_hash: str,
    parent_version_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    if not await db.professional_cases.find_one({"id": case_id}):
        raise LookupError("case not found")
    version = {
        "id": _id("DOCV"),
        "case_id": case_id,
        "document_type": document_type.upper(),
        "title": title,
        "content_hash": content_hash.lower(),
        "parent_version_id": parent_version_id,
        "metadata": metadata or {},
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.governance_document_versions.insert_one(dict(version))
    await audit_event(
        event_type="governance.document.version_registered",
        actor_id=actor_id,
        resource_type="professional_case",
        resource_id=case_id,
        payload={"version_id": version["id"], "content_hash": version["content_hash"]},
        after=version,
        reason="Immutable document version registered",
        result="REGISTERED",
    )
    return version


async def create_decision(
    *,
    actor_id: str,
    case_id: str,
    subject: str,
    rationale: str,
    state: str = "PROPOSED",
    evidence_refs: Optional[Iterable[str]] = None,
) -> Dict[str, Any]:
    target = state.upper()
    if target not in DECISION_STATES:
        raise ValueError("invalid decision state")
    if not await db.professional_cases.find_one({"id": case_id}):
        raise LookupError("case not found")
    decision = {
        "id": _id("DEC"),
        "case_id": case_id,
        "subject": subject,
        "rationale": rationale,
        "state": target,
        "evidence_refs": list(evidence_refs or []),
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }
    decision["decision_hash"] = _canonical_hash(decision)
    await db.governance_decisions.insert_one(dict(decision))
    await audit_event(
        event_type="governance.decision.created",
        actor_id=actor_id,
        resource_type="professional_case",
        resource_id=case_id,
        payload={
            "decision_id": decision["id"],
            "state": target,
            "decision_hash": decision["decision_hash"],
        },
        after=decision,
        reason=rationale,
        result=target,
    )
    return decision


async def transition_decision(
    *, actor_id: str, decision_id: str, state: str
) -> Dict[str, Any]:
    target = state.upper()
    if target not in DECISION_STATES:
        raise ValueError("invalid decision state")
    decision = await db.governance_decisions.find_one({"id": decision_id}, {"_id": 0})
    if not decision:
        raise LookupError("decision not found")
    if decision["state"] in TERMINAL_DECISION_STATES:
        raise ValueError("terminal decision cannot be mutated; create a superseding decision")
    now = utc_now_iso()
    result = await db.governance_decisions.update_one(
        {"id": decision_id, "state": decision["state"]},
        {"$set": {"state": target, "updated_at": now}},
    )
    if result.modified_count != 1:
        raise ValueError("decision state changed concurrently")
    after = {**decision, "state": target, "updated_at": now}
    await audit_event(
        event_type="governance.decision.state_changed",
        actor_id=actor_id,
        resource_type="decision",
        resource_id=decision_id,
        payload={"from": decision["state"], "to": target},
        before=decision,
        after=after,
        reason=decision.get("rationale"),
        result=target,
    )
    return after
