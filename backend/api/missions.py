"""Missions — catalogue, accept, submit, mine."""

from __future__ import annotations

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from auth import get_current_user, get_current_user_optional
from badges_engine import award_threshold_badges
from db import db, utc_now_iso
from models import User
from qualification import has_any_of
from services.frek_core import frek_core

router = APIRouter(prefix="/missions", tags=["missions"])


@router.get("")
async def list_missions(current: Optional[User] = Depends(get_current_user_optional)):
    """RAIL 2 — the Opportunity view: each mission is annotated with
    `eligible` (never filtered out — the catalogue stays browsable so a
    learner can see what to work towards). A mission with no
    `required_qualification_codes` (every mission that predates this
    ticket) is `eligible=True` for everyone, signed in or not."""
    missions = await db.missions.find({}, {"_id": 0}).to_list(200)
    for m in missions:
        required = m.get("required_qualification_codes") or []
        if not required:
            m["eligible"] = True
        elif current is None:
            m["eligible"] = False
        else:
            m["eligible"] = await has_any_of(current.id, required)
    return missions


@router.get("/mine")
async def my_missions(current: User = Depends(get_current_user)):
    return await db.user_missions.find({"user_id": current.id}, {"_id": 0}).to_list(200)


@router.post("/{mission_code}/accept")
async def accept_mission(mission_code: str, current: User = Depends(get_current_user)):
    mission = await db.missions.find_one({"code": mission_code}, {"_id": 0})
    if not mission:
        raise HTTPException(status_code=404, detail="Mission introuvable")
    required = mission.get("required_qualification_codes") or []
    if required and not await has_any_of(current.id, required):
        raise HTTPException(
            status_code=403,
            detail="Qualification requise non détenue pour cette mission",
        )
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
    """ECON-01 (Audit Chirurgical 2026-09-07) — closes the reward-farming
    path a repeated submit used to open: no prior-state check (a submit
    with no accepted `user_mission` at all still validated and paid
    out), no re-verified eligibility, and no protection against a
    second submit paying out a second time.

    State machine enforced here: `accepted` -> `validated`, exactly
    once. The transition itself is the idempotency guard — `update_one`
    filtered on `status: "accepted"` is MongoDB's own compare-and-swap:
    under real concurrency (two near-simultaneous submits, or a client
    retry racing the original request) at most one call's filter can
    still match "accepted" by the time it executes, so at most one call
    ever proceeds to `modified_count == 1` and only that call credits
    CC. Every other call — concurrent or a plain repeat afterwards —
    sees `modified_count == 0`, and returns the same, already-settled
    result with `cc_earned: 0` rather than crediting again.
    """
    mission = await db.missions.find_one({"code": mission_code}, {"_id": 0})
    if not mission:
        raise HTTPException(status_code=404, detail="Mission introuvable")

    existing = await db.user_missions.find_one(
        {"user_id": current.id, "mission_code": mission_code}, {"_id": 0}
    )
    if not existing:
        raise HTTPException(
            status_code=400,
            detail="Vous devez accepter cette mission avant de la soumettre.",
        )
    if existing.get("status") == "validated":
        # Idempotent no-op: the reward was already granted exactly once.
        return {"ok": True, "cc_earned": 0, "new_stade": current.stade, "already_validated": True}

    # Re-verify eligibility at submit time, not just at accept time — a
    # qualification held when the mission was accepted may since have
    # been revoked.
    required = mission.get("required_qualification_codes") or []
    if required and not await has_any_of(current.id, required):
        raise HTTPException(
            status_code=403,
            detail="Qualification requise non détenue pour cette mission",
        )

    cas_result = await db.user_missions.update_one(
        {
            "user_id": current.id,
            "mission_code": mission_code,
            "status": "accepted",
        },
        {"$set": {"status": "validated", "submitted_at": utc_now_iso()}},
    )
    if cas_result.modified_count == 0:
        # Lost the race (or someone/something else already validated
        # it between our read above and this write) — same idempotent
        # no-op, never a second credit.
        return {"ok": True, "cc_earned": 0, "new_stade": current.stade, "already_validated": True}

    reward = int(mission.get("cc_reward", 0))
    new_cc, new_stade = await frek_core.credit_cc(current.id, reward)
    await frek_core.emit_signal(current.id, "FREK-WORK", {"mission": mission_code})
    await award_threshold_badges(current.id, new_cc)
    return {"ok": True, "cc_earned": reward, "new_stade": new_stade}
