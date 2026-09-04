"""ACA-0006 — Canonical FMS runtime API.

Every read and write here is scoped to real, authenticated identity —
`PUBLIC_DISCOVERY_ACTIVATION = OUT_OF_SCOPE` for this mission, so unlike
`formations.py` this router does not use `get_current_user_optional`
anywhere; every route requires `get_current_user`. Import stays
admin-only, mirroring `fms.py`'s existing `/fms/import` precedent.
"""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from auth import get_current_user, require_role
from fms_canonical import (
    CanonicalFormation,
    CanonicalImportResult,
    CanonicalModule,
    CanonicalModuleProgress,
    CanonicalSkillDefinition,
    FileProvenance,
    count_zip_files,
    get_canonical_formation,
    get_canonical_module,
    get_user_canonical_progress,
    import_canonical_fms_zip,
    list_canonical_formations,
    list_canonical_modules,
    list_canonical_skill_definitions,
    list_zip_provenance,
    record_content_viewed,
)
from models import ADMIN_ROLES, STAFF_ROLES, User

router = APIRouter(prefix="/canonical", tags=["canonical-fms"])

MAX_ZIP_BYTES = 50 * 1024 * 1024


@router.get("/formations", response_model=List[CanonicalFormation])
async def list_formations(current: User = Depends(get_current_user)):
    return await list_canonical_formations()


@router.get("/formations/{formation_code}", response_model=CanonicalFormation)
async def get_formation(formation_code: str, current: User = Depends(get_current_user)):
    formation = await get_canonical_formation(formation_code)
    if not formation:
        raise HTTPException(
            status_code=404,
            detail="Formation canonique introuvable (métier inconnu ou pas encore importé).",
        )
    return formation


@router.get(
    "/formations/{formation_code}/modules", response_model=List[CanonicalModule]
)
async def list_modules(formation_code: str, current: User = Depends(get_current_user)):
    return await list_canonical_modules(formation_code)


@router.get(
    "/formations/{formation_code}/modules/{module_code}", response_model=CanonicalModule
)
async def get_module(
    formation_code: str, module_code: str, current: User = Depends(get_current_user)
):
    module = await get_canonical_module(formation_code, module_code)
    if not module:
        raise HTTPException(status_code=404, detail="Module canonique introuvable.")
    return module


@router.get(
    "/formations/{formation_code}/skills", response_model=List[CanonicalSkillDefinition]
)
async def list_skills(formation_code: str, current: User = Depends(get_current_user)):
    return await list_canonical_skill_definitions(formation_code)


@router.post(
    "/formations/{formation_code}/modules/{module_code}/viewed",
    response_model=CanonicalModuleProgress,
)
async def mark_content_viewed(
    formation_code: str, module_code: str, current: User = Depends(get_current_user)
):
    module = await get_canonical_module(formation_code, module_code)
    if not module:
        raise HTTPException(status_code=404, detail="Module canonique introuvable.")
    return await record_content_viewed(current.id, formation_code, module_code)


@router.get("/progress/mine", response_model=List[CanonicalModuleProgress])
async def my_progress(
    formation_code: Optional[str] = None, current: User = Depends(get_current_user)
):
    return await get_user_canonical_progress(
        current.id, canonical_formation_code=formation_code
    )


@router.post("/import", response_model=CanonicalImportResult)
async def import_zip(
    file: UploadFile = File(...),
    current: User = Depends(require_role(*ADMIN_ROLES)),
):
    """Imports an FMS archive AND, per the Founder's blocking correction,
    unconditionally builds the full per-file provenance ledger alongside
    it — `all_zip_files_accounted_for` is a real cross-check (independent
    ZIP entry count vs. provenance records written), not an assumption."""
    if not file.filename or not file.filename.lower().endswith(".zip"):
        raise HTTPException(
            status_code=400, detail="Le fichier doit être une archive .zip"
        )
    raw = await file.read()
    if len(raw) > MAX_ZIP_BYTES:
        raise HTTPException(
            status_code=400, detail="Archive trop volumineuse (max 50 Mo)."
        )
    report, provenance_records, inserted, updated = await import_canonical_fms_zip(
        raw, file.filename, created_by=current.id
    )
    zip_total = count_zip_files(raw)
    parsed = sum(1 for r in provenance_records if r.parsing_status == "parsed")
    unparsed = len(provenance_records) - parsed
    return CanonicalImportResult(
        import_id=report.id,
        zip_total_files=zip_total,
        parsed_count=parsed,
        unparsed_count=unparsed,
        provenance_inserted=inserted,
        provenance_updated=updated,
        all_zip_files_accounted_for=(zip_total == len(provenance_records)),
    )


@router.get("/provenance", response_model=List[FileProvenance])
async def provenance(current: User = Depends(require_role(*STAFF_ROLES))):
    """The full source-file ledger — every real ZIP entry, parsed or
    not, with its sha256/byte_size/audience. Staff-only: this is an
    audit surface, not learner content."""
    return await list_zip_provenance()
