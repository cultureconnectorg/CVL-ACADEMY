from unittest.mock import AsyncMock

import pytest

from services import protocol_execution
from services.protocol_master_runtime import load_protocol_controls

CONTROLS = load_protocol_controls()


def _context(control):
    context = {
        "actor_id": "actor-1",
        "evidence_ref": f"evidence:{control['control_id']}",
        "control_id": control["control_id"],
        "behavior_fingerprint": control["behavior_fingerprint"],
        "control_version_ref": f"version:{control['control_id']}:1",
        "policy_version_id": "POLV-1",
        "integration_refs": {
            name: f"integration:{name}" for name in control["integrates_with"]
        },
        "frek_proof_ref": "frek:1",
        "production_gate_evidence_ref": "gate:1",
        "expert_review_ref": "expert:1",
        "cvln_ios_ref": "ios:1",
        "systemic": False,
    }
    context.update(
        {
            "GOVERNANCE": {"authority_context": "delegated"},
            "LEGAL": {"jurisdiction": "FR", "expert_review_state": "REVIEWED"},
            "PRIVACY": {
                "data_classification": "PERSONAL",
                "lawful_basis": "CONSENT",
            },
            "SECURITY": {"severity": "LOW"},
            "ACCOUNTING": {
                "entity_context": "ACADEMY",
                "accounting_state": "PREPARED",
            },
            "RISK": {"risk_level": "R2", "owner": "risk-owner"},
            "QUALITY": {"quality_scope": "academy"},
            "TRUST": {"proof_ref": "proof:1", "proof_verified": True},
            "DATA": {
                "provenance_ref": "prov:1",
                "data_classification": "INTERNAL",
            },
            "REGULATORY": {
                "jurisdiction": "FR",
                "applicability_state": "REVIEWED",
                "expert_review_state": "REVIEWED",
            },
        }[control["domain"]]
    )
    if control["control_id"] == "REG-04":
        context["legal_assurance_level"] = "REVIEWED_BY_LAWYER"
    return context


def _authority_result(effect="ALLOW"):
    return {
        "id": "AUTHDEC-1",
        "decision": effect,
        "matched_rule_id": "R1" if effect == "ALLOW" else "R2",
        "policy_version_id": "POLV-1",
        "policy_content_hash": "a" * 64,
        "decision_hash": "b" * 64,
    }


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "control",
    CONTROLS,
    ids=[control["control_id"] for control in CONTROLS],
)
async def test_all_227_runtime_executions_are_wrapped_by_authority_engine(
    control, monkeypatch
):
    mocked = AsyncMock(return_value=_authority_result("ALLOW"))
    monkeypatch.setattr(protocol_execution.authority_policy, "evaluate_authority", mocked)

    decision = await protocol_execution.execute_protocol_control_runtime(
        control=control,
        context=_context(control),
        actor_role="admin",
    )

    assert decision["allowed"] is True
    assert decision["authority"]["decision"] == "ALLOW"
    call = mocked.await_args.kwargs
    assert call["action"] == f"EXECUTE_PROTOCOL_CONTROL:{control['control_id']}"
    assert call["policy_version_id"] == "POLV-1"
    assert call["context"]["protocol_behavior_fingerprint"] == control["behavior_fingerprint"]
    assert call["context"]["protocol_row_hash"] == control["row_hash"]


@pytest.mark.asyncio
async def test_authority_deny_overrides_a_complete_excel_contract(monkeypatch):
    control = CONTROLS[0]
    mocked = AsyncMock(return_value=_authority_result("DENY"))
    monkeypatch.setattr(protocol_execution.authority_policy, "evaluate_authority", mocked)

    decision = await protocol_execution.execute_protocol_control_runtime(
        control=control,
        context=_context(control),
        actor_role="founder",
    )

    assert decision["allowed"] is False
    assert "AUTHORITY_DENY" in decision["reasons"]


@pytest.mark.asyncio
async def test_missing_policy_version_fails_closed_before_authority_call(monkeypatch):
    control = next(row for row in CONTROLS if row["control_id"] == "GOV-02")
    context = _context(control)
    context.pop("policy_version_id")
    mocked = AsyncMock(return_value=_authority_result("ALLOW"))
    monkeypatch.setattr(protocol_execution.authority_policy, "evaluate_authority", mocked)

    decision = await protocol_execution.execute_protocol_control_runtime(
        control=control,
        context=context,
        actor_role="founder",
    )

    assert decision["allowed"] is False
    assert "MISSING:policy_version_id" in decision["reasons"]
    mocked.assert_not_awaited()
