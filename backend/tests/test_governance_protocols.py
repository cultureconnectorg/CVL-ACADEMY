from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import authority_policy, governance_protocols, professional_governance


@pytest.fixture
async def governance_protocol_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_governance_protocol_test"]
    for module in (authority_policy, governance_protocols, professional_governance):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


@pytest.mark.asyncio
async def test_escalation_requires_canonical_source(governance_protocol_db):
    with pytest.raises(LookupError, match="source not found"):
        await governance_protocols.create_escalation(
            actor_id="founder",
            source_type="RISK",
            source_id="RISK-MISSING",
            domain="LEGAL",
            severity="HIGH",
            target_authority_level="A4_CVL",
            reason="Escalate unresolved legal exposure",
            evidence_refs=["E-1"],
        )


@pytest.mark.asyncio
async def test_high_escalation_blocks_until_authorised_and_resolved(
    governance_protocol_db,
):
    await governance_protocol_db.risks.insert_one(
        {"id": "RISK-1", "level": 4, "domain": "LEGAL"}
    )
    row = await governance_protocols.create_escalation(
        actor_id="risk-owner",
        source_type="RISK",
        source_id="RISK-1",
        domain="LEGAL",
        severity="HIGH",
        target_authority_level="A4_CVL",
        reason="Requires CVL authority review",
        evidence_refs=["RISK-EVID-1"],
    )
    assert (await governance_protocols.escalation_gate(domain="LEGAL"))["pass"] is False

    await governance_protocol_db.authority_decisions.insert_one(
        {
            "id": "AUTH-1",
            "decision": "ALLOW",
            "action": "GOVERNANCE_ESCALATION_ACKNOWLEDGE",
            "decision_hash": "a" * 64,
            "context": {
                "escalation_id": row["id"],
                "domain": "LEGAL",
                "authority_level": "A4_CVL",
            },
        }
    )
    acknowledged = await governance_protocols.acknowledge_escalation(
        actor_id="founder",
        escalation_id=row["id"],
        authority_decision_id="AUTH-1",
        evidence_refs=["AUTH-EVID-1"],
    )
    assert acknowledged["status"] == "ACKNOWLEDGED"
    assert acknowledged["authority_decision_id"] == "AUTH-1"

    resolved = await governance_protocols.close_escalation(
        actor_id="founder",
        escalation_id=row["id"],
        status="RESOLVED",
        resolution="Risk treatment approved and assigned",
        evidence_refs=["RESOLUTION-1"],
    )
    assert resolved["status"] == "RESOLVED"
    assert (await governance_protocols.escalation_gate(domain="LEGAL"))["pass"] is True


@pytest.mark.asyncio
async def test_authority_decision_must_be_bound_to_exact_escalation(
    governance_protocol_db,
):
    await governance_protocol_db.incidents.insert_one(
        {"id": "INC-1", "domains": ["SECURITY"]}
    )
    row = await governance_protocols.create_escalation(
        actor_id="security",
        source_type="INCIDENT",
        source_id="INC-1",
        domain="SECURITY",
        severity="CRITICAL",
        target_authority_level="A4_CVL",
        reason="Critical incident",
        evidence_refs=["INC-EVID-1"],
    )
    await governance_protocol_db.authority_decisions.insert_one(
        {
            "id": "AUTH-WRONG",
            "decision": "ALLOW",
            "action": "GOVERNANCE_ESCALATION_ACKNOWLEDGE",
            "context": {
                "escalation_id": "ESC-OTHER",
                "domain": "SECURITY",
                "authority_level": "A4_CVL",
            },
        }
    )
    with pytest.raises(ValueError, match="not bound"):
        await governance_protocols.acknowledge_escalation(
            actor_id="founder",
            escalation_id=row["id"],
            authority_decision_id="AUTH-WRONG",
            evidence_refs=["E-ACK"],
        )
