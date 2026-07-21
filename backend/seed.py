"""Idempotent seed for CVLN Academy formations, badges and missions."""
from __future__ import annotations

from db import db
from seed_data import FORMATIONS, BADGES, MISSIONS, POLES


def _pole_lookup():
    return {p["code"]: p for p in POLES}


async def seed_if_empty() -> None:
    poles = _pole_lookup()

    # Formations
    if await db.formations.count_documents({}) == 0:
        docs = []
        for f in FORMATIONS:
            pole = poles.get(f["pole"], {"name": f["pole"], "color": "#525252"})
            doc = {**f, "pole_name": pole["name"], "pole_color": pole["color"]}
            docs.append(doc)
        if docs:
            await db.formations.insert_many(docs)

    # Badges
    if await db.badges.count_documents({}) == 0:
        await db.badges.insert_many(BADGES)

    # Missions
    if await db.missions.count_documents({}) == 0:
        await db.missions.insert_many(MISSIONS)

    # Poles (static reference)
    await db.poles.delete_many({})
    await db.poles.insert_many(POLES)
