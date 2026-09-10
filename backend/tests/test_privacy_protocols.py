from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import evidence_graph, policy_registry, privacy_protocols, professional_governance


@pytest.fixture
async def privacy_protocol_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_privacy_protocol_test"]
    for module in (privacy_protocols, policy_registry, evidence_graph, professional_governance):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


async def _policy(key: str, privacy_protocol_db):
    return await policy_registry.register_version(
        actor_id="founder",
        policy_key=key,
        version="1.0.0",
        kind="POLICY",
        title=key,
        content={"evidence_first": True},
        effective_at="2026-09-10T00:00:00+00:00",
        evidence_refs=[key],
    )


@pytest.mark.asyncio
async def test_legal_basis_is_versioned_by_supersession(privacy_protocol_db):
    first = await privacy_protocols.register_legal_basis(
        actor_id="dpo", code="CONTRACT", label="Contract", jurisdiction="FR",
        authority_ref="DPO-REVIEW-1", rationale="Reviewed basis", evidence_refs=["SRC-1"]
    )
    second = await privacy_protocols.register_legal_basis(
        actor_id="dpo", code="CONTRACT", label="Contractual necessity", jurisdiction="FR",
        authority_ref="DPO-REVIEW-2", rationale="Updated reviewed basis", evidence_refs=["SRC-2"]
    )
    previous = await privacy_protocol_db.privacy_legal_bases.find_one({"id": first["id"]}, {"_id": 0})
    assert previous["status"] == "SUPERSEDED"
    assert second["supersedes_id"] == first["id"]


@pytest.mark.asyncio
async def test_purpose_and_minimisation_are_evidence_backed(privacy_protocol_db):
    await privacy_protocol_db.privacy_processing_activities.insert_one({"id": "PA-1", "purpose": "training delivery"})
    purpose = await privacy_protocols.assess_purpose_limitation(
        actor_id="dpo", processing_activity_id="PA-1", requested_purpose="advertising",
        compatible=False, rationale="Outside registered purpose", evidence_refs=["REVIEW-1"]
    )
    assert purpose["decision"] == "BLOCK_NEW_PROCESSING_PENDING_REVIEW"
    minimisation = await privacy_protocols.assess_data_minimisation(
        actor_id="dpo", processing_activity_id="PA-1",
        required_fields=["email"], collected_fields=["email", "birth_city"],
        rationale="Compare collection to operational need", evidence_refs=["SCHEMA-1"]
    )
    assert minimisation["pass"] is False
    assert minimisation["excess_fields"] == ["birth_city"]


@pytest.mark.asyncio
async def test_verified_frek_consent_requires_canonical_verification_evidence(privacy_protocol_db):
    await privacy_protocol_db.privacy_consents.insert_one({"id": "CONS-1"})
    with pytest.raises(ValueError, match="canonical verification evidence"):
        await privacy_protocols.record_consent_frek_proof(
            actor_id="dpo", consent_id="CONS-1", frek_proof_ref="FREK-1",
            proof_status="VERIFIED", evidence_refs=["LOCAL-ASSERTION"]
        )
    verified = await privacy_protocols.record_consent_frek_proof(
        actor_id="dpo", consent_id="CONS-1", frek_proof_ref="FREK-1",
        proof_status="VERIFIED", evidence_refs=["FREK_VERIFY:verification-1"]
    )
    assert verified["proof_status"] == "VERIFIED"
    assert verified["legal_effect"] == "none"


@pytest.mark.asyncio
async def test_restriction_objection_workflow_is_explicit(privacy_protocol_db):
    await privacy_protocol_db.privacy_processing_activities.insert_one({"id": "PA-1"})
    row = await privacy_protocols.create_restriction_or_objection(
        actor_id="user-1", user_id="user-1", request_type="OBJECTION",
        processing_activity_id="PA-1", rationale="Object to this purpose", evidence_refs=["REQ-1"]
    )
    for target in ("IDENTITY_VERIFIED", "IN_REVIEW", "APPROVED", "EXECUTED", "CLOSED"):
        row = await privacy_protocols.transition_restriction_or_objection(
            actor_id="dpo", request_id=row["id"], status=target, evidence_refs=[f"E-{target}"]
        )
    assert row["status"] == "CLOSED"


