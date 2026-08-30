"""FMS resources — ZIP import (admin), search, navigation, dependency graph.

The "Importer un métier FMS" button (rule 15) is just this import endpoint
called from the Admin CMS; everything else here (search/nav/graph) is what
the rest of the platform (catalogue, module pages, admin) reads back.
"""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile

from auth import require_role
from db import db
from fms_import import (
    build_dependency_graph,
    build_navigation,
    import_fms_zip,
    search_resources,
)
from fms_import.models import ImportReport
from models import ADMIN_ROLES, User

router = APIRouter(prefix="/fms", tags=["fms"])

MAX_ZIP_BYTES = 50 * 1024 * 1024  # 50 MB — generous for a Markdown-only métier archive


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
):
    return await search_resources(q, formation_code, resource_type, limit)


@router.get("/resources/{code}")
async def get_resource(code: str):
    doc = await db.fms_resources.find_one({"code": code}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Ressource FMS introuvable")
    return doc


@router.get("/formations/{formation_code}/navigation")
async def get_navigation(formation_code: str):
    return await build_navigation(formation_code)


@router.get("/formations/{formation_code}/dependency-graph")
async def get_dependency_graph(formation_code: str):
    return await build_dependency_graph(formation_code)
