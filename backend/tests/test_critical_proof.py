from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import authority_policy, critical_proof, policy_registry, professional_governance
from services import proof_bridge


@pytest.fixture
async def proof_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_critical_proof_test"]
    for module in (
        authority_policy,
        critical_proof,
        policy_registry,
        professional_governance,
        proof_bridge,
    ):
        monkeypatch.setattr(module, "db", test_db)

    async def fake_notarize(package):
        return {
            **package,
            "anchored_at": "2026-09-10T00:00:00+00:00",
            "verification_status": "FREK_NOTARIZED",
            "frek_notary": {
                "height": 42,
                "payload_hash": "b" * 64,
                "block_hash": "c" * 64,
                "timestamp": "2026-09-10T00:00:00+00:00",
                "btc_anchored": False,
                "btc_block_height": None,
            },
        }

    monkeypatch.setattr(proof_bridge, "notarize_package", fake_notarize)
    yield test_db
    client.close()


async def _authority(effect="ALLOW"):
    policy = await authority_policy.register_policy_version(
        actor_id="founder",
        policy_key="CRITICAL_SECURITY_DECISION",
        version="1.0.0",
        title="Critical security decisions",
        rules=[
            {
                "id": "R1",
                "priority": 1,
                "effect": effect,
                "reason": "explicit critical authority",
                "conditions": {
                    "actor_roles": ["ADMIN"],
                    "actions": ["CRITICAL_SECURITY_DECISION"],
                    "domains": ["SECURITY"],
                    "minimum_authority_level": "A4_CVL_AUTHORITY",
                },
            }
        ],
        effective_at="2026-09-10T00:00:00+00:00",
        doctrine_ref="GOV-007",
        evidence_refs=["GOV-007"],
    )
    decision = await authority_policy.evaluate_authority(
        actor_id="admin",
        actor_role="admin",
        action="CRITICAL_SECURITY_DECISION",
        context={"domain": "SECURITY", "authority_level": "A4_CVL_AUTHORITY"},
        policy_version_id=policy["id"],
    )
    return policy, decision


@pytest.mark.asyncio
async def test_critical_proof_binds_exact_authority_policy_and_resource(proof_db):
    policy, decision = await _authority()
    row = await critical_proof.create_critical_decision_proof(
        actor_id="admin",
        domain="SECURITY",
        resource_type="security_remediation",
        resource_id="REMED-1",
        resource_hash="a" * 64,
        authority_decision_id=decision["id"],
        policy_version_id=policy["id"],
        evidence_refs=["TEST-1"],
    )
    assert row["status"] == "FREK_NOTARIZED"
    assert row["frek_block_hash"] == "c" * 64
    assert row["legal_effect"] == "none"
    gate = await critical_proof.proof_gate(
        domain="SECURITY",
        resource_type="security_remediation",
        resource_id="REMED-1",
        resource_hash="a" * 64,
    )
    assert gate["pass"] is True


@pytest.mark.asyncio
async def test_denied_authority_cannot_be_notarized_as_critical_approval(proof_db):
    policy, decision = await _authority("DENY")
    with pytest.raises(ValueError, match="ALLOW"):
        await critical_proof.create_critical_decision_proof(
            actor_id="admin",
            domain="SECURITY",
            resource_type="security_remediation",
            resource_id="REMED-2",
            resource_hash="a" * 64,
            authority_decision_id=decision["id"],
            policy_version_id=policy["id"],
            evidence_refs=["TEST-2"],
        )


@pytest.mark.asyncio
async def test_domain_mismatch_is_rejected(proof_db):
    policy, decision = await _authority()
    with pytest.raises(ValueError, match="domain"):
        await critical_proof.create_critical_decision_proof(
            actor_id="admin",
            domain="LEGAL",
            resource_type="contract",
            resource_id="CTR-1",
            resource_hash="a" * 64,
            authority_decision_id=decision["id"],
            policy_version_id=policy["id"],
            evidence_refs=["TEST-3"],
        )
