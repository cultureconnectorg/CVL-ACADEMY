from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import legal_ops


@pytest.fixture
async def legal_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_legal_ops_test"]
    monkeypatch.setattr(legal_ops, "db", test_db)
    yield test_db
    client.close()


@pytest.mark.asyncio
async def test_create_and_transition_legal_matter(legal_db):
    matter = await legal_ops.create_legal_matter(
        actor_id="legal-1",
        title="Review learner terms",
        matter_type="terms_review",
        jurisdiction="FR",
        owner_id="lawyer-1",
        evidence_refs=["DOC-1"],
    )
    assert matter["status"] == "OPEN"
    assert matter["matter_type"] == "TERMS_REVIEW"

    reviewed = await legal_ops.transition_legal_matter(
        actor_id="legal-1", matter_id=matter["id"], status="in_review"
    )
    assert reviewed["status"] == "IN_REVIEW"


@pytest.mark.asyncio
async def test_review_policy_decision_requires_explicit_policy_and_rationale(legal_db):
    matter = await legal_ops.create_legal_matter(
        actor_id="legal-1", title="Contract question", matter_type="contract"
    )

    with pytest.raises(ValueError, match="policy_ref"):
        await legal_ops.record_review_policy_decision(
            actor_id="legal-1",
            matter_id=matter["id"],
            external_review_required=True,
            rationale="Needs counsel",
            policy_ref="",
        )

    decision = await legal_ops.record_review_policy_decision(
        actor_id="legal-1",
        matter_id=matter["id"],
        external_review_required=True,
        rationale="Jurisdictional interpretation requires external counsel",
        policy_ref="LEGAL-REVIEW-POLICY-v1",
        evidence_refs=["POLICY-EVID-1"],
    )
    assert decision["external_review_required"] is True
    stored = await legal_db.legal_matters.find_one({"id": matter["id"]}, {"_id": 0})
    assert stored["status"] == "WAITING_EXTERNAL"


@pytest.mark.asyncio
async def test_contract_signed_transition_requires_accepted_signature_decision(legal_db):
    contract = await legal_ops.create_contract(
        actor_id="legal-1",
        title="Trainer services agreement",
        contract_type="services",
        counterparty="Trainer Example",
        jurisdiction="FR",
    )

    with pytest.raises(ValueError, match="invalid contract transition"):
        await legal_ops.transition_contract(
            actor_id="legal-1", contract_id=contract["id"], status="ACTIVE"
        )

    await legal_ops.transition_contract(
        actor_id="legal-1", contract_id=contract["id"], status="IN_REVIEW"
    )
    approved = await legal_ops.transition_contract(
        actor_id="legal-1", contract_id=contract["id"], status="APPROVED"
    )
    assert approved["status"] == "APPROVED"

    with pytest.raises(ValueError, match="requires evidence"):
        await legal_ops.transition_contract(
            actor_id="legal-1", contract_id=contract["id"], status="SIGNED"
        )

    with pytest.raises(ValueError, match="accepted signature decision"):
        await legal_ops.transition_contract(
            actor_id="legal-1",
            contract_id=contract["id"],
            status="SIGNED",
            evidence_refs=["ARBITRARY-SIGNATURE-REF"],
        )

    decision = await legal_ops.record_signature_decision(
        actor_id="legal-1",
        contract_id=contract["id"],
        policy_ref="SIGNATURE-ACCEPTANCE-v1",
        rationale="External signature evidence reviewed by authorized human",
        external_evidence_refs=["DOCUSIGN-ENVELOPE-123"],
    )
    assert decision["outcome"] == "ACCEPTED_FOR_LIFECYCLE"
    assert decision["legal_effect_claimed"] is False

    signed = await legal_ops.transition_contract(
        actor_id="legal-1",
        contract_id=contract["id"],
        status="SIGNED",
        evidence_refs=[decision["id"]],
    )
    assert signed["status"] == "SIGNED"
    assert signed["last_transition_evidence_refs"] == [decision["id"]]


