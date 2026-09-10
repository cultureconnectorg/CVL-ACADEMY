from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import authority_policy, professional_governance


@pytest.fixture
async def authority_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_authority_policy_test"]
    monkeypatch.setattr(authority_policy, "db", test_db)
    monkeypatch.setattr(professional_governance, "db", test_db)
    yield test_db
    client.close()


async def _policy(authority_db):
    return await authority_policy.register_policy_version(
        actor_id="founder-1",
        policy_key="LEGAL_REVIEW_AUTHORITY",
        version="1.0.0",
        title="Legal review authority",
        effective_at="2026-09-10T00:00:00+00:00",
        doctrine_ref="GOV-14",
        evidence_refs=["MASTER:GOV-14", "XCP-001"],
        rules=[
            {
                "id": "LEGAL-A4",
                "priority": 10,
                "effect": "ALLOW",
                "reason": "CVL authority may approve a legal review in the scoped context.",
                "conditions": {
                    "actor_roles": ["founder", "super_admin"],
                    "actions": ["LEGAL_REVIEW_APPROVE"],
                    "domains": ["LEGAL"],
                    "minimum_authority_level": "A4_CVL_AUTHORITY",
                },
            },
            {
                "id": "LEGAL-EXTERNAL-ESCALATE",
                "priority": 20,
                "effect": "ESCALATE",
                "reason": "External experts propose; CVL authority decides.",
                "conditions": {
                    "actor_roles": ["expert"],
                    "actions": ["LEGAL_REVIEW_APPROVE"],
                    "domains": ["LEGAL"],
                },
            },
        ],
    )


@pytest.mark.asyncio
async def test_policy_version_requires_evidence(authority_db):
    with pytest.raises(ValueError, match="requires evidence"):
        await authority_policy.register_policy_version(
            actor_id="founder-1",
            policy_key="TEST",
            version="1",
            title="Test policy",
            effective_at="2026-09-10T00:00:00+00:00",
            doctrine_ref="GOV-14",
            evidence_refs=[],
            rules=[{"effect": "DENY", "reason": "deny", "conditions": {}}],
        )


@pytest.mark.asyncio
async def test_duplicate_policy_version_is_rejected(authority_db):
    await _policy(authority_db)
    with pytest.raises(ValueError, match="already exists"):
        await _policy(authority_db)


@pytest.mark.asyncio
async def test_founder_role_does_not_bypass_missing_authority_level(authority_db):
    policy = await _policy(authority_db)
    decision = await authority_policy.evaluate_authority(
        actor_id="founder-1",
        actor_role="founder",
        action="LEGAL_REVIEW_APPROVE",
        context={"domain": "LEGAL", "authority_level": "A2_DOMAIN_REVIEWER"},
        policy_version_id=policy["id"],
    )
    assert decision["decision"] == "DENY"
    assert decision["matched_rule_id"] is None


@pytest.mark.asyncio
async def test_matching_policy_produces_explicit_allow_and_reason(authority_db):
    policy = await _policy(authority_db)
    decision = await authority_policy.evaluate_authority(
        actor_id="founder-1",
        actor_role="founder",
        action="legal_review_approve",
        context={"domain": "LEGAL", "authority_level": "A4_CVL_AUTHORITY"},
        policy_version_id=policy["id"],
        request_id="REQ-1",
    )
    assert decision["decision"] == "ALLOW"
    assert decision["matched_rule_id"] == "LEGAL-A4"
    assert decision["request_id"] == "REQ-1"
    assert decision["reason"]
    assert decision["policy_hash"] == policy["policy_hash"]
    assert len(decision["decision_hash"]) == 64


@pytest.mark.asyncio
async def test_external_expert_is_escalated_not_silently_authorized(authority_db):
    policy = await _policy(authority_db)
    decision = await authority_policy.evaluate_authority(
        actor_id="expert-1",
        actor_role="expert",
        action="LEGAL_REVIEW_APPROVE",
        context={"domain": "LEGAL", "authority_level": "A3_EXTERNAL_EXPERT"},
        policy_version_id=policy["id"],
    )
    assert decision["decision"] == "ESCALATE"
    assert decision["matched_rule_id"] == "LEGAL-EXTERNAL-ESCALATE"


@pytest.mark.asyncio
async def test_unknown_action_fails_closed(authority_db):
    policy = await _policy(authority_db)
    decision = await authority_policy.evaluate_authority(
        actor_id="founder-1",
        actor_role="founder",
        action="UNDECLARED_ACTION",
        context={"domain": "LEGAL", "authority_level": "A4_CVL_AUTHORITY"},
        policy_version_id=policy["id"],
    )
    assert decision["decision"] == "DENY"
    assert "fail-closed" in decision["reason"]


@pytest.mark.asyncio
async def test_tampered_policy_is_rejected(authority_db):
    policy = await _policy(authority_db)
    await authority_db.authority_policy_versions.update_one(
        {"id": policy["id"]}, {"$set": {"title": "tampered"}}
    )
    with pytest.raises(ValueError, match="integrity check failed"):
        await authority_policy.evaluate_authority(
            actor_id="founder-1",
            actor_role="founder",
            action="LEGAL_REVIEW_APPROVE",
            context={"domain": "LEGAL", "authority_level": "A4_CVL_AUTHORITY"},
            policy_version_id=policy["id"],
        )


@pytest.mark.asyncio
async def test_decision_reuses_canonical_governance_audit(authority_db):
    policy = await _policy(authority_db)
    decision = await authority_policy.evaluate_authority(
        actor_id="founder-1",
        actor_role="founder",
        action="LEGAL_REVIEW_APPROVE",
        context={"domain": "LEGAL", "authority_level": "A4_CVL_AUTHORITY"},
        policy_version_id=policy["id"],
    )
    events = await authority_db.governance_audit_events.find({}, {"_id": 0}).to_list(20)
    event_types = {event["event_type"] for event in events}
    assert "authority.policy_version.registered" in event_types
    assert "authority.decision.recorded" in event_types
    assert any(event["resource_id"] == decision["id"] for event in events)
