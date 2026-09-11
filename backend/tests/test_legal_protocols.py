from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import (
    authority_policy,
    governance_protocols,
    legal_protocols,
    policy_registry,
    professional_governance,
)


@pytest.fixture
async def legal_protocol_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_legal_protocol_test"]
    for module in (
        authority_policy,
        governance_protocols,
        legal_protocols,
        policy_registry,
        professional_governance,
    ):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


async def _policy(key: str):
    return await policy_registry.register_version(
        actor_id="founder",
        policy_key=key,
        version="1.0.0",
        kind="POLICY",
        title=key,
        content={"evidence_first": True},
        effective_at="2026-09-10T00:00:00+00:00",
        evidence_refs=[f"{key}-EVID"],
    )


@pytest.mark.asyncio
async def test_legal_risk_classification_is_versioned(legal_protocol_db):
    await legal_protocol_db.risks.insert_one(
        {"id": "RISK-L1", "domain": "LEGAL", "level": 4}
    )
    policy = await _policy("LEGAL_RISK_CLASSIFICATION")
    first = await legal_protocols.classify_legal_risk(
        actor_id="legal",
        risk_id="RISK-L1",
        category="CONTRACT",
        rationale="Contract exposure review",
        authority_ref="COUNSEL-1",
        policy_version_id=policy["id"],
        evidence_refs=["RISK-1"],
    )
    second = await legal_protocols.classify_legal_risk(
        actor_id="legal",
        risk_id="RISK-L1",
        category="IP",
        rationale="Updated classification after evidence review",
        authority_ref="COUNSEL-2",
        policy_version_id=policy["id"],
        evidence_refs=["RISK-2"],
    )
    previous = await legal_protocol_db.legal_risk_classifications.find_one(
        {"id": first["id"]}, {"_id": 0}
    )
    assert previous["status"] == "SUPERSEDED"
    assert second["supersedes_id"] == first["id"]


@pytest.mark.asyncio
async def test_legal_escalation_reuses_governance_protocol(legal_protocol_db):
    await legal_protocol_db.legal_matters.insert_one(
        {"id": "MAT-1", "case_id": None, "status": "OPEN"}
    )
    escalation = await legal_protocols.escalate_legal_matter(
        actor_id="legal",
        matter_id="MAT-1",
        severity="HIGH",
        target_authority_level="A4_CVL",
        reason="External legal review required",
        evidence_refs=["MAT-EVID-1"],
    )
    assert escalation["source_type"] == "LEGAL_MATTER"
    assert escalation["domain"] == "LEGAL"
    assert (await governance_protocols.escalation_gate(domain="LEGAL"))["pass"] is False


@pytest.mark.asyncio
async def test_privilege_confidentiality_is_reviewed_not_inferred(legal_protocol_db):
    await legal_protocol_db.legal_matters.insert_one({"id": "MAT-1"})
    policy = await _policy("LEGAL_PRIVILEGE_CONFIDENTIALITY")
    row = await legal_protocols.classify_privilege_confidentiality(
        actor_id="counsel",
        resource_type="LEGAL_MATTER",
        resource_id="MAT-1",
        classification="PRIVILEGE_REVIEW_REQUIRED",
        rationale="Counsel review required before privilege claim",
        authority_ref="COUNSEL-REVIEW-1",
        policy_version_id=policy["id"],
        evidence_refs=["DOC-CHAIN-1"],
    )
    assert row["classification"] == "PRIVILEGE_REVIEW_REQUIRED"
    assert row["legal_effect"] == (
        "RECORDED_CLASSIFICATION_NOT_AUTOMATIC_LEGAL_DETERMINATION"
    )


