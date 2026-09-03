"""ACA-0005 — Module Lineage API.

Read access: any staff role (trainer/corrector/jury/admin/super_admin/
founder) — lineage context is useful to anyone grading or advising, not
just admins. Write access (create/update): admin roles only, mirroring
`fms.py`'s `/fms/import` precedent for governance-sensitive actions.

Every write goes through `fms_lineage.service`, which is the only place
the non-negotiable ACA-0005 rules are enforced — this router does no
business logic of its own, only auth + HTTP-shape translation.
"""

from __future__ import annotations

from typing import List, Literal

from fastapi import APIRouter, Depends, HTTPException

from auth import require_role
from fms_lineage import (
    LineageCreateInput,
    LineageError,
    LineageUpdateInput,
    ModuleLineage,
    ResolvedTarget,
    create_lineage,
    get_lineage_for_canonical_module,
    get_lineage_for_legacy_module,
    list_lineage_for_formation,
    resolve_canonical_target,
    update_lineage,
)
from models import ADMIN_ROLES, STAFF_ROLES, User

router = APIRouter(prefix="/fms/lineage", tags=["fms-lineage"])


@router.get(
    "/legacy/{formation_code}/{module_code}", response_model=List[ModuleLineage]
)
async def lineage_for_legacy(
    formation_code: str,
    module_code: str,
    active_only: bool = True,
    current: User = Depends(require_role(*STAFF_ROLES)),
):
    return await get_lineage_for_legacy_module(
        formation_code, module_code, active_only=active_only
    )


@router.get(
    "/canonical/{formation_code}/{module_code}", response_model=List[ModuleLineage]
)
async def lineage_for_canonical(
    formation_code: str,
    module_code: str,
    active_only: bool = True,
    current: User = Depends(require_role(*STAFF_ROLES)),
):
    return await get_lineage_for_canonical_module(
        formation_code, module_code, active_only=active_only
    )


@router.get("/formation/{formation_code}", response_model=List[ModuleLineage])
async def lineage_for_formation(
    formation_code: str,
    side: Literal["legacy", "canonical", "both"] = "both",
    active_only: bool = True,
    current: User = Depends(require_role(*STAFF_ROLES)),
):
    return await list_lineage_for_formation(
        formation_code, side=side, active_only=active_only
    )


@router.get("/resolve/{formation_code}/{module_code}", response_model=ResolvedTarget)
async def resolve(
    formation_code: str,
    module_code: str,
    current: User = Depends(require_role(*STAFF_ROLES)),
):
    """Conservative, read-only resolution of a legacy module's lineage.
    Never returns `credit_transfer=True` — see `fms_lineage/service.py`."""
    return await resolve_canonical_target(formation_code, module_code)


@router.post("", response_model=ModuleLineage)
async def create(
    payload: LineageCreateInput,
    current: User = Depends(require_role(*ADMIN_ROLES)),
):
    try:
        return await create_lineage(payload, created_by=current.id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.patch("/{lineage_id}", response_model=ModuleLineage)
async def update(
    lineage_id: str,
    payload: LineageUpdateInput,
    current: User = Depends(require_role(*ADMIN_ROLES)),
):
    try:
        return await update_lineage(lineage_id, payload)
    except LineageError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
