from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import legal_ops, proof_bridge


@pytest.fixture
async def proof_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_proof_bridge_test"]
    monkeypatch.setattr(proof_bridge, "db", test_db)
    monkeypatch.setattr(legal_ops, "db", test_db)
    yield test_db
    client.close()


def test_evidence_package_chain_hash_detects_tampering():
    package = proof_bridge.build_evidence_package(
        subject="academy:test",
        claims=[{"statement": "x", "status": "OBSERVED", "evidence_ref": "E-1"}],
        artefacts=[{"id": "doc-1", "hash": "a" * 64, "algorithm": "sha256"}],
        events=["event-1"],
        decisions=["decision-1"],
        package_id="EPKG-test",
    )
    verification = proof_bridge.verify_evidence_package(package)
    assert verification["chain_hash_valid"] is True
    assert verification["signature_present"] is False
    assert verification["frek_notarized"] is False
    assert verification["legal_effect"] == "none"

    tampered = {**package, "claims": [{"statement": "changed"}]}
    verification = proof_bridge.verify_evidence_package(tampered)
    assert verification["chain_hash_valid"] is False
    assert "chain_hash_mismatch" in verification["errors"]


def test_invalid_document_digest_is_rejected():
    with pytest.raises(proof_bridge.InvalidEvidence):
        proof_bridge.build_evidence_package(
            subject="academy:test",
            claims=[],
            artefacts=[{"id": "doc", "hash": "not-a-sha256"}],
        )


@pytest.mark.asyncio
async def test_missing_frek_config_fails_closed(monkeypatch):
    monkeypatch.delenv("FREK_CORE_BASE_URL", raising=False)
    monkeypatch.delenv("FREK_CORE_ACCESS_TOKEN", raising=False)
    monkeypatch.delenv("FREK_CORE_API_KEY", raising=False)
    monkeypatch.delenv("FREK_CORE_CLIENT_ID", raising=False)
    monkeypatch.delenv("FREK_CORE_CLIENT_SECRET", raising=False)
    package = proof_bridge.build_evidence_package(
        subject="academy:test",
        claims=[],
        artefacts=[{"id": "doc", "hash": "b" * 64}],
    )
    with pytest.raises(proof_bridge.FrekNotaryUnavailable):
        await proof_bridge.notarize_package(package)


@pytest.mark.asyncio
async def test_signer_authorization_requires_evidence(proof_db):
    contract = await legal_ops.create_contract(
        actor_id="admin",
        title="Artist agreement",
        contract_type="service",
        counterparty="Artist",
    )
    await legal_ops.transition_contract(
        actor_id="admin", contract_id=contract["id"], status="IN_REVIEW"
    )
    with pytest.raises(ValueError, match="requires evidence"):
        await legal_ops.authorize_contract_signer(
            actor_id="admin",
            contract_id=contract["id"],
            signer_user_id="user-1",
            signer_frek_id="FREK-001",
            signer_role="counterparty",
            evidence_refs=[],
        )


@pytest.mark.asyncio
async def test_native_attestation_requires_authorized_frek_identity(proof_db, monkeypatch):
    contract = await legal_ops.create_contract(
        actor_id="admin",
        title="Artist agreement",
        contract_type="service",
        counterparty="Artist",
    )
    review = await legal_ops.transition_contract(
        actor_id="admin", contract_id=contract["id"], status="IN_REVIEW"
    )
    approved = await legal_ops.transition_contract(
        actor_id="admin", contract_id=review["id"], status="APPROVED"
    )
    assert approved["status"] == "APPROVED"

    called = False

    async def fake_notarize(package):
        nonlocal called
        called = True
        return package

    monkeypatch.setattr(proof_bridge, "notarize_package", fake_notarize)
    with pytest.raises(PermissionError, match="not an authorized signer"):
        await proof_bridge.create_contract_native_attestation(
            actor_id="user-1",
            actor_frek_id="FREK-001",
            contract_id=contract["id"],
            document_hash="c" * 64,
            intent="SIGN",
        )
    assert called is False
    assert await proof_db.native_signature_attestations.count_documents({}) == 0


