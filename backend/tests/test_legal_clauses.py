from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import legal_clauses, legal_documents, legal_ops
from services import professional_governance as governance


@pytest.fixture
async def clause_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_clause_test"]
    for module in (legal_clauses, legal_documents, legal_ops, governance):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


async def _setup():
    case = await governance.create_case(
        actor_id="admin-1", title="Clause review", domain="LEGAL", description="Clause work"
    )
    matter = await legal_ops.create_legal_matter(
        actor_id="admin-1",
        title="Partner agreement",
        matter_type="CONTRACT",
        case_id=case["id"],
        evidence_refs=["M-1"],
    )
    doc = await legal_documents.create_document(
        actor_id="admin-1",
        case_id=case["id"],
        matter_id=matter["id"],
        document_type="CONTRACT",
        title="Partner Agreement",
        jurisdiction="FR",
        content_hash="a" * 64,
        evidence_refs=["D-1"],
    )
    clause = await legal_clauses.create_clause(
        actor_id="admin-1",
        case_id=case["id"],
        code="TERM-001",
        title="Termination",
        context_tags=["partner", "fr"],
        content_hash="b" * 64,
        evidence_refs=["C-1"],
    )
    return case, matter, doc, clause


@pytest.mark.asyncio
async def test_clause_usage_binds_exact_clause_and_document_versions(clause_db):
    _case, _matter, doc, clause = await _setup()
    usage = await legal_clauses.register_usage(
        actor_id="admin-1",
        clause_id=clause["id"],
        document_id=doc["id"],
        version_id=None,
        evidence_refs=["USE-1"],
    )
    assert usage["clause_version_id"] == clause["current_version_id"]
    assert usage["document_version_id"] == doc["current_version_id"]


@pytest.mark.asyncio
async def test_clause_change_queues_every_affected_document_for_rereview(clause_db):
    _case, _matter, doc, clause = await _setup()
    await legal_clauses.register_usage(
        actor_id="admin-1",
        clause_id=clause["id"],
        document_id=doc["id"],
        version_id=None,
        evidence_refs=["USE-2"],
    )
    new_version = await legal_clauses.add_clause_version(
        actor_id="lawyer-1",
        clause_id=clause["id"],
        content_hash="c" * 64,
        evidence_refs=["CHANGE-1"],
    )
    impact = await legal_clauses.impact_for_version(new_version["id"])
    assert impact["affected_document_ids"] == [doc["id"]]
    assert impact["queue"][0]["previous_clause_version_id"] == clause["current_version_id"]
    assert impact["queue"][0]["status"] == "OPEN"


@pytest.mark.asyncio
async def test_old_clause_version_remains_immutable_after_revision(clause_db):
    _case, _matter, _doc, clause = await _setup()
    old_id = clause["current_version_id"]
    await legal_clauses.add_clause_version(
        actor_id="lawyer-1",
        clause_id=clause["id"],
        content_hash="d" * 64,
        evidence_refs=["CHANGE-2"],
    )
    old = await clause_db.governance_document_versions.find_one({"id": old_id}, {"_id": 0})
    assert old["content_hash"] == "b" * 64
