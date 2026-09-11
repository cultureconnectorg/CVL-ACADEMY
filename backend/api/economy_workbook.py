"""Admin runtime access to every projected Economy 3D workbook row."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from auth import require_role
from db import db
from models import User
from services.economy_learning_to_work import calculate_mission_fees
from services.economy_workbook_runtime import (
    OFFER_PHASE,
    SHEETS,
    set_phase_state,
)

router = APIRouter(
    prefix="/master/economy-workbook",
    tags=["master-registry"],
)
Admin = Depends(require_role("admin", "super_admin", "founder"))


class PhaseStatePayload(BaseModel):
    active: bool
    evidence_ref: str = ""


@router.get("/summary")
async def economy_workbook_summary(current: User = Admin):
    manifest = await db.academy_economy_workbook_manifest.find_one(
        {"kind": "ECONOMY_3D_WORKBOOK"},
        {"_id": 0},
    )
    runtime_rows = await db.academy_economy_workbook_rows.count_documents({})
    return {
        "expected_sheets": len(SHEETS),
        "runtime_rows": runtime_rows,
        "manifest": manifest,
    }


@router.get("/sheets")
async def list_economy_workbook_sheets(current: User = Admin):
    manifest = await db.academy_economy_workbook_manifest.find_one(
        {"kind": "ECONOMY_3D_WORKBOOK"},
        {"_id": 0},
    )
    counts = (manifest or {}).get("sheet_rows", {})
    return [
        {"sheet": sheet, "runtime_rows": counts.get(sheet, 0)}
        for sheet in SHEETS
    ]


@router.get("/sheets/{sheet}")
async def economy_workbook_sheet(
    sheet: str,
    limit: int = Query(default=1000, ge=1, le=2000),
    current: User = Admin,
):
    if sheet not in SHEETS:
        raise HTTPException(
            status_code=404,
            detail="unknown Economy workbook sheet",
        )
    return (
        await db.academy_economy_workbook_rows.find(
            {"sheet": sheet},
            {"_id": 0},
        )
        .sort("csv_row", 1)
        .limit(limit)
        .to_list(limit)
    )


@router.get("/sheets/{sheet}/rows/{csv_row}")
async def economy_workbook_row(
    sheet: str,
    csv_row: int,
    current: User = Admin,
):
    if sheet not in SHEETS:
        raise HTTPException(
            status_code=404,
            detail="unknown Economy workbook sheet",
        )
    row = await db.academy_economy_workbook_rows.find_one(
        {"sheet": sheet, "csv_row": csv_row},
        {"_id": 0},
    )
    if not row:
        raise HTTPException(
            status_code=404,
            detail="Economy workbook row not found",
        )
    return row


@router.get("/learning-to-work/mission-fee")
async def learning_to_work_mission_fee(
    gmv_eur: float = Query(gt=0),
    current: User = Admin,
):
    return calculate_mission_fees(gmv_eur)


@router.get("/phases")
async def economy_phase_states(current: User = Admin):
    states = await db.academy_economy_phase_state.find(
        {},
        {"_id": 0},
    ).to_list(10)
    by_phase = {state["phase"]: state for state in states}
    return {
        "offer_phase": OFFER_PHASE,
        "states": {
            phase: by_phase.get(
                phase,
                {"phase": phase, "active": False},
            )
            for phase in ("PHASE_2", "PHASE_3")
        },
    }


@router.put("/phases/{phase}")
async def update_economy_phase(
    phase: str,
    payload: PhaseStatePayload,
    current: User = Admin,
):
    try:
        return await set_phase_state(
            db,
            phase=phase,
            active=payload.active,
            evidence_ref=payload.evidence_ref,
            actor_id=current.id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
