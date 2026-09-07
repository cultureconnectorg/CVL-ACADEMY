"""Canonical FREK runtime API — "raccorder ces corpus au même
runtime/funnel Academy" (Founder instruction, 2026-09-07). Mirrors
`api/kor_canonical.py`/`api/klt_canonical.py` exactly: every read
requires real authenticated identity, import is admin-only. Additive
only — `formations.py`/legacy routes and every other canonical package
are untouched.

No `/skills` or `/modules/{code}/viewed` staff-facing skill-registry
endpoint here (unlike KOR) — FRK's real corpus carries no skill
registry (see `frk_canonical/models.py`'s own docstring for why).
"""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException

from auth import get_current_user, require_role
from frk_canonical import (CanonicalFrkFormation, CanonicalFrkModule,
                           CanonicalFrkModuleProgress, FrkCanonicalImportResult,
                           FrkFileProvenance, get_canonical_frk_formation,
                           get_canonical_frk_module, get_user_frk_progress,
                           import_frk_docs, list_canonical_frk_formations,
                           list_canonical_frk_modules, list_frk_provenance,
                           record_content_viewed)
from models import ADMIN_ROLES, STAFF_ROLES, User

router = APIRouter(prefix="/frk-canonical", tags=["canonical-frek"])


@router.get("/formations", response_model=List[CanonicalFrkFormation])
async def list_formations(current: User = Depends(get_current_user)):
    return await list_canonical_frk_formations()


@router.get("/formations/{formation_code}", response_model=CanonicalFrkFormation)
async def get_formation(formation_code: str, current: User = Depends(get_current_user)):
    formation = await get_canonical_frk_formation(formation_code)
    if not formation:
        raise HTTPException(
            status_code=404,
            detail="Formation FREK canonique introuvable (code inconnu, pas "
            "encore importée, ou bloquée/non construite — voir "
            "docs/frk/README.md).",
        )
    return formation


@router.get(
    "/formations/{formation_code}/modules", response_model=List[CanonicalFrkModule]
)
async def list_modules(formation_code: str, current: User = Depends(get_current_user)):
    return await list_canonical_frk_modules(formation_code)


@router.get(
    "/formations/{formation_code}/modules/{module_code}",
    response_model=CanonicalFrkModule,
)
async def get_module(
    formation_code: str, module_code: str, current: User = Depends(get_current_user)
):
    module = await get_canonical_frk_module(formation_code, module_code)
    if not module:
        raise HTTPException(status_code=404, detail="Module FREK canonique introuvable.")
    return module


@router.post(
    "/formations/{formation_code}/modules/{module_code}/viewed",
    response_model=CanonicalFrkModuleProgress,
)
async def mark_content_viewed(
    formation_code: str, module_code: str, current: User = Depends(get_current_user)
):
    module = await get_canonical_frk_module(formation_code, module_code)
    if not module:
        raise HTTPException(status_code=404, detail="Module FREK canonique introuvable.")
    return await record_content_viewed(current.id, formation_code, module_code)


@router.get("/progress/mine", response_model=List[CanonicalFrkModuleProgress])
async def my_progress(
    formation_code: Optional[str] = None, current: User = Depends(get_current_user)
):
    return await get_user_frk_progress(current.id, frk_formation_code=formation_code)


@router.post("/import", response_model=FrkCanonicalImportResult)
async def import_docs(current: User = Depends(require_role(*ADMIN_ROLES))):
    """Scans the real `docs/frk/` tree on the server filesystem and
    persists a structured read model — no upload, since the FREK corpus
    already lives unpacked in this repo. Idempotent: safe to re-run
    after any docs/frk/ update."""
    return await import_frk_docs(created_by=current.id)


@router.get("/provenance", response_model=List[FrkFileProvenance])
async def provenance(current: User = Depends(require_role(*STAFF_ROLES))):
    """The full source-file ledger — every real file under docs/frk/,
    parsed or not. Staff-only audit surface."""
    return await list_frk_provenance()
