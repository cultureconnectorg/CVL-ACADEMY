from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import (
    architecture_reuse,
    assurance_core,
    data_classification,
    evidence_graph,
    production_gates,
    professional_governance,
    retention_executor,
    security_remediation,
    threat_model,
)


@pytest.fixture
async def gates_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_production_gates_test"]
    for module in (
        architecture_reuse,
        assurance_core,
        data_classification,
        evidence_graph,
        production_gates,
        professional_governance,
        retention_executor,
        security_remediation,
        threat_model,
    ):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


@pytest.mark.asyncio
async def test_staging_gate_never_passes_without_exact_evidence(gates_db):
    result = await production_gates.evaluate_gate(
        gate_id="PG-10", commit_sha="abcdef123456"
    )
    assert result["pass"] is False
    await production_gates.record_gate_evidence(
        actor_id="admin",
        gate_id="PG-10",
        commit_sha="abcdef123456",
        environment="staging",
        evidence_refs=["STAGING-RUN-1"],
        result="PASS",
    )
    exact = await production_gates.evaluate_gate(
        gate_id="PG-10", commit_sha="abcdef123456"
    )
    other = await production_gates.evaluate_gate(
        gate_id="PG-10", commit_sha="different999"
    )
    assert exact["pass"] is True
    assert other["pass"] is False


@pytest.mark.asyncio
async def test_architecture_manifest_is_locked_and_conflicts_fail(gates_db):
    synced = await architecture_reuse.sync_manifest(actor_id="admin")
    assert synced["count"] == len(architecture_reuse.MANIFEST)
    gate = await architecture_reuse.gate()
    assert gate["pass"] is True
    await architecture_reuse.register_build_decision(
        actor_id="admin",
        theme="Payments",
        component="accounting payment reader",
        decision="REUSE",
        canonical_owner="Payments Core",
        evidence_ref="PG-13",
    )
    with pytest.raises(ValueError, match="conflicts"):
        await architecture_reuse.register_build_decision(
            actor_id="admin",
            theme="Payments",
            component="new payment engine",
            decision="BUILD",
            canonical_owner="Payments Core",
            evidence_ref="BAD",
        )

    await gates_db.architecture_build_decisions.insert_one(
        {
            "theme": "Payments",
            "component": "legacy manual payment clone",
            "decision": "BUILD",
            "canonical_owner": "Payments Core",
            "manifest_id": "REUSE-07",
            "evidence_ref": "LEGACY-BAD",
        }
    )
    gate = await architecture_reuse.gate()
    assert gate["pass"] is False
    assert gate["conflict_count"] == 1
    assert gate["conflicts"][0]["conflict_reason"] == "DECISION_CONFLICT"


@pytest.mark.asyncio
async def test_cross_cutting_gate_requires_all_eight_verified(gates_db):
    for index in range(1, 8):
        await production_gates.record_xcp_evidence(
            actor_id="admin",
            primitive_id=f"XCP-{index:03d}",
            evidence_refs=[f"TEST-XCP-{index}"],
            status="VERIFIED",
        )
    gate = await production_gates.evaluate_gate(gate_id="PG-14")
    assert gate["pass"] is False
    assert gate["structural"]["checks"]["missing"] == ["XCP-008"]
    await production_gates.record_xcp_evidence(
        actor_id="admin",
        primitive_id="XCP-008",
        evidence_refs=["TEST-XCP-8"],
        status="VERIFIED",
    )
    gate = await production_gates.evaluate_gate(gate_id="PG-14")
    assert gate["pass"] is True


@pytest.mark.asyncio
async def test_v1_closed_false_while_evidence_only_p0_gates_open(gates_db):
    await architecture_reuse.sync_manifest(actor_id="admin")
    summary = await production_gates.evaluate_all(commit_sha="abcdef123456")
    assert summary["v1_closed"] is False
    assert "PG-09" in summary["p0_open"]
    assert "PG-10" in summary["p0_open"]
    assert "PG-12" in summary["p0_open"]
