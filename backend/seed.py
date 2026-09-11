"""Idempotent seed for CVLN Academy formations, badges, missions and masters."""

from __future__ import annotations

from db import db
from seed_data import BADGES, FORMATIONS, MISSIONS, POLES
from services.catalogue_importer import import_catalogue_master
from services.cartography_2d_runtime import import_cartography_2d_runtime
from services.economy_importer import import_economy_master
from services.economy_runtime import sync_economy_runtime_links
from services.economy_workbook_runtime import import_economy_workbook_runtime
from services.protocol_master_runtime import import_protocol_master_runtime
from services.requirement_registry import sync_master_requirements


def _pole_lookup():
    return {p["code"]: p for p in POLES}


async def seed_if_empty() -> None:
    poles = _pole_lookup()
    for f in FORMATIONS:
        pole = poles.get(f["pole"], {"name": f["pole"], "color": "#525252"})
        doc = {**f, "pole_name": pole["name"], "pole_color": pole["color"]}
        await db.formations.update_one({"code": f["code"]}, {"$set": doc}, upsert=True)
    await db.formations.update_many(
        {"content_status": {"$exists": False}},
        {"$set": {"content_status": "published"}},
    )

    await import_catalogue_master(db)
    await import_economy_master(db)
    await import_economy_workbook_runtime(db)
    await sync_master_requirements(db)
    await sync_economy_runtime_links(db)
    await import_cartography_2d_runtime(db)
    await import_protocol_master_runtime(db)

    if await db.badges.count_documents({}) == 0:
        await db.badges.insert_many(BADGES)
    if await db.missions.count_documents({}) == 0:
        await db.missions.insert_many(MISSIONS)
    await db.poles.delete_many({})
    await db.poles.insert_many(POLES)
