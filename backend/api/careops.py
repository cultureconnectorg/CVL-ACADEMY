"""CVLN CareOps API — one service desk surface for Laurentia and CVLN Academy."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from auth import get_current_user
from models import User
from services.careops import create_ticket, list_user_tickets

router = APIRouter(prefix="/careops", tags=["careops"])


class CareOpsIntake(BaseModel):
    message: str = Field(min_length=2, max_length=4000)
    product: str = Field(default="academy", min_length=2, max_length=64)
    channel: str = Field(default="academy", min_length=2, max_length=64)


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


@router.get("/tickets")
async def my_tickets(
    limit: int = Query(default=50, ge=1, le=100),
    current: User = Depends(get_current_user),
):
    return await list_user_tickets(current.id, limit=limit)


@router.get("/tickets/{ticket_id}")
async def ticket_detail(ticket_id: str, current: User = Depends(get_current_user)):
    from db import db

    ticket = await db.careops_tickets.find_one(
        {"ticket_id": ticket_id, "user_id": current.id}, {"_id": 0}
    )
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket introuvable")
    return ticket
