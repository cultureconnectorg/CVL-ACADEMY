"""FREK profile + global progression summary."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends

from api.learning import user_learning_path
from auth import get_current_user, user_public
from db import db
from lifecycle import is_returning_session
from models import User
from services.canonical_convergence import get_canonical_progress_summary
from services.progressive_horizon import HorizonItem, compute_progressive_horizon

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

    # RETURNING (W-FUNNEL-1, docs/ACADEMY_LIFECYCLE_STATE_MODEL.md): a
    # derived read-time signal, not a stored field — see lifecycle.py's
    # own module docstring for why no schema change was needed.
    refresh_stamps = [
        r.get("created_at")
        for r in await db.refresh_tokens.find(
            {"user_id": current.id}, {"_id": 0, "created_at": 1}
        ).to_list(200)
    ]
    returning = is_returning_session(current.created_at, refresh_stamps)

    # CAN-01/CAN-02 (Audit Chirurgical 2026-09-07) — additive convergence,
    # never merged into `modules_completed` above (see
    # services/canonical_convergence.py module docstring for why).
    canonical = await get_canonical_progress_summary(current.id)

    return {
        "user": user_public(current).model_dump(),
        "stade_progress_pct": pct,
        "stade_next_at": hi,
        "modules_completed": len(progress),
        "badges_count": len(badges),
        "signals": current.signals,
        "recent_signals": signals[:20],
        "returning": returning,
        "canonical": canonical,
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

    # CAN-01/CAN-02 — see frek_profile() above for the same note.
    canonical = await get_canonical_progress_summary(current.id)

    return {
        "completed_modules": completed,
        "total_modules": total,
        "global_pct": global_pct,
        "stade": current.stade,
        "cc_credits": current.cc_credits,
        "canonical": canonical,
    }


@router.get("/progression/horizon", response_model=List[HorizonItem])
async def progressive_horizon(current: User = Depends(get_current_user)):
    """ACA-0027 — the next relevant learning/opportunity, in real
    priority order. See `services/progressive_horizon.py`'s own
    docstring for exactly which real, pre-existing signals each item
    type traces back to — nothing here is an invented recommendation.
    """
    learning_path = await user_learning_path(current)
    return await compute_progressive_horizon(current.id, learning_path)
