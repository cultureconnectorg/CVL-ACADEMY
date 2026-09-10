from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import assurance_core
from services import data_classification
from services import policy_registry
from services import professional_governance


@pytest.fixture
async def classification_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_data_classification_test"]
    for module in (
        assurance_core,
        data_classification,
        policy_registry,
        professional_governance,
    ):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


async def _policy():
    return await policy_registry.register_version(
        actor_id="founder-1",
        policy_key="DATA_CLASSIFICATION",
        version="1.0.0",
        kind="POLICY",
        title="Academy data classification",
        content={"rule": "explicit classification only"},
        effective_at="2026-09-10T00:00:00+00:00",
        evidence_refs=["XCP-002", "FOUNDER:CLASSIFY_ALL"],
    )


@pytest.mark.asyncio
async def test_declared_resource_is_unclassified_until_explicit_decision(classification_db):
    resource = await data_classification.declare_resource(
        actor_id="admin-1",
        resource_kind="provider",
        resource_type="processor",
        resource_id="PROC-1",
        owner="privacy",
        source="academy",
    )
    assert resource["classification_status"] == "UNCLASSIFIED"
    gate = await data_classification.unclassified_gate()
    assert gate["pass"] is False
    assert gate["unclassified_count"] == 1


@pytest.mark.asyncio
async def test_classification_reuses_existing_privacy_taxonomy_and_policy_registry(classification_db):
    await assurance_core.register_data_class(
        actor_id="dpo-1",
        code="IDENTITY",
        name="Identity data",
        sensitivity="sensitive",
        retention_days=3650,
        legal_basis_required=True,
    )
    policy = await _policy()
    resource = await data_classification.declare_resource(
        actor_id="admin-1",
        resource_kind="data",
        resource_type="learner_profile",
        resource_id="USR-1",
        owner="academy",
        source="mongo",
        metadata={"collection": "users"},
    )
    classification = await data_classification.classify_resource(
        actor_id="dpo-1",
        resource_record_id=resource["id"],
        data_class_code="IDENTITY",
        policy_version_id=policy["id"],
        rationale="Profile contains identity attributes",
        evidence_refs=["SCHEMA:users"],
        handling_controls={"access": "need_to_know"},
    )
    assert classification["data_class_code"] == "IDENTITY"
    assert classification["policy_version_id"] == policy["id"]
    assert classification["sensitivity"] == "SENSITIVE"
    assert len(classification["classification_hash"]) == 64
    gate = await data_classification.unclassified_gate()
    assert gate["pass"] is True


@pytest.mark.asyncio
async def test_unknown_data_class_is_rejected(classification_db):
    policy = await _policy()
    resource = await data_classification.declare_resource(
        actor_id="admin-1",
        resource_kind="object",
        resource_type="certificate",
        resource_id="CERT-1",
        owner="academy",
        source="academy",
    )
    with pytest.raises(LookupError, match="registered data class not found"):
        await data_classification.classify_resource(
            actor_id="dpo-1",
            resource_record_id=resource["id"],
            data_class_code="INVENTED",
            policy_version_id=policy["id"],
            rationale="Do not invent taxonomy",
            evidence_refs=["TEST"],
        )


@pytest.mark.asyncio
async def test_wrong_policy_cannot_govern_classification(classification_db):
    await assurance_core.register_data_class(
        actor_id="dpo-1",
        code="PUBLIC",
        name="Public data",
        sensitivity="public",
        retention_days=None,
        legal_basis_required=False,
    )
    policy = await policy_registry.register_version(
        actor_id="founder-1",
        policy_key="LEGAL_REVIEW",
        version="1.0.0",
        kind="POLICY",
        title="Legal review",
        content={"review": True},
        effective_at="2026-09-10T00:00:00+00:00",
        evidence_refs=["LEGAL"],
    )
    resource = await data_classification.declare_resource(
        actor_id="admin-1",
        resource_kind="object",
        resource_type="landing_page",
        resource_id="HOME",
        owner="academy",
        source="frontend",
    )
    with pytest.raises(ValueError, match="not a DATA_CLASSIFICATION policy"):
        await data_classification.classify_resource(
            actor_id="dpo-1",
            resource_record_id=resource["id"],
            data_class_code="PUBLIC",
            policy_version_id=policy["id"],
            rationale="Public web content",
            evidence_refs=["ROUTE:/"],
        )


@pytest.mark.asyncio
async def test_reclassification_is_append_only_and_supersedes_previous(classification_db):
    for code, sensitivity in (("INTERNAL", "internal"), ("SENSITIVE", "sensitive")):
        await assurance_core.register_data_class(
            actor_id="dpo-1",
            code=code,
            name=code.title(),
            sensitivity=sensitivity,
            retention_days=365,
            legal_basis_required=True,
        )
    policy = await _policy()
    resource = await data_classification.declare_resource(
        actor_id="admin-1",
        resource_kind="provider",
        resource_type="integration",
        resource_id="EXT-1",
        owner="platform",
        source="academy",
    )
    first = await data_classification.classify_resource(
        actor_id="dpo-1",
        resource_record_id=resource["id"],
        data_class_code="INTERNAL",
        policy_version_id=policy["id"],
        rationale="Initial assessment",
        evidence_refs=["ASSESS-1"],
    )
    second = await data_classification.classify_resource(
        actor_id="dpo-1",
        resource_record_id=resource["id"],
        data_class_code="SENSITIVE",
        policy_version_id=policy["id"],
        rationale="Provider now receives personal metadata",
        evidence_refs=["ASSESS-2"],
    )
    old = await classification_db.resource_classifications.find_one(
        {"id": first["id"]}, {"_id": 0}
    )
    assert old["status"] == "SUPERSEDED"
    assert old["superseded_by"] == second["id"]
    assert second["supersedes_classification_id"] == first["id"]
    assert await classification_db.resource_classifications.count_documents({}) == 2


@pytest.mark.asyncio
async def test_declaration_is_idempotent_for_same_canonical_resource(classification_db):
    kwargs = dict(
        actor_id="admin-1",
        resource_kind="provider",
        resource_type="processor",
        resource_id="PROC-9",
        owner="privacy",
        source="academy",
    )
    first = await data_classification.declare_resource(**kwargs)
    second = await data_classification.declare_resource(**kwargs)
    assert first["id"] == second["id"]
    assert await classification_db.classification_resources.count_documents({}) == 1
