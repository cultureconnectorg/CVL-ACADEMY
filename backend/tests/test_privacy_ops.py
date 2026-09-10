from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import assurance_core, privacy_ops


@pytest.fixture
async def privacy_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_privacy_ops_test"]
    monkeypatch.setattr(privacy_ops, "db", test_db)
    monkeypatch.setattr(assurance_core, "db", test_db)
    yield test_db
    client.close()


@pytest.mark.asyncio
async def test_retention_rule_is_upserted_by_data_class_and_trigger(privacy_db):
    first = await privacy_ops.create_retention_rule(
        actor_id="dpo-1",
        data_class="identity",
        retention_days=3650,
        trigger="account_closed",
        action="anonymize",
    )
    second = await privacy_ops.create_retention_rule(
        actor_id="dpo-1",
        data_class="identity",
        retention_days=1825,
        trigger="account_closed",
        action="review",
    )
    rows = await privacy_db.privacy_retention_rules.find({}, {"_id": 0}).to_list(10)
    assert len(rows) == 1
    assert first["data_class"] == "IDENTITY"
    assert second["retention_days"] == 1825
    assert rows[0]["action"] == "REVIEW"


@pytest.mark.asyncio
async def test_processor_cannot_be_approved_without_dpa_evidence(privacy_db):
    processor = await privacy_ops.register_processor(
        actor_id="dpo-1",
        name="Vendor",
        service="email",
        data_classes=["IDENTITY"],
        regions=["EU"],
    )
    with pytest.raises(ValueError, match="DPA evidence"):
        await privacy_ops.transition_processor(
            actor_id="dpo-1", processor_id=processor["id"], status="APPROVED"
        )

    evidenced = await privacy_ops.register_processor(
        actor_id="dpo-1",
        name="Vendor 2",
        service="storage",
        data_classes=["LEARNING"],
        regions=["EU"],
        dpa_evidence_ref="DPA-1",
    )
    approved = await privacy_ops.transition_processor(
        actor_id="dpo-1", processor_id=evidenced["id"], status="APPROVED"
    )
    assert approved["status"] == "APPROVED"


@pytest.mark.asyncio
async def test_deletion_workflow_requires_impact_and_execution_evidence(privacy_db):
    request = await privacy_ops.create_deletion_request(
        actor_id="user-1", user_id="user-1", reason="account closure"
    )
    request = await privacy_ops.transition_deletion_request(
        actor_id="admin-1", request_id=request["id"], status="IDENTITY_VERIFIED"
    )
    with pytest.raises(ValueError, match="impact assessment"):
        await privacy_ops.transition_deletion_request(
            actor_id="admin-1", request_id=request["id"], status="IMPACT_ASSESSED"
        )
    request = await privacy_ops.transition_deletion_request(
        actor_id="admin-1",
        request_id=request["id"],
        status="IMPACT_ASSESSED",
        impact={"legal_hold": False, "resources": ["profile"]},
    )
    request = await privacy_ops.transition_deletion_request(
        actor_id="admin-1", request_id=request["id"], status="APPROVED"
    )
    request = await privacy_ops.transition_deletion_request(
        actor_id="admin-1", request_id=request["id"], status="EXECUTING"
    )
    entry = await privacy_ops.record_deletion_execution(
        actor_id="admin-1",
        request_id=request["id"],
        resource_type="profile",
        action="anonymize",
        evidence_ref="ERASURE-1",
    )
    assert entry["evidence_ref"] == "ERASURE-1"


@pytest.mark.asyncio
async def test_privacy_incident_cascade_is_idempotent(privacy_db):
    incident = await assurance_core.create_privacy_incident(
        actor_id="dpo-1",
        title="Disclosure",
        severity="high",
        data_classes=["IDENTITY"],
        description="Disclosure test",
    )
    first = await privacy_ops.cascade_privacy_incident_to_risk(
        actor_id="risk-1",
        incident_id=incident["id"],
        impact=5,
        probability=3,
        owner="dpo",
        mitigation="Contain and notify",
        deadline="2026-09-11",
        evidence_refs=["IR-1"],
    )
    second = await privacy_ops.cascade_privacy_incident_to_risk(
        actor_id="risk-1",
        incident_id=incident["id"],
        impact=5,
        probability=3,
    )
    assert first["id"] == second["id"]
    assert first["source_type"] == "PRIVACY_INCIDENT"
