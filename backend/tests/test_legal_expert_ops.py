from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import authority_policy, expert_access, legal_expert_ops, legal_ops
from services import policy_registry, professional_governance as governance


@pytest.fixture
async def legal_expert_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_legal_expert_ops_test"]
    for module in (
        authority_policy,
        expert_access,
        legal_expert_ops,
        legal_ops,
        policy_registry,
        governance,
    ):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


def _future(hours: int = 24) -> str:
    return (datetime.now(timezone.utc) + timedelta(hours=hours)).isoformat()


def _past(minutes: int = 5) -> str:
    return (datetime.now(timezone.utc) - timedelta(minutes=minutes)).isoformat()


async def _setup(
    legal_expert_db,
    *,
    scope: list[str] | None = None,
    case_domain: str = "LEGAL",
    policy_effect: str = "ALLOW",
):
    case = await governance.create_case(
        actor_id="admin-1",
        title="Contract review",
        domain=case_domain,
        description="Scoped professional review",
        sensitivity="CONFIDENTIAL",
    )
    expert = await governance.create_expert(
        actor_id="admin-1",
        display_name="Legal reviewer",
        email="legal-reviewer@example.test",
        domains=["LEGAL"],
    )
    assignment = await governance.assign_expert(
        actor_id="admin-1",
        case_id=case["id"],
        expert_id=expert["id"],
        scope=scope or ["case:read", "legal:matter:write"],
        authority_level="A3_EXTERNAL_EXPERT",
    )
    raw_key, _public = await governance.issue_expert_api_key(
        actor_id="admin-1",
        assignment_id=assignment["id"],
        expires_at=_future(),
    )
    matter = await legal_ops.create_legal_matter(
        actor_id="admin-1",
        title="Distribution agreement",
        matter_type="CONTRACT",
        jurisdiction="FR",
        case_id=case["id"],
        evidence_refs=["EVIDENCE-MATTER-1"],
    )
    policy = await authority_policy.register_policy_version(
        actor_id="founder-1",
        policy_key="LEGAL_EXPERT_AUTHORITY",
        version=f"1.0.0-{case['id']}",
        title="Legal expert authority",
        rules=[
            {
                "id": "LEGAL-EXPERT-WRITE",
                "priority": 1,
                "effect": policy_effect,
                "reason": "Founder decision FD-L01 scoped legal expert authority.",
                "conditions": {
                    "actor_roles": ["EXTERNAL_EXPERT"],
                    "actions": ["LEGAL_EXPERT_MODIFY"],
                    "domains": ["LEGAL"],
                    "minimum_authority_level": "A3_EXTERNAL_EXPERT",
                },
            }
        ],
        effective_at=_past(),
        doctrine_ref="FD-L01",
        evidence_refs=["FOUNDER-DECISION-FD-L01"],
    )
    return case, expert, assignment, raw_key, matter, policy


@pytest.mark.asyncio
async def test_legal_expert_can_modify_directly_inside_scope_with_policy_and_audit(
    legal_expert_db,
):
    case, expert, assignment, raw_key, matter, policy = await _setup(
        legal_expert_db
    )

    result = await legal_expert_ops.modify_legal_matter(
        raw_key=raw_key,
        case_id=case["id"],
        matter_id=matter["id"],
        patch={
            "title": "Distribution agreement — corrected",
            "evidence_refs": ["EVIDENCE-MATTER-1", "EVIDENCE-EXPERT-EDIT-1"],
        },
        policy_version_id=policy["id"],
        rationale="Correct the legal matter after scoped review.",
        evidence_refs=["EVIDENCE-EXPERT-EDIT-1"],
    )

    assert result["matter"]["title"] == "Distribution agreement — corrected"
    assert result["matter"]["updated_by"] == expert["id"]
    assert result["authority"]["decision"] == "ALLOW"
    assert result["change"]["assignment_id"] == assignment["id"]
    assert result["change"]["policy_version_id"] == policy["id"]
    assert result["change"]["change_hash"]

    stored_change = await legal_expert_db.legal_expert_changes.find_one(
        {"id": result["change"]["id"]}, {"_id": 0}
    )
    assert stored_change["before"]["title"] == "Distribution agreement"
    assert stored_change["after"]["title"] == "Distribution agreement — corrected"

    audit = await legal_expert_db.governance_audit_events.find_one(
        {
            "event_type": "legal.expert.matter_modified",
            "resource_id": matter["id"],
        },
        {"_id": 0},
    )
    assert audit["actor_id"] == expert["id"]
    assert audit["payload"]["authority_decision_id"] == result["authority"]["id"]


