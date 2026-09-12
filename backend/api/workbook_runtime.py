"""Admin inspection and repair surface for source-backed workbook runtimes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from auth import require_role
from db import db
from models import User
from services.workbook_runtime import ensure_workbook_runtimes, workbook_runtime_summary

router = APIRouter(prefix="/workbooks/runtime", tags=["workbook-runtime"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


@router.get("/summary")
async def runtime_summary(current: User = Admin):
    summary = await workbook_runtime_summary(db)
    summary["all_ready"] = all(section["ready"] for section in summary.values())
    return summary


@router.post("/sync")
async def sync_runtime(current: User = Admin):
    result = await ensure_workbook_runtimes(db)
    if not result["all_ready"]:
        raise HTTPException(
            status_code=503,
            detail="workbook runtime reconciliation incomplete",
        )
    return result
