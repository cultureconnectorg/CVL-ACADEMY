from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import assurance_core
from services import data_classification
from services import policy_registry
from services import privacy_ops
from services import professional_governance
from services import retention_executor


@pytest.fixture
async def retention_runtime_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_retention_runtime_test"]
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


def _instant(delta: timedelta) -> str:
    return (datetime.now(timezone.utc) + delta).isoformat()


async def _setup_job(*, trigger_at: str, action: str = "DELETE"):
    await assurance_core.register_data_class(
        actor_id="dpo",
        code="IDENTITY",
        name="Identity",
        sensitivity="sensitive",
        retention_days=0,
        legal_basis_required=True,
    )
    class_policy = await policy_registry.register_version(
        actor_id="founder",
        policy_key="DATA_CLASSIFICATION",
        version="1.0.0",
        kind="POLICY",
        title="Classification",
        content={"explicit": True},
        effective_at=_instant(timedelta(hours=-2)),
        evidence_refs=["XCP-002"],
    )
    access_policy = await policy_registry.register_version(
        actor_id="founder",
        policy_key="DATA_ACCESS",
        version="1.0.0",
        kind="POLICY",
        title="Data access",
        content={"explicit": True},
        effective_at=_instant(timedelta(hours=-2)),
        evidence_refs=["PRI-001"],
    )
    retention_policy = await policy_registry.register_version(
        actor_id="founder",
        policy_key="RETENTION",
        version="1.0.0",
        kind="POLICY",
        title="Retention",
        content={"execution_requires_proof": True},
        effective_at=_instant(timedelta(hours=-2)),
        evidence_refs=["XCP-003"],
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
        purpose="Execute evidence-backed learner retention policy",
        legal_basis="CONTRACT",
        retention_days=0,
        processor_refs=[],
        locations=["EU"],
        rationale="Identity data",
        evidence_refs=["SCHEMA:users"],
    )
    await privacy_ops.create_retention_rule(
        actor_id="dpo",
        data_class="IDENTITY",
        retention_days=0,
        trigger="ACCOUNT_CLOSED",
        action=action,
        evidence_refs=["RET-POLICY"],
    )
    job = await retention_executor.schedule_job(
        actor_id="admin",
        resource_record_id=resource["id"],
        trigger="ACCOUNT_CLOSED",
        trigger_at=trigger_at,
        policy_version_id=retention_policy["id"],
    )
    return resource, job


@pytest.mark.asyncio
async def test_future_job_cannot_begin_or_fake_completion(retention_runtime_db):
    _resource, job = await _setup_job(trigger_at=_instant(timedelta(days=2)))
    preview = await retention_executor.dry_run_job(job["id"])
    assert preview["dry_run"] is True
    assert preview["due"] is False
    assert preview["executable"] is False

    with pytest.raises(ValueError, match="not due yet"):
        await retention_executor.begin_execution(actor_id="worker", job_id=job["id"])

    with pytest.raises(ValueError, match="not due yet"):
        await retention_executor.record_execution(
            actor_id="worker",
            job_id=job["id"],
            adapter="mongo-users-v1",
            evidence_ref="IMPOSSIBLE-EARLY-PROOF",
            outcome="SUCCESS",
        )


@pytest.mark.asyncio
async def test_failed_job_requires_evidence_for_retry(retention_runtime_db):
    _resource, job = await _setup_job(trigger_at=_instant(timedelta(days=-1)))
    failed = await retention_executor.record_execution(
        actor_id="worker",
        job_id=job["id"],
        adapter="mongo-users-v1",
        evidence_ref="FAIL-RECEIPT-1",
        outcome="FAILED",
        details={"error": "transient"},
    )
    assert failed["status"] == "EXECUTION_FAILED"

    with pytest.raises(ValueError, match="retry requires evidence"):
        await retention_executor.retry_failed_job(
            actor_id="dpo", job_id=job["id"], evidence_refs=[]
        )

    retried = await retention_executor.retry_failed_job(
        actor_id="dpo",
        job_id=job["id"],
        evidence_refs=["RETRY-DECISION-1"],
    )
    assert retried["status"] == "SCHEDULED"
    assert retried["retry_count"] == 1

    completed = await retention_executor.record_execution(
        actor_id="worker",
        job_id=job["id"],
        adapter="mongo-users-v1",
        evidence_ref="SUCCESS-RECEIPT-2",
        outcome="SUCCESS",
    )
    assert completed["status"] == "VERIFIED_EXECUTED"
    assert completed["execution"]["attempt_number"] == 2


@pytest.mark.asyncio
async def test_replay_preserves_verified_original(retention_runtime_db):
    _resource, job = await _setup_job(trigger_at=_instant(timedelta(days=-1)))
    original = await retention_executor.record_execution(
        actor_id="worker",
        job_id=job["id"],
        adapter="mongo-users-v1",
        evidence_ref="ERASURE-PROOF-1",
        outcome="SUCCESS",
    )
    assert original["status"] == "VERIFIED_EXECUTED"

    with pytest.raises(ValueError, match="replay requires reason and evidence"):
        await retention_executor.replay_verified_job(
            actor_id="dpo",
            job_id=job["id"],
            reason="",
            evidence_refs=[],
        )

    replay = await retention_executor.replay_verified_job(
        actor_id="dpo",
        job_id=job["id"],
        reason="Source was restored from backup and must be processed again",
        evidence_refs=["RESTORE-EVENT-1"],
    )
    assert replay["id"] != job["id"]
    assert replay["replay_of_job_id"] == job["id"]
    assert replay["status"] == "SCHEDULED"

    stored_original = await retention_runtime_db.retention_jobs.find_one(
        {"id": job["id"]}, {"_id": 0}
    )
    assert stored_original["status"] == "VERIFIED_EXECUTED"


@pytest.mark.asyncio
async def test_due_worker_view_excludes_held_jobs(retention_runtime_db):
    resource, job = await _setup_job(trigger_at=_instant(timedelta(days=-1)))
    await retention_executor.create_legal_hold(
        actor_id="legal",
        resource_record_id=resource["id"],
        reason="Litigation hold",
        evidence_refs=["LEGAL-CASE-1"],
    )
    due = await retention_executor.list_due_jobs()
    assert all(row["id"] != job["id"] for row in due)
    refreshed = await retention_executor.refresh_job(job["id"])
    assert refreshed["status"] == "BLOCKED_HOLD"
