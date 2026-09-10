from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import authority_policy, legal_documents, legal_ops, legal_policy
from services import policy_registry, professional_governance as governance


@pytest.fixture
async def legal_documents_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_legal_documents_test"]
    for module in (
        authority_policy,
        legal_documents,
        legal_ops,
        legal_policy,
        policy_registry,
        governance,
    ):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


async def _setup_document():
    case = await governance.create_case(
        actor_id="admin-1",
        title="Legal publication",
        domain="LEGAL",
        description="Publish Academy terms",
        sensitivity="LEGAL_PRIVILEGED",
    )
    matter = await legal_ops.create_legal_matter(
        actor_id="admin-1",
        title="Terms publication",
        matter_type="POLICY",
        jurisdiction="FR",
        case_id=case["id"],
        evidence_refs=["MATTER-EVID-1"],
    )
    doc = await legal_documents.create_document(
        actor_id="admin-1",
        case_id=case["id"],
        matter_id=matter["id"],
        document_type="CGU",
        title="CVLN Academy Terms",
        jurisdiction="FR",
        content_hash="1" * 64,
        evidence_refs=["SOURCE-1"],
    )
    return case, matter, doc


async def _authority_policy(key, action, level="A4_CVL_AUTHORITY"):
    return await authority_policy.register_policy_version(
        actor_id="founder-1",
        policy_key=key,
        version="1.0.0",
        title=key,
        effective_at="2026-09-10T00:00:00+00:00",
        doctrine_ref="FD-L02/L04",
        evidence_refs=[f"MASTER:{key}"],
        rules=[
            {
                "id": f"{key}-ALLOW",
                "priority": 1,
                "effect": "ALLOW",
                "reason": "Authorized by explicit Academy legal policy.",
                "conditions": {
                    "actor_roles": ["founder"],
                    "actions": [action],
                    "domains": ["LEGAL"],
                    "minimum_authority_level": level,
                },
            }
        ],
    )


@pytest.mark.asyncio
async def test_legal_versions_reuse_governance_registry_and_chain_parent(legal_documents_db):
    _case, _matter, doc = await _setup_document()
    first_id = doc["current_version_id"]
    second = await legal_documents.add_version(
        actor_id="admin-1",
        document_id=doc["id"],
        content_hash="2" * 64,
        evidence_refs=["REVISION-1"],
    )
    assert second["parent_version_id"] == first_id
    assert second["metadata"]["legal_document_id"] == doc["id"]
    first = await legal_documents_db.governance_document_versions.find_one(
        {"id": first_id}, {"_id": 0}
    )
    assert first["content_hash"] == "1" * 64


@pytest.mark.asyncio
async def test_document_approval_requires_distinct_internal_and_external_when_policy_requires_it(
    legal_documents_db,
):
    _case, matter, doc = await _setup_document()
    await legal_documents.transition_document(
        actor_id="admin-1", document_id=doc["id"], status="IN_REVIEW"
    )
    await legal_documents_db.legal_matters.update_one(
        {"id": matter["id"]}, {"$set": {"external_review_required": True}}
    )
    internal_policy = await _authority_policy(
        "LEGAL_INTERNAL_APPROVAL", "LEGAL_INTERNAL_APPROVE"
    )
    await legal_policy.record_approval(
        actor_id="founder-1",
        actor_role="founder",
        authority_level="A4_CVL_AUTHORITY",
        matter_id=matter["id"],
        approval_kind="INTERNAL_APPROVED",
        policy_version_id=internal_policy["id"],
        rationale="Internal approval.",
        evidence_refs=["INT-APP-1"],
    )
    with pytest.raises(ValueError, match="not externally approved"):
        await legal_documents.transition_document(
            actor_id="founder-1", document_id=doc["id"], status="APPROVED"
        )


@pytest.mark.asyncio
async def test_signed_rejects_unverified_attestation(legal_documents_db):
    _case, matter, doc = await _setup_document()
    await legal_documents.transition_document(
        actor_id="admin-1", document_id=doc["id"], status="IN_REVIEW"
    )
    policy = await _authority_policy(
        "LEGAL_INTERNAL_APPROVAL", "LEGAL_INTERNAL_APPROVE"
    )
    await legal_policy.record_approval(
        actor_id="founder-1",
        actor_role="founder",
        authority_level="A4_CVL_AUTHORITY",
        matter_id=matter["id"],
        approval_kind="INTERNAL_APPROVED",
        policy_version_id=policy["id"],
        rationale="Internal approval.",
        evidence_refs=["INT-APP-2"],
    )
    await legal_documents.transition_document(
        actor_id="founder-1", document_id=doc["id"], status="APPROVED"
    )
    await legal_documents_db.native_signature_attestations.insert_one(
        {
            "id": "NSIG-UNVERIFIED",
            "document_hash": "1" * 64,
            "status": "FREK_NOTARIZED",
        }
    )
    with pytest.raises(ValueError, match="verified native signature evidence"):
        await legal_documents.transition_document(
            actor_id="founder-1",
            document_id=doc["id"],
            status="SIGNED",
            evidence_refs=["NSIG-UNVERIFIED"],
        )


@pytest.mark.asyncio
async def test_publish_is_a4_policy_gated_and_binds_exact_immutable_version(
    legal_documents_db,
):
    _case, matter, doc = await _setup_document()
    await legal_documents.transition_document(
        actor_id="admin-1", document_id=doc["id"], status="IN_REVIEW"
    )
    approval_policy = await _authority_policy(
        "LEGAL_INTERNAL_APPROVAL", "LEGAL_INTERNAL_APPROVE"
    )
    await legal_policy.record_approval(
        actor_id="founder-1",
        actor_role="founder",
        authority_level="A4_CVL_AUTHORITY",
        matter_id=matter["id"],
        approval_kind="INTERNAL_APPROVED",
        policy_version_id=approval_policy["id"],
        rationale="Internal approval.",
        evidence_refs=["INT-APP-3"],
    )
    await legal_documents.transition_document(
        actor_id="founder-1", document_id=doc["id"], status="APPROVED"
    )
    await legal_documents_db.native_signature_attestations.insert_one(
        {
            "id": "NSIG-VERIFIED",
            "document_hash": "1" * 64,
            "status": "FREK_NOTARIZED",
        }
    )
    await legal_documents_db.native_signature_verifications.insert_one(
        {
            "id": "NSIGVER-1",
            "attestation_id": "NSIG-VERIFIED",
            "status": "VERIFIED_FREK",
        }
    )
    await legal_documents.transition_document(
        actor_id="founder-1",
        document_id=doc["id"],
        status="SIGNED",
        evidence_refs=["NSIG-VERIFIED"],
    )
    publication_policy = await _authority_policy(
        "LEGAL_PUBLICATION_AUTHORITY", "LEGAL_DOCUMENT_PUBLISH"
    )
    result = await legal_documents.publish_document(
        actor_id="founder-1",
        actor_role="founder",
        authority_level="A4_CVL_AUTHORITY",
        document_id=doc["id"],
        policy_version_id=publication_policy["id"],
        evidence_refs=["PUBLICATION-EVID-1"],
    )
    assert result["publication"]["version_id"] == doc["current_version_id"]
    assert result["publication"]["content_hash"] == "1" * 64
    assert result["publication"]["authority_decision_id"]
