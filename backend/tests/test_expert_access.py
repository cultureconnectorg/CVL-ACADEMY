from __future__ import annotations

from datetime import datetime, timedelta, timezone

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


def _future(hours: int = 24) -> str:
    return (datetime.now(timezone.utc) + timedelta(hours=hours)).isoformat()


async def _issue(expert_db, scope, expires_at=None):
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
        actor_id="admin-1",
        assignment_id=assignment["id"],
        expires_at=expires_at or _future(),
    )
    return case, expert, assignment, raw, public


@pytest.mark.asyncio
async def test_expert_key_authenticates_without_storing_raw_secret(expert_db):
    case, expert, assignment, raw, public = await _issue(expert_db, ["case:read"])
    stored = await expert_db.governance_api_keys.find_one({"id": public["id"]})
    assert raw.startswith("cvln_exp_")
    assert stored["token_hash"] != raw
    assert "token_hash" not in public
    assert stored["expires_at"]

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


@pytest.mark.asyncio
async def test_issuance_requires_explicit_future_timezone_aware_expiry(expert_db):
    case = await governance.create_case(
        actor_id="admin-1",
        title="Expiry policy",
        domain="LEGAL",
        description="Credential expiry checks",
    )
    expert = await governance.create_expert(
        actor_id="admin-1",
        display_name="Reviewer",
        email="expiry@example.test",
        domains=["LEGAL"],
    )
    assignment = await governance.assign_expert(
        actor_id="admin-1",
        case_id=case["id"],
        expert_id=expert["id"],
        scope=["case:read"],
    )
    for expiry in (
        "",
        "not-a-date",
        "2099-01-01T00:00:00",
        (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat(),
    ):
        with pytest.raises(ValueError):
            await governance.issue_expert_api_key(
                actor_id="admin-1",
                assignment_id=assignment["id"],
                expires_at=expiry,
            )


@pytest.mark.asyncio
async def test_expired_key_fails_closed_and_is_marked_expired(expert_db):
    case, _expert, _assignment, raw, public = await _issue(expert_db, ["case:read"])
    expired = (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat()
    await expert_db.governance_api_keys.update_one(
        {"id": public["id"]}, {"$set": {"expires_at": expired}}
    )

    with pytest.raises(PermissionError, match="expired"):
        await expert_access.authorize_case_scope(raw, case["id"], "case:read")

    stored = await expert_db.governance_api_keys.find_one(
        {"id": public["id"]}, {"_id": 0}
    )
    assert stored["status"] == "EXPIRED"
    assert stored["expired_at"]


@pytest.mark.asyncio
async def test_successful_use_updates_last_used_usage_count_and_audit(expert_db):
    case, _expert, _assignment, raw, public = await _issue(expert_db, ["case:read"])

    first = await expert_access.authorize_case_scope(raw, case["id"], "case:read")
    second = await expert_access.authorize_case_scope(raw, case["id"], "case:read")
    assert first["usage"]["scope"] == "case:read"
    assert second["usage"]["used_at"]

    stored = await expert_db.governance_api_keys.find_one(
        {"id": public["id"]}, {"_id": 0}
    )
    assert stored["usage_count"] == 2
    assert stored["last_used_at"]
    usages = await expert_db.governance_api_key_usage.find(
        {"key_id": public["id"]}, {"_id": 0}
    ).to_list(10)
    assert len(usages) == 2
    assert {row["scope"] for row in usages} == {"case:read"}


@pytest.mark.asyncio
async def test_rotation_revokes_old_key_and_new_key_keeps_scope(expert_db):
    case, _expert, _assignment, old_raw, old_public = await _issue(
        expert_db, ["case:read"]
    )
    new_raw, new_public = await governance.rotate_expert_api_key(
        actor_id="admin-1",
        key_id=old_public["id"],
        expires_at=_future(48),
    )

    assert new_public["id"] != old_public["id"]
    assert new_public["expires_at"]
    old = await expert_db.governance_api_keys.find_one(
        {"id": old_public["id"]}, {"_id": 0}
    )
    assert old["status"] == "ROTATED"
    assert old["rotated_to_key_id"] == new_public["id"]

    with pytest.raises(PermissionError, match="invalid or revoked"):
        await expert_access.authorize_case_scope(old_raw, case["id"], "case:read")
    context = await expert_access.authorize_case_scope(new_raw, case["id"], "case:read")
    assert context["assignment"]["case_id"] == case["id"]
