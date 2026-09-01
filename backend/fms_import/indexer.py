"""Search index + auto-generated navigation/sommaire + dependency graph.

Three things every imported FMS batch needs, built from the same
`fms_resources` collection:

1. A Mongo text index (search engine — swappable later for a dedicated
   search service without changing the query-side API contract).
2. A navigation tree: formation -> resource type -> resources, in a
   stable order, for the "sommaire" auto-generated per formation.
3. A prerequisites graph: which resources unlock which.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from db import db
from models import Formation

from .models import RESOURCE_TYPE_LABELS

_TEXT_INDEX_ENSURED = False

# Sommaire order: conceptual before applied, applied before evaluated —
# mirrors the gabarit's own 10-step construction sequence (see
# 00_GABARIT_Construction_Metier.md §1).
TYPE_ORDER = [
    "referentiel",
    "matrice_pedagogique",
    "learning_map",
    "module_map",
    "cas_fil_rouge",
    "competency_matrix",
    "matrice_tracabilite",
    "infrastructure",
    "evidence_registry",
    "skill_ids_registry",
    "rubric_master",
    "blueprint",
    "module",
    "guide_formateur",
    "guide_correcteur",
    "guide_candidat",
    "templates_etudiants",
    "banque_n1",
    "banque_n2",
    "cas_inedit",
    "sujet_officiel",
    "grille_certificative",
    "guide_jury",
    "note_harmonisation",
    "guide",
    "gabarit",
    "index",
]


async def ensure_search_index() -> None:
    """Idempotent — safe to call on every import (and at app startup)."""
    global _TEXT_INDEX_ENSURED
    if _TEXT_INDEX_ENSURED:
        return
    await db.fms_resources.create_index(
        [("title", "text"), ("body_markdown", "text"), ("code", "text")],
        name="fms_resources_text",
    )
    await db.fms_resources.create_index("code")
    await db.fms_resources.create_index("formation_code")
    _TEXT_INDEX_ENSURED = True


async def search_resources(
    query: str = "",
    formation_code: Optional[str] = None,
    resource_type: Optional[str] = None,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    await ensure_search_index()
    mongo_filter: Dict[str, Any] = {}
    if query:
        mongo_filter["$text"] = {"$search": query}
    if formation_code:
        mongo_filter["formation_code"] = formation_code
    if resource_type:
        mongo_filter["type"] = resource_type

    projection: Dict[str, Any] = {"_id": 0}
    if query:
        projection["score"] = {"$meta": "textScore"}
    cursor = db.fms_resources.find(mongo_filter, projection)
    if query:
        cursor = cursor.sort([("score", {"$meta": "textScore"})])
    return await cursor.to_list(limit)


async def build_navigation(formation_code: str) -> Dict[str, Any]:
    """Auto-generated sommaire for one formation — grouped by resource
    type, in TYPE_ORDER, each group sorted by code."""
    docs = await db.fms_resources.find(
        {"formation_code": formation_code}, {"_id": 0}
    ).to_list(1000)
    by_type: Dict[str, List[Dict[str, Any]]] = {}
    for d in docs:
        by_type.setdefault(d["type"], []).append(d)
    for group in by_type.values():
        group.sort(key=lambda r: r["code"])

    formation_doc = await db.formations.find_one({"code": formation_code}, {"_id": 0})
    formation = Formation(**formation_doc) if formation_doc else None

    sections = [
        {
            "type": t,
            "label": RESOURCE_TYPE_LABELS[t],
            "resources": [
                {"code": r["code"], "title": r["title"], "version": r["version"]}
                for r in by_type.get(t, [])
            ],
        }
        for t in TYPE_ORDER
        if by_type.get(t)
    ]
    return {
        "formation_code": formation_code,
        "formation_name": formation.name if formation else None,
        "sections": sections,
        "total_resources": len(docs),
    }


async def build_dependency_graph(formation_code: str) -> Dict[str, Any]:
    """Prerequisite edges between resources of one formation — the raw
    data a "module map" / roadmap view renders from."""
    docs = await db.fms_resources.find(
        {"formation_code": formation_code}, {"_id": 0}
    ).to_list(1000)
    nodes = [{"code": d["code"], "type": d["type"], "title": d["title"]} for d in docs]
    edges = [
        {"from": prereq, "to": d["code"]}
        for d in docs
        for prereq in d.get("prerequisites", [])
    ]
    return {"formation_code": formation_code, "nodes": nodes, "edges": edges}
