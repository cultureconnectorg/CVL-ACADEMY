from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import incident_core, professional_governance, security_incident_protocol


@pytest.fixture
async def security_protocol_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_security_incident_protocol_test"]
    for module in (incident_core, professional_governance, security_incident_protocol):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


async def _security_incident():
    return await incident_core.create_incident(
        actor_id="sec-1",
        title="Credential abuse",
        description="Observed credential abuse against Academy",
        severity="HIGH",
        domains=["SECURITY"],
        evidence_refs=["LOG-1"],
        asset_id="API-1",
    )


@pytest.mark.asyncio
async def test_security_incident_sev_classification_preserves_canonical_severity(
    security_protocol_db,
):
    incident = await _security_incident()
    classification = await security_incident_protocol.classify_security_incident(
        actor_id="sec-1",
        incident_id=incident["id"],
        sev_level="SEV-2",
        rationale="Material security incident requiring coordinated response",
        evidence_refs=["TRIAGE-1"],
    )
    stored = await security_protocol_db.incidents.find_one(
        {"id": incident["id"]}, {"_id": 0}
    )
    assert classification["sev_level"] == "SEV-2"
    assert classification["ordinal"] == 2
    assert classification["canonical_severity"] == "HIGH"
    assert stored["severity"] == "HIGH"
    assert stored["metadata"]["security_sev_classification_id"] == classification["id"]


@pytest.mark.asyncio
async def test_security_classification_supersedes_without_hidden_severity_conversion(
    security_protocol_db,
):
    incident = await _security_incident()
    first = await security_incident_protocol.classify_security_incident(
        actor_id="sec-1",
        incident_id=incident["id"],
        sev_level="SEV-3",
        rationale="Initial evidence-based triage",
        evidence_refs=["TRIAGE-1"],
    )
    second = await security_incident_protocol.classify_security_incident(
        actor_id="sec-lead",
        incident_id=incident["id"],
        sev_level="SEV-1",
        rationale="New evidence establishes highest internal severity",
        evidence_refs=["TRIAGE-2"],
    )
    previous = await security_protocol_db.security_incident_classifications.find_one(
        {"id": first["id"]}, {"_id": 0}
    )
    stored_incident = await security_protocol_db.incidents.find_one(
        {"id": incident["id"]}, {"_id": 0}
    )
    assert previous["status"] == "SUPERSEDED"
    assert previous["superseded_by"] == second["id"]
    assert second["supersedes_classification_id"] == first["id"]
    assert stored_incident["severity"] == "HIGH"


@pytest.mark.asyncio
async def test_non_security_incident_cannot_receive_security_sev(
    security_protocol_db,
):
    incident = await incident_core.create_incident(
        actor_id="privacy-1",
        title="Data correction",
        description="Privacy-only incident",
        severity="MEDIUM",
        domains=["PRIVACY"],
        evidence_refs=["PRIV-1"],
    )
    with pytest.raises(ValueError, match="not scoped to SECURITY"):
        await security_incident_protocol.classify_security_incident(
            actor_id="sec-1",
            incident_id=incident["id"],
            sev_level="SEV-2",
            rationale="Invalid cross-domain classification",
            evidence_refs=["TRIAGE"],
        )


@pytest.mark.asyncio
async def test_disclosure_requires_evidence_and_never_exposes_source_code(
    security_protocol_db,
):
    with pytest.raises(ValueError, match="disclosure requires"):
        await security_incident_protocol.record_vulnerability_disclosure(
            actor_id="sec-1",
            summary="Potential IDOR",
            reporter_ref="REPORTER-1",
            channel="security-email",
            evidence_refs=[],
        )

    disclosure = await security_incident_protocol.record_vulnerability_disclosure(
        actor_id="sec-1",
        summary="Potential IDOR",
        reporter_ref="REPORTER-1",
        channel="security-email",
        evidence_refs=["REPORT-1"],
    )
    assert disclosure["status"] == "RECEIVED"
    assert disclosure["source_code_exposed"] is False


@pytest.mark.asyncio
async def test_accepted_disclosure_must_link_to_finding_or_canonical_incident(
    security_protocol_db,
):
    disclosure = await security_incident_protocol.record_vulnerability_disclosure(
        actor_id="sec-1",
        summary="Potential SSRF",
        reporter_ref="REPORTER-2",
        channel="security-email",
        evidence_refs=["REPORT-2"],
    )
    with pytest.raises(ValueError, match="must link to a finding or canonical incident"):
        await security_incident_protocol.transition_vulnerability_disclosure(
            actor_id="sec-1",
            disclosure_id=disclosure["id"],
            status="ACCEPTED",
            rationale="Confirmed as valid",
            evidence_refs=["TRIAGE-2"],
        )

    await security_protocol_db.security_findings.insert_one(
        {"id": "FIND-SSRF-1", "severity": "HIGH", "status": "OPEN"}
    )
    accepted = await security_incident_protocol.transition_vulnerability_disclosure(
        actor_id="sec-1",
        disclosure_id=disclosure["id"],
        status="ACCEPTED",
        rationale="Confirmed and converted to tracked finding",
        evidence_refs=["TRIAGE-3"],
        finding_id="FIND-SSRF-1",
    )
    assert accepted["status"] == "ACCEPTED"
    assert accepted["finding_id"] == "FIND-SSRF-1"
