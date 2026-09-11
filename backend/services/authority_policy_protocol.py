"""GOV-02 Authority Policy Engine Protocol.

This protocol wraps the existing XCP-001 Authority Policy Engine. It never
creates a second authority source: the exact GOV-02 Excel contract is checked
first, then the canonical versioned authority policy is evaluated fail-closed.
"""
from __future__ import annotations

from typing import Any

from db import db, utc_now_iso
from services import authority_policy
from services.protocol_master_runtime import (
    evaluate_protocol_control,
    load_protocol_controls,
)


def gov_02_contract() -> dict[str, Any]:
    return next(
        control
        for control in load_protocol_controls()
        if control["control_id"] == "GOV-02"
    )


async def execute_authority_policy_protocol(
    *,
    actor_id: str,
    actor_role: str,
    action: str,
    authority_context: str,
    policy_version_id: str,
    evidence_ref: str,
    control_version_ref: str,
    frek_proof_ref: str,
    production_gate_evidence_ref: str,
    expert_review_ref: str,
    cvln_ios_ref: str,
    integration_refs: dict[str, str],
    policy_context: dict[str, Any] | None = None,
    request_id: str | None = None,
) -> dict[str, Any]:
    """Execute GOV-02 preflight and canonical Authority Engine decision."""
    control = gov_02_contract()
    protocol_context = {
        "actor_id": actor_id,
        "authority_context": authority_context,
        "evidence_ref": evidence_ref,
        "control_id": control["control_id"],
        "behavior_fingerprint": control["behavior_fingerprint"],
        "control_version_ref": control_version_ref,
        "integration_refs": integration_refs,
        "frek_proof_ref": frek_proof_ref,
        "production_gate_evidence_ref": production_gate_evidence_ref,
        "expert_review_ref": expert_review_ref,
        "cvln_ios_ref": cvln_ios_ref,
        "policy_version_id": policy_version_id,
    }
    preflight = evaluate_protocol_control(control, protocol_context)
    if not preflight["allowed"]:
        raise PermissionError(
            "GOV-02 protocol preflight denied: " + ", ".join(preflight["reasons"])
        )

    authority_decision = await authority_policy.evaluate_authority(
        actor_id=actor_id,
        actor_role=actor_role,
        action=action,
        context=policy_context or {},
        policy_version_id=policy_version_id,
        request_id=request_id,
    )
    execution = {
        "control_id": "GOV-02",
        "behavior_fingerprint": control["behavior_fingerprint"],
        "row_hash": control["row_hash"],
        "protocol_preflight": preflight,
        "authority_decision_id": authority_decision["id"],
        "authority_decision_hash": authority_decision["decision_hash"],
        "authority_decision": authority_decision["decision"],
        "policy_version_id": authority_decision["policy_version_id"],
        "evidence_ref": evidence_ref,
        "executed_at": utc_now_iso(),
    }
    await db.academy_protocol_executions.insert_one(dict(execution))
    return {**execution, "authority": authority_decision}