@pytest.mark.asyncio
async def test_native_attestation_notarizes_but_does_not_fake_legal_signature(
    proof_db, monkeypatch
):
    contract = await legal_ops.create_contract(
        actor_id="admin",
        title="Artist agreement",
        contract_type="service",
        counterparty="Artist",
        document_id="DOC-1",
    )
    await legal_ops.transition_contract(
        actor_id="admin", contract_id=contract["id"], status="IN_REVIEW"
    )
    await legal_ops.authorize_contract_signer(
        actor_id="admin",
        contract_id=contract["id"],
        signer_user_id="user-1",
        signer_frek_id="FREK-001",
        signer_role="counterparty",
        evidence_refs=["AUTHORITY-1"],
    )
    await legal_ops.transition_contract(
        actor_id="admin", contract_id=contract["id"], status="APPROVED"
    )

    async def fake_notarize(package):
        return {
            **package,
            "anchored_at": "2026-09-10T16:00:00+00:00",
            "verification_status": "FREK_NOTARIZED",
            "frek_notary": {
                "height": 42,
                "payload_hash": "d" * 64,
                "block_hash": "e" * 64,
                "timestamp": "2026-09-10T16:00:00+00:00",
                "btc_anchored": False,
                "btc_block_height": None,
            },
        }

    monkeypatch.setattr(proof_bridge, "notarize_package", fake_notarize)
    attestation = await proof_bridge.create_contract_native_attestation(
        actor_id="user-1",
        actor_frek_id="FREK-001",
        contract_id=contract["id"],
        document_hash="c" * 64,
        intent="SIGN",
        evidence_refs=["CONSENT-CLICK-1"],
    )

    assert attestation["status"] == "FREK_NOTARIZED"
    assert attestation["signature_level"] == "CVLN_NATIVE_ATTESTATION"
    assert attestation["legal_effect"] == "none"
    assert attestation["evidence_package"]["signature"] is None
    assert attestation["evidence_package"]["frek_notary"]["height"] == 42

    stored_contract = await proof_db.legal_contracts.find_one(
        {"id": contract["id"]}, {"_id": 0}
    )
    assert stored_contract["status"] == "APPROVED"


@pytest.mark.asyncio
async def test_native_attestation_is_idempotent_for_same_actor_and_document(
    proof_db, monkeypatch
):
    contract = await legal_ops.create_contract(
        actor_id="admin",
        title="Service agreement",
        contract_type="service",
        counterparty="Partner",
    )
    await legal_ops.transition_contract(
        actor_id="admin", contract_id=contract["id"], status="IN_REVIEW"
    )
    await legal_ops.authorize_contract_signer(
        actor_id="admin",
        contract_id=contract["id"],
        signer_user_id="user-2",
        signer_frek_id="FREK-002",
        signer_role="counterparty",
        evidence_refs=["AUTHORITY-2"],
    )
    await legal_ops.transition_contract(
        actor_id="admin", contract_id=contract["id"], status="APPROVED"
    )

    calls = 0

    async def fake_notarize(package):
        nonlocal calls
        calls += 1
        return {
            **package,
            "anchored_at": "2026-09-10T16:00:00+00:00",
            "verification_status": "FREK_NOTARIZED",
            "frek_notary": {
                "height": 43,
                "payload_hash": "d" * 64,
                "block_hash": "e" * 64,
                "timestamp": "2026-09-10T16:00:00+00:00",
                "btc_anchored": False,
                "btc_block_height": None,
            },
        }

    monkeypatch.setattr(proof_bridge, "notarize_package", fake_notarize)
    kwargs = dict(
        actor_id="user-2",
        actor_frek_id="FREK-002",
        contract_id=contract["id"],
        document_hash="f" * 64,
        intent="SIGN",
    )
    first = await proof_bridge.create_contract_native_attestation(**kwargs)
    second = await proof_bridge.create_contract_native_attestation(**kwargs)
    assert first["id"] == second["id"]
    assert calls == 1
    assert await proof_db.native_signature_attestations.count_documents({}) == 1
