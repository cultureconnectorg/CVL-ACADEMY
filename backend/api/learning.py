"""LX v2 — module journey: phases, deliverable, mini-mission, learning path."""

from __future__ import annotations

from typing import Dict, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from auth import get_current_user
from db import db, utc_now_iso
from lx import (
    DELIVERABLE_MIN_CHARS,
    EMPTY_PROGRESS,
    compute_status,
    enrich_module,
    is_formation_unlocked,
    is_module_unlocked,
    phase_completion_flags,
)
from models import User
from services.frek_core import frek_core

router = APIRouter(tags=["learning"])


@router.get("/modules/{formation_code}/{module_code}")
async def get_module_journey(
    formation_code: str,
    module_code: str,
    current: User = Depends(get_current_user),
):
    """Full learning-journey payload for one module — phases + user progress."""
    form = await db.formations.find_one({"code": formation_code}, {"_id": 0})
    if not form:
        raise HTTPException(status_code=404, detail="Formation introuvable")
    mod = next((m for m in form.get("modules", []) if m["code"] == module_code), None)
    if not mod:
        raise HTTPException(status_code=404, detail="Module introuvable")

    # Check lock
    progress_docs = await db.progress.find({"user_id": current.id}, {"_id": 0}).to_list(
        500
    )
    prog_by_mod = {p["module_code"]: p for p in progress_docs}

    all_forms = await db.formations.find({}, {"_id": 0}).to_list(200)
    form_unlocked, form_reason = is_formation_unlocked(
        current.metier_vise, form, all_forms, prog_by_mod
    )
    mod_unlocked = form_unlocked and is_module_unlocked(form, module_code, prog_by_mod)

    progress = prog_by_mod.get(
        module_code,
        {
            **EMPTY_PROGRESS,
            "user_id": current.id,
            "formation_code": formation_code,
            "module_code": module_code,
        },
    )

    enriched = enrich_module(mod)
    return {
        "formation": {
            "code": form["code"],
            "name": form["name"],
            "pole": form["pole"],
            "pole_name": form.get("pole_name"),
            "pole_color": form.get("pole_color"),
        },
        "module": enriched,
        "is_unlocked": mod_unlocked,
        "lock_reason": (
            form_reason
            if not form_unlocked
            else ("" if mod_unlocked else "Termine le module précédent d'abord.")
        ),
        "progress": {
            **{k: progress.get(k, v) for k, v in EMPTY_PROGRESS.items()},
        },
        "status": compute_status(progress),
        "phase_flags": phase_completion_flags(progress),
    }


class PhaseTickInput(BaseModel):
    key: str  # 'hook' | 'objectives' | 'workshop' | 'course'
    progress_pct: Optional[int] = None  # only for course


@router.post("/modules/{formation_code}/{module_code}/phase")
async def tick_phase(
    formation_code: str,
    module_code: str,
    inp: PhaseTickInput,
    current: User = Depends(get_current_user),
):
    if inp.key not in ("hook", "objectives", "course", "workshop"):
        raise HTTPException(status_code=400, detail="Phase inconnue")

    form = await db.formations.find_one({"code": formation_code}, {"_id": 0})
    if not form:
        raise HTTPException(status_code=404, detail="Formation introuvable")
    if not any(m["code"] == module_code for m in form.get("modules", [])):
        raise HTTPException(status_code=404, detail="Module introuvable")

    now = utc_now_iso()
    set_fields: Dict[str, object] = {
        "user_id": current.id,
        "formation_code": formation_code,
        "module_code": module_code,
    }
    if inp.key == "course":
        pct = max(0, min(100, int(inp.progress_pct or 0)))
        set_fields["course_progress_pct"] = pct
    else:
        set_fields[f"{inp.key}_viewed_at"] = now

    await db.progress.update_one(
        {"user_id": current.id, "module_code": module_code},
        {"$set": set_fields},
        upsert=True,
    )
    await frek_core.emit_signal(
        current.id,
        "FREK-TIME",
        {
            "module": module_code,
            "phase": inp.key,
        },
    )
    updated = await db.progress.find_one(
        {"user_id": current.id, "module_code": module_code},
        {"_id": 0},
    )
    return {
        "ok": True,
        "status": compute_status(updated),
        "phase_flags": phase_completion_flags(updated),
    }


class DeliverableInput(BaseModel):
    text: str


