"""Admin control plane for validating and synchronizing Excel-derived masters."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from auth import require_role
from db import db
from models import User
from services.master_sync import sync_all_masters, validate_master_sources

router = APIRouter(prefix="/master", tags=["master-registry"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


@router.get("/sync/validate")
async def validate_excel_master_sources(current: User = Admin):
    try:
        return validate_master_sources()
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.post("/sync")
async def synchronize_excel_masters(current: User = Admin):
    """Fail-fast, idempotent refresh of all currently coded Excel masters."""
    try:
        return await sync_all_masters(db)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
