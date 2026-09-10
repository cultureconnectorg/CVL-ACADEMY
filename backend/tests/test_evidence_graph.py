from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import evidence_graph
from services import policy_registry
from services import professional_governance


@pytest.fixture
async def evidence_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_evidence_graph_test"]
    for module in (evidence_graph, policy_registry, professional_governance):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


async def _access_policy():
    return await policy_registry.register_version(
        actor_id="founder",
        policy_key="EVIDENCE_ACCESS",
        version="1.0.0",
        kind="POLICY",
        title="Evidence access",
        content={"reference_only": True},
        effective_at="2026-09-10T00:00:00+00:00",
        evidence_refs=["XCP-004"],
    )


@pytest.mark.asyncio
async def test_evidence_node_requires_real_hash_and_access_policy(evidence_db):
    policy = await _access_policy()
    with pytest.raises(ValueError):
        await evidence_graph.register_node(
            actor_id="admin",
            source_type="CERTIFICATION",
            source_id="CERT-1",
            content_hash="bad",
            provenance_refs=["CERT-1"],
            access_policy_version_id=policy["id"],
        )


@pytest.mark.asyncio
async def test_pack_composes_refs_not_payload_copies(evidence_db):
    policy = await _access_policy()
    node = await evidence_graph.register_node(
        actor_id="admin",
        source_type="CERTIFICATION",
        source_id="CERT-1",
        content_hash="a" * 64,
        provenance_refs=["CERT-1", "ASSESS-1"],
        access_policy_version_id=policy["id"],
        metadata={"issuer": "CVLN Academy"},
    )
    pack = await evidence_graph.create_pack(
        actor_id="quality",
        title="Certification quality pack",
        consumer="QUALITY",
        node_ids=[node["id"]],
        purpose="Audit certification evidence",
        evidence_refs=["QLT-REVIEW-1"],
    )
    assert pack["composition_mode"] == "REFERENCE_ONLY"
    assert pack["node_refs"][0]["node_id"] == node["id"]
    assert pack["node_refs"][0]["content_hash"] == "a" * 64
    assert "metadata" not in pack["node_refs"][0]
    assert "provenance_refs" not in pack["node_refs"][0]


@pytest.mark.asyncio
async def test_link_requires_existing_nodes_and_evidence(evidence_db):
    policy = await _access_policy()
    first = await evidence_graph.register_node(
        actor_id="admin",
        source_type="LEARNING_EVENT",
        source_id="EV-1",
        content_hash="b" * 64,
        provenance_refs=["EVENT-1"],
        access_policy_version_id=policy["id"],
    )
    second = await evidence_graph.register_node(
        actor_id="admin",
        source_type="ASSESSMENT",
        source_id="ASM-1",
        content_hash="c" * 64,
        provenance_refs=["ASM-1"],
        access_policy_version_id=policy["id"],
    )
    link = await evidence_graph.link_nodes(
        actor_id="admin",
        from_node_id=second["id"],
        to_node_id=first["id"],
        relation="DERIVES_FROM",
        evidence_refs=["TRACE-1"],
    )
    assert link["relation"] == "DERIVES_FROM"
    with pytest.raises(ValueError, match="requires evidence_refs"):
        await evidence_graph.link_nodes(
            actor_id="admin",
            from_node_id=first["id"],
            to_node_id=second["id"],
            relation="SUPPORTS",
            evidence_refs=[],
        )


@pytest.mark.asyncio
async def test_wrong_policy_cannot_control_evidence_access(evidence_db):
    policy = await policy_registry.register_version(
        actor_id="founder",
        policy_key="RETENTION",
        version="1",
        kind="POLICY",
        title="Retention",
        content={"x": True},
        effective_at="2026-09-10T00:00:00+00:00",
        evidence_refs=["XCP-003"],
    )
    with pytest.raises(ValueError, match="not an EVIDENCE_ACCESS policy"):
        await evidence_graph.register_node(
            actor_id="admin",
            source_type="SECURITY_FINDING",
            source_id="FIND-1",
            content_hash="d" * 64,
            provenance_refs=["FIND-1"],
            access_policy_version_id=policy["id"],
        )


@pytest.mark.asyncio
async def test_integrity_gate_detects_dangling_graph_reference(evidence_db):
    policy = await _access_policy()
    node = await evidence_graph.register_node(
        actor_id="admin",
        source_type="LEGAL_DECISION",
        source_id="DEC-1",
        content_hash="e" * 64,
        provenance_refs=["DEC-1"],
        access_policy_version_id=policy["id"],
    )
    pack = await evidence_graph.create_pack(
        actor_id="legal",
        title="Legal proof pack",
        consumer="LEGAL",
        node_ids=[node["id"]],
        purpose="Review legal provenance",
        evidence_refs=["LEGAL-1"],
    )
    gate = await evidence_graph.integrity_gate()
    assert gate["pass"] is True
    await evidence_db.evidence_nodes.delete_one({"id": node["id"]})
    gate = await evidence_graph.integrity_gate()
    assert gate["pass"] is False
    assert gate["dangling_pack_refs"] == [{"pack_id": pack["id"], "node_id": node["id"]}]
