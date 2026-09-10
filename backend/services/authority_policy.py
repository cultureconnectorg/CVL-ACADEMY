"""Cross-cutting Authority Policy Engine (XCP-001).

The engine does not replace Academy authentication/RBAC. It consumes an already
resolved actor identity/role plus explicit runtime context and an immutable policy
version, then produces an auditable ALLOW / DENY / ESCALATE decision with reason.

No policy => no authority decision. No matching rule => DENY. There is deliberately
no hidden Founder/admin bypass: elevated authority must be expressed by policy.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import professional_governance as governance


DECISIONS = {"ALLOW", "DENY", "ESCALATE"}
AUTHORITY_LEVELS = {
    "A0_SYSTEM": 0,
    "A1_OPERATOR": 1,
    "A2_DOMAIN_REVIEWER": 2,
    "A3_EXTERNAL_EXPERT": 3,
    "A4_CVL_AUTHORITY": 4,
}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _canonical_hash(payload: Dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _normalise(values: Iterable[str] | None) -> list[str]:
    return sorted({str(value).strip().upper() for value in (values or []) if str(value).strip()})


def _match_dimension(expected: list[str], actual: Optional[str]) -> bool:
    if not expected or "*" in expected:
        return True
    return bool(actual and actual.upper() in expected)


def _rule_matches(rule: Dict[str, Any], *, actor_role: str, action: str, context: Dict[str, Any]) -> bool:
    conditions = rule.get("conditions") or {}
    if not _match_dimension(_normalise(conditions.get("actor_roles")), actor_role):
        return False
    if not _match_dimension(_normalise(conditions.get("actions")), action):
        return False
    if not _match_dimension(_normalise(conditions.get("domains")), context.get("domain")):
        return False
    if not _match_dimension(_normalise(conditions.get("jurisdictions")), context.get("jurisdiction")):
        return False
    if not _match_dimension(_normalise(conditions.get("sensitivities")), context.get("sensitivity")):
        return False

    required_level = conditions.get("minimum_authority_level")
    if required_level:
        required = AUTHORITY_LEVELS.get(str(required_level).upper())
        actual = AUTHORITY_LEVELS.get(str(context.get("authority_level", "")).upper())
        if required is None or actual is None or actual < required:
            return False
    return True


async def register_policy_version(
    *,
    actor_id: str,
    policy_key: str,
    version: str,
    title: str,
    rules: list[Dict[str, Any]],
    effective_at: str,
    doctrine_ref: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    """Register one immutable, immediately-active authority policy version.

    XCP-008 will own the broader doctrine/policy lifecycle and supersession model.
    For XCP-001 the minimum safe primitive is an immutable version with evidence,
    effective date and deterministic rule order.
    """
    key = policy_key.strip().upper()
    ver = version.strip()
    refs = list(dict.fromkeys(evidence_refs))
    if not key or not ver or not title.strip() or not doctrine_ref.strip():
        raise ValueError("policy_key, version, title and doctrine_ref are required")
    if not refs:
        raise ValueError("authority policy registration requires evidence")
    if not rules:
        raise ValueError("authority policy requires at least one rule")
    if await db.authority_policy_versions.find_one({"policy_key": key, "version": ver}):
        raise ValueError("authority policy version already exists")

    normalised_rules: list[Dict[str, Any]] = []
    for index, raw_rule in enumerate(rules):
        effect = str(raw_rule.get("effect", "")).upper()
        reason = str(raw_rule.get("reason", "")).strip()
        if effect not in DECISIONS or not reason:
            raise ValueError("each authority rule requires valid effect and reason")
        normalised_rules.append(
            {
                "id": str(raw_rule.get("id") or f"R{index + 1}"),
                "priority": int(raw_rule.get("priority", index + 1)),
                "effect": effect,
                "reason": reason,
                "conditions": raw_rule.get("conditions") or {},
            }
        )
    normalised_rules.sort(key=lambda row: (row["priority"], row["id"]))

    body = {
        "policy_key": key,
        "version": ver,
        "title": title.strip(),
        "rules": normalised_rules,
        "effective_at": effective_at,
        "doctrine_ref": doctrine_ref.strip(),
        "evidence_refs": refs,
    }
    row = {
        "id": _id("POLV"),
        **body,
        "policy_hash": _canonical_hash(body),
        "status": "ACTIVE",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "immutable": True,
    }
    await db.authority_policy_versions.insert_one(dict(row))
    await governance.audit_event(
        event_type="authority.policy_version.registered",
        actor_id=actor_id,
        resource_type="authority_policy_version",
        resource_id=row["id"],
        payload={"policy_key": key, "version": ver, "policy_hash": row["policy_hash"]},
    )
    return row


async def evaluate_authority(
    *,
    actor_id: str,
    actor_role: str,
    action: str,
    context: Dict[str, Any],
    policy_version_id: str,
    request_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Evaluate one explicit authority question against one immutable version."""
    policy = await db.authority_policy_versions.find_one(
        {"id": policy_version_id, "status": "ACTIVE", "immutable": True}, {"_id": 0}
    )
    if not policy:
        raise LookupError("active immutable authority policy version not found")

    expected_hash = _canonical_hash(
        {
            "policy_key": policy["policy_key"],
            "version": policy["version"],
            "title": policy["title"],
            "rules": policy["rules"],
            "effective_at": policy["effective_at"],
            "doctrine_ref": policy["doctrine_ref"],
            "evidence_refs": policy["evidence_refs"],
        }
    )
    if expected_hash != policy.get("policy_hash"):
        raise ValueError("authority policy integrity check failed")

    selected: Optional[Dict[str, Any]] = None
    for rule in policy["rules"]:
        if _rule_matches(rule, actor_role=actor_role, action=action, context=context):
            selected = rule
            break

    effect = selected["effect"] if selected else "DENY"
    reason = selected["reason"] if selected else "No authority policy rule matched; fail-closed denial."
    now = utc_now_iso()
    decision = {
        "id": _id("AUTHDEC"),
        "request_id": request_id or _id("AUTHREQ"),
        "actor_id": actor_id,
        "actor_role": actor_role,
        "action": action.upper(),
        "context": context,
        "context_hash": _canonical_hash(context),
        "decision": effect,
        "reason": reason,
        "matched_rule_id": selected["id"] if selected else None,
        "policy_version_id": policy["id"],
        "policy_key": policy["policy_key"],
        "policy_version": policy["version"],
        "policy_hash": policy["policy_hash"],
        "doctrine_ref": policy["doctrine_ref"],
        "decided_at": now,
    }
    decision["decision_hash"] = _canonical_hash(decision)
    await db.authority_decisions.insert_one(dict(decision))
    await governance.audit_event(
        event_type="authority.decision.recorded",
        actor_id=actor_id,
        resource_type="authority_decision",
        resource_id=decision["id"],
        payload={
            "decision": effect,
            "action": decision["action"],
            "policy_version_id": policy["id"],
            "decision_hash": decision["decision_hash"],
        },
    )
    return decision


async def get_decision(decision_id: str) -> Dict[str, Any]:
    row = await db.authority_decisions.find_one({"id": decision_id}, {"_id": 0})
    if not row:
        raise LookupError("authority decision not found")
    return row
