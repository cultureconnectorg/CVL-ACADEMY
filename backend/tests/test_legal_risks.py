from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import assurance_core, legal_ops, legal_risks
from services import professional_governance as governance


@pytest.fixture
async def legal_risk_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_legal_risk_test"]
    for module in (assurance_core, legal_ops, legal_risks, governance):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


@pytest.mark.asyncio
async def test_legal_risk_reuses_risk_core_and_links_matter(legal_risk_db):
    matter = await legal_ops.create_legal_matter(
        actor_id="legal-1",
        title="Rights dispute",
        matter_type="IP",
        jurisdiction="FR",
        evidence_refs=["MATTER-1"],
    )
    risk = await legal_risks.register_legal_risk(
        actor_id="legal-1",
        matter_id=matter["id"],
        title="Rights ownership ambiguity",
        impact=5,
        probability=4,
        owner="legal-owner",
        mitigation="Obtain chain-of-title evidence",
        deadline="2026-10-01",
        evidence_refs=["RISK-EVID-1"],
    )
    assert risk["domain"] == "LEGAL"
    assert risk["source_type"] == "LEGAL_MATTER"
    assert risk["source_id"] == matter["id"]
    assert risk["level"] == assurance_core.score_risk(5, 4, 0)

    stored_matter = await legal_risk_db.legal_matters.find_one(
        {"id": matter["id"]}, {"_id": 0}
    )
    assert stored_matter["risk_ids"] == [risk["id"]]
    rows = await legal_risks.list_matter_risks(matter["id"])
    assert [row["id"] for row in rows] == [risk["id"]]


@pytest.mark.asyncio
async def test_legal_risk_is_idempotent_for_same_matter_and_title(legal_risk_db):
    matter = await legal_ops.create_legal_matter(
        actor_id="legal-1", title="Contract", matter_type="CONTRACT"
    )
    kwargs = dict(
        actor_id="legal-1",
        matter_id=matter["id"],
        title="Termination exposure",
        impact=3,
        probability=3,
        evidence_refs=["RISK-EVID-2"],
    )
    first = await legal_risks.register_legal_risk(**kwargs)
    second = await legal_risks.register_legal_risk(**kwargs)
    assert second["id"] == first["id"]
    assert await legal_risk_db.risks.count_documents({}) == 1


@pytest.mark.asyncio
async def test_legal_risk_requires_real_matter_and_evidence(legal_risk_db):
    with pytest.raises(LookupError, match="legal matter not found"):
        await legal_risks.register_legal_risk(
            actor_id="legal-1",
            matter_id="missing",
            title="Missing source",
            impact=2,
            probability=2,
            evidence_refs=["EVID-1"],
        )

    matter = await legal_ops.create_legal_matter(
        actor_id="legal-1", title="Contract", matter_type="CONTRACT"
    )
    with pytest.raises(ValueError, match="requires evidence"):
        await legal_risks.register_legal_risk(
            actor_id="legal-1",
            matter_id=matter["id"],
            title="No evidence",
            impact=2,
            probability=2,
            evidence_refs=[],
        )