@pytest.mark.asyncio
async def test_native_signature_decision_requires_verified_attestation(legal_db):
    contract = await legal_ops.create_contract(
        actor_id="legal-1",
        title="Artist agreement",
        contract_type="services",
        counterparty="Artist",
    )
    await legal_ops.transition_contract(
        actor_id="legal-1", contract_id=contract["id"], status="IN_REVIEW"
    )
    await legal_ops.transition_contract(
        actor_id="legal-1", contract_id=contract["id"], status="APPROVED"
    )
    await legal_db.native_signature_attestations.insert_one(
        {"id": "NSIG-1", "contract_id": contract["id"]}
    )

    with pytest.raises(ValueError, match="not independently verified"):
        await legal_ops.record_signature_decision(
            actor_id="legal-1",
            contract_id=contract["id"],
            policy_ref="SIGNATURE-ACCEPTANCE-v1",
            rationale="Native signature verification required",
            native_attestation_ids=["NSIG-1"],
        )

    await legal_db.native_signature_verifications.insert_one(
        {
            "id": "NSIGVER-1",
            "attestation_id": "NSIG-1",
            "status": "VERIFIED_FREK",
            "verified_at": "2026-09-10T16:00:00Z",
        }
    )
    decision = await legal_ops.record_signature_decision(
        actor_id="legal-1",
        contract_id=contract["id"],
        policy_ref="SIGNATURE-ACCEPTANCE-v1",
        rationale="FREK proof verified and accepted under policy",
        native_attestation_ids=["NSIG-1"],
    )
    assert decision["native_attestation_ids"] == ["NSIG-1"]


@pytest.mark.asyncio
async def test_btc_policy_rejects_frek_only_verification(legal_db):
    contract = await legal_ops.create_contract(
        actor_id="legal-1",
        title="High assurance agreement",
        contract_type="services",
        counterparty="Partner",
    )
    await legal_ops.transition_contract(
        actor_id="legal-1", contract_id=contract["id"], status="IN_REVIEW"
    )
    await legal_ops.transition_contract(
        actor_id="legal-1", contract_id=contract["id"], status="APPROVED"
    )
    await legal_db.native_signature_attestations.insert_one(
        {"id": "NSIG-BTC", "contract_id": contract["id"]}
    )
    await legal_db.native_signature_verifications.insert_one(
        {
            "id": "NSIGVER-FREK",
            "attestation_id": "NSIG-BTC",
            "status": "VERIFIED_FREK",
            "verified_at": "2026-09-10T16:00:00Z",
        }
    )

    with pytest.raises(ValueError, match="not independently verified"):
        await legal_ops.record_signature_decision(
            actor_id="legal-1",
            contract_id=contract["id"],
            policy_ref="HIGH-ASSURANCE-SIGNATURE-v1",
            rationale="This contract requires BTC anchored proof",
            native_attestation_ids=["NSIG-BTC"],
            require_btc_anchor=True,
        )

    await legal_db.native_signature_verifications.insert_one(
        {
            "id": "NSIGVER-BTC",
            "attestation_id": "NSIG-BTC",
            "status": "VERIFIED_FREK_BTC",
            "verified_at": "2026-09-10T17:00:00Z",
        }
    )
    decision = await legal_ops.record_signature_decision(
        actor_id="legal-1",
        contract_id=contract["id"],
        policy_ref="HIGH-ASSURANCE-SIGNATURE-v1",
        rationale="BTC anchored FREK proof satisfies this policy",
        native_attestation_ids=["NSIG-BTC"],
        require_btc_anchor=True,
    )
    assert decision["require_btc_anchor"] is True


@pytest.mark.asyncio
async def test_contract_requires_existing_legal_matter_when_linked(legal_db):
    with pytest.raises(LookupError, match="legal matter not found"):
        await legal_ops.create_contract(
            actor_id="legal-1",
            title="Invalid contract",
            contract_type="services",
            counterparty="Example",
            matter_id="LMAT-missing",
        )


@pytest.mark.asyncio
async def test_termination_cannot_be_recorded_without_evidence(legal_db):
    contract = await legal_ops.create_contract(
        actor_id="legal-1",
        title="Active agreement",
        contract_type="services",
        counterparty="Partner",
    )
    for state in ("IN_REVIEW", "APPROVED"):
        await legal_ops.transition_contract(
            actor_id="legal-1", contract_id=contract["id"], status=state
        )
    decision = await legal_ops.record_signature_decision(
        actor_id="legal-1",
        contract_id=contract["id"],
        policy_ref="SIGNATURE-ACCEPTANCE-v1",
        rationale="External evidence accepted",
        external_evidence_refs=["SIG-1"],
    )
    await legal_ops.transition_contract(
        actor_id="legal-1",
        contract_id=contract["id"],
        status="SIGNED",
        evidence_refs=[decision["id"]],
    )
    await legal_ops.transition_contract(
        actor_id="legal-1", contract_id=contract["id"], status="ACTIVE"
    )

    with pytest.raises(ValueError, match="requires evidence"):
        await legal_ops.transition_contract(
            actor_id="legal-1", contract_id=contract["id"], status="TERMINATED"
        )
