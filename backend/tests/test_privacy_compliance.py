from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import assurance_core, authority_policy, data_classification
from services import incident_core, legal_ops, policy_registry, privacy_compliance
from services import privacy_ops, professional_governance, retention_executor


@pytest.fixture
async def privacy_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_privacy_compliance_test"]
    for module in (
        assurance_core,
        authority_policy,
        data_classification,
        incident_core,
        legal_ops,
        policy_registry,
        privacy_compliance,
        privacy_ops,
        professional_governance,
        retention_executor,
    ):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


def _past() -> str:
    return (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()


async def _policy(key: str, version: str = "1.0.0"):
    return await policy_registry.register_version(
        actor_id="founder",
        policy_key=key,
        version=version,
        kind="POLICY",
        title=key,
        content={"evidence_first": True},
        effective_at=_past(),
        evidence_refs=[f"MASTER:{key}"],
    )


async def _authority_policy(key: str, action: str, minimum: str = "A4_CVL_AUTHORITY"):
    return await authority_policy.register_policy_version(
        actor_id="founder",
        policy_key=key,
        version="1.0.0",
        title=key,
        rules=[
            {
                "id": f"{key}-ALLOW",
                "priority": 1,
                "effect": "ALLOW",
                "reason": "Explicit test authority",
                "conditions": {
                    "actor_roles": ["FOUNDER"],
                    "actions": [action],
                    "domains": ["PRIVACY"],
                    "minimum_authority_level": minimum,
                },
            }
        ],
        effective_at=_past(),
        doctrine_ref="GOV-14",
        evidence_refs=[f"MASTER:{key}"],
    )


@pytest.mark.asyncio
async def test_ropa_requires_registered_classes_processors_and_evidence(privacy_db):
    await assurance_core.register_data_class(
        actor_id="dpo",
        code="IDENTITY",
        name="Identity",
        sensitivity="sensitive",
        retention_days=365,
        legal_basis_required=True,
    )
    processor = await privacy_ops.register_processor(
        actor_id="dpo",
        name="Hosting provider",
        service="hosting",
        data_classes=["IDENTITY"],
        regions=["EU"],
        dpa_evidence_ref="DPA-1",
    )

    with pytest.raises(LookupError, match="unknown privacy data classes"):
        await privacy_compliance.register_processing_activity(
            actor_id="dpo",
            name="Account management",
            purpose="Provide learner account",
            data_classes=["UNKNOWN"],
            legal_basis="contract",
            processors=[processor["id"]],
            regions=["EU"],
            controller="CVLN Academy",
            evidence_refs=["ROPA-EVID-1"],
        )

    ropa = await privacy_compliance.register_processing_activity(
        actor_id="dpo",
        name="Account management",
        purpose="Provide learner account",
        data_classes=["IDENTITY"],
        legal_basis="contract",
        processors=[processor["id"]],
        regions=["EU"],
        controller="CVLN Academy",
        recipients=["support"],
        systems=["academy-api"],
        retention_refs=["RET-IDENTITY"],
        evidence_refs=["ROPA-EVID-1"],
    )
    assert ropa["ropa_complete"] is True
    assert ropa["controller"] == "CVLN Academy"
    assert ropa["processors"] == [processor["id"]]


@pytest.mark.asyncio
async def test_consent_is_versioned_and_required_purpose_cannot_be_withdrawn(privacy_db):
    policy = await _policy("CONSENT")
    optional = await privacy_compliance.register_consent_purpose(
        actor_id="dpo",
        purpose="marketing",
        required=False,
        policy_version_id=policy["id"],
        evidence_refs=["PURPOSE-1"],
    )
    required = await privacy_compliance.register_consent_purpose(
        actor_id="dpo",
        purpose="service-essential",
        required=True,
        policy_version_id=policy["id"],
        evidence_refs=["PURPOSE-2"],
    )
    assert optional["required"] is False
    assert required["required"] is True

    granted = await privacy_compliance.record_consent(
        actor_id="user-1",
        user_id="user-1",
        purpose="marketing",
        granted=True,
        policy_version_id=policy["id"],
        evidence_refs=["UI-CONSENT-1"],
        frek_evidence_ref="FREK-EVENT-1",
    )
    withdrawn = await privacy_compliance.record_consent(
        actor_id="user-1",
        user_id="user-1",
        purpose="marketing",
        granted=False,
        policy_version_id=policy["id"],
        evidence_refs=["UI-CONSENT-2"],
    )
    assert granted["policy_hash"] == policy["content_hash"]
    assert withdrawn["granted"] is False
    assert await privacy_db.privacy_consents.count_documents({"user_id": "user-1"}) == 2

    with pytest.raises(PermissionError, match="required consent purpose"):
        await privacy_compliance.record_consent(
            actor_id="user-1",
            user_id="user-1",
            purpose="service-essential",
            granted=False,
            policy_version_id=policy["id"],
            evidence_refs=["UI-CONSENT-3"],
        )

    prefs = await privacy_compliance.consent_preferences("user-1")
    marketing = next(row for row in prefs if row["purpose"] == "MARKETING")
    assert marketing["granted"] is False


@pytest.mark.asyncio
async def test_dsar_export_requires_identity_and_persists_manifest_not_payload(privacy_db):
    await privacy_db.users.insert_one({"id": "user-1", "email": "user@example.test"})
    await privacy_db.progress.insert_one(
        {"id": "PROG-1", "user_id": "user-1", "module_code": "M1"}
    )
    dsar = await privacy_compliance.create_dsar(
        actor_id="user-1", user_id="user-1", request_type="export"
    )

    with pytest.raises(PermissionError, match="verified identity"):
        await privacy_compliance.build_dsar_export(actor_id="dpo", dsar_id=dsar["id"])

    await privacy_compliance.verify_dsar_identity(
        actor_id="dpo",
        dsar_id=dsar["id"],
        evidence_refs=["IDENTITY-CHECK-1"],
    )
    result = await privacy_compliance.build_dsar_export(
        actor_id="dpo", dsar_id=dsar["id"]
    )
    assert result["manifest"]["payload_persisted"] is False
    assert result["manifest"]["source_counts"]["users"] == 1
    assert result["manifest"]["source_counts"]["progress"] == 1
    stored = await privacy_db.privacy_dsar_exports.find_one(
        {"id": result["manifest"]["id"]}, {"_id": 0}
    )
    assert "export" not in stored
    assert len(stored["payload_hash"]) == 64


@pytest.mark.asyncio
async def test_deletion_requires_a4_policy_then_verified_retention_jobs(privacy_db):
    await assurance_core.register_data_class(
        actor_id="dpo",
        code="IDENTITY",
        name="Identity",
        sensitivity="sensitive",
        retention_days=0,
        legal_basis_required=True,
    )
    class_policy = await _policy("DATA_CLASSIFICATION")
    retention_policy = await _policy("RETENTION")
    deletion_policy = await _authority_policy(
        "PRIVACY_DELETION", "PRIVACY_DELETION_APPROVE"
    )
    resource = await data_classification.declare_resource(
        actor_id="dpo",
        resource_kind="DATA",
        resource_type="LEARNER_PROFILE",
        resource_id="user-1",
        owner="academy",
        source="mongo",
    )
    await data_classification.classify_resource(
        actor_id="dpo",
        resource_record_id=resource["id"],
        data_class_code="IDENTITY",
        policy_version_id=class_policy["id"],
        rationale="Identity profile",
        evidence_refs=["SCHEMA:users"],
    )
    await privacy_ops.create_retention_rule(
        actor_id="dpo",
        data_class="IDENTITY",
        retention_days=0,
        trigger="DELETION_APPROVED",
        action="DELETE",
        evidence_refs=["RET-RULE-1"],
    )
    request = await privacy_ops.create_deletion_request(
        actor_id="user-1", user_id="user-1", reason="Delete my account"
    )
    await privacy_ops.transition_deletion_request(
        actor_id="dpo", request_id=request["id"], status="IDENTITY_VERIFIED"
    )
    await privacy_ops.transition_deletion_request(
        actor_id="dpo",
        request_id=request["id"],
        status="IMPACT_ASSESSED",
        impact={"resources": [resource["id"]]},
    )

    approved = await privacy_compliance.approve_deletion_request(
        actor_id="founder-1",
        actor_role="FOUNDER",
        authority_level="A4_CVL_AUTHORITY",
        request_id=request["id"],
        policy_version_id=deletion_policy["id"],
        evidence_refs=["APPROVAL-1"],
    )
    assert approved["status"] == "APPROVED"

    scheduled = await privacy_compliance.schedule_deletion_retention_jobs(
        actor_id="dpo",
        request_id=request["id"],
        resource_record_ids=[resource["id"]],
        trigger_at=(datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat(),
        retention_policy_version_id=retention_policy["id"],
    )
    job = scheduled["jobs"][0]
    with pytest.raises(ValueError, match="VERIFIED_EXECUTED"):
        await privacy_compliance.complete_deletion_from_retention(
            actor_id="dpo",
            request_id=request["id"],
            evidence_refs=["COMPLETE-1"],
        )

    await retention_executor.record_execution(
        actor_id="worker",
        job_id=job["id"],
        adapter="mongo-users-v1",
        evidence_ref="ERASURE-RECEIPT-1",
        outcome="SUCCESS",
    )
    completed = await privacy_compliance.complete_deletion_from_retention(
        actor_id="dpo",
        request_id=request["id"],
        evidence_refs=["COMPLETION-REVIEW-1"],
    )
    assert completed["status"] == "COMPLETED"


@pytest.mark.asyncio
async def test_privacy_incident_originates_in_canonical_incident_core(privacy_db):
    incident = await privacy_compliance.open_privacy_incident(
        actor_id="dpo",
        title="Data disclosure",
        description="Personal data exposed to an unauthorized recipient",
        severity="HIGH",
        data_classes=["IDENTITY"],
        evidence_refs=["INC-EVID-1"],
    )
    assert incident["id"].startswith("INC-")
    assert incident["domains"] == ["LEGAL", "PRIVACY", "RISK"]
    assert await privacy_db.incidents.count_documents({"id": incident["id"]}) == 1
    assert await privacy_db.privacy_incidents.count_documents({}) == 0

    projected = await privacy_compliance.project_privacy_incident(
        actor_id="dpo",
        incident_id=incident["id"],
        risk_impact=4,
        risk_probability=3,
        risk_owner="privacy",
        risk_mitigation="Contain and notify",
        risk_deadline="2026-09-12",
        jurisdiction="FR",
    )
    assert set(projected["projections"]) == {"LEGAL", "PRIVACY", "RISK"}
    privacy_projection = projected["projections"]["PRIVACY"]
    assert privacy_projection["canonical_incident_id"] == incident["id"]
