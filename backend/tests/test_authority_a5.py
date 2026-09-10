from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import authority_policy, policy_registry, professional_governance


@pytest.fixture
async def authority_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_authority_a5_test"]
    for module in (authority_policy, policy_registry, professional_governance):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


@pytest.mark.asyncio
async def test_a5_founder_systemic_is_distinct_and_above_a4(authority_db):
    policy = await authority_policy.register_policy_version(
        actor_id="founder-1",
        policy_key="SYSTEMIC_AUTHORITY",
        version="1.0.0",
        title="Systemic founder authority",
        effective_at="2026-09-10T00:00:00+00:00",
        doctrine_ref="XCP-001",
        evidence_refs=["MASTER:XCP-001"],
        rules=[
            {
                "id": "A5-ONLY",
                "priority": 1,
                "effect": "ALLOW",
                "reason": "Systemic decisions require A5 founder authority.",
                "conditions": {
                    "actor_roles": ["founder"],
                    "actions": ["SYSTEMIC_DECISION"],
                    "minimum_authority_level": "A5_FOUNDER_SYSTEMIC",
                },
            }
        ],
    )

    denied = await authority_policy.evaluate_authority(
        actor_id="founder-1",
        actor_role="founder",
        action="SYSTEMIC_DECISION",
        context={"authority_level": "A4_CVL_AUTHORITY"},
        policy_version_id=policy["id"],
    )
    allowed = await authority_policy.evaluate_authority(
        actor_id="founder-1",
        actor_role="founder",
        action="SYSTEMIC_DECISION",
        context={"authority_level": "A5_FOUNDER_SYSTEMIC"},
        policy_version_id=policy["id"],
    )
    assert denied["decision"] == "DENY"
    assert allowed["decision"] == "ALLOW"
