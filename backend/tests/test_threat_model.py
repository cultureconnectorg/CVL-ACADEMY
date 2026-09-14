from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import threat_model


@pytest.fixture
async def threat_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_threat_model_test"]
    monkeypatch.setattr(threat_model, "db", test_db)
    yield test_db
    client.close()


@pytest.mark.asyncio
async def test_high_threat_blocks_release_until_verified_with_evidence(threat_db):
    await threat_db.security_assets.insert_one({"id": "ASSET-1", "name": "API"})
    threat = await threat_model.create_threat(
        actor_id="sec-1",
        title="Cross-case expert access",
        category="authorization",
        asset_id="ASSET-1",
        attack_surface="/api/expert/cases/{case_id}",
        abuse_case="Expert attempts to read a case outside its assignment",
        severity="high",
    )
    gate = await threat_model.threat_release_gate()
    assert gate["pass"] is False

    with pytest.raises(ValueError, match="mitigation and regression-test evidence"):
        await threat_model.transition_threat(
            actor_id="sec-1", threat_id=threat["id"], status="VERIFIED"
        )

    await threat_model.add_threat_evidence(
        actor_id="sec-1",
        threat_id=threat["id"],
        mitigation="Case and scope checked on every request",
        test_ref="backend/tests/test_expert_access.py::test_expert_key_cannot_cross_case_boundary",
    )
    verified = await threat_model.transition_threat(
        actor_id="sec-1", threat_id=threat["id"], status="VERIFIED"
    )
    assert verified["status"] == "VERIFIED"
    assert (await threat_model.threat_release_gate())["pass"] is True


@pytest.mark.asyncio
async def test_threat_with_unknown_asset_is_rejected(threat_db):
    with pytest.raises(LookupError, match="asset"):
        await threat_model.create_threat(
            actor_id="sec-1",
            title="Unknown asset threat",
            category="availability",
            asset_id="missing",
            attack_surface="worker",
            abuse_case="unbounded workload",
            severity="medium",
        )


@pytest.mark.asyncio
async def test_invalid_severity_is_rejected(threat_db):
    with pytest.raises(ValueError, match="severity"):
        await threat_model.create_threat(
            actor_id="sec-1",
            title="Invalid threat",
            category="test",
            asset_id=None,
            attack_surface="test",
            abuse_case="test",
            severity="catastrophic",
        )
