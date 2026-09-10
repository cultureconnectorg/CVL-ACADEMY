from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import assurance_core, authority_policy, data_classification, expert_access
from services import policy_registry, privacy_advanced, privacy_ops
from services import professional_governance


@pytest.fixture
async def privacy_advanced_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_privacy_advanced_test"]
    for module in (
        assurance_core,
        authority_policy,
        data_classification,
        expert_access,
        policy_registry,
        privacy_advanced,
        privacy_ops,
        professional_governance,
    ):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


def _past() -> str:
    return (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()


async def _plain_policy(key: str):
    return await policy_registry.register_version(
        actor_id="founder",
        policy_key=key,
        version="1.0.0",
        kind="POLICY",
        title=key,
        content={"evidence_first": True},
        effective_at=_past(),
        evidence_refs=[f"MASTER:{key}"],
    )


async def _authority(key: str, action: str, level: str):
    return await authority_policy.register_policy_version(
        actor_id="founder",
        policy_key=key,
        version="1.0.0",
        title=key,
        rules=[
            {
                "id": "ALLOW",
                "priority": 1,
                "effect": "ALLOW",
                "reason": "Explicit authority",
                "conditions": {
                    "actor_roles": ["FOUNDER"],
                    "actions": [action],
                    "domains": ["PRIVACY"],
                    "minimum_authority_level": level,
                },
            }
        ],
        effective_at=_past(),
        doctrine_ref="GOV-14",
        evidence_refs=[f"MASTER:{key}"],
    )


async def _classified_resource():
    await assurance_core.register_data_class(
        actor_id="dpo",
        code="IDENTITY",
        name="Identity",
        sensitivity="sensitive",
        retention_days=365,
        legal_basis_required=True,
    )
    policy = await _plain_policy("DATA_CLASSIFICATION")
    resource = await data_classification.declare_resource(
        actor_id="dpo",
        resource_kind="DATA",
        resource_type="PROFILE",
        resource_id="user-1",
        owner="academy",
        source="mongo",
    )
    await data_classification.classify_resource(
        actor_id="dpo",
        resource_record_id=resource["id"],
        data_class_code="IDENTITY",
        policy_version_id=policy["id"],
        rationale="Identity profile",
        evidence_refs=["SCHEMA:users"],
    )
    return resource


@pytest.mark.asyncio
async def test_rectification_tracks_before_after_hashes_without_dynamic_mutation(
    privacy_advanced_db,
):
    resource = await _classified_resource()
    rect = await privacy_advanced.create_rectification_request(
        actor_id="user-1",
        user_id="user-1",
        resource_record_id=resource["id"],
        requested_changes={"display_name": "Correct Name"},
        rationale="Incorrect profile value",
        evidence_refs=["USER-REQUEST-1"],
    )
    approved = await privacy_advanced.approve_rectification(
        actor_id="dpo",
        rectification_id=rect["id"],
        evidence_refs=["REVIEW-1"],
    )
    assert approved["status"] == "APPROVED"
    executed = await privacy_advanced.record_rectification_execution(
        actor_id="worker",
        rectification_id=rect["id"],
        adapter="profile-service-v1",
        before_hash="a" * 64,
        after_hash="b" * 64,
        evidence_refs=["UPDATE-RECEIPT-1"],
    )
    assert executed["status"] == "EXECUTED"
    assert executed["execution"]["before_hash"] == "a" * 64
    assert executed["execution"]["after_hash"] == "b" * 64


@pytest.mark.asyncio
async def test_anonymisation_candidate_is_not_claimed_anonymous_until_review(
    privacy_advanced_db,
):
    resource = await _classified_resource()
    policy = await _plain_policy("ANONYMISATION")
    recipe = await privacy_advanced.register_anonymisation_recipe(
        actor_id="dpo",
        data_class_code="IDENTITY",
        operations={"email": "DROP", "name": "GENERALIZE"},
        policy_version_id=policy["id"],
        evidence_refs=["ANON-POLICY-1"],
    )
    candidate = privacy_advanced.apply_anonymisation_candidate(
        {"email": "a@example.test", "name": "Alice", "cohort": "C1"},
        recipe["operations"],
    )
    assert "email" not in candidate
    assert candidate["name"].startswith("A")

    run = await privacy_advanced.record_anonymisation_run(
        actor_id="worker",
        recipe_id=recipe["id"],
        resource_record_id=resource["id"],
        before_hash="1" * 64,
        candidate_hash="2" * 64,
        adapter="analytics-pipeline-v1",
        evidence_refs=["RUN-1"],
        metrics={"direct_identifiers_remaining": 0},
    )
    assert run["status"] == "ANONYMISATION_CANDIDATE"
    assert run["verified_anonymised"] is False

    verified = await privacy_advanced.verify_anonymisation(
        actor_id="dpo",
        run_id=run["id"],
        rationale="Direct identifiers removed and residual risk reviewed",
        residual_reidentification_risk="LOW",
        evidence_refs=["REVIEW-1"],
    )
    assert verified["status"] == "VERIFIED_ANONYMISED"


@pytest.mark.asyncio
async def test_derived_commercial_asset_requires_verified_anonymisation_and_a5(
    privacy_advanced_db,
):
    resource = await _classified_resource()
    anon_policy = await _plain_policy("ANONYMISATION")
    recipe = await privacy_advanced.register_anonymisation_recipe(
        actor_id="dpo",
        data_class_code="IDENTITY",
        operations={"email": "DROP"},
        policy_version_id=anon_policy["id"],
        evidence_refs=["ANON-1"],
    )
    run = await privacy_advanced.record_anonymisation_run(
        actor_id="worker",
        recipe_id=recipe["id"],
        resource_record_id=resource["id"],
        before_hash="3" * 64,
        candidate_hash="4" * 64,
        adapter="analytics-v1",
        evidence_refs=["RUN-2"],
    )
    commercial_policy = await _authority(
        "DERIVED_KNOWLEDGE_COMMERCIALISATION",
        "COMMERCIALISE_DERIVED_KNOWLEDGE",
        "A5_FOUNDER_SYSTEMIC",
    )
    with pytest.raises(ValueError, match="VERIFIED_ANONYMISED"):
        await privacy_advanced.approve_derived_knowledge_asset(
            actor_id="founder",
            actor_role="FOUNDER",
            authority_level="A5_FOUNDER_SYSTEMIC",
            anonymisation_run_id=run["id"],
            asset_name="Cohort benchmark",
            policy_version_id=commercial_policy["id"],
            evidence_refs=["ASSET-1"],
        )

    await privacy_advanced.verify_anonymisation(
        actor_id="dpo",
        run_id=run["id"],
        rationale="Reviewed",
        residual_reidentification_risk="LOW",
        evidence_refs=["VERIFY-2"],
    )
    asset = await privacy_advanced.approve_derived_knowledge_asset(
        actor_id="founder",
        actor_role="FOUNDER",
        authority_level="A5_FOUNDER_SYSTEMIC",
        anonymisation_run_id=run["id"],
        asset_name="Cohort benchmark",
        policy_version_id=commercial_policy["id"],
        evidence_refs=["ASSET-1"],
    )
    assert asset["asset_class"] == "COMMERCIAL_ASSET"
    assert asset["personal_archive"] is False


@pytest.mark.asyncio
async def test_cross_border_requires_approved_classified_processor_and_policy(
    privacy_advanced_db,
):
    await assurance_core.register_data_class(
        actor_id="dpo",
        code="LEARNING",
        name="Learning",
        sensitivity="sensitive",
        retention_days=365,
        legal_basis_required=True,
    )
    class_policy = await _plain_policy("DATA_CLASSIFICATION")
    processor = await privacy_ops.register_processor(
        actor_id="dpo",
        name="EU Vendor",
        service="hosting",
        purpose="Host learner data",
        data_classes=["LEARNING"],
        regions=["EU"],
        dpa_evidence_ref="DPA-1",
    )
    await data_classification.classify_resource(
        actor_id="dpo",
        resource_record_id=processor["classification_resource_id"],
        data_class_code="LEARNING",
        policy_version_id=class_policy["id"],
        rationale="Vendor processes learner data",
        evidence_refs=["ASSESS-1"],
    )
    await privacy_ops.transition_processor(
        actor_id="dpo", processor_id=processor["id"], status="APPROVED"
    )
    transfer_policy = await _authority(
        "CROSS_BORDER_TRANSFER",
        "PRIVACY_CROSS_BORDER_TRANSFER",
        "A4_CVL_AUTHORITY",
    )
    transfer = await privacy_advanced.assess_cross_border_transfer(
        actor_id="founder",
        actor_role="FOUNDER",
        authority_level="A4_CVL_AUTHORITY",
        processor_id=processor["id"],
        destination_region="US",
        transfer_mechanism="SCC",
        policy_version_id=transfer_policy["id"],
        evidence_refs=["SCC-1", "TIA-1"],
    )
    assert transfer["status"] == "APPROVED"
    assert transfer["destination_region"] == "US"


@pytest.mark.asyncio
async def test_privacy_workspace_is_case_scoped(privacy_advanced_db):
    case = await professional_governance.create_case(
        actor_id="admin",
        title="Privacy review",
        domain="PRIVACY",
        description="Scoped DPO review",
        metadata={"dsar_ids": ["DSAR-1"]},
    )
    expert = await professional_governance.create_expert(
        actor_id="admin",
        display_name="Privacy Expert",
        email="privacy@example.test",
        domains=["PRIVACY"],
    )
    assignment = await professional_governance.assign_expert(
        actor_id="admin",
        case_id=case["id"],
        expert_id=expert["id"],
        scope=["privacy:case:read"],
    )
    raw_key, _public = await professional_governance.issue_expert_api_key(
        actor_id="admin",
        assignment_id=assignment["id"],
        expires_at=(datetime.now(timezone.utc) + timedelta(hours=2)).isoformat(),
    )
    await privacy_advanced_db.privacy_dsar.insert_one(
        {"id": "DSAR-1", "user_id": "user-1", "status": "OPEN"}
    )
    workspace = await privacy_advanced.get_privacy_workspace(
        raw_key=raw_key, case_id=case["id"]
    )
    assert workspace["case"]["id"] == case["id"]
    assert [row["id"] for row in workspace["dsars"]] == ["DSAR-1"]

    other = await professional_governance.create_case(
        actor_id="admin",
        title="Other privacy case",
        domain="PRIVACY",
        description="Not assigned",
    )
    with pytest.raises(PermissionError, match="not assigned"):
        await privacy_advanced.get_privacy_workspace(
            raw_key=raw_key, case_id=other["id"]
        )
