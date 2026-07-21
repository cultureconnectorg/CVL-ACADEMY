"""Idempotent seed for CVLN Academy formations, badges and missions."""
from __future__ import annotations

from db import db
from seed_data import FORMATIONS, BADGES, MISSIONS, POLES


def _pole_lookup():
    return {p["code"]: p for p in POLES}


async def seed_if_empty() -> None:
    poles = _pole_lookup()

    # Formations — UPSERT so that content updates in seed_data propagate on restart
    # (does NOT touch user data collections: progress, user_missions, user_badges, users).
    for f in FORMATIONS:
        pole = poles.get(f["pole"], {"name": f["pole"], "color": "#525252"})
        doc = {**f, "pole_name": pole["name"], "pole_color": pole["color"]}
        await db.formations.update_one(
            {"code": f["code"]},
            {"$set": doc},
            upsert=True,
        )

    # Badges
    if await db.badges.count_documents({}) == 0:
        await db.badges.insert_many(BADGES)

    # Missions
    if await db.missions.count_documents({}) == 0:
        await db.missions.insert_many(MISSIONS)

    # Poles (static reference)
    await db.poles.delete_many({})
    await db.poles.insert_many(POLES)
