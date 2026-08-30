"""Onboarding — FREK Origin Story wizard."""

from __future__ import annotations

import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from auth import get_current_user, user_public
from badges_engine import award_threshold_badges
from db import db, utc_now_iso
from models import OnboardingInput, OnboardingResult, User
from services.frek_core import frek_core

router = APIRouter(prefix="/onboarding", tags=["onboarding"])

TERRITOIRES = [
    {"code": "martinique", "name": "Martinique"},
    {"code": "guadeloupe", "name": "Guadeloupe"},
    {"code": "guyane", "name": "Guyane"},
    {"code": "france", "name": "France hexagonale"},
    {"code": "caraibe", "name": "Autre Caraïbe"},
    {"code": "diaspora", "name": "Diaspora monde"},
    {"code": "autre", "name": "Autre"},
]


@router.get("/options")
async def onboarding_options():
    """Returns available options for the FREK Origin Story wizard."""
    poles = await db.poles.find({}, {"_id": 0}).to_list(50)
    return {
        "langs": [
            {"code": "fr", "name": "Français"},
            {"code": "en", "name": "English"},
            {"code": "kr", "name": "Kreyòl"},
        ],
        "metiers": poles,  # each pole = career direction
        "territoires": TERRITOIRES,
    }


@router.post("/complete", response_model=OnboardingResult)
async def onboarding_complete(
    inp: OnboardingInput,
    current: User = Depends(get_current_user),
):
    # 1) Validate pole
    pole = await db.poles.find_one({"code": inp.metier_vise}, {"_id": 0})
    if not pole:
        raise HTTPException(status_code=400, detail="Métier visé inconnu")
    if inp.lang not in ("fr", "en", "kr"):
        raise HTTPException(status_code=400, detail="Langue invalide")
    if not any(t["code"] == inp.territoire for t in TERRITOIRES):
        raise HTTPException(status_code=400, detail="Territoire invalide")

    # 2) Persist onboarding data
    await db.users.update_one(
        {"id": current.id},
        {
            "$set": {
                "lang": inp.lang,
                "metier_vise": inp.metier_vise,
                "territoire": inp.territoire,
                "objectif_perso": inp.objectif_perso.strip(),
                "onboarding_completed": True,
            }
        },
    )

    # 3) Emit 3 FREK-TIME signals (language / territory / objective)
    signals_emitted: List[str] = []
    for reason in ("language_selected", "territory_selected", "objective_set"):
        await frek_core.emit_signal(
            current.id,
            "FREK-TIME",
            {
                "onboarding_step": reason,
                "value": {
                    "language_selected": inp.lang,
                    "territory_selected": inp.territoire,
                    "objective_set": inp.objectif_perso[:60],
                }[reason],
            },
        )
        signals_emitted.append("FREK-TIME")

    # 4) Auto-award BADGE-DECOUVERTE (threshold=0) — user has 5 CC already from register
    await award_threshold_badges(current.id, current.cc_credits)
    badge_earned = await db.badges.find_one({"code": "BADGE-DECOUVERTE"}, {"_id": 0})

    # 5) Recommend a first formation matching the pole (prefer one with modules,
    #    else fall back to any formation of this pole)
    formations = await db.formations.find(
        {"pole": inp.metier_vise}, {"_id": 0}
    ).to_list(50)
    formations.sort(key=lambda f: (0 if f.get("modules") else 1, f.get("code", "")))
    recommended_formation = formations[0] if formations else None
    if recommended_formation:
        recommended_formation = {
            "code": recommended_formation["code"],
            "name": recommended_formation["name"],
            "pole": recommended_formation["pole"],
            "pole_name": recommended_formation.get("pole_name"),
            "pole_color": recommended_formation.get("pole_color"),
            "duration_h": recommended_formation["duration_h"],
            "cc": recommended_formation["cc"],
            "description": recommended_formation.get("description", ""),
            "modules_count": len(recommended_formation.get("modules", [])),
        }

    # 6) Recommend + auto-accept a first mission matching the pole (any stade,
    #    prefer 'featured', else 'open'). Falls back to any mission if pole has none.
    missions_pool = await db.missions.find(
        {"pole": inp.metier_vise}, {"_id": 0}
    ).to_list(50)
    if not missions_pool:
        missions_pool = await db.missions.find({}, {"_id": 0}).to_list(50)
    missions_pool.sort(
        key=lambda m: (
            0 if m.get("status_type") == "featured" else 1,
            m.get("cc_reward", 0),
        )
    )
    recommended_mission = missions_pool[0] if missions_pool else None
    if recommended_mission:
        existing = await db.user_missions.find_one(
            {
                "user_id": current.id,
                "mission_code": recommended_mission["code"],
            }
        )
        if not existing:
            await db.user_missions.insert_one(
                {
                    "id": str(uuid.uuid4()),
                    "user_id": current.id,
                    "mission_code": recommended_mission["code"],
                    "status": "accepted",
                    "accepted_at": utc_now_iso(),
                    "source": "onboarding",
                }
            )
            await frek_core.emit_signal(
                current.id,
                "FREK-MISSION",
                {
                    "mission": recommended_mission["code"],
                    "source": "onboarding",
                },
            )

    # 7) Reload user for accurate public payload
    doc = await db.users.find_one({"id": current.id}, {"_id": 0})
    reloaded = User(**doc) if doc else current
    return OnboardingResult(
        user=user_public(reloaded),
        recommended_formation=recommended_formation,
        recommended_mission=recommended_mission,
        badge_earned=badge_earned,
        signals_emitted=signals_emitted,
    )
