from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import professional_governance, regulatory_applicability


@pytest.fixture
async def regulatory_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_regulatory_applicability_test"]
    for module in (professional_governance, regulatory_applicability):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


@pytest.mark.asyncio
async def test_all_regulatory_areas_require_review_by_default(regulatory_db):
    created = []
    for regulatory_id in regulatory_applicability.REGULATORY_AREAS:
        scope = await regulatory_applicability.declare_scope(
            actor_id="admin",
            regulatory_id=regulatory_id,
            jurisdiction="FR",
            activity=f"activity {regulatory_id}",
            entity_ref="CVLN-ACADEMY",
            product_scope="academy",
            evidence_refs=[f"EVID-{regulatory_id}"],
        )
        created.append(scope)
        assert scope["status"] == "REVIEW_REQUIRED"

    gate = await regulatory_applicability.applicability_gate()
    assert gate["pass"] is False
    assert gate["open_count"] == 8
    assert {row["regulatory_id"] for row in gate["open_scopes"]} == set(
        regulatory_applicability.REGULATORY_AREAS
    )


@pytest.mark.asyncio
async def test_applicability_requires_explicit_authority_rationale_and_sources(regulatory_db):
    scope = await regulatory_applicability.declare_scope(
        actor_id="admin",
        regulatory_id="REG-01",
        jurisdiction="FR",
        activity="learner data processing",
        entity_ref="CVLN-ACADEMY",
        product_scope="academy",
        evidence_refs=["SCOPE-1"],
    )

    with pytest.raises(ValueError, match="rationale, authority and sources"):
        await regulatory_applicability.record_applicability_decision(
            actor_id="admin",
            scope_id=scope["id"],
            outcome="APPLICABLE",
            rationale="",
            authority_ref="",
            source_refs=[],
            effective_at="2026-09-11T00:00:00+00:00",
        )


@pytest.mark.asyncio
async def test_current_decision_is_superseded_and_gate_closes(regulatory_db):
    scope = await regulatory_applicability.declare_scope(
        actor_id="admin",
        regulatory_id="REG-04",
        jurisdiction="EU",
        activity="native electronic signature",
        entity_ref="CVLN-ACADEMY",
        product_scope="trust-signature",
        evidence_refs=["SCOPE-REG04"],
    )
    first = await regulatory_applicability.record_applicability_decision(
        actor_id="counsel",
        scope_id=scope["id"],
        outcome="APPLICABLE",
        rationale="External regulatory review",
        authority_ref="COUNSEL-REVIEW-1",
        source_refs=["SOURCE-1"],
        effective_at="2026-09-11T00:00:00+00:00",
        review_due_at="2027-03-11T00:00:00+00:00",
    )
    second = await regulatory_applicability.record_applicability_decision(
        actor_id="counsel",
        scope_id=scope["id"],
        outcome="NOT_APPLICABLE",
        rationale="Scope changed after reviewed product boundary",
        authority_ref="COUNSEL-REVIEW-2",
        source_refs=["SOURCE-2"],
        effective_at="2026-10-01T00:00:00+00:00",
        review_due_at="2027-04-01T00:00:00+00:00",
    )

    previous = await regulatory_db.regulatory_applicability_decisions.find_one(
        {"id": first["id"]}, {"_id": 0}
    )
    current_scope = await regulatory_db.regulatory_scopes.find_one(
        {"id": scope["id"]}, {"_id": 0}
    )
    assert previous["status"] == "SUPERSEDED"
    assert previous["superseded_by"] == second["id"]
    assert second["supersedes_decision_id"] == first["id"]
    assert current_scope["status"] == "NOT_APPLICABLE"
    assert current_scope["current_decision_id"] == second["id"]

    gate = await regulatory_applicability.applicability_gate(regulatory_id="REG-04")
    assert gate["pass"] is True
    assert gate["open_count"] == 0


@pytest.mark.asyncio
async def test_invalid_regulatory_identifier_is_rejected(regulatory_db):
    with pytest.raises(ValueError, match="unknown regulatory area"):
        await regulatory_applicability.declare_scope(
            actor_id="admin",
            regulatory_id="REG-99",
            jurisdiction="FR",
            activity="unknown",
            entity_ref="CVLN-ACADEMY",
            product_scope="academy",
            evidence_refs=["EVIDENCE"],
        )
