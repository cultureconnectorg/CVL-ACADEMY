from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import evidence_graph, native_attestation_verifier, professional_governance
from services import proof_bridge, trust_signature


@pytest.fixture
async def trust_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_trust_signature_test"]
    for module in (
        evidence_graph,
        professional_governance,
        proof_bridge,
        trust_signature,
    ):
        monkeypatch.setattr(module, "db", test_db)

    async def fake_notarize(package):
        return {
            **package,
            "anchored_at": "2026-09-10T00:00:00+00:00",
            "verification_status": "FREK_NOTARIZED",
            "frek_notary": {
                "height": 7,
                "payload_hash": "b" * 64,
                "block_hash": "c" * 64,
                "timestamp": "2026-09-10T00:00:00+00:00",
                "btc_anchored": False,
                "btc_block_height": None,
            },
        }

    async def fake_fetch(package_id):
        return {
            "payload_id": package_id,
            "block": {"block_hash": "c" * 64, "payload_hash": "b" * 64},
        }

    monkeypatch.setattr(proof_bridge, "notarize_package", fake_notarize)
    monkeypatch.setattr(native_attestation_verifier, "fetch_frek_proof", fake_fetch)
    yield test_db
    client.close()


@pytest.mark.asyncio
async def test_exact_version_hash_and_signer_identity_are_required(trust_db):
    request = await trust_signature.create_signature_request(
        actor_id="admin",
        subject_type="QUALITY_ATTENDANCE",
        subject_id="ATT-1",
        document_version_id="VER-1",
        document_hash="a" * 64,
        required_signers=[
            {
                "signer_user_id": "user-1",
                "signer_frek_id": "FREK-1",
                "signer_role": "LEARNER",
            }
        ],
        evidence_refs=["ATT-1"],
    )
    with pytest.raises(ValueError, match="differs"):
        await trust_signature.sign_intent(
            actor_id="user-1",
            actor_frek_id="FREK-1",
            signature_request_id=request["id"],
            document_hash="d" * 64,
            intent="SIGN",
        )
    signature = await trust_signature.sign_intent(
        actor_id="user-1",
        actor_frek_id="FREK-1",
        signature_request_id=request["id"],
        document_hash="a" * 64,
        intent="SIGN",
    )
    assert signature["document_version_id"] == "VER-1"
    assert signature["legal_effect"] == "none"


@pytest.mark.asyncio
async def test_independent_verification_and_multisig_completion(trust_db):
    request = await trust_signature.create_signature_request(
        actor_id="admin",
        subject_type="CONTRACT",
        subject_id="CTR-1",
        document_version_id="VER-1",
        document_hash="a" * 64,
        required_signers=[
            {"signer_user_id": "u1", "signer_frek_id": "F1", "signer_role": "PARTY_A"},
            {"signer_user_id": "u2", "signer_frek_id": "F2", "signer_role": "PARTY_B"},
        ],
        evidence_refs=["CTR-1"],
    )
    first = await trust_signature.sign_intent(
        actor_id="u1",
        actor_frek_id="F1",
        signature_request_id=request["id"],
        document_hash="a" * 64,
        intent="SIGN",
    )
    await trust_signature.verify_signature(actor_id="reviewer", signature_id=first["id"])
    gate = await trust_signature.evaluate_multisignature(request["id"])
    assert gate["pass"] is False
    assert gate["verified_count"] == 1

    second = await trust_signature.sign_intent(
        actor_id="u2",
        actor_frek_id="F2",
        signature_request_id=request["id"],
        document_hash="a" * 64,
        intent="SIGN",
    )
    await trust_signature.verify_signature(actor_id="reviewer", signature_id=second["id"])
    gate = await trust_signature.evaluate_multisignature(request["id"])
    assert gate["pass"] is True
    stored = await trust_db.trust_signature_requests.find_one({"id": request["id"]})
    assert stored["status"] == "COMPLETE"


@pytest.mark.asyncio
async def test_revoked_authority_invalidates_verification(trust_db):
    request = await trust_signature.create_signature_request(
        actor_id="admin",
        subject_type="POLICY",
        subject_id="POL-1",
        document_version_id="VER-1",
        document_hash="a" * 64,
        required_signers=[
            {"signer_user_id": "u1", "signer_frek_id": "F1", "signer_role": "OWNER"}
        ],
        evidence_refs=["POL-1"],
    )
    auth = await trust_db.trust_signer_authorizations.find_one(
        {"signature_request_id": request["id"]}, {"_id": 0}
    )
    signature = await trust_signature.sign_intent(
        actor_id="u1",
        actor_frek_id="F1",
        signature_request_id=request["id"],
        document_hash="a" * 64,
        intent="SIGN",
    )
    await trust_signature.revoke_signer_authority(
        actor_id="admin",
        authorization_id=auth["id"],
        evidence_refs=["REV-1"],
    )
    verification = await trust_signature.verify_signature(
        actor_id="reviewer", signature_id=signature["id"]
    )
    assert verification["status"] == "FAILED"
    assert verification["checks"]["authorization_active"] is False


@pytest.mark.asyncio
async def test_document_invalidation_revokes_all_active_authorities(trust_db):
    request = await trust_signature.create_signature_request(
        actor_id="admin",
        subject_type="LEGAL_DOCUMENT",
        subject_id="DOC-1",
        document_version_id="V1",
        document_hash="a" * 64,
        required_signers=[
            {"signer_user_id": "u1", "signer_frek_id": "F1", "signer_role": "OWNER"}
        ],
        evidence_refs=["DOC-1"],
    )
    invalidated = await trust_signature.invalidate_document_version(
        actor_id="admin",
        signature_request_id=request["id"],
        replacement_version_id="V2",
        replacement_hash="d" * 64,
        evidence_refs=["NEW-VERSION"],
    )
    assert invalidated["status"] == "INVALIDATED"
    assert await trust_db.trust_signer_authorizations.count_documents(
        {"signature_request_id": request["id"], "status": "AUTHORIZED"}
    ) == 0


@pytest.mark.asyncio
async def test_delegation_requires_explicit_evidence(trust_db):
    request = await trust_signature.create_signature_request(
        actor_id="admin",
        subject_type="CONTRACT",
        subject_id="CTR-2",
        document_version_id="V1",
        document_hash="a" * 64,
        required_signers=[
            {"signer_user_id": "u1", "signer_frek_id": "F1", "signer_role": "DIRECTOR"}
        ],
        evidence_refs=["CTR-2"],
    )
    auth = await trust_db.trust_signer_authorizations.find_one(
        {"signature_request_id": request["id"]}, {"_id": 0}
    )
    with pytest.raises(ValueError, match="requires evidence"):
        await trust_signature.delegate_signer_authority(
            actor_id="admin",
            authorization_id=auth["id"],
            delegate_user_id="u2",
            delegate_frek_id="F2",
            delegate_role="DELEGATE",
            evidence_refs=[],
        )
