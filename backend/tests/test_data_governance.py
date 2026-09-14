from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import (
    authority_policy,
    data_classification,
    data_governance,
    policy_registry,
    professional_governance,
)


@pytest.fixture
async def data_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_data_governance_test"]
    for module in (
        authority_policy,
        data_classification,
        data_governance,
        policy_registry,
        professional_governance,
    ):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


@pytest.mark.asyncio
async def test_dataset_source_hash_lineage_and_archive_are_explicit(data_db):
    parent = await data_governance.register_dataset(
        actor_id="admin",
        name="Learning events",
        source_system="academy",
        source_ref="mongo:listening-events",
        content_hash="a" * 64,
        owner="academy",
        evidence_refs=["SCHEMA-1"],
    )
    child = await data_governance.register_dataset(
        actor_id="admin",
        name="Aggregates",
        source_system="academy",
        source_ref="job:aggregate-v1",
        content_hash="b" * 64,
        owner="academy",
        evidence_refs=["JOB-1"],
    )
    lineage = await data_governance.record_lineage(
        actor_id="admin",
        parent_dataset_id=parent["id"],
        child_dataset_id=child["id"],
        transformation="aggregate counts",
        code_or_job_ref="git:abc",
        evidence_refs=["RUN-1"],
    )
    assert lineage["parent_dataset_id"] == parent["id"]
    archived = await data_governance.archive_dataset(
        actor_id="admin",
        dataset_id=parent["id"],
        archive_ref="object://archive/1",
        archive_hash="c" * 64,
        evidence_refs=["ARCHIVE-1"],
    )
    assert archived["status"] == "ARCHIVED"
    assert archived["archive_hash"] == "c" * 64


@pytest.mark.asyncio
async def test_personal_archive_cannot_become_commercial_without_verified_anonymisation(data_db):
    source = await data_governance.register_dataset(
        actor_id="admin",
        name="Personal",
        source_system="academy",
        source_ref="mongo:users",
        content_hash="a" * 64,
        owner="academy",
        evidence_refs=["SCHEMA"],
    )
    derived = await data_governance.register_dataset(
        actor_id="admin",
        name="Derived",
        source_system="academy",
        source_ref="job:anon",
        content_hash="b" * 64,
        owner="academy",
        evidence_refs=["JOB"],
    )
    with pytest.raises(ValueError, match="verified anonymisation"):
        await data_governance.register_anonymised_derived_asset(
            actor_id="admin",
            source_dataset_id=source["id"],
            derived_dataset_id=derived["id"],
            anonymisation_execution_ref="ANON-MISSING",
            evidence_refs=["ANON"],
        )


@pytest.mark.asyncio
async def test_commercial_eligibility_is_authority_driven_and_license_is_versioned(data_db):
    source = await data_governance.register_dataset(
        actor_id="admin",
        name="Personal",
        source_system="academy",
        source_ref="mongo:users",
        content_hash="a" * 64,
        owner="academy",
        evidence_refs=["SCHEMA"],
    )
    derived = await data_governance.register_dataset(
        actor_id="admin",
        name="Anonymous aggregates",
        source_system="academy",
        source_ref="job:anon",
        content_hash="b" * 64,
        owner="academy",
        evidence_refs=["JOB"],
    )
    await data_db.privacy_anonymisation_executions.insert_one(
        {"id": "ANON-1", "status": "VERIFIED_ANONYMISED"}
    )
    asset = await data_governance.register_anonymised_derived_asset(
        actor_id="admin",
        source_dataset_id=source["id"],
        derived_dataset_id=derived["id"],
        anonymisation_execution_ref="ANON-1",
        evidence_refs=["ANON-1"],
    )
    authority = await authority_policy.register_policy_version(
        actor_id="founder",
        policy_key="DERIVED_KNOWLEDGE_COMMERCIALISATION",
        version="1.0.0",
        title="Derived knowledge commercialisation",
        rules=[
            {
                "id": "R1",
                "priority": 1,
                "effect": "ALLOW",
                "reason": "explicit eligible decision",
                "conditions": {
                    "actor_roles": ["FOUNDER"],
                    "actions": ["DATA_COMMERCIAL_ELIGIBILITY"],
                    "domains": ["PRIVACY"],
                    "minimum_authority_level": "A5_FOUNDER_SYSTEMIC",
                },
            }
        ],
        effective_at="2026-09-10T00:00:00+00:00",
        doctrine_ref="DAT-09",
        evidence_refs=["DAT-09"],
    )
    eligible = await data_governance.decide_commercial_eligibility(
        actor_id="founder",
        actor_role="founder",
        authority_level="A5_FOUNDER_SYSTEMIC",
        derived_asset_id=asset["id"],
        policy_version_id=authority["id"],
        eligible=True,
        rationale="Verified anonymisation and explicit commercial decision",
        evidence_refs=["LEGAL-REVIEW-1"],
    )
    assert eligible["commercial_eligibility"] == "ELIGIBLE"

    license_policy = await policy_registry.register_version(
        actor_id="founder",
        policy_key="DATASET_LICENSING",
        version="1.0.0",
        kind="POLICY",
        title="Dataset licensing",
        content={"requires_explicit_purpose": True},
        effective_at="2026-09-10T00:00:00+00:00",
        evidence_refs=["DAT-12"],
    )
    license_row = await data_governance.issue_dataset_license(
        actor_id="admin",
        derived_asset_id=asset["id"],
        licensee_id="TENANT-1",
        purpose="aggregate benchmark",
        starts_at="2026-09-10T00:00:00+00:00",
        ends_at="2027-09-10T00:00:00+00:00",
        policy_version_id=license_policy["id"],
        evidence_refs=["CONTRACT-1"],
    )
    assert license_row["status"] == "ACTIVE"
    withdrawn = await data_governance.withdraw_dataset_license(
        actor_id="admin",
        license_id=license_row["id"],
        reason="contract ended",
        evidence_refs=["TERM-1"],
    )
    assert withdrawn["status"] == "WITHDRAWN"


@pytest.mark.asyncio
async def test_data_access_audit_is_append_only(data_db):
    dataset = await data_governance.register_dataset(
        actor_id="admin",
        name="Audit data",
        source_system="academy",
        source_ref="mongo:audit",
        content_hash="a" * 64,
        owner="academy",
        evidence_refs=["SCHEMA"],
    )
    row = await data_governance.audit_data_access(
        actor_id="expert-1",
        dataset_id=dataset["id"],
        action="READ",
        purpose="case review",
        decision="ALLOW",
        evidence_refs=["CASE-1"],
    )
    assert row["decision"] == "ALLOW"
    assert await data_db.data_access_audit.count_documents({}) == 1
