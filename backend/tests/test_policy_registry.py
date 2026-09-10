from __future__ import annotations

from datetime import datetime, timezone

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import policy_registry, professional_governance


@pytest.fixture
async def policy_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_policy_registry_test"]
    monkeypatch.setattr(policy_registry, "db", test_db)
    monkeypatch.setattr(professional_governance, "db", test_db)
    yield test_db
    client.close()


async def _register(policy_db, version="1.0.0", supersedes=None, effective_at="2026-09-10T00:00:00+00:00"):
    return await policy_registry.register_version(
        actor_id="founder-1",
        policy_key="PROFESSIONAL_API_CREDENTIAL",
        version=version,
        kind="POLICY",
        title="Professional API Credential Policy",
        content={"max_ttl_days": 90, "rotation_required": True},
        effective_at=effective_at,
        evidence_refs=["GOV-07", "XCP-008"],
        supersedes_version_id=supersedes,
    )


@pytest.mark.asyncio
async def test_version_requires_timezone(policy_db):
    with pytest.raises(ValueError, match="include timezone"):
        await _register(policy_db, effective_at="2026-09-10T00:00:00")


@pytest.mark.asyncio
async def test_policy_version_content_hash_is_verifiable(policy_db):
    version = await _register(policy_db)
    assert version["content_immutable"] is True
    assert len(version["content_hash"]) == 64
    assert await policy_registry.verify_version_integrity(version) is True


@pytest.mark.asyncio
async def test_second_active_version_requires_explicit_supersession(policy_db):
    await _register(policy_db)
    with pytest.raises(ValueError, match="explicitly superseded"):
        await _register(policy_db, version="1.1.0")


@pytest.mark.asyncio
async def test_supersession_preserves_old_version_and_links_both_sides(policy_db):
    first = await _register(policy_db)
    second = await _register(policy_db, version="1.1.0", supersedes=first["id"])

    old = await policy_registry.get_version(first["id"])
    new = await policy_registry.get_version(second["id"])
    assert old["status"] == "SUPERSEDED"
    assert old["superseded_by_version_id"] == new["id"]
    assert old["content"]["max_ttl_days"] == 90
    assert new["supersedes_version_id"] == old["id"]
    assert new["status"] == "ACTIVE"


@pytest.mark.asyncio
async def test_superseded_version_cannot_govern_new_decision(policy_db):
    first = await _register(policy_db)
    await _register(policy_db, version="1.1.0", supersedes=first["id"])
    with pytest.raises(ValueError, match="not active and immutable"):
        await policy_registry.require_effective_version(first["id"])


@pytest.mark.asyncio
async def test_future_version_is_not_effective(policy_db):
    version = await _register(policy_db, effective_at="2099-01-01T00:00:00+00:00")
    with pytest.raises(ValueError, match="not yet effective"):
        await policy_registry.require_effective_version(
            version["id"], at=datetime(2026, 9, 10, tzinfo=timezone.utc)
        )


@pytest.mark.asyncio
async def test_registry_uses_canonical_governance_audit(policy_db):
    version = await _register(policy_db)
    events = await policy_db.governance_audit_events.find({}, {"_id": 0}).to_list(20)
    assert any(
        event["event_type"] == "governance.policy_version.registered"
        and event["resource_id"] == version["id"]
        for event in events
    )
