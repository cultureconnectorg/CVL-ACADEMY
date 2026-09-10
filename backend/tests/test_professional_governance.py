from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import professional_governance as gov


@pytest.fixture
async def governance_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_governance_test"]
    monkeypatch.setattr(gov, "db", test_db)
    yield test_db
    client.close()


@pytest.mark.asyncio
async def test_case_decision_and_audit_are_persisted(governance_db):
    case = await gov.create_case(
        actor_id="founder-1",
        title="Legal review",
        domain="legal",
        description="Review a professional agreement.",
    )
    assert case["status"] == "OPEN"
    assert case["domain"] == "LEGAL"

    decision = await gov.create_decision(
        actor_id="founder-1",
        case_id=case["id"],
        subject="Approve review scope",
        rationale="Scope is bounded and evidence-backed.",
        evidence_refs=["DOCV-1"],
    )
    assert decision["state"] == "PROPOSED"
    assert len(decision["decision_hash"]) == 64

    approved = await gov.transition_decision(
        actor_id="founder-1", decision_id=decision["id"], state="APPROVED"
    )
    assert approved["state"] == "APPROVED"

    events = await governance_db.governance_audit_events.find(
        {}, {"_id": 0}
    ).to_list(20)
    event_types = {event["event_type"] for event in events}
    assert "governance.case.created" in event_types
    assert "governance.decision.created" in event_types
    assert "governance.decision.state_changed" in event_types
    assert all(len(event["payload_hash"]) == 64 for event in events)


@pytest.mark.asyncio
async def test_terminal_decision_cannot_be_mutated(governance_db):
    case = await gov.create_case(
        actor_id="admin-1",
        title="Quality case",
        domain="quality",
        description="Quality assurance review",
    )
    decision = await gov.create_decision(
        actor_id="admin-1",
        case_id=case["id"],
        subject="Release gate",
        rationale="Evidence complete",
    )
    await gov.transition_decision(
        actor_id="admin-1", decision_id=decision["id"], state="APPROVED"
    )
    with pytest.raises(ValueError, match="terminal decision"):
        await gov.transition_decision(
            actor_id="admin-1", decision_id=decision["id"], state="REJECTED"
        )


@pytest.mark.asyncio
async def test_expert_assignment_is_case_scoped(governance_db):
    case = await gov.create_case(
        actor_id="founder-1",
        title="Privacy review",
        domain="privacy",
        description="Privacy assessment",
    )
    expert = await gov.create_expert(
        actor_id="founder-1",
        display_name="External Reviewer",
        email="reviewer@example.com",
        domains=["privacy"],
    )
    assignment = await gov.assign_expert(
        actor_id="founder-1",
        case_id=case["id"],
        expert_id=expert["id"],
        scope=["documents:read", "decisions:propose"],
    )
    assert assignment["case_id"] == case["id"]
    assert assignment["expert_id"] == expert["id"]
    assert assignment["scope"] == ["decisions:propose", "documents:read"]


@pytest.mark.asyncio
async def test_document_versions_are_append_only(governance_db):
    case = await gov.create_case(
        actor_id="admin-1",
        title="Policy",
        domain="legal",
        description="Versioned policy",
    )
    v1 = await gov.register_document_version(
        actor_id="admin-1",
        case_id=case["id"],
        document_type="policy",
        title="Policy v1",
        content_hash="a" * 64,
    )
    v2 = await gov.register_document_version(
        actor_id="admin-1",
        case_id=case["id"],
        document_type="policy",
        title="Policy v2",
        content_hash="b" * 64,
        parent_version_id=v1["id"],
    )

    rows = await governance_db.governance_document_versions.find(
        {"case_id": case["id"]}, {"_id": 0}
    ).to_list(10)
    assert len(rows) == 2
    assert v2["parent_version_id"] == v1["id"]
