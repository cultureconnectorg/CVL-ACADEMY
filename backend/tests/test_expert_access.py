from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import expert_access, professional_governance as governance


@pytest.fixture
async def expert_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_expert_access_test"]
    monkeypatch.setattr(expert_access, "db", test_db)
    monkeypatch.setattr(governance, "db", test_db)
    yield test_db
    client.close()


async def _issue(expert_db, scope):
    case = await governance.create_case(
        actor_id="admin-1",
        title="Legal review",
        domain="LEGAL",
        description="Review contract",
    )
    expert = await governance.create_expert(
        actor_id="admin-1",
        display_name="Reviewer",
        email="reviewer@example.test",
        domains=["LEGAL"],
    )
    assignment = await governance.assign_expert(
        actor_id="admin-1",
        case_id=case["id"],
        expert_id=expert["id"],
        scope=scope,
    )
    raw, public = await governance.issue_expert_api_key(
        actor_id="admin-1", assignment_id=assignment["id"]
    )
    return case, expert, assignment, raw, public


@pytest.mark.asyncio
async def test_expert_key_authenticates_without_storing_raw_secret(expert_db):
    case, expert, assignment, raw, public = await _issue(expert_db, ["case:read"])
    stored = await expert_db.governance_api_keys.find_one({"id": public["id"]})
    assert raw.startswith("cvln_exp_")
    assert stored["token_hash"] != raw
    assert "token_hash" not in public

    context = await expert_access.authorize_case_scope(raw, case["id"], "case:read")
    assert context["expert"]["id"] == expert["id"]
    assert context["assignment"]["id"] == assignment["id"]


@pytest.mark.asyncio
async def test_expert_key_cannot_cross_case_boundary(expert_db):
    case, _expert, _assignment, raw, _public = await _issue(expert_db, ["case:read"])
    other = await governance.create_case(
        actor_id="admin-1",
        title="Other case",
        domain="PRIVACY",
        description="Separate matter",
    )
    assert case["id"] != other["id"]
    with pytest.raises(PermissionError, match="not assigned"):
        await expert_access.authorize_case_scope(raw, other["id"], "case:read")


@pytest.mark.asyncio
async def test_expert_key_cannot_exceed_scope(expert_db):
    case, _expert, _assignment, raw, _public = await _issue(expert_db, ["case:read"])
    with pytest.raises(PermissionError, match="scope denied"):
        await expert_access.authorize_case_scope(raw, case["id"], "decision:write")


@pytest.mark.asyncio
async def test_revoked_key_fails_closed(expert_db):
    case, _expert, _assignment, raw, public = await _issue(expert_db, ["case:read"])
    revoked = await expert_access.revoke_expert_api_key(
        actor_id="admin-1", key_id=public["id"]
    )
    assert revoked["status"] == "REVOKED"
    with pytest.raises(PermissionError, match="invalid or revoked"):
        await expert_access.authorize_case_scope(raw, case["id"], "case:read")


@pytest.mark.asyncio
async def test_narrowing_assignment_invalidates_old_key_scope(expert_db):
    case, _expert, assignment, raw, _public = await _issue(
        expert_db, ["case:read", "decision:write"]
    )
    await expert_db.governance_expert_assignments.update_one(
        {"id": assignment["id"]}, {"$set": {"scope": ["case:read"]}}
    )
    with pytest.raises(PermissionError, match="assignment scope denied"):
        await expert_access.authorize_case_scope(raw, case["id"], "decision:write")
