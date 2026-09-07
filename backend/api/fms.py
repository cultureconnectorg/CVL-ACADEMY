"""FMS resources — ZIP import (admin), search, navigation, dependency graph.

The "Importer un métier FMS" button (rule 15) is just this import endpoint
called from the Admin CMS; everything else here (search/nav/graph) is what
the rest of the platform (catalogue, module pages, admin) reads back.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile

from auth import get_current_user, require_role
from db import db
from fms_canonical.models import is_learner_facing
from fms_import import (
    build_dependency_graph,
    build_navigation,
    import_fms_zip,
    search_resources,
)
from fms_import.models import ImportReport
from models import ADMIN_ROLES, STAFF_ROLES, User

router = APIRouter(prefix="/fms", tags=["fms"])

MAX_ZIP_BYTES = 50 * 1024 * 1024  # 50 MB — generous for a Markdown-only métier archive


def _visible_to(current: User, resource_type: str) -> bool:
    """AUTH-01 sweep (Audit Chirurgical 2026-09-07) — the legacy
    `fms_import`/`db.fms_resources` surface (search, direct lookup,
    navigation, dependency graph) had no audience filtering at all,
    unauthenticated or not: `banque_n1`/`banque_n2`/`cas_inedit`/
    `sujet_officiel`/`grille_certificative`/`guide_jury`/`guide_
    correcteur` — real exam/grading material — were reachable by
    anyone who could guess or search for a resource code. Reuses
    `fms_canonical.models.RESOURCE_AUDIENCE` rather than inventing a
    second mapping: it already classifies this exact same
    `FmsResourceType` vocabulary (fms_canonical's own docstring
    confirms it was built "exhaustively" against `fms_import`'s real
    26-type table) — one taxonomy, not two that could drift apart.
    Staff (STAFF_ROLES) sees everything, matching every other admin/
    staff surface in this codebase."""
    if current.role in STAFF_ROLES:
        return True
    return is_learner_facing(resource_type)


@router.post("/import", response_model=ImportReport)
async def import_zip(
    file: UploadFile = File(...),
    current: User = Depends(require_role(*ADMIN_ROLES)),
):
    if not file.filename or not file.filename.lower().endswith(".zip"):
        raise HTTPException(
            status_code=400, detail="Le fichier doit être une archive .zip"
        )
    raw = await file.read()
    if len(raw) > MAX_ZIP_BYTES:
        raise HTTPException(
            status_code=400, detail="Archive trop volumineuse (max 50 Mo)."
        )
    return await import_fms_zip(raw, file.filename, created_by=current.id)


@router.get("/imports", response_model=List[ImportReport])
async def list_imports(current: User = Depends(require_role(*ADMIN_ROLES))):
    docs = await db.fms_imports.find({}, {"_id": 0}).sort("created_at", -1).to_list(200)
    return [ImportReport(**d) for d in docs]


@router.get("/imports/{import_id}", response_model=ImportReport)
async def get_import(
    import_id: str, current: User = Depends(require_role(*ADMIN_ROLES))
):
    doc = await db.fms_imports.find_one({"id": import_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Rapport d'import introuvable")
    return ImportReport(**doc)


@router.get("/resources")
async def list_resources(
    q: str = "",
    formation_code: Optional[str] = None,
    resource_type: Optional[str] = Query(None, alias="type"),
    limit: int = 50,
    current: User = Depends(get_current_user),
):
    results = await search_resources(q, formation_code, resource_type, limit)
    return [r for r in results if _visible_to(current, r.get("type", ""))]


@router.get("/resources/{code}")
async def get_resource(code: str, current: User = Depends(get_current_user)):
    doc = await db.fms_resources.find_one({"code": code}, {"_id": 0})
    if not doc or not _visible_to(current, doc.get("type", "")):
        # Same 404 whether the resource doesn't exist or exists but is
        # staff-only — never a distinct "exists but you can't see it"
        # response that would itself leak which codes are real.
        raise HTTPException(status_code=404, detail="Ressource FMS introuvable")
    return doc


@router.get("/formations/{formation_code}/navigation")
async def get_navigation(
    formation_code: str, current: User = Depends(get_current_user)
) -> Dict[str, Any]:
    nav = await build_navigation(formation_code)
    sections = [
        {**section, "resources": [
            r for r in section["resources"] if _visible_to(current, section["type"])
        ]}
        for section in nav["sections"]
    ]
    nav["sections"] = [s for s in sections if s["resources"]]
    return nav


@router.get("/formations/{formation_code}/dependency-graph")
async def get_dependency_graph(
    formation_code: str, current: User = Depends(get_current_user)
) -> Dict[str, Any]:
    graph = await build_dependency_graph(formation_code)
    visible_codes = {
        n["code"] for n in graph["nodes"] if _visible_to(current, n["type"])
    }
    graph["nodes"] = [n for n in graph["nodes"] if n["code"] in visible_codes]
    graph["edges"] = [
        e for e in graph["edges"]
        if e["from"] in visible_codes and e["to"] in visible_codes
    ]
    return graph
