"""CVLN CareOps API — one service desk surface for Laurentia and CVLN Academy."""

from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from auth import get_current_user, require_role
from db import db
from models import ADMIN_ROLES, User
from services.careops import create_ticket, list_user_tickets
from services.careops_incidents import record_maintenance_result
from services.laurentia_careops import handle_with_laurentia

router = APIRouter(prefix="/careops", tags=["careops"])


class CareOpsIntake(BaseModel):
    message: str = Field(min_length=2, max_length=4000)
    product: str = Field(default="academy", min_length=2, max_length=64)
    channel: str = Field(default="academy", min_length=2, max_length=64)


class LaurentiaCareOpsInput(CareOpsIntake):
    session_id: str = Field(min_length=1, max_length=128)


class MaintenanceResultInput(BaseModel):
    success: bool
    evidence: Dict[str, Any]


@router.post("/intake")
async def intake(inp: CareOpsIntake, current: User = Depends(get_current_user)):
    ticket = await create_ticket(
        user_id=current.id,
        message=inp.message,
        product=inp.product,
        channel=inp.channel,
    )
    return {
        "ticket": ticket,
        "handled_by": "laurentia",
        "founder_required": False,
        "next_action": ticket["queue"],
    }


@router.post("/laurentia")
async def laurentia(
    inp: LaurentiaCareOpsInput,
    current: User = Depends(get_current_user),
):
    result = await handle_with_laurentia(
        user=current,
        session_id=inp.session_id,
        message=inp.message,
        product=inp.product,
        channel=inp.channel,
    )
    result["handled_by"] = "laurentia"
    result["founder_required"] = False
    return result


@router.get("/tickets")
async def my_tickets(
    limit: int = Query(default=50, ge=1, le=100),
    current: User = Depends(get_current_user),
):
    return await list_user_tickets(current.id, limit=limit)


@router.get("/tickets/{ticket_id}")
async def ticket_detail(ticket_id: str, current: User = Depends(get_current_user)):
    ticket = await db.careops_tickets.find_one(
        {"ticket_id": ticket_id, "user_id": current.id}, {"_id": 0}
    )
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket introuvable")
    return ticket


@router.get("/ops/incidents")
async def list_incidents(
    limit: int = Query(default=50, ge=1, le=100),
    current: User = Depends(require_role(*ADMIN_ROLES)),
):
    return await db.careops_incidents.find({}, {"_id": 0}).sort("created_at", -1).limit(limit).to_list(limit)


@router.get("/ops/maintenance")
async def list_maintenance(
    limit: int = Query(default=50, ge=1, le=100),
    current: User = Depends(require_role(*ADMIN_ROLES)),
):
    return await db.careops_maintenance.find({}, {"_id": 0}).sort("created_at", -1).limit(limit).to_list(limit)


@router.post("/ops/maintenance/{maintenance_id}/result")
async def maintenance_result(
    maintenance_id: str,
    inp: MaintenanceResultInput,
    current: User = Depends(require_role(*ADMIN_ROLES)),
):
    if not inp.evidence:
        raise HTTPException(status_code=422, detail="Preuve de vérification requise")
    try:
        return await record_maintenance_result(
            maintenance_id=maintenance_id,
            success=inp.success,
            evidence=inp.evidence,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Tâche de maintenance introuvable") from exc
