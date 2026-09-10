from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import authority_policy, legal_ops, legal_policy, policy_registry
from services import professional_governance as governance


@pytest.fixture
async def legal_policy_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_legal_policy_test"]
    for module in (
        authority_policy,
        legal_ops,
        legal_policy,
        policy_registry,
        governance,
    ):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


async def _matter():
    return await legal_ops.create_legal_matter(
        actor_id="admin-1",
        title="Distribution agreement",
        matter_type="CONTRACT",
        jurisdiction="FR",
        evidence_refs=["DOC-1"],
    )


async def _policy(key, action, effect, level, evidence):
    return await authority_policy.register_policy_version(
        actor_id="founder-1",
        policy_key=key,
        version="1.0.0",
        title=key.replace("_", " ").title(),
        effective_at="2026-09-10T00:00:00+00:00",
        doctrine_ref="FD-L02/L03/L04",
        evidence_refs=[evidence],
        rules=[
            {
                "id": f"{key}-RULE",
                "priority": 1,
                "effect": effect,
                "reason": "Explicit legal authority rule.",
                "conditions": {
                    "actor_roles": ["founder"],
                    "actions": [action],
                    "domains": ["LEGAL"],
                    "minimum_authority_level": level,
                },
            }
        ],
    )


@pytest.mark.asyncio
async def test_review_requirement_uses_policy_effect_not_caller_boolean(legal_policy_db):
    matter = await _matter()
    policy = await authority_policy.register_policy_version(
        actor_id="founder-1",
        policy_key="LEGAL_REVIEW_REQUIREMENT",
        version="1.0.0",
        title="Legal review requirement",
        effective_at="2026-09-10T00:00:00+00:00",
        doctrine_ref="FD-L03",
        evidence_refs=["FOUNDER-FD-L03"],
        rules=[
            {
                "id": "HIGH-EXTERNAL",
                "priority": 1,
                "effect": "ESCALATE",
                "reason": "High risk contract requires external review.",
                "conditions": {
                    "actor_roles": ["founder"],
                    "actions": ["LEGAL_REVIEW_DECIDE"],
                    "domains": ["LEGAL"],
                    "risk_levels": ["R3 HIGH", "R4 CRITICAL"],
                    "resource_types": ["CONTRACT"],
                    "minimum_authority_level": "A4_CVL_AUTHORITY",
                },
            },
            {
                "id": "LOW-INTERNAL",
                "priority": 2,
                "effect": "ALLOW",
                "reason": "Moderate contract review may remain internal.",
                "conditions": {
                    "actor_roles": ["founder"],
                    "actions": ["LEGAL_REVIEW_DECIDE"],
                    "domains": ["LEGAL"],
                    "risk_levels": ["R2 MODERATE"],
                    "resource_types": ["CONTRACT"],
                    "minimum_authority_level": "A4_CVL_AUTHORITY",
                },
            },
        ],
    )

    high = await legal_policy.decide_review_requirement(
        actor_id="founder-1",
        actor_role="founder",
        authority_level="A4_CVL_AUTHORITY",
        matter_id=matter["id"],
        policy_version_id=policy["id"],
        risk_level="R3 HIGH",
        evidence_refs=["ASSESSMENT-1"],
    )
    assert high["external_review_required"] is True
    assert high["authority"]["matched_rule_id"] == "HIGH-EXTERNAL"
    stored = await legal_policy_db.legal_matters.find_one(
        {"id": matter["id"]}, {"_id": 0}
    )
    assert stored["status"] == "WAITING_EXTERNAL"


@pytest.mark.asyncio
async def test_review_requirement_rejects_wrong_policy_key(legal_policy_db):
    matter = await _matter()
    policy = await _policy(
        "WRONG_POLICY",
        "LEGAL_REVIEW_DECIDE",
        "ALLOW",
        "A4_CVL_AUTHORITY",
        "EVID-WRONG",
    )
    with pytest.raises(ValueError, match="LEGAL_REVIEW_REQUIREMENT"):
        await legal_policy.decide_review_requirement(
            actor_id="founder-1",
            actor_role="founder",
            authority_level="A4_CVL_AUTHORITY",
            matter_id=matter["id"],
            policy_version_id=policy["id"],
            risk_level="R2 MODERATE",
            evidence_refs=["ASSESSMENT-2"],
        )


@pytest.mark.asyncio
async def test_internal_and_external_approvals_remain_distinct(legal_policy_db):
    matter = await _matter()
    internal_policy = await _policy(
        "LEGAL_INTERNAL_APPROVAL",
        "LEGAL_INTERNAL_APPROVE",
        "ALLOW",
        "A4_CVL_AUTHORITY",
        "FOUNDER-FD-L04-INTERNAL",
    )
    external_policy = await _policy(
        "LEGAL_EXTERNAL_APPROVAL",
        "LEGAL_EXTERNAL_APPROVE",
        "ALLOW",
        "A3_EXTERNAL_EXPERT",
        "FOUNDER-FD-L04-EXTERNAL",
    )

    internal = await legal_policy.record_approval(
        actor_id="founder-1",
        actor_role="founder",
        authority_level="A4_CVL_AUTHORITY",
        matter_id=matter["id"],
        approval_kind="INTERNAL_APPROVED",
        policy_version_id=internal_policy["id"],
        rationale="Internal CVL authority approval.",
        evidence_refs=["INT-APPROVAL-1"],
    )
    external = await legal_policy.record_approval(
        actor_id="founder-1",
        actor_role="founder",
        authority_level="A4_CVL_AUTHORITY",
        matter_id=matter["id"],
        approval_kind="EXTERNAL_LEGAL_APPROVED",
        policy_version_id=external_policy["id"],
        rationale="External legal conclusion received and recorded.",
        evidence_refs=["EXT-APPROVAL-1"],
    )
    assert internal["approval_kind"] == "INTERNAL_APPROVED"
    assert external["approval_kind"] == "EXTERNAL_LEGAL_APPROVED"

    state = await legal_policy.approval_state(matter["id"])
    assert state["internal_approved"] is True
    assert state["external_legal_approved"] is True
    assert len(state["approvals"]) == 2


@pytest.mark.asyncio
async def test_a3_cannot_satisfy_a4_internal_approval(legal_policy_db):
    matter = await _matter()
    policy = await _policy(
        "LEGAL_INTERNAL_APPROVAL",
        "LEGAL_INTERNAL_APPROVE",
        "ALLOW",
        "A4_CVL_AUTHORITY",
        "FOUNDER-FD-L02",
    )
    with pytest.raises(PermissionError, match="did not allow"):
        await legal_policy.record_approval(
            actor_id="expert-1",
            actor_role="founder",
            authority_level="A3_EXTERNAL_EXPERT",
            matter_id=matter["id"],
            approval_kind="INTERNAL_APPROVED",
            policy_version_id=policy["id"],
            rationale="Insufficient authority.",
            evidence_refs=["ATTEMPT-1"],
        )
