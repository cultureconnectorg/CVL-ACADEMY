"""Poles + formations catalogue (list, detail with per-user lock state)."""

from __future__ import annotations

from typing import Dict, Optional

from fastapi import APIRouter, Depends, HTTPException

from auth import get_current_user_optional
from db import db
from lx import (
    compute_status,
    is_formation_unlocked,
    is_module_unlocked,
    phase_completion_flags,
)
from models import User

router = APIRouter(tags=["formations"])


@router.get("/poles")
async def list_poles():
    return await db.poles.find({}, {"_id": 0}).to_list(50)


@router.get("/formations")
async def list_formations():
    docs = await db.formations.find({}, {"_id": 0}).to_list(200)
    # Return summary shape (no modules for the list)
    return [
        {
            "code": d["code"],
            "name": d["name"],
            "pole": d["pole"],
            "pole_name": d.get("pole_name"),
            "pole_color": d.get("pole_color"),
            "duration_h": d["duration_h"],
            "stades": d["stades"],
            "cc": d["cc"],
            "badge_name": d["badge_name"],
            "description": d.get("description", ""),
            "contexts": d.get("contexts", []),
            "audience_levels": d.get("audience_levels", []),
            "bridge_entities": d.get("bridge_entities", []),
            "positioning_note": d.get("positioning_note", ""),
            "primary_job": (d.get("cartography") or {}).get("primary_job"),
            "reconstruction_status": d.get("reconstruction_status"),
            "needs_external_calibration": d.get("needs_external_calibration", True),
            "delivery_formats": (d.get("cartography") or {}).get(
                "delivery_formats", []
            ),
            "market_job_title": d.get("market_job_title"),
            "calibration_confidence": d.get("calibration_confidence"),
            "calibration_date": d.get("calibration_date"),
            "reconciliation_flags": d.get("reconciliation_flags", []),
            "modules_count": len(d.get("modules", [])),
        }
        for d in docs
    ]


@router.get("/formations/{code}")
async def get_formation(
    code: str, current: Optional[User] = Depends(get_current_user_optional)
):
    doc = await db.formations.find_one({"code": code}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Formation introuvable")

    # If no user (unauth preview), return base structure with modules locked=False
    if not current:
        for m in doc.get("modules", []):
            m["is_unlocked"] = True
            m["status"] = "available"
            m["phase_flags"] = phase_completion_flags(None)
        doc["is_unlocked"] = True
        doc["lock_reason"] = ""
        return doc

    # User is authenticated → compute lock/status per module
    progress_docs = await db.progress.find({"user_id": current.id}, {"_id": 0}).to_list(
        1000
    )
    prog_by_mod: Dict[str, Dict] = {p["module_code"]: p for p in progress_docs}

    all_formations = await db.formations.find({}, {"_id": 0}).to_list(200)
    is_unlocked, reason = is_formation_unlocked(
        current.metier_vise, doc, all_formations, prog_by_mod
    )
    doc["is_unlocked"] = is_unlocked
    doc["lock_reason"] = reason

    for m in doc.get("modules", []):
        m["is_unlocked"] = is_unlocked and is_module_unlocked(
            doc, m["code"], prog_by_mod
        )
        p = prog_by_mod.get(m["code"])
        m["status"] = compute_status(p)
        m["phase_flags"] = phase_completion_flags(p)
        m["course_progress_pct"] = int((p or {}).get("course_progress_pct", 0))
        m["quiz_score"] = float((p or {}).get("quiz_score", 0.0))

    return doc
