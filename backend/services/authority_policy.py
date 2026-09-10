"""Cross-cutting Authority Policy Engine (XCP-001).

The engine does not replace Academy authentication/RBAC. It consumes an already
resolved actor identity/role plus explicit runtime context and one immutable policy
version from the canonical XCP-008 registry, then records ALLOW / DENY / ESCALATE
with an explicit reason.

No matching rule => DENY. There is no hidden Founder/admin bypass.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import policy_registry, professional_governance as governance


DECISIONS = {"ALLOW", "DENY", "ESCALATE"}
AUTHORITY_LEVELS = {
    "A0_SYSTEM": 0,
    "A1_OPERATOR": 1,
    "A2_DOMAIN_REVIEWER": 2,
    "A3_EXTERNAL_EXPERT": 3,
    "A4_CVL_AUTHORITY": 4,
    "A5_FOUNDER_SYSTEMIC": 5,
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
    if not _match_dimension(_normalise(conditions.get("risk_levels")), context.get("risk_level")):
        return False
    if not _match_dimension(_normalise(conditions.get("resource_types")), context.get("resource_type")):
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
    supersedes_version_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Register authority rules in the single canonical policy registry."""
    if not doctrine_ref.strip():
        raise ValueError("doctrine_ref is required")
    if not rules:
        raise ValueError("authority policy requires at least one rule")

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

    return await policy_registry.register_version(
        actor_id=actor_id,
        policy_key=policy_key,
        version=version,
        kind="POLICY",
        title=title,
        content={"rules": normalised_rules, "doctrine_ref": doctrine_ref.strip()},
        effective_at=effective_at,
        evidence_refs=evidence_refs,
        supersedes_version_id=supersedes_version_id,
    )


async def evaluate_authority(
    *,
    actor_id: str,
    actor_role: str,
    action: str,
    context: Dict[str, Any],
    policy_version_id: str,
    request_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Evaluate one explicit authority question against one effective version."""
    policy = await policy_registry.require_effective_version(policy_version_id)
    if policy.get("kind") != "POLICY":
        raise ValueError("authority engine requires a POLICY version")
    content = policy.get("content") or {}
    rules = content.get("rules") or []
    if not rules:
        raise ValueError("authority policy has no rules")

    selected: Optional[Dict[str, Any]] = None
    for rule in rules:
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
        "policy_effective_at": policy["effective_at"],
        "policy_content_hash": policy["content_hash"],
        "policy_supersedes_version_id": policy.get("supersedes_version_id"),
        "doctrine_ref": content.get("doctrine_ref"),
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
            "policy_content_hash": policy["content_hash"],
            "decision_hash": decision["decision_hash"],
        },
    )
    return decision


async def get_decision(decision_id: str) -> Dict[str, Any]:
    row = await db.authority_decisions.find_one({"id": decision_id}, {"_id": 0})
    if not row:
        raise LookupError("authority decision not found")
    return row
