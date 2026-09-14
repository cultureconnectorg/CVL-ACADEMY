"""Runtime execution boundary for the 227 Protocol Master controls.

Every control is evaluated against its exact Excel row contract first, then
against the canonical Authority Policy Engine. No protocol execution can be
accepted solely because a caller has an admin role.
"""
from __future__ import annotations

from typing import Any

from services import authority_policy
from services.protocol_master_runtime import evaluate_protocol_control


def _authority_context(control: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    authority_context = dict(context)
    authority_context["protocol_control_id"] = control["control_id"]
    authority_context["protocol_behavior_fingerprint"] = control["behavior_fingerprint"]
    authority_context["protocol_row_hash"] = control["row_hash"]
    authority_context["domain"] = control["domain"]
    authority_context["resource_type"] = "academy_protocol_control"
    return authority_context


async def execute_protocol_control_runtime(
    *,
    control: dict[str, Any],
    context: dict[str, Any],
    actor_role: str,
) -> dict[str, Any]:
    """Execute one exact row contract under versioned authority policy.

    The local row contract must pass first. Authority then evaluates a stable,
    control-specific action. Missing/invalid policy evidence fails closed via
    the Authority Policy Engine; there is no founder/admin bypass here.
    """
    local = evaluate_protocol_control(control, context)
    if not local["allowed"]:
        return {**local, "authority": None}

    policy_version_id = context.get("policy_version_id")
    if not policy_version_id:
        return {
            **local,
            "allowed": False,
            "reasons": [*local["reasons"], "MISSING:policy_version_id"],
            "authority": None,
        }

    action = f"EXECUTE_PROTOCOL_CONTROL:{control['control_id']}"
    authority = await authority_policy.evaluate_authority(
        actor_id=context["actor_id"],
        actor_role=actor_role,
        action=action,
        context=_authority_context(control, context),
        policy_version_id=policy_version_id,
        request_id=context.get("request_id"),
    )
    authority_effect = authority["decision"]
    allowed = authority_effect == "ALLOW"
    reasons = list(local["reasons"])
    if not allowed:
        reasons.append(f"AUTHORITY_{authority_effect}")

    return {
        **local,
        "allowed": allowed,
        "reasons": reasons,
        "authority": {
            "decision_id": authority["id"],
            "decision": authority_effect,
            "matched_rule_id": authority.get("matched_rule_id"),
            "policy_version_id": authority["policy_version_id"],
            "policy_content_hash": authority["policy_content_hash"],
            "decision_hash": authority["decision_hash"],
        },
    }
