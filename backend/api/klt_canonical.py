"""Canonical Kiltikonet runtime API — "branchage complet de Kiltikonet"
(Founder, 2026-09-04). Mirrors `api/canonical.py` (ACA-0006) exactly:
every read requires real authenticated identity, import is admin-only.
Additive only — `formations.py`/legacy routes are untouched.
"""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException

from auth import get_current_user, require_role
from klt_canonical import (CanonicalKltFormation, CanonicalKltModule,
                           CanonicalKltModuleProgress, CanonicalKltSkill,
                           KltCanonicalImportResult, KltFileProvenance,
                           get_canonical_klt_formation,
                           get_canonical_klt_module, get_user_klt_progress,
                           import_klt_docs, list_canonical_klt_formations,
                           list_canonical_klt_modules,
                           list_canonical_klt_skills, list_klt_provenance,
                           record_klt_content_viewed)
from models import ADMIN_ROLES, STAFF_ROLES, User

router = APIRouter(prefix="/klt-canonical", tags=["canonical-kiltikonet"])


@router.get("/formations", response_model=List[CanonicalKltFormation])
async def list_formations(current: User = Depends(get_current_user)):
    return await list_canonical_klt_formations()


@router.get("/formations/{formation_code}", response_model=CanonicalKltFormation)
async def get_formation(formation_code: str, current: User = Depends(get_current_user)):
    formation = await get_canonical_klt_formation(formation_code)
    if not formation:
        raise HTTPException(
            status_code=404,
            detail="Formation Kiltikonet canonique introuvable (code inconnu ou pas "
            "encore importée).",
        )
    return formation


@router.get(
    "/formations/{formation_code}/modules", response_model=List[CanonicalKltModule]
)
async def list_modules(formation_code: str, current: User = Depends(get_current_user)):
    return await list_canonical_klt_modules(formation_code)


@router.get(
    "/formations/{formation_code}/modules/{module_code}",
    response_model=CanonicalKltModule,
)
async def get_module(
    formation_code: str, module_code: str, current: User = Depends(get_current_user)
):
    module = await get_canonical_klt_module(formation_code, module_code)
    if not module:
        raise HTTPException(
            status_code=404, detail="Module Kiltikonet canonique introuvable."
        )
    return module


@router.get(
    "/formations/{formation_code}/skills", response_model=List[CanonicalKltSkill]
)
async def list_skills(formation_code: str, current: User = Depends(get_current_user)):
    """Deliberately includes `BLOCKED` skills, not just `BUILT` ones —
    this is the one endpoint a client can use to render "5/7 built, 2
    blocked" honestly rather than silently listing only what exists."""
    return await list_canonical_klt_skills(formation_code)


@router.post(
    "/formations/{formation_code}/modules/{module_code}/viewed",
    response_model=CanonicalKltModuleProgress,
)
async def mark_content_viewed(
    formation_code: str, module_code: str, current: User = Depends(get_current_user)
):
    module = await get_canonical_klt_module(formation_code, module_code)
    if not module:
        raise HTTPException(
            status_code=404, detail="Module Kiltikonet canonique introuvable."
        )
    return await record_klt_content_viewed(current.id, formation_code, module_code)


@router.get("/progress/mine", response_model=List[CanonicalKltModuleProgress])
async def my_progress(
    formation_code: Optional[str] = None, current: User = Depends(get_current_user)
):
    return await get_user_klt_progress(current.id, klt_formation_code=formation_code)


@router.post("/import", response_model=KltCanonicalImportResult)
async def import_docs(current: User = Depends(require_role(*ADMIN_ROLES))):
    """Scans the real `docs/klt/` tree on the server filesystem and
    persists a structured read model — no upload, unlike FMS's ZIP
    import, since the Kiltikonet corpus already lives unpacked in this
    repo. Idempotent: safe to re-run after any docs/klt/ update."""
    return await import_klt_docs(created_by=current.id)


@router.get("/provenance", response_model=List[KltFileProvenance])
async def provenance(current: User = Depends(require_role(*STAFF_ROLES))):
    """The full source-file ledger — every real file under docs/klt/,
    parsed or not. Staff-only audit surface."""
    return await list_klt_provenance()
