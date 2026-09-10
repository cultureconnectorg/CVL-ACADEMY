from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import license_entitlement, policy_registry, professional_governance


@pytest.fixture
async def license_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_license_entitlement_test"]
    for module in (license_entitlement, policy_registry, professional_governance):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


def _past() -> str:
    return (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()


@pytest.mark.asyncio
async def test_entitlement_view_hides_internal_doctrine_and_evidence(license_db):
    tenant = await license_entitlement.register_tenant(
        actor_id="founder",
        tenant_key="PARTNER-A",
        display_name="Partner A",
        owner_ref="ORG-1",
        evidence_refs=["LICENSE-AGREEMENT-1"],
    )
    entitlement = await license_entitlement.register_entitlement_version(
        actor_id="founder",
        tenant_id=tenant["id"],
        version="1.0.0",
        effective_at=_past(),
        capabilities=["ACADEMY_CATALOG", "QUALITY_PACKS"],
        public_constraints={"max_seats": 100},
        evidence_refs=["LICENSE-AGREEMENT-1"],
    )
    assert entitlement["governance_policy"]["content"]["internal_doctrine_exposed"] is False

    view = await license_entitlement.entitlement_view(tenant["id"])
    assert view["capabilities"] == ["ACADEMY_CATALOG", "QUALITY_PACKS"]
    assert view["constraints"] == {"max_seats": 100}
    assert view["internal_doctrine"] is None
    assert view["internal_policy_content"] is None
    assert view["evidence_refs"] is None


@pytest.mark.asyncio
async def test_unlicensed_capability_fails_closed(license_db):
    tenant = await license_entitlement.register_tenant(
        actor_id="founder",
        tenant_key="PARTNER-B",
        display_name="Partner B",
        owner_ref="ORG-2",
        evidence_refs=["LICENSE-2"],
    )
    await license_entitlement.register_entitlement_version(
        actor_id="founder",
        tenant_id=tenant["id"],
        version="1.0.0",
        effective_at=_past(),
        capabilities=["ACADEMY_CATALOG"],
        public_constraints={},
        evidence_refs=["LICENSE-2"],
    )
    ok = await license_entitlement.require_capability(tenant["id"], "ACADEMY_CATALOG")
    assert ok["entitled"] is True
    with pytest.raises(PermissionError, match="not entitled"):
        await license_entitlement.require_capability(tenant["id"], "INTERNAL_POLICY")


@pytest.mark.asyncio
async def test_entitlement_versions_require_explicit_supersession(license_db):
    tenant = await license_entitlement.register_tenant(
        actor_id="founder",
        tenant_key="PARTNER-C",
        display_name="Partner C",
        owner_ref="ORG-3",
        evidence_refs=["LICENSE-3"],
    )
    first = await license_entitlement.register_entitlement_version(
        actor_id="founder",
        tenant_id=tenant["id"],
        version="1.0.0",
        effective_at=_past(),
        capabilities=["ACADEMY_CATALOG"],
        public_constraints={},
        evidence_refs=["LICENSE-3"],
    )
    with pytest.raises(ValueError, match="explicitly superseded"):
        await license_entitlement.register_entitlement_version(
            actor_id="founder",
            tenant_id=tenant["id"],
            version="1.1.0",
            effective_at=_past(),
            capabilities=["ACADEMY_CATALOG", "QUALITY_PACKS"],
            public_constraints={},
            evidence_refs=["LICENSE-3-AMENDMENT"],
        )
    second = await license_entitlement.register_entitlement_version(
        actor_id="founder",
        tenant_id=tenant["id"],
        version="1.1.0",
        effective_at=_past(),
        capabilities=["ACADEMY_CATALOG", "QUALITY_PACKS"],
        public_constraints={},
        evidence_refs=["LICENSE-3-AMENDMENT"],
        supersedes_version_id=first["policy_version_id"],
    )
    assert second["policy_version_id"] != first["policy_version_id"]
