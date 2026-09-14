"""Quality improvement/proof protocols (QLT-21/QLT-27).

Improvement evidence extends the canonical Quality Core action store. FREK proof reuses
the cross-domain Critical Proof service; this module never creates a second notary.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Iterable

from db import db, utc_now_iso
from services import critical_proof
from services import professional_governance as governance


def _refs(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(str(v).strip() for v in values if str(v).strip()))


def _hash(payload: Dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


async def record_improvement_evidence(
    *,
    actor_id: str,
    action_id: str,
    status: str,
    outcome: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    action = await db.quality_improvement_actions.find_one({"id": action_id}, {"_id": 0})
    if not action:
        raise LookupError("quality improvement action not found")
    target = str(status or "").strip().upper()
    allowed = {
        "OPEN": {"IN_PROGRESS"},
        "IN_PROGRESS": {"VERIFIED"},
        "VERIFIED": {"CLOSED"},
        "CLOSED": set(),
    }
    if target not in allowed.get(action.get("status"), set()):
        raise ValueError(f"invalid improvement transition {action.get('status')}->{target}")
    refs = _refs(evidence_refs)
    if not outcome.strip() or not refs:
        raise ValueError("improvement transition requires outcome and evidence")
    now = utc_now_iso()
    event = {
        "from": action["status"],
        "to": target,
        "outcome": outcome.strip(),
        "evidence_refs": refs,
        "actor_id": actor_id,
        "recorded_at": now,
    }
    update = {
        "status": target,
        "last_outcome": outcome.strip(),
        "last_evidence_refs": refs,
        "updated_at": now,
    }
    result = await db.quality_improvement_actions.update_one(
        {"id": action_id, "status": action["status"]},
        {"$set": update, "$push": {"evidence_history": event}},
    )
    if result.modified_count != 1:
        raise ValueError("quality improvement action changed concurrently")
    await governance.audit_event(
        event_type="quality.improvement.state_changed",
        actor_id=actor_id,
        resource_type="quality_improvement_action",
        resource_id=action_id,
        before={"status": action["status"]},
        after={"status": target},
        reason=outcome.strip(),
        result=target,
        payload={"evidence_refs": refs},
    )
    return {**action, **update, "last_event": event}


async def create_quality_frek_proof(
    *,
    actor_id: str,
    resource_type: str,
    resource_id: str,
    authority_decision_id: str,
    policy_version_id: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    """Create QLT-27 proof only for a concrete canonical Quality record."""
    normalized = str(resource_type or "").strip().upper()
    collections = {
        "QUALITY_IMPROVEMENT_ACTION": db.quality_improvement_actions,
        "QUALITY_AUDIT_PACK": db.quality_audit_packs,
        "QUALITY_COMPLAINT": db.quality_complaints,
    }
    collection = collections.get(normalized)
    if collection is None:
        raise ValueError("unsupported quality proof resource_type")
    resource = await collection.find_one({"id": resource_id}, {"_id": 0})
    if not resource:
        raise LookupError("quality proof resource not found")
    refs = _refs(evidence_refs)
    if not refs:
        raise ValueError("quality FREK proof requires evidence")
    digest = _hash(resource)
    return await critical_proof.create_critical_decision_proof(
        actor_id=actor_id,
        domain="QUALITY",
        resource_type=normalized,
        resource_id=resource_id,
        resource_hash=digest,
        authority_decision_id=authority_decision_id,
        policy_version_id=policy_version_id,
        evidence_refs=refs,
    )