@pytest.mark.asyncio
async def test_legal_expert_write_fails_closed_without_write_scope(legal_expert_db):
    case, _expert, _assignment, raw_key, matter, policy = await _setup(
        legal_expert_db,
        scope=["case:read"],
    )

    with pytest.raises(PermissionError, match="scope denied"):
        await legal_expert_ops.modify_legal_matter(
            raw_key=raw_key,
            case_id=case["id"],
            matter_id=matter["id"],
            patch={"title": "Forbidden edit"},
            policy_version_id=policy["id"],
            rationale="Attempt outside scope.",
            evidence_refs=["EVIDENCE-ATTEMPT-1"],
        )


@pytest.mark.asyncio
async def test_legal_expert_cannot_modify_protected_identity_or_lifecycle_fields(
    legal_expert_db,
):
    case, _expert, _assignment, raw_key, matter, policy = await _setup(
        legal_expert_db
    )

    with pytest.raises(PermissionError, match="protected legal fields"):
        await legal_expert_ops.modify_legal_matter(
            raw_key=raw_key,
            case_id=case["id"],
            matter_id=matter["id"],
            patch={"status": "RESOLVED"},
            policy_version_id=policy["id"],
            rationale="Try to bypass lifecycle.",
            evidence_refs=["EVIDENCE-ATTEMPT-2"],
        )


@pytest.mark.asyncio
async def test_legal_expert_write_requires_authority_allow(legal_expert_db):
    case, _expert, _assignment, raw_key, matter, policy = await _setup(
        legal_expert_db,
        policy_effect="DENY",
    )

    with pytest.raises(PermissionError, match="did not allow"):
        await legal_expert_ops.modify_legal_matter(
            raw_key=raw_key,
            case_id=case["id"],
            matter_id=matter["id"],
            patch={"title": "Policy-denied edit"},
            policy_version_id=policy["id"],
            rationale="A denied action must not mutate state.",
            evidence_refs=["EVIDENCE-ATTEMPT-3"],
        )

    stored = await legal_expert_db.legal_matters.find_one(
        {"id": matter["id"]}, {"_id": 0}
    )
    assert stored["title"] == "Distribution agreement"


@pytest.mark.asyncio
async def test_legal_expert_cannot_cross_case_or_non_legal_boundary(legal_expert_db):
    case, _expert, _assignment, raw_key, matter, policy = await _setup(
        legal_expert_db
    )
    other = await governance.create_case(
        actor_id="admin-1",
        title="Separate legal case",
        domain="LEGAL",
        description="Must remain isolated",
    )

    with pytest.raises(PermissionError, match="not assigned"):
        await legal_expert_ops.modify_legal_matter(
            raw_key=raw_key,
            case_id=other["id"],
            matter_id=matter["id"],
            patch={"title": "Cross-case edit"},
            policy_version_id=policy["id"],
            rationale="Must fail.",
            evidence_refs=["EVIDENCE-ATTEMPT-4"],
        )

    await legal_expert_db.professional_cases.update_one(
        {"id": case["id"]}, {"$set": {"domain": "PRIVACY"}}
    )
    with pytest.raises(PermissionError, match="requires a LEGAL professional case"):
        await legal_expert_ops.modify_legal_matter(
            raw_key=raw_key,
            case_id=case["id"],
            matter_id=matter["id"],
            patch={"title": "Wrong-domain edit"},
            policy_version_id=policy["id"],
            rationale="Must fail.",
            evidence_refs=["EVIDENCE-ATTEMPT-5"],
        )
