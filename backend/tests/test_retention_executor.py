from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import assurance_core
from services import data_classification
from services import policy_registry
from services import privacy_ops
from services import professional_governance
from services import retention_executor


@pytest.fixture
async def retention_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_retention_executor_test"]
    for module in (
        assurance_core,
        data_classification,
        policy_registry,
        privacy_ops,
        professional_governance,
        retention_executor,
    ):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


async def _classified_resource():
    await assurance_core.register_data_class(
        actor_id="dpo",
        code="IDENTITY",
        name="Identity",
        sensitivity="sensitive",
        retention_days=30,
        legal_basis_required=True,
    )
    class_policy = await policy_registry.register_version(
        actor_id="founder",
        policy_key="DATA_CLASSIFICATION",
        version="1.0.0",
        kind="POLICY",
        title="Classification",
        content={"explicit": True},
        effective_at="2026-09-10T00:00:00+00:00",
        evidence_refs=["XCP-002"],
    )
    access_policy = await policy_registry.register_version(
        actor_id="founder",
        policy_key="DATA_ACCESS",
        version="1.0.0",
        kind="POLICY",
        title="Data access",
        content={"explicit": True},
        effective_at="2026-09-10T00:00:00+00:00",
        evidence_refs=["PRI-001"],
    )
    resource = await data_classification.declare_resource(
        actor_id="admin",
        resource_kind="DATA",
        resource_type="LEARNER_PROFILE",
        resource_id="USER-1",
        owner="academy",
        source="mongo",
    )
    await data_classification.classify_resource(
        actor_id="dpo",
        resource_record_id=resource["id"],
        data_class_code="IDENTITY",
        policy_version_id=class_policy["id"],
        access_policy_version_id=access_policy["id"],
        purpose="Retain learner identity data according to policy",
        legal_basis="CONTRACT",
        retention_days=30,
        processor_refs=[],
        locations=["EU"],
        rationale="Contains identity data",
        evidence_refs=["SCHEMA:users"],
    )
    return resource


async def _retention_policy():
    return await policy_registry.register_version(
        actor_id="founder",
        policy_key="RETENTION",
        version="1.0.0",
        kind="POLICY",
        title="Retention policy",
        content={"execution_requires_proof": True},
        effective_at="2026-09-10T00:00:00+00:00",
        evidence_refs=["XCP-003"],
    )


@pytest.mark.asyncio
async def test_unclassified_resource_cannot_be_scheduled(retention_db):
    policy = await _retention_policy()
    resource = await data_classification.declare_resource(
        actor_id="admin",
        resource_kind="DATA",
        resource_type="EVENT",
        resource_id="EV-1",
        owner="academy",
        source="mongo",
    )
    with pytest.raises(ValueError, match="explicitly classified"):
        await retention_executor.schedule_job(
            actor_id="admin",
            resource_record_id=resource["id"],
            trigger="ACCOUNT_CLOSED",
            trigger_at="2026-09-10T00:00:00+00:00",
            policy_version_id=policy["id"],
        )


@pytest.mark.asyncio
async def test_schedule_uses_classification_and_retention_rule(retention_db):
    resource = await _classified_resource()
    policy = await _retention_policy()
    rule = await privacy_ops.create_retention_rule(
        actor_id="dpo",
        data_class="IDENTITY",
        retention_days=30,
        trigger="ACCOUNT_CLOSED",
        action="ANONYMIZE",
        evidence_refs=["RET-DECISION-1"],
    )
    job = await retention_executor.schedule_job(
        actor_id="admin",
        resource_record_id=resource["id"],
        trigger="ACCOUNT_CLOSED",
        trigger_at="2026-09-10T00:00:00+00:00",
        policy_version_id=policy["id"],
    )
    assert job["rule_id"] == rule["id"]
    assert job["action"] == "ANONYMIZE"
    assert job["due_at"].startswith("2026-10-10T00:00:00")
    assert job["status"] == "SCHEDULED"


