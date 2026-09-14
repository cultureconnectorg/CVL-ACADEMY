"""Canonical Evidence Graph (XCP-004).

Evidence is referenced, not copied. Nodes point to canonical source records, carry
provenance and content hashes, and bind to an effective access-policy version. Packs
for quality/legal/security compose node references only.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import policy_registry
from services import professional_governance as governance
from services.proof_bridge import validate_sha256

RELATIONS = {"SUPPORTS", "DERIVES_FROM", "CONTRADICTS", "SUPERSEDES", "PROVES", "RELATES_TO"}
CONSUMERS = {"QUALITY", "LEGAL", "SECURITY", "PRIVACY", "RISK", "CERTIFICATION", "LEARNING", "GOVERNANCE"}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


async def register_node(
    *,
    actor_id: str,
    source_type: str,
    source_id: str,
    content_hash: str,
    provenance_refs: Iterable[str],
    access_policy_version_id: str,
    classification_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    digest = validate_sha256(content_hash)
    refs = list(dict.fromkeys(provenance_refs))
    if not source_type.strip() or not source_id.strip() or not refs:
        raise ValueError("source_type, source_id and provenance_refs are required")
    policy = await policy_registry.require_effective_version(access_policy_version_id)
    if policy.get("policy_key") != "EVIDENCE_ACCESS":
        raise ValueError("access policy version is not an EVIDENCE_ACCESS policy")
    if classification_id:
        classification = await db.resource_classifications.find_one(
            {"id": classification_id, "status": "CURRENT"}, {"_id": 0}
        )
        if not classification:
            raise LookupError("current classification not found")
    existing = await db.evidence_nodes.find_one(
        {"source_type": source_type.strip().upper(), "source_id": source_id.strip(), "content_hash": digest},
        {"_id": 0},
    )
    if existing:
        return existing
    row = {
        "id": _id("EVID"),
        "source_type": source_type.strip().upper(),
        "source_id": source_id.strip(),
        "content_hash": digest,
        "provenance_refs": refs,
        "classification_id": classification_id,
        "access_policy_version_id": policy["id"],
        "access_policy_hash": policy["content_hash"],
        "metadata": metadata or {},
        "status": "ACTIVE",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.evidence_nodes.insert_one(dict(row))
    await governance.audit_event(
        event_type="evidence.node.registered",
        actor_id=actor_id,
        resource_type="evidence_node",
        resource_id=row["id"],
        payload={"source_type": row["source_type"], "source_id": row["source_id"], "content_hash": digest},
    )
    return row


async def link_nodes(
    *, actor_id: str, from_node_id: str, to_node_id: str, relation: str, evidence_refs: Iterable[str]
) -> Dict[str, Any]:
    rel = relation.strip().upper()
    if rel not in RELATIONS:
        raise ValueError("invalid evidence relation")
    if from_node_id == to_node_id:
        raise ValueError("self-links are not allowed")
    refs = list(dict.fromkeys(evidence_refs))
    if not refs:
        raise ValueError("evidence graph link requires evidence_refs")
    nodes = await db.evidence_nodes.find(
        {"id": {"$in": [from_node_id, to_node_id]}, "status": "ACTIVE"}, {"_id": 0}
    ).to_list(2)
    if len(nodes) != 2:
        raise LookupError("evidence node not found")
    existing = await db.evidence_edges.find_one(
        {"from_node_id": from_node_id, "to_node_id": to_node_id, "relation": rel}, {"_id": 0}
    )
    if existing:
        return existing
    row = {
        "id": _id("EEDGE"),
        "from_node_id": from_node_id,
        "to_node_id": to_node_id,
        "relation": rel,
        "evidence_refs": refs,
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.evidence_edges.insert_one(dict(row))
    return row


async def create_pack(
    *,
    actor_id: str,
    title: str,
    consumer: str,
    node_ids: Iterable[str],
    purpose: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    target = consumer.strip().upper()
    if target not in CONSUMERS:
        raise ValueError("invalid evidence consumer")
    ids = list(dict.fromkeys(node_ids))
    refs = list(dict.fromkeys(evidence_refs))
    if not ids or not refs or not title.strip() or not purpose.strip():
        raise ValueError("title, purpose, node_ids and evidence_refs are required")
    nodes = await db.evidence_nodes.find({"id": {"$in": ids}, "status": "ACTIVE"}, {"_id": 0}).to_list(len(ids))
    if len(nodes) != len(ids):
        raise LookupError("one or more evidence nodes are missing")
    by_id = {node["id"]: node for node in nodes}
    ordered_refs = [
        {
            "node_id": node_id,
            "source_type": by_id[node_id]["source_type"],
            "source_id": by_id[node_id]["source_id"],
            "content_hash": by_id[node_id]["content_hash"],
            "access_policy_version_id": by_id[node_id]["access_policy_version_id"],
        }
        for node_id in ids
    ]
    row = {
        "id": _id("EPACK"),
        "title": title.strip(),
        "consumer": target,
        "purpose": purpose.strip(),
        "node_refs": ordered_refs,
        "evidence_refs": refs,
        "composition_mode": "REFERENCE_ONLY",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.evidence_packs.insert_one(dict(row))
    await governance.audit_event(
        event_type="evidence.pack.created",
        actor_id=actor_id,
        resource_type="evidence_pack",
        resource_id=row["id"],
        payload={"consumer": target, "node_ids": ids, "composition_mode": "REFERENCE_ONLY"},
    )
    return row


async def get_pack(pack_id: str) -> Dict[str, Any]:
    pack = await db.evidence_packs.find_one({"id": pack_id}, {"_id": 0})
    if not pack:
        raise LookupError("evidence pack not found")
    return pack


async def integrity_gate() -> Dict[str, Any]:
    nodes = await db.evidence_nodes.find({"status": "ACTIVE"}, {"_id": 0}).to_list(10000)
    node_ids = {node["id"] for node in nodes}
    edges = await db.evidence_edges.find({}, {"_id": 0}).to_list(10000)
    packs = await db.evidence_packs.find({}, {"_id": 0}).to_list(10000)
    dangling_edges = [e for e in edges if e["from_node_id"] not in node_ids or e["to_node_id"] not in node_ids]
    dangling_pack_refs = [
        {"pack_id": pack["id"], "node_id": ref["node_id"]}
        for pack in packs
        for ref in pack.get("node_refs", [])
        if ref["node_id"] not in node_ids
    ]
    blockers = len(dangling_edges) + len(dangling_pack_refs)
    return {
        "pass": blockers == 0,
        "blocking_count": blockers,
        "dangling_edges": dangling_edges,
        "dangling_pack_refs": dangling_pack_refs,
    }
