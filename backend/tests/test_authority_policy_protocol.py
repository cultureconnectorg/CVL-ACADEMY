from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from services import authority_policy_protocol


class _Executions:
    def __init__(self):
        self.rows = []

    async def insert_one(self, row):
        self.rows.append(row)
        return SimpleNamespace(inserted_id="exec-1")


@pytest.mark.asyncio
async def test_gov_02_preflight_calls_canonical_authority_engine(monkeypatch):
    control = authority_policy_protocol.gov_02_contract()
    execution_store = _Executions()
    monkeypatch.setattr(
        authority_policy_protocol,
        "db",
        SimpleNamespace(academy_protocol_executions=execution_store),
    )
    decision = {
        "id": "AUTHDEC-1",
        "decision_hash": "hash-1",
        "decision": "ALLOW",
        "policy_version_id": "POLV-1",
    }
    evaluate = AsyncMock(return_value=decision)
    monkeypatch.setattr(
        authority_policy_protocol.authority_policy,
        "evaluate_authority",
        evaluate,
    )
    integration_refs = {
        name: f"proof:{name}" for name in control["integrates_with"]
    }

    result = await authority_policy_protocol.execute_authority_policy_protocol(
        actor_id="user-1",
        actor_role="admin",
        action="FORMATION_PUBLISH",
        authority_context="delegated",
        policy_version_id="POLV-1",
        evidence_ref="evidence-1",
        control_version_ref="gov-02-v1",
        frek_proof_ref="frek-proof-1",
        production_gate_evidence_ref="gate-proof-1",
        expert_review_ref="founder-review-1",
        cvln_ios_ref="ios-context-1",
        integration_refs=integration_refs,
        policy_context={"domain": "ACADEMY"},
        request_id="request-1",
    )

    evaluate.assert_awaited_once()
    assert result["control_id"] == "GOV-02"
    assert result["behavior_fingerprint"] == control["behavior_fingerprint"]
    assert result["authority_decision_id"] == "AUTHDEC-1"
    assert result["authority_decision"] == "ALLOW"
    assert len(execution_store.rows) == 1


@pytest.mark.asyncio
async def test_gov_02_fails_before_authority_engine_when_proof_missing(
    monkeypatch,
):
    control = authority_policy_protocol.gov_02_contract()
    evaluate = AsyncMock()
    monkeypatch.setattr(
        authority_policy_protocol.authority_policy,
        "evaluate_authority",
        evaluate,
    )
    integration_refs = {
        name: f"proof:{name}" for name in control["integrates_with"]
    }
    integration_refs.pop("FREK")

    with pytest.raises(PermissionError, match="GOV-02 protocol preflight denied"):
        await authority_policy_protocol.execute_authority_policy_protocol(
            actor_id="user-1",
            actor_role="admin",
            action="FORMATION_PUBLISH",
            authority_context="delegated",
            policy_version_id="POLV-1",
            evidence_ref="evidence-1",
            control_version_ref="gov-02-v1",
            frek_proof_ref="frek-proof-1",
            production_gate_evidence_ref="gate-proof-1",
            expert_review_ref="founder-review-1",
            cvln_ios_ref="ios-context-1",
            integration_refs=integration_refs,
            policy_context={"domain": "ACADEMY"},
        )

    evaluate.assert_not_awaited()
