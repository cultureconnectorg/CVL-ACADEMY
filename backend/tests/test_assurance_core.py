from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import assurance_core as core


@pytest.fixture
async def assurance_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_assurance_test"]
    monkeypatch.setattr(core, "db", test_db)
    yield test_db
    client.close()


@pytest.mark.asyncio
async def test_legal_document_lifecycle_and_clause_impact(assurance_db):
    doc = await core.create_legal_document(
        actor_id="admin-1", title="Terms", document_type="terms", jurisdiction="FR"
    )
    assert doc["state"] == "DRAFT"
    reviewed = await core.transition_legal_document(
        actor_id="admin-1", document_id=doc["id"], state="REVIEW"
    )
    assert reviewed["state"] == "REVIEW"

    clause = await core.register_clause(
        actor_id="admin-1", code="PAY-01", title="Payment", text_hash="a" * 64, version=1
    )
    usage = await core.link_clause_usage(
        actor_id="admin-1", document_id=doc["id"], clause_id=clause["id"]
    )
    impact = await core.clause_impact(clause["id"])
    assert usage["document_id"] == doc["id"]
    assert impact == [usage]


@pytest.mark.asyncio
async def test_illegal_legal_document_transition_is_rejected(assurance_db):
    doc = await core.create_legal_document(
        actor_id="admin-1", title="Privacy policy", document_type="policy"
    )
    with pytest.raises(ValueError, match="invalid legal transition"):
        await core.transition_legal_document(
            actor_id="admin-1", document_id=doc["id"], state="PUBLISHED"
        )


@pytest.mark.asyncio
async def test_consent_registry_is_append_only_and_current_view_uses_latest(assurance_db):
    await core.record_consent(
        actor_id="user-1", user_id="user-1", purpose="marketing", policy_version="1", granted=True
    )
    await core.record_consent(
        actor_id="user-1", user_id="user-1", purpose="marketing", policy_version="1", granted=False
    )
    rows = await assurance_db.privacy_consents.find({"user_id": "user-1"}, {"_id": 0}).to_list(10)
    assert len(rows) == 2
    assert await core.current_consents("user-1") == {"marketing": False}
    assert all(len(row["evidence_hash"]) == 64 for row in rows)


@pytest.mark.asyncio
async def test_processing_activity_and_dsar_are_persisted(assurance_db):
    await core.register_data_class(
        actor_id="dpo-1", code="IDENTITY", name="Identity data",
        sensitivity="personal", retention_days=3650,
    )
    ropa = await core.register_processing_activity(
        actor_id="dpo-1", name="Account management", purpose="Provide learner account",
        data_classes=["IDENTITY"], legal_basis="contract", regions=["EU"],
    )
    dsar = await core.create_dsar(actor_id="user-1", user_id="user-1", request_type="export")
    assert ropa["legal_basis"] == "contract"
    assert dsar["status"] == "OPEN"


@pytest.mark.asyncio
async def test_security_release_gate_blocks_high_open_finding(assurance_db):
    asset = await core.create_security_asset(
        actor_id="sec-1", name="Academy API", asset_type="api", owner="academy",
        exposure="internet", criticality="high",
    )
    finding = await core.create_security_finding(
        actor_id="sec-1", title="IDOR", severity="high", asset_id=asset["id"],
        evidence_refs=["TEST-1"], remediation="Enforce ownership checks",
    )
    gate = await core.release_security_gate()
    assert gate["pass"] is False
    assert gate["blocking_count"] == 1

    await core.accept_security_risk(
        actor_id="founder-1", finding_id=finding["id"], rationale="Temporary exception",
        expires_at="2026-09-30T00:00:00+00:00",
    )
    gate = await core.release_security_gate()
    assert gate["pass"] is True


@pytest.mark.asyncio
async def test_risk_score_and_critical_gate_require_owner_mitigation_deadline_and_evidence(assurance_db):
    risk = await core.create_risk(
        actor_id="risk-1", title="Provider outage", domain="operations",
        impact=5, probability=4, control_effectiveness=0,
    )
    assert risk["level"] == 5
    gate = await core.critical_risk_gate()
    assert gate["pass"] is False
    assert gate["blocking_count"] == 1

    complete = await core.create_risk(
        actor_id="risk-1", title="Payment outage", domain="operations",
        impact=5, probability=4, control_effectiveness=0, owner="ops",
        mitigation="Fail closed and alert", deadline="2026-09-20",
        evidence_refs=["RUNBOOK-1"],
    )
    assert complete["level"] == 5
    gate = await core.critical_risk_gate()
    assert gate["blocking_count"] == 1


@pytest.mark.asyncio
async def test_privacy_incident_writes_audit_event(assurance_db):
    incident = await core.create_privacy_incident(
        actor_id="dpo-1", title="Accidental disclosure", severity="high",
        data_classes=["IDENTITY"], description="Test incident",
    )
    audit = await assurance_db.governance_audit_events.find_one(
        {"resource_id": incident["id"]}, {"_id": 0}
    )
    assert audit["event_type"] == "privacy.incident.created"
    assert len(audit["payload_hash"]) == 64
