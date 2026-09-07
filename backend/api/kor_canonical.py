"""Canonical KORA runtime API — RAIL 2 ("Master -> Runtime Academy",
Founder, 2026-09-06). Mirrors `api/klt_canonical.py` exactly: every read
requires real authenticated identity, import is admin-only. Additive
only — `formations.py`/legacy routes are untouched.
"""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException

from auth import get_current_user, require_role
from kor_canonical import (CanonicalKorFormation, CanonicalKorModule,
                           CanonicalKorModuleProgress, CanonicalKorSkill,
                           KorCanonicalImportResult, KorFileProvenance,
                           get_canonical_kor_formation,
                           get_canonical_kor_module, get_user_kor_progress,
                           import_kor_docs, list_canonical_kor_formations,
                           list_canonical_kor_modules,
                           list_canonical_kor_skills, list_kor_provenance,
                           record_content_viewed)
from models import ADMIN_ROLES, STAFF_ROLES, User

router = APIRouter(prefix="/kor-canonical", tags=["canonical-kora"])


@router.get("/formations", response_model=List[CanonicalKorFormation])
async def list_formations(current: User = Depends(get_current_user)):
    return await list_canonical_kor_formations()


@router.get("/formations/{formation_code}", response_model=CanonicalKorFormation)
async def get_formation(formation_code: str, current: User = Depends(get_current_user)):
    formation = await get_canonical_kor_formation(formation_code)
    if not formation:
        raise HTTPException(
            status_code=404,
            detail="Formation KORA canonique introuvable (code inconnu ou pas "
            "encore importée).",
        )
    return formation


@router.get(
    "/formations/{formation_code}/modules", response_model=List[CanonicalKorModule]
)
async def list_modules(formation_code: str, current: User = Depends(get_current_user)):
    return await list_canonical_kor_modules(formation_code)


@router.get(
    "/formations/{formation_code}/modules/{module_code}",
    response_model=CanonicalKorModule,
)
async def get_module(
    formation_code: str, module_code: str, current: User = Depends(get_current_user)
):
    module = await get_canonical_kor_module(formation_code, module_code)
    if not module:
        raise HTTPException(status_code=404, detail="Module KORA canonique introuvable.")
    return module


@router.get(
    "/formations/{formation_code}/skills", response_model=List[CanonicalKorSkill]
)
async def list_skills(formation_code: str, current: User = Depends(get_current_user)):
    return await list_canonical_kor_skills(formation_code)


@router.post(
    "/formations/{formation_code}/modules/{module_code}/viewed",
    response_model=CanonicalKorModuleProgress,
)
async def mark_content_viewed(
    formation_code: str, module_code: str, current: User = Depends(get_current_user)
):
    module = await get_canonical_kor_module(formation_code, module_code)
    if not module:
        raise HTTPException(status_code=404, detail="Module KORA canonique introuvable.")
    return await record_content_viewed(current.id, formation_code, module_code)


@router.get("/progress/mine", response_model=List[CanonicalKorModuleProgress])
async def my_progress(
    formation_code: Optional[str] = None, current: User = Depends(get_current_user)
):
    return await get_user_kor_progress(current.id, kor_formation_code=formation_code)


@router.post("/import", response_model=KorCanonicalImportResult)
async def import_docs(current: User = Depends(require_role(*ADMIN_ROLES))):
    """Scans the real `docs/kor/` tree on the server filesystem and
    persists a structured read model — no upload, unlike FMS's ZIP
    import, since the KORA corpus already lives unpacked in this repo.
    Idempotent: safe to re-run after any docs/kor/ update."""
    return await import_kor_docs(created_by=current.id)


@router.get("/provenance", response_model=List[KorFileProvenance])
async def provenance(current: User = Depends(require_role(*STAFF_ROLES))):
    """The full source-file ledger — every real file under docs/kor/,
    parsed or not. Staff-only audit surface."""
    return await list_kor_provenance()