@pytest.mark.asyncio
async def test_legal_hold_blocks_execution_until_evidence_backed_release(retention_db):
    resource = await _classified_resource()
    policy = await _retention_policy()
    await privacy_ops.create_retention_rule(
        actor_id="dpo",
        data_class="IDENTITY",
        retention_days=0,
        trigger="CASE_CLOSED",
        action="DELETE",
        evidence_refs=["RET-DECISION-1"],
    )
    hold = await retention_executor.create_legal_hold(
        actor_id="legal",
        resource_record_id=resource["id"],
        reason="Litigation preservation",
        evidence_refs=["LEGAL-MATTER-1"],
    )
    job = await retention_executor.schedule_job(
        actor_id="admin",
        resource_record_id=resource["id"],
        trigger="CASE_CLOSED",
        trigger_at="2026-09-10T00:00:00+00:00",
        policy_version_id=policy["id"],
    )
    assert job["status"] == "BLOCKED_HOLD"
    with pytest.raises(ValueError, match="blocked by legal hold"):
        await retention_executor.record_execution(
            actor_id="worker",
            job_id=job["id"],
            adapter="mongo-users-v1",
            evidence_ref="DELETE-RECEIPT-1",
            outcome="SUCCESS",
        )
    with pytest.raises(ValueError, match="release requires evidence"):
        await retention_executor.release_legal_hold(
            actor_id="legal", hold_id=hold["id"], evidence_refs=[]
        )
    await retention_executor.release_legal_hold(
        actor_id="legal", hold_id=hold["id"], evidence_refs=["COURT-RELEASE-1"]
    )
    refreshed = await retention_executor.refresh_job(job["id"])
    assert refreshed["status"] == "SCHEDULED"


@pytest.mark.asyncio
async def test_destructive_completion_requires_adapter_receipt(retention_db):
    resource = await _classified_resource()
    policy = await _retention_policy()
    await privacy_ops.create_retention_rule(
        actor_id="dpo",
        data_class="IDENTITY",
        retention_days=0,
        trigger="ACCOUNT_CLOSED",
        action="DELETE",
        evidence_refs=["RET-DECISION-1"],
    )
    job = await retention_executor.schedule_job(
        actor_id="admin",
        resource_record_id=resource["id"],
        trigger="ACCOUNT_CLOSED",
        trigger_at="2026-09-10T00:00:00+00:00",
        policy_version_id=policy["id"],
    )
    with pytest.raises(ValueError, match="adapter and evidence_ref"):
        await retention_executor.record_execution(
            actor_id="worker",
            job_id=job["id"],
            adapter="",
            evidence_ref="",
            outcome="SUCCESS",
        )
    completed = await retention_executor.record_execution(
        actor_id="worker",
        job_id=job["id"],
        adapter="mongo-users-v1",
        evidence_ref="ERASURE-PROOF-1",
        outcome="SUCCESS",
        details={"matched": 1, "modified": 1},
    )
    assert completed["status"] == "VERIFIED_EXECUTED"
    assert completed["execution"]["evidence_ref"] == "ERASURE-PROOF-1"


@pytest.mark.asyncio
async def test_wrong_policy_is_rejected(retention_db):
    resource = await _classified_resource()
    await privacy_ops.create_retention_rule(
        actor_id="dpo",
        data_class="IDENTITY",
        retention_days=30,
        trigger="ACCOUNT_CLOSED",
        action="DELETE",
        evidence_refs=["RET-DECISION-1"],
    )
    wrong = await policy_registry.register_version(
        actor_id="founder",
        policy_key="QUALITY",
        version="1.0.0",
        kind="POLICY",
        title="Quality",
        content={"x": True},
        effective_at="2026-09-10T00:00:00+00:00",
        evidence_refs=["QLT"],
    )
    with pytest.raises(ValueError, match="not a RETENTION policy"):
        await retention_executor.schedule_job(
            actor_id="admin",
            resource_record_id=resource["id"],
            trigger="ACCOUNT_CLOSED",
            trigger_at="2026-09-10T00:00:00+00:00",
            policy_version_id=wrong["id"],
        )
