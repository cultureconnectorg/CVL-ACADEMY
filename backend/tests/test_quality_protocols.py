from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import critical_proof, policy_registry, professional_governance, quality_protocols


@pytest.fixture
async def quality_protocol_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_quality_protocol_test"]
    for module in (quality_protocols, critical_proof, policy_registry, professional_governance):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


@pytest.mark.asyncio
async def test_improvement_action_requires_evidence_for_each_transition(quality_protocol_db):
    await quality_protocol_db.quality_improvement_actions.insert_one(
        {"id": "QACT-1", "status": "OPEN", "title": "Fix learner feedback loop"}
    )
    with pytest.raises(ValueError, match="outcome and evidence"):
        await quality_protocols.record_improvement_evidence(
            actor_id="quality", action_id="QACT-1", status="IN_PROGRESS",
            outcome="Started", evidence_refs=[]
        )
    row = await quality_protocols.record_improvement_evidence(
        actor_id="quality", action_id="QACT-1", status="IN_PROGRESS",
        outcome="Action assigned and work started", evidence_refs=["TASK-1"]
    )
    row = await quality_protocols.record_improvement_evidence(
        actor_id="quality", action_id=row["id"], status="VERIFIED",
        outcome="Retest passed", evidence_refs=["RETEST-1"]
    )
    row = await quality_protocols.record_improvement_evidence(
        actor_id="quality", action_id=row["id"], status="CLOSED",
        outcome="Evidence reviewed", evidence_refs=["REVIEW-1"]
    )
    assert row["status"] == "CLOSED"
    stored = await quality_protocol_db.quality_improvement_actions.find_one({"id": "QACT-1"}, {"_id": 0})
    assert len(stored["evidence_history"]) == 3


@pytest.mark.asyncio
async def test_quality_frek_proof_reuses_critical_proof_service(
    quality_protocol_db, monkeypatch
):
    await quality_protocol_db.quality_improvement_actions.insert_one(
        {"id": "QACT-1", "status": "VERIFIED", "title": "Improvement"}
    )
    calls = []

    async def fake_create(**kwargs):
        calls.append(kwargs)
        return {"id": "CRITPROOF-1", "domain": kwargs["domain"], "legal_effect": "none"}

    monkeypatch.setattr(critical_proof, "create_critical_decision_proof", fake_create)
    result = await quality_protocols.create_quality_frek_proof(
        actor_id="quality", resource_type="QUALITY_IMPROVEMENT_ACTION",
        resource_id="QACT-1", authority_decision_id="AUTH-1",
        policy_version_id="POL-1", evidence_refs=["QUALITY-REVIEW-1"]
    )
    assert result["id"] == "CRITPROOF-1"
    assert calls[0]["domain"] == "QUALITY"
    assert len(calls[0]["resource_hash"]) == 64