@router.post("/modules/{formation_code}/{module_code}/deliverable")
async def submit_deliverable(
    formation_code: str,
    module_code: str,
    inp: DeliverableInput,
    current: User = Depends(get_current_user),
):
    text = (inp.text or "").strip()
    if len(text) < DELIVERABLE_MIN_CHARS:
        raise HTTPException(
            status_code=400,
            detail=f"Livrable trop court (min {DELIVERABLE_MIN_CHARS} caractères).",
        )
    form = await db.formations.find_one({"code": formation_code}, {"_id": 0})
    if not form:
        raise HTTPException(status_code=404, detail="Formation introuvable")
    mod = next((m for m in form.get("modules", []) if m["code"] == module_code), None)
    if not mod:
        raise HTTPException(status_code=404, detail="Module introuvable")

    now = utc_now_iso()
    await db.progress.update_one(
        {"user_id": current.id, "module_code": module_code},
        {
            "$set": {
                "user_id": current.id,
                "formation_code": formation_code,
                "module_code": module_code,
                "deliverable_text": text,
                "deliverable_submitted_at": now,
            }
        },
        upsert=True,
    )
    signal = mod.get("frek_signal", "FREK-WORK").split(" ")[0]
    await frek_core.emit_signal(
        current.id,
        signal,
        {
            "module": module_code,
            "phase": "deliverable",
        },
    )
    updated = await db.progress.find_one(
        {"user_id": current.id, "module_code": module_code},
        {"_id": 0},
    )
    return {
        "ok": True,
        "status": compute_status(updated),
        "phase_flags": phase_completion_flags(updated),
    }


@router.post("/modules/{formation_code}/{module_code}/mini-mission/commit")
async def commit_mini_mission(
    formation_code: str,
    module_code: str,
    current: User = Depends(get_current_user),
):
    form = await db.formations.find_one({"code": formation_code}, {"_id": 0})
    if not form:
        raise HTTPException(status_code=404, detail="Formation introuvable")
    mod = next((m for m in form.get("modules", []) if m["code"] == module_code), None)
    if not mod:
        raise HTTPException(status_code=404, detail="Module introuvable")

    # mini-mission requires quiz already passed
    p = await db.progress.find_one(
        {"user_id": current.id, "module_code": module_code},
        {"_id": 0},
    )
    if not p or not p.get("quiz_passed"):
        raise HTTPException(
            status_code=400,
            detail="Passe d'abord le quiz de validation.",
        )

    now = utc_now_iso()
    await db.progress.update_one(
        {"user_id": current.id, "module_code": module_code},
        {
            "$set": {
                "mini_mission_committed_at": now,
                "completed": True,
                "completed_at": now,
            }
        },
        upsert=True,
    )
    await frek_core.emit_signal(
        current.id,
        "FREK-MISSION",
        {
            "module": module_code,
            "mini_mission": True,
        },
    )
    updated = await db.progress.find_one(
        {"user_id": current.id, "module_code": module_code},
        {"_id": 0},
    )
    return {
        "ok": True,
        "status": compute_status(updated),
        "phase_flags": phase_completion_flags(updated),
    }


@router.get("/user/learning-path")
async def user_learning_path(current: User = Depends(get_current_user)):
    """Personalized sequential learning path — pole-first, then others."""
    all_forms = await db.formations.find({}, {"_id": 0}).to_list(200)
    progress_docs = await db.progress.find(
        {"user_id": current.id},
        {"_id": 0},
    ).to_list(1000)
    prog_by_mod = {p["module_code"]: p for p in progress_docs}

    def summarize_formation(f: Dict) -> Dict:
        mods = f.get("modules", [])
        total = len(mods)
        validated = sum(
            1 for m in mods if compute_status(prog_by_mod.get(m["code"])) == "validated"
        )
        unlocked, reason = is_formation_unlocked(
            current.metier_vise, f, all_forms, prog_by_mod
        )
        return {
            "code": f["code"],
            "name": f["name"],
            "pole": f["pole"],
            "pole_name": f.get("pole_name"),
            "pole_color": f.get("pole_color"),
            "duration_h": f["duration_h"],
            "cc": f["cc"],
            "modules_count": total,
            "validated_count": validated,
            "progress_pct": int((validated / total) * 100) if total else 0,
            "is_unlocked": unlocked,
            "lock_reason": reason,
            "is_recommended": f["pole"] == current.metier_vise,
        }

    summarized = [summarize_formation(f) for f in all_forms]
    # Split: own pole first (in code order), then others
    own = [s for s in summarized if s["is_recommended"]]
    own.sort(key=lambda x: x["code"])
    others = [s for s in summarized if not s["is_recommended"]]
    others.sort(key=lambda x: (x["pole"], x["code"]))

    # Compute next actionable module
    next_action = None
    for s in own + others:
        if not s["is_unlocked"]:
            continue
        f_doc = next((f for f in all_forms if f["code"] == s["code"]), None)
        if f_doc is None:
            continue
        for m in f_doc.get("modules", []):
            if not is_module_unlocked(f_doc, m["code"], prog_by_mod):
                continue
            status = compute_status(prog_by_mod.get(m["code"]))
            if status != "validated":
                next_action = {
                    "formation_code": s["code"],
                    "formation_name": s["name"],
                    "module_code": m["code"],
                    "module_name": m["name"],
                    "status": status,
                    "pole_color": s["pole_color"],
                }
                break
        if next_action:
            break

    return {
        "own_pole": own,
        "other_poles": others,
        "next_action": next_action,
        "metier_vise": current.metier_vise,
    }