@pytest.mark.asyncio
async def test_pseudonymisation_and_residency_require_canonical_policy(privacy_protocol_db):
    await privacy_protocol_db.privacy_data_classes.insert_one({"code": "IDENTITY"})
    pseudo_policy = await _policy("PSEUDONYMISATION", privacy_protocol_db)
    residency_policy = await _policy("DATA_RESIDENCY", privacy_protocol_db)
    pseudo = await privacy_protocols.register_pseudonymisation_policy(
        actor_id="dpo", name="Identity token", operation="VAULT_REFERENCE",
        key_or_vault_ref="vault://privacy/identity", policy_version_id=pseudo_policy["id"],
        evidence_refs=["ARCH-1"]
    )
    assert pseudo["secret_material_stored"] is False
    residency = await privacy_protocols.register_data_residency_rule(
        actor_id="dpo", data_class_code="IDENTITY", allowed_regions=["EU"],
        prohibited_regions=["US"], policy_version_id=residency_policy["id"], evidence_refs=["RES-1"]
    )
    assert residency["allowed_regions"] == ["EU"]


@pytest.mark.asyncio
async def test_breach_investigation_requires_canonical_privacy_incident(privacy_protocol_db):
    await privacy_protocol_db.incidents.insert_one({"id": "INC-SEC", "domains": ["SECURITY"]})
    with pytest.raises(ValueError, match="canonical PRIVACY incident"):
        await privacy_protocols.open_breach_investigation(
            actor_id="dpo", incident_id="INC-SEC", hypothesis="possible breach", evidence_refs=["LOG"]
        )
    await privacy_protocol_db.incidents.insert_one({"id": "INC-PRI", "domains": ["PRIVACY"]})
    investigation = await privacy_protocols.open_breach_investigation(
        actor_id="dpo", incident_id="INC-PRI", hypothesis="possible disclosure", evidence_refs=["LOG-2"]
    )
    finding = await privacy_protocols.record_breach_finding(
        actor_id="dpo", investigation_id=investigation["id"], finding="Exposure confirmed",
        evidence_refs=["FORENSICS-1"], status="ASSESSED"
    )
    assert finding["status"] == "ASSESSED"


@pytest.mark.asyncio
async def test_minor_user_assessment_never_infers_legal_outcome(privacy_protocol_db):
    row = await privacy_protocols.assess_minor_user(
        actor_id="dpo", user_id="user-minor", jurisdiction="FR", age_or_age_band="13-15",
        outcome="REVIEW_REQUIRED", authority_ref="COUNSEL-1",
        rationale="Needs jurisdiction-specific review", evidence_refs=["AGE-EVID-1"]
    )
    assert row["outcome"] == "REVIEW_REQUIRED"


@pytest.mark.asyncio
async def test_jurisdiction_pack_refuses_unresolved_regulatory_scope(privacy_protocol_db):
    policy = await _policy("PRIVACY_JURISDICTION", privacy_protocol_db)
    await privacy_protocol_db.regulatory_scopes.insert_one(
        {"id": "REGS-1", "status": "REVIEW_REQUIRED", "current_decision_id": None}
    )
    with pytest.raises(ValueError, match="unresolved regulatory scope"):
        await privacy_protocols.create_jurisdiction_pack(
            actor_id="dpo", jurisdiction="FR", regulatory_scope_ids=["REGS-1"],
            policy_version_ids=[policy["id"]], evidence_refs=["PACK-1"]
        )


@pytest.mark.asyncio
async def test_privacy_evidence_pack_reuses_canonical_evidence_graph(privacy_protocol_db):
    access_policy = await _policy("EVIDENCE_ACCESS", privacy_protocol_db)
    node = await evidence_graph.register_node(
        actor_id="dpo", source_type="PRIVACY_REVIEW", source_id="REV-1",
        content_hash="a" * 64, provenance_refs=["SRC-1"],
        access_policy_version_id=access_policy["id"]
    )
    pack = await privacy_protocols.create_privacy_evidence_pack(
        actor_id="dpo", title="Privacy audit pack", evidence_node_ids=[node["id"]],
        evidence_refs=["AUDIT-1"]
    )
    assert pack["consumer"] == "PRIVACY"
    assert pack["composition_mode"] == "REFERENCE_ONLY"