@pytest.mark.asyncio
async def test_legal_retention_requires_bound_allow_decision(legal_protocol_db):
    policy = await _policy("LEGAL_RETENTION")
    await legal_protocol_db.authority_decisions.insert_one(
        {
            "id": "AUTH-DENY",
            "decision": "DENY",
            "action": "LEGAL_RETENTION_CONFIGURE",
            "policy_version_id": policy["id"],
            "context": {"domain": "LEGAL"},
        }
    )
    with pytest.raises(PermissionError, match="ALLOW"):
        await legal_protocols.register_legal_retention_rule(
            actor_id="legal",
            record_type="LEGAL_DOCUMENT",
            jurisdiction="FR",
            retention_days=3650,
            trigger="CLOSED",
            action="ARCHIVE",
            policy_version_id=policy["id"],
            authority_decision_id="AUTH-DENY",
            evidence_refs=["RET-EVID-1"],
        )

    await legal_protocol_db.authority_decisions.insert_one(
        {
            "id": "AUTH-ALLOW",
            "decision": "ALLOW",
            "action": "LEGAL_RETENTION_CONFIGURE",
            "policy_version_id": policy["id"],
            "decision_hash": "b" * 64,
            "context": {"domain": "LEGAL"},
        }
    )
    row = await legal_protocols.register_legal_retention_rule(
        actor_id="legal",
        record_type="LEGAL_DOCUMENT",
        jurisdiction="FR",
        retention_days=3650,
        trigger="CLOSED",
        action="ARCHIVE",
        policy_version_id=policy["id"],
        authority_decision_id="AUTH-ALLOW",
        evidence_refs=["RET-EVID-2"],
    )
    assert row["status"] == "ACTIVE"
    assert row["authority_decision_id"] == "AUTH-ALLOW"


@pytest.mark.asyncio
async def test_jurisdiction_mapping_refuses_unresolved_scope(legal_protocol_db):
    await legal_protocol_db.legal_matters.insert_one({"id": "MAT-1"})
    await legal_protocol_db.regulatory_scopes.insert_one(
        {
            "id": "SCOPE-1",
            "jurisdiction": "FR",
            "status": "REVIEW_REQUIRED",
            "current_decision_id": None,
        }
    )
    with pytest.raises(ValueError, match="unresolved"):
        await legal_protocols.map_jurisdiction(
            actor_id="legal",
            matter_id="MAT-1",
            jurisdiction="FR",
            regulatory_scope_ids=["SCOPE-1"],
            rationale="Map reviewed legal scope",
            evidence_refs=["MAP-1"],
        )

    await legal_protocol_db.regulatory_scopes.update_one(
        {"id": "SCOPE-1"},
        {"$set": {"status": "APPLICABLE", "current_decision_id": "REGDEC-1"}},
    )
    await legal_protocol_db.regulatory_applicability_decisions.insert_one(
        {
            "id": "REGDEC-1",
            "scope_id": "SCOPE-1",
            "outcome": "APPLICABLE",
            "status": "CURRENT",
        }
    )
    mapping = await legal_protocols.map_jurisdiction(
        actor_id="legal",
        matter_id="MAT-1",
        jurisdiction="FR",
        regulatory_scope_ids=["SCOPE-1"],
        rationale="Reviewed scope mapped to matter",
        evidence_refs=["MAP-2"],
    )
    assert mapping["status"] == "CURRENT"
    assert mapping["regulatory_scope_ids"] == ["SCOPE-1"]


@pytest.mark.asyncio
async def test_regulatory_requirement_registry_tracks_applicability(legal_protocol_db):
    await legal_protocol_db.regulatory_scopes.insert_one(
        {
            "id": "SCOPE-1",
            "regulatory_id": "REG-01",
            "jurisdiction": "FR",
            "status": "APPLICABLE",
            "current_decision_id": "REGDEC-1",
        }
    )
    await legal_protocol_db.regulatory_applicability_decisions.insert_one(
        {
            "id": "REGDEC-1",
            "scope_id": "SCOPE-1",
            "outcome": "APPLICABLE",
            "status": "CURRENT",
        }
    )
    first = await legal_protocols.register_regulatory_requirement(
        actor_id="legal",
        requirement_key="DATA-RIGHTS-NOTICE",
        scope_id="SCOPE-1",
        title="Reviewed notice requirement",
        requirement="Maintain the reviewed requirement text and authority source.",
        authority_ref="DPO-LEGAL-1",
        source_refs=["SOURCE-1"],
        effective_at="2026-09-11T00:00:00+00:00",
    )
    second = await legal_protocols.register_regulatory_requirement(
        actor_id="legal",
        requirement_key="DATA-RIGHTS-NOTICE",
        scope_id="SCOPE-1",
        title="Updated reviewed notice requirement",
        requirement="Updated requirement after a new reviewed authority source.",
        authority_ref="DPO-LEGAL-2",
        source_refs=["SOURCE-2"],
        effective_at="2026-09-12T00:00:00+00:00",
    )
    previous = await legal_protocol_db.legal_regulatory_requirements.find_one(
        {"id": first["id"]}, {"_id": 0}
    )
    assert previous["status"] == "SUPERSEDED"
    assert second["supersedes_id"] == first["id"]
    assert second["applicability_decision_id"] == "REGDEC-1"
