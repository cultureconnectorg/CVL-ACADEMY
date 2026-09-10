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
async def test_contract_lifecycle_rejects_skips_and_requires_evidence_for_signature(legal_db):
    matter = await legal_ops.create_legal_matter(
        actor_id="legal-1", title="Trainer agreement", matter_type="contract"
    )
    contract = await legal_ops.create_contract(
        actor_id="legal-1",
        title="Trainer services agreement",
        contract_type="services",
        counterparty="Trainer Example",
        matter_id=matter["id"],
        jurisdiction="FR",
    )

    with pytest.raises(ValueError, match="invalid contract transition"):
        await legal_ops.transition_contract(
            actor_id="legal-1", contract_id=contract["id"], status="ACTIVE"
        )

    review = await legal_ops.transition_contract(
        actor_id="legal-1", contract_id=contract["id"], status="IN_REVIEW"
    )
    approved = await legal_ops.transition_contract(
        actor_id="legal-1", contract_id=contract["id"], status="APPROVED"
    )
    assert review["status"] == "IN_REVIEW"
    assert approved["status"] == "APPROVED"

    with pytest.raises(ValueError, match="requires evidence"):
        await legal_ops.transition_contract(
            actor_id="legal-1", contract_id=contract["id"], status="SIGNED"
        )

    signed = await legal_ops.transition_contract(
        actor_id="legal-1",
        contract_id=contract["id"],
        status="SIGNED",
        evidence_refs=["SIGNATURE-EVIDENCE-1"],
    )
    assert signed["status"] == "SIGNED"
    assert signed["last_transition_evidence_refs"] == ["SIGNATURE-EVIDENCE-1"]


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
    await legal_ops.transition_contract(
        actor_id="legal-1",
        contract_id=contract["id"],
        status="SIGNED",
        evidence_refs=["SIG-1"],
    )
    await legal_ops.transition_contract(
        actor_id="legal-1", contract_id=contract["id"], status="ACTIVE"
    )

    with pytest.raises(ValueError, match="requires evidence"):
        await legal_ops.transition_contract(
            actor_id="legal-1", contract_id=contract["id"], status="TERMINATED"
        )
