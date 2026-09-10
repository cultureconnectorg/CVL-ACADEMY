from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import assurance_core, incident_core, legal_ops, professional_governance


@pytest.fixture
async def incident_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_incident_core_test"]
    for module in (assurance_core, incident_core, legal_ops, professional_governance):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


@pytest.mark.asyncio
async def test_incident_requires_evidence_and_valid_domains(incident_db):
    with pytest.raises(ValueError, match="requires evidence"):
        await incident_core.create_incident(
            actor_id="admin",
            title="Provider outage",
            description="External outage",
            severity="high",
            domains=["RISK"],
            evidence_refs=[],
        )
    with pytest.raises(ValueError, match="valid projection domains"):
        await incident_core.create_incident(
            actor_id="admin",
            title="Provider outage",
            description="External outage",
            severity="high",
            domains=["INVENTED"],
            evidence_refs=["OBS-1"],
        )


@pytest.mark.asyncio
async def test_one_incident_projects_to_privacy_security_legal_and_risk(incident_db):
    incident = await incident_core.create_incident(
        actor_id="admin",
        title="Learner data exposure",
        description="Identity data exposed by provider",
        severity="critical",
        domains=["PRIVACY", "SECURITY", "LEGAL", "RISK"],
        evidence_refs=["LOG-1"],
        data_classes=["IDENTITY"],
        asset_id="ASSET-API",
    )
    projected = await incident_core.project_incident(
        actor_id="admin",
        incident_id=incident["id"],
        security_remediation="Contain provider access",
        jurisdiction="FR",
        risk_impact=5,
        risk_probability=4,
        risk_owner="security",
        risk_mitigation="Contain and rotate credentials",
        risk_deadline="2026-09-11",
    )
    assert set(projected["projections"]) == {"PRIVACY", "SECURITY", "LEGAL", "RISK"}
    assert projected["projections"]["PRIVACY"]["canonical_incident_id"] == incident["id"]
    assert projected["projections"]["SECURITY"]["canonical_incident_id"] == incident["id"]
    assert projected["projections"]["LEGAL"]["case_id"] == incident["id"]
    assert projected["projections"]["RISK"]["source_id"] == incident["id"]
    stored = await incident_core.get_incident(incident["id"])
    assert set(stored["projections"]) == {"PRIVACY", "SECURITY", "LEGAL", "RISK"}


@pytest.mark.asyncio
async def test_projection_is_idempotent(incident_db):
    incident = await incident_core.create_incident(
        actor_id="admin",
        title="Security event",
        description="Credential misuse",
        severity="high",
        domains=["SECURITY"],
        evidence_refs=["LOG-2"],
    )
    first = await incident_core.project_incident(
        actor_id="admin",
        incident_id=incident["id"],
        security_remediation="Revoke credential",
    )
    second = await incident_core.project_incident(
        actor_id="admin",
        incident_id=incident["id"],
        security_remediation="Different text should not duplicate",
    )
    assert first["projections"]["SECURITY"]["id"] == second["projections"]["SECURITY"]["id"]
    assert await incident_db.security_findings.count_documents({}) == 1


@pytest.mark.asyncio
async def test_risk_projection_never_infers_score_from_severity(incident_db):
    incident = await incident_core.create_incident(
        actor_id="admin",
        title="Risk event",
        description="Needs explicit scoring",
        severity="critical",
        domains=["RISK"],
        evidence_refs=["LOG-3"],
    )
    with pytest.raises(ValueError, match="explicit impact and probability"):
        await incident_core.project_incident(actor_id="admin", incident_id=incident["id"])
    assert await incident_db.risks.count_documents({}) == 0


@pytest.mark.asyncio
async def test_resolution_and_close_require_evidence(incident_db):
    incident = await incident_core.create_incident(
        actor_id="admin",
        title="Contained event",
        description="Lifecycle proof",
        severity="medium",
        domains=["LEGAL"],
        evidence_refs=["LOG-4"],
    )
    contained = await incident_core.transition_incident(
        actor_id="admin", incident_id=incident["id"], status="CONTAINED", evidence_refs=[]
    )
    with pytest.raises(ValueError, match="resolved transition requires evidence"):
        await incident_core.transition_incident(
            actor_id="admin", incident_id=incident["id"], status="RESOLVED", evidence_refs=[]
        )
    resolved = await incident_core.transition_incident(
        actor_id="admin",
        incident_id=contained["id"],
        status="RESOLVED",
        evidence_refs=["FIX-1"],
    )
    closed = await incident_core.transition_incident(
        actor_id="admin",
        incident_id=resolved["id"],
        status="CLOSED",
        evidence_refs=["REVIEW-1"],
    )
    assert closed["status"] == "CLOSED"
