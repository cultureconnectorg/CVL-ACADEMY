from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import assurance_core
from services import risk_ops


@pytest.fixture
async def risk_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_risk_ops_test"]
    monkeypatch.setattr(risk_ops, "db", test_db)
    monkeypatch.setattr(assurance_core, "db", test_db)
    yield test_db
    client.close()


@pytest.mark.asyncio
async def test_incident_cascade_creates_one_linked_risk_and_is_idempotent(risk_db):
    first = await risk_ops.cascade_incident_to_risk(
        actor_id="admin-1",
        incident_type="privacy_incident",
        incident_id="PI-001",
        title="Identity disclosure",
        domain="privacy",
        impact=5,
        probability=4,
        owner="dpo",
        mitigation="Contain and notify",
        deadline="2026-09-11",
        evidence_refs=["EVID-1"],
    )
    second = await risk_ops.cascade_incident_to_risk(
        actor_id="admin-2",
        incident_type="privacy_incident",
        incident_id="PI-001",
        title="Should not duplicate",
        domain="privacy",
        impact=1,
        probability=1,
    )

    assert first["id"] == second["id"]
    assert first["source_type"] == "PRIVACY_INCIDENT"
    assert first["source_id"] == "PI-001"
    assert "PI-001" in first["evidence_refs"]
    assert "EVID-1" in first["evidence_refs"]
    assert await risk_db.risks.count_documents({"source_id": "PI-001"}) == 1


@pytest.mark.asyncio
async def test_critical_risk_auto_creates_single_open_insurance_review(risk_db):
    risk = await assurance_core.create_risk(
        actor_id="risk-1",
        title="Critical provider failure",
        domain="operations",
        impact=5,
        probability=4,
        owner="ops",
        mitigation="Fail closed",
        deadline="2026-09-15",
        evidence_refs=["RUNBOOK-1"],
    )
    assert risk["level"] >= 4

    first = await risk_ops.auto_insurance_review_for_critical_risk(
        actor_id="admin-1", risk_id=risk["id"]
    )
    second = await risk_ops.auto_insurance_review_for_critical_risk(
        actor_id="admin-2", risk_id=risk["id"]
    )

    assert first is not None
    assert first["id"] == second["id"]
    assert first["coverage_confirmed"] is False
    assert first["status"] == "OPEN"
    assert await risk_db.insurance_review_triggers.count_documents(
        {"risk_id": risk["id"]}
    ) == 1


@pytest.mark.asyncio
async def test_noncritical_risk_does_not_fabricate_insurance_review(risk_db):
    risk = await assurance_core.create_risk(
        actor_id="risk-1",
        title="Minor scheduling issue",
        domain="operations",
        impact=1,
        probability=1,
        owner="ops",
        mitigation="Reschedule",
        deadline="2026-09-15",
        evidence_refs=["OPS-1"],
    )

    result = await risk_ops.auto_insurance_review_for_critical_risk(
        actor_id="admin-1", risk_id=risk["id"]
    )

    assert result is None
    assert await risk_db.insurance_review_triggers.count_documents({}) == 0


@pytest.mark.asyncio
async def test_coverage_confirmation_requires_external_evidence(risk_db):
    risk = await assurance_core.create_risk(
        actor_id="risk-1",
        title="Critical liability risk",
        domain="liability",
        impact=5,
        probability=5,
        owner="legal",
        mitigation="Transfer and contract controls",
        deadline="2026-09-15",
        evidence_refs=["LEGAL-1"],
    )
    trigger = await risk_ops.create_insurance_review_trigger(
        actor_id="admin-1",
        risk_id=risk["id"],
        reason="Coverage review required",
        coverage_types=["professional_liability"],
    )

    with pytest.raises(ValueError, match="without evidence"):
        await risk_ops.record_insurance_review(
            actor_id="admin-1",
            trigger_id=trigger["id"],
            coverage_confirmed=True,
            evidence_refs=[],
        )

    stored = await risk_db.insurance_review_triggers.find_one(
        {"id": trigger["id"]}, {"_id": 0}
    )
    assert stored["coverage_confirmed"] is False
    assert stored["status"] == "OPEN"


@pytest.mark.asyncio
async def test_review_can_close_with_evidence_without_claiming_coverage(risk_db):
    risk = await assurance_core.create_risk(
        actor_id="risk-1",
        title="Cyber transfer review",
        domain="cyber",
        impact=5,
        probability=4,
        owner="security",
        mitigation="Review cyber policy",
        deadline="2026-09-15",
        evidence_refs=["SEC-1"],
    )
    trigger = await risk_ops.create_insurance_review_trigger(
        actor_id="admin-1",
        risk_id=risk["id"],
        reason="Policy review",
        coverage_types=["cyber"],
    )

    reviewed = await risk_ops.record_insurance_review(
        actor_id="admin-1",
        trigger_id=trigger["id"],
        coverage_confirmed=False,
        evidence_refs=["BROKER-RESPONSE-1"],
        notes="Provider confirms no current coverage.",
    )

    assert reviewed["status"] == "CLOSED"
    assert reviewed["coverage_confirmed"] is False
    assert reviewed["evidence_refs"] == ["BROKER-RESPONSE-1"]
