"""FREK profile + global progression summary."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from auth import get_current_user, user_public
from db import db
from models import User

router = APIRouter(tags=["progression"])

# stage progression: percentage inside current stade band
STADE_BANDS = [
    ("graine", 0),
    ("pousse", 10),
    ("racine", 50),
    ("branches", 100),
    ("arbre", 150),
    ("foret", 300),
]


@router.get("/frek/profile")
async def frek_profile(current: User = Depends(get_current_user)):
    signals = (
        await db.frek_signals.find({"user_id": current.id}, {"_id": 0})
        .sort("ts", -1)
        .to_list(200)
    )
    progress = await db.progress.find(
        {"user_id": current.id, "completed": True}, {"_id": 0}
    ).to_list(500)
    badges = await db.user_badges.find({"user_id": current.id}, {"_id": 0}).to_list(50)

    idx = next((i for i, (n, _) in enumerate(STADE_BANDS) if n == current.stade), 0)
    lo = STADE_BANDS[idx][1]
    hi = STADE_BANDS[idx + 1][1] if idx + 1 < len(STADE_BANDS) else lo + 200
    pct = (
        100
        if hi <= lo
        else max(0, min(100, int((current.cc_credits - lo) * 100 / (hi - lo))))
    )
    return {
        "user": user_public(current).model_dump(),
        "stade_progress_pct": pct,
        "stade_next_at": hi,
        "modules_completed": len(progress),
        "badges_count": len(badges),
        "signals": current.signals,
        "recent_signals": signals[:20],
    }


@router.get("/progression/summary")
async def progression_summary(current: User = Depends(get_current_user)):
    # LX v2: only count modules that are FULLY validated (quiz passed + mini-mission committed)
    completed = await db.progress.count_documents(
        {"user_id": current.id, "completed": True}
    )
    total_modules_doc = await db.formations.aggregate(
        [
            {"$project": {"count": {"$size": {"$ifNull": ["$modules", []]}}}},
            {"$group": {"_id": None, "total": {"$sum": "$count"}}},
        ]
    ).to_list(1)
    total = (total_modules_doc[0]["total"] if total_modules_doc else 0) or 0
    global_pct = int((completed / total) * 100) if total else 0
    return {
        "completed_modules": completed,
        "total_modules": total,
        "global_pct": global_pct,
        "stade": current.stade,
        "cc_credits": current.cc_credits,
    }
