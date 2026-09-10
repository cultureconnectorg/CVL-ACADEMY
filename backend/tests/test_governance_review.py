from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import authority_policy, governance_review, policy_registry, professional_governance


@pytest.fixture
async def review_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_governance_review_test"]
    for module in (authority_policy, governance_review, policy_registry, professional_governance):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


async def _case():
    return await professional_governance.create_case(
        actor_id="admin",
        title="Review case",
        domain="LEGAL",
        description="Explicit review states",
    )


async def _policy(effect: str = "ALLOW"):
    return await authority_policy.register_policy_version(
        actor_id="founder",
        policy_key="PROFESSIONAL_REVIEW",
        version="1.0.0",
        title="Professional review authority",
        rules=[
            {
                "id": "R1",
                "priority": 1,
                "effect": effect,
                "reason": "review authority",
                "conditions": {
                    "actor_roles": ["ADMIN"],
                    "actions": [
                        "PROFESSIONAL_REVIEW_CVL_APPROVE",
                        "PROFESSIONAL_REVIEW_EXPERT_VALIDATE",
                    ],
                    "domains": ["LEGAL"],
                    "minimum_authority_level": "A4_CVL_AUTHORITY",
                },
            }
        ],
        effective_at="2026-09-10T00:00:00+00:00",
        doctrine_ref="GOV-006",
        evidence_refs=["GOV-006"],
    )


@pytest.mark.asyncio
async def test_ai_prepared_is_not_approved(review_db):
    case = await _case()
    review = await governance_review.create_review(
        actor_id="ai-router",
        case_id=case["id"],
        subject="Draft review",
        prepared_by="AI",
        evidence_refs=["INPUT-1"],
    )
    assert review["state"] == "AI_PREPARED"
    assert review.get("authority_decision_id") is None


@pytest.mark.asyncio
async def test_approval_requires_authority_policy_and_evidence(review_db):
    case = await _case()
    review = await governance_review.create_review(
        actor_id="admin",
        case_id=case["id"],
        subject="Human review",
        prepared_by="HUMAN",
        evidence_refs=["INPUT-1"],
    )
    review = await governance_review.transition_review(
        actor_id="admin",
        actor_role="admin",
        authority_level="A4_CVL_AUTHORITY",
        review_id=review["id"],
        target_state="HUMAN_REVIEW",
        policy_version_id=None,
        rationale="Ready for decision",
        evidence_refs=["REVIEW-1"],
    )
    policy = await _policy()
    approved = await governance_review.transition_review(
        actor_id="admin",
        actor_role="admin",
        authority_level="A4_CVL_AUTHORITY",
        review_id=review["id"],
        target_state="CVL_APPROVED",
        policy_version_id=policy["id"],
        rationale="Approved under CVL policy",
        evidence_refs=["DECISION-1"],
    )
    assert approved["state"] == "CVL_APPROVED"
    assert approved["authority_decision_id"]


@pytest.mark.asyncio
async def test_deny_policy_blocks_approval(review_db):
    case = await _case()
    review = await governance_review.create_review(
        actor_id="admin",
        case_id=case["id"],
        subject="Blocked review",
        prepared_by="HUMAN",
        evidence_refs=["INPUT-1"],
    )
    review = await governance_review.transition_review(
        actor_id="admin",
        actor_role="admin",
        authority_level="A4_CVL_AUTHORITY",
        review_id=review["id"],
        target_state="HUMAN_REVIEW",
        policy_version_id=None,
        rationale="Ready",
        evidence_refs=["REVIEW-1"],
    )
    policy = await _policy("DENY")
    with pytest.raises(PermissionError, match="did not allow"):
        await governance_review.transition_review(
            actor_id="admin",
            actor_role="admin",
            authority_level="A4_CVL_AUTHORITY",
            review_id=review["id"],
            target_state="CVL_APPROVED",
            policy_version_id=policy["id"],
            rationale="Attempt",
            evidence_refs=["DECISION-1"],
        )
