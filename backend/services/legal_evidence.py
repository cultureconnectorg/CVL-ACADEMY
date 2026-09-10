"""Legal Evidence Pack composer (LEG-014).

Packs contain references to XCP-004 Evidence Graph nodes only. Legal source payloads
are never copied into a parallel evidence store.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable

from db import db
from services import evidence_graph


async def create_legal_pack(
    *,
    actor_id: str,
    matter_id: str,
    title: str,
    purpose: str,
    node_ids: Iterable[str],
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    matter = await db.legal_matters.find_one({"id": matter_id}, {"_id": 0})
    if not matter:
        raise LookupError("legal matter not found")
    ids = list(dict.fromkeys(str(value).strip() for value in node_ids if str(value).strip()))
    refs = list(dict.fromkeys(str(value).strip() for value in evidence_refs if str(value).strip()))
    if not ids or not refs:
        raise ValueError("legal evidence pack requires nodes and evidence")

    nodes = await db.evidence_nodes.find(
        {"id": {"$in": ids}, "status": "ACTIVE"}, {"_id": 0}
    ).to_list(len(ids))
    if len(nodes) != len(ids):
        raise LookupError("one or more evidence nodes are missing")
    for node in nodes:
        linked_matter = (node.get("metadata") or {}).get("matter_id")
        if linked_matter and linked_matter != matter_id:
            raise PermissionError("evidence node belongs to another legal matter")

    pack = await evidence_graph.create_pack(
        actor_id=actor_id,
        title=title,
        consumer="LEGAL",
        node_ids=ids,
        purpose=purpose,
        evidence_refs=[matter_id, *refs],
    )
    await db.evidence_packs.update_one(
        {"id": pack["id"]},
        {"$set": {"legal_matter_id": matter_id}},
    )
    return {**pack, "legal_matter_id": matter_id}


async def list_matter_packs(matter_id: str) -> list[Dict[str, Any]]:
    if not await db.legal_matters.find_one({"id": matter_id}):
        raise LookupError("legal matter not found")
    return await db.evidence_packs.find(
        {"consumer": "LEGAL", "legal_matter_id": matter_id}, {"_id": 0}
    ).sort("created_at", 1).to_list(1000)
