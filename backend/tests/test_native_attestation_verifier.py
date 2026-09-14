from __future__ import annotations

import hashlib
import json

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import native_attestation_verifier as verifier
from services import proof_bridge


def _payload_hash(package):
    payload_data = {
        "subject": package["subject"],
        "chain_hash": package["chain_hash"],
        "legal_effect": "none",
    }
    raw = json.dumps(payload_data, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _remote_proof(package, *, btc=False, tamper_block=False):
    payload_hash = _payload_hash(package)
    block = {
        "height": 12,
        "prev_hash": "1" * 64,
        "payload_type": "academy_evidence_package",
        "payload_id": package["package_id"],
        "payload_hash": payload_hash,
        "timestamp": "2026-09-10T16:30:00+00:00",
        "event_id": None,
        "spec_version": "1.0.0",
    }
    raw = (
        f"{block['height']}|{block['prev_hash']}|{block['payload_hash']}|"
        f"{block['payload_type']}|{block['payload_id']}|{block['timestamp']}||"
        f"{block['spec_version']}"
    )
    block["block_hash"] = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    if tamper_block:
        block["block_hash"] = "9" * 64
    return {
        "payload_id": package["package_id"],
        "block": block,
        "chain_proof": {
            "height": block["height"],
            "prev_hash": block["prev_hash"],
            "payload_hash": block["payload_hash"],
            "block_hash": block["block_hash"],
            "timestamp": block["timestamp"],
        },
        "ots_proof_b64": "OTS" if btc else None,
        "btc_anchored": btc,
        "btc_attestation": {"btc_block_height": 900000} if btc else None,
        "verification_url": "https://example.invalid/block/900000" if btc else None,
    }


@pytest.fixture
async def verification_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_attestation_verification_test"]
    monkeypatch.setattr(verifier, "db", test_db)
    monkeypatch.setattr(proof_bridge, "db", test_db)
    yield test_db
    client.close()


async def _seed_attestation(db):
    package = proof_bridge.build_evidence_package(
        subject="academy:contract:CTR-1:signing-intent",
        claims=[
            {
                "statement": "Authorized actor explicitly asserted SIGN intent",
                "status": "OBSERVED",
                "evidence_ref": "a" * 64,
            }
        ],
        artefacts=[
            {
                "type": "contract_document",
                "id": "DOC-1",
                "hash": "a" * 64,
                "algorithm": "sha256",
            }
        ],
        events=["actor:user-1:SIGN", "frek:FREK-001"],
        decisions=["SIGAUTH-1"],
        package_id="EPKG-1",
    )
    remote = _remote_proof(package)
    block = remote["block"]
    package.update(
        anchored_at=block["timestamp"],
        verification_status="FREK_NOTARIZED",
        frek_notary={
            "height": block["height"],
            "payload_hash": block["payload_hash"],
            "block_hash": block["block_hash"],
            "timestamp": block["timestamp"],
            "btc_anchored": False,
            "btc_block_height": None,
        },
    )
    row = {
        "id": "NSIG-1",
        "contract_id": "CTR-1",
        "actor_id": "user-1",
        "actor_frek_id": "FREK-001",
        "document_hash": "a" * 64,
        "evidence_package": package,
        "status": "FREK_NOTARIZED",
        "signature_level": "CVLN_NATIVE_ATTESTATION",
        "legal_effect": "none",
        "created_at": "2026-09-10T16:30:00+00:00",
    }
    await db.native_signature_attestations.insert_one(dict(row))
    return row, remote


@pytest.mark.asyncio
async def test_verification_gate_passes_matching_frek_proof(verification_db, monkeypatch):
    attestation, remote = await _seed_attestation(verification_db)

    async def fake_fetch(package_id):
        assert package_id == "EPKG-1"
        return remote

    monkeypatch.setattr(verifier, "fetch_frek_proof", fake_fetch)
    result = await verifier.verify_native_attestation(
        actor_id="admin-1", attestation_id=attestation["id"]
    )

    assert result["status"] == "VERIFIED_FREK"
    assert result["errors"] == []
    assert all(result["checks"].values())
    assert result["legal_effect"] == "none"
    assert await verification_db.native_signature_verifications.count_documents({}) == 1


@pytest.mark.asyncio
async def test_verification_gate_detects_remote_block_tampering(verification_db, monkeypatch):
    attestation, _ = await _seed_attestation(verification_db)
    tampered = _remote_proof(attestation["evidence_package"], tamper_block=True)

    async def fake_fetch(_package_id):
        return tampered

    monkeypatch.setattr(verifier, "fetch_frek_proof", fake_fetch)
    result = await verifier.verify_native_attestation(
        actor_id="admin-1", attestation_id=attestation["id"]
    )

    assert result["status"] == "FAILED"
    assert result["checks"]["stored_block_hash"] is False
    assert result["checks"]["block_hash_recomputed"] is False
    assert "stored_block_hash" in result["errors"]
    assert "block_hash_recomputed" in result["errors"]


@pytest.mark.asyncio
async def test_btc_gate_fails_when_only_frek_notarized(verification_db, monkeypatch):
    attestation, remote = await _seed_attestation(verification_db)

    async def fake_fetch(_package_id):
        return remote

    monkeypatch.setattr(verifier, "fetch_frek_proof", fake_fetch)
    result = await verifier.verify_native_attestation(
        actor_id="admin-1",
        attestation_id=attestation["id"],
        require_btc_anchor=True,
    )

    assert result["status"] == "FAILED"
    assert result["checks"]["btc_anchor_requirement"] is False
    assert "btc_anchor_requirement" in result["errors"]


@pytest.mark.asyncio
async def test_btc_gate_passes_when_frek_reports_anchor(verification_db, monkeypatch):
    attestation, _ = await _seed_attestation(verification_db)
    remote = _remote_proof(attestation["evidence_package"], btc=True)

    async def fake_fetch(_package_id):
        return remote

    monkeypatch.setattr(verifier, "fetch_frek_proof", fake_fetch)
    result = await verifier.verify_native_attestation(
        actor_id="admin-1",
        attestation_id=attestation["id"],
        require_btc_anchor=True,
    )

    assert result["status"] == "VERIFIED_FREK_BTC"
    assert result["btc_anchored"] is True
    assert result["checks"]["btc_anchor_requirement"] is True
    assert result["legal_effect"] == "none"


@pytest.mark.asyncio
async def test_contract_attestation_listing_requires_real_contract(verification_db):
    with pytest.raises(LookupError, match="contract not found"):
        await verifier.list_contract_attestations("CTR-missing")

    await verification_db.legal_contracts.insert_one({"id": "CTR-1"})
    await verification_db.native_signature_attestations.insert_many(
        [
            {"id": "NSIG-2", "contract_id": "CTR-1", "created_at": "2026-09-10T02:00:00Z"},
            {"id": "NSIG-1", "contract_id": "CTR-1", "created_at": "2026-09-10T01:00:00Z"},
        ]
    )
    rows = await verifier.list_contract_attestations("CTR-1")
    assert [row["id"] for row in rows] == ["NSIG-1", "NSIG-2"]
