"""Missions — catalogue, accept, submit, mine."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException

from auth import get_current_user
from badges_engine import award_threshold_badges
from db import db, utc_now_iso
from models import User
from services.frek_core import frek_core

router = APIRouter(prefix="/missions", tags=["missions"])


@router.get("")
async def list_missions():
    return await db.missions.find({}, {"_id": 0}).to_list(200)


@router.get("/mine")
async def my_missions(current: User = Depends(get_current_user)):
    return await db.user_missions.find({"user_id": current.id}, {"_id": 0}).to_list(200)


@router.post("/{mission_code}/accept")
async def accept_mission(mission_code: str, current: User = Depends(get_current_user)):
    mission = await db.missions.find_one({"code": mission_code}, {"_id": 0})
    if not mission:
        raise HTTPException(status_code=404, detail="Mission introuvable")
    existing = await db.user_missions.find_one(
        {"user_id": current.id, "mission_code": mission_code}
    )
    if existing:
        return {"ok": True, "status": existing.get("status", "accepted")}
    await db.user_missions.insert_one(
        {
            "id": str(uuid.uuid4()),
            "user_id": current.id,
            "mission_code": mission_code,
            "status": "accepted",
            "accepted_at": utc_now_iso(),
        }
    )
    await frek_core.emit_signal(current.id, "FREK-MISSION", {"mission": mission_code})
    return {"ok": True, "status": "accepted"}


@router.post("/{mission_code}/submit")
async def submit_mission(
    mission_code: str,
    current: User = Depends(get_current_user),
):
    mission = await db.missions.find_one({"code": mission_code}, {"_id": 0})
    if not mission:
        raise HTTPException(status_code=404, detail="Mission introuvable")
    await db.user_missions.update_one(
        {"user_id": current.id, "mission_code": mission_code},
        {
            "$set": {
                "user_id": current.id,
                "mission_code": mission_code,
                "status": "validated",
                "submitted_at": utc_now_iso(),
            }
        },
        upsert=True,
    )
    reward = int(mission.get("cc_reward", 0))
    new_cc = current.cc_credits + reward
    new_stade = frek_core.resolve_stade(new_cc)
    await db.users.update_one(
        {"id": current.id}, {"$set": {"cc_credits": new_cc, "stade": new_stade}}
    )
    await frek_core.emit_signal(current.id, "FREK-WORK", {"mission": mission_code})
    await award_threshold_badges(current.id, new_cc)
    return {"ok": True, "cc_earned": reward, "new_stade": new_stade}
