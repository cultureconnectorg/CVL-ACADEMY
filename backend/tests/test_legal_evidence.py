from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import evidence_graph, legal_evidence, legal_ops, policy_registry
from services import professional_governance as governance


@pytest.fixture
async def evidence_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_legal_evidence_test"]
    for module in (evidence_graph, legal_evidence, legal_ops, policy_registry, governance):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


async def _access_policy():
    return await policy_registry.register_version(
        actor_id="founder-1",
        policy_key="EVIDENCE_ACCESS",
        version="1.0.0",
        kind="POLICY",
        title="Evidence Access",
        content={"scope": "legal"},
        effective_at="2026-09-10T00:00:00+00:00",
        evidence_refs=["MASTER:XCP-004"],
    )


@pytest.mark.asyncio
async def test_legal_pack_reuses_evidence_graph_without_copying_payload(evidence_db):
    matter = await legal_ops.create_legal_matter(
        actor_id="legal-1", title="Evidence case", matter_type="CONTRACT"
    )
    policy = await _access_policy()
    node = await evidence_graph.register_node(
        actor_id="legal-1",
        source_type="LEGAL_DOCUMENT_VERSION",
        source_id="DOCV-1",
        content_hash="a" * 64,
        provenance_refs=["SOURCE-1"],
        access_policy_version_id=policy["id"],
        metadata={"matter_id": matter["id"], "payload_should_not_copy": "secret"},
    )
    pack = await legal_evidence.create_legal_pack(
        actor_id="legal-1",
        matter_id=matter["id"],
        title="Legal evidence pack",
        purpose="External review evidence",
        node_ids=[node["id"]],
        evidence_refs=["PACK-REQ-1"],
    )
    assert pack["consumer"] == "LEGAL"
    assert pack["composition_mode"] == "REFERENCE_ONLY"
    assert pack["node_refs"][0]["node_id"] == node["id"]
    assert "metadata" not in pack["node_refs"][0]
    assert "payload_should_not_copy" not in str(pack["node_refs"])


@pytest.mark.asyncio
async def test_legal_pack_rejects_node_explicitly_owned_by_other_matter(evidence_db):
    first = await legal_ops.create_legal_matter(
        actor_id="legal-1", title="First", matter_type="CONTRACT"
    )
    second = await legal_ops.create_legal_matter(
        actor_id="legal-1", title="Second", matter_type="CONTRACT"
    )
    policy = await _access_policy()
    node = await evidence_graph.register_node(
        actor_id="legal-1",
        source_type="LEGAL_DOCUMENT_VERSION",
        source_id="DOCV-2",
        content_hash="b" * 64,
        provenance_refs=["SOURCE-2"],
        access_policy_version_id=policy["id"],
        metadata={"matter_id": first["id"]},
    )
    with pytest.raises(PermissionError, match="another legal matter"):
        await legal_evidence.create_legal_pack(
            actor_id="legal-1",
            matter_id=second["id"],
            title="Wrong pack",
            purpose="Must fail",
            node_ids=[node["id"]],
            evidence_refs=["PACK-REQ-2"],
        )
