"""Idempotent seed for CVLN Academy formations, badges, missions and masters."""

from __future__ import annotations

import logging
from typing import Any

from db import db
from seed_data import BADGES, FORMATIONS, MISSIONS, POLES
from services.catalogue_importer import (
    import_catalogue_master,
    load_catalogue_rows,
)
from services.cartography_2d_runtime import (
    SOURCE_WORKBOOK_SHA256 as CARTOGRAPHY_SOURCE_SHA256,
    TOTAL_NONEMPTY_ROWS as CARTOGRAPHY_EXPECTED_ROWS,
    import_cartography_2d_runtime,
)
from services.economy_importer import import_economy_master, load_economy_rows
from services.protocol_master_runtime import (
    EXPECTED_ROWS as PROTOCOL_EXPECTED_CONTROLS,
    EXPECTED_WORKBOOK_ROWS as PROTOCOL_EXPECTED_WORKBOOK_ROWS,
    import_protocol_master_runtime,
    load_protocol_workbook_rows,
)
from services.requirement_registry import sync_master_requirements

logger = logging.getLogger("cvln.seed")


def _pole_lookup():
    return {p["code"]: p for p in POLES}


async def _source_hashes_match(
    collection: Any,
    expected: dict[str, str],
    *,
    query: dict[str, Any] | None = None,
    key_field: str = "code",
) -> bool:
    """Compare a complete runtime projection with its deterministic source hashes.

    The check is intentionally read-only and bounded.  It replaces thousands of
    idempotent remote writes on every web-process boot with one projection read.
    Any missing, extra or drifted record returns False and falls back to the
    existing reconciliation import path.
    """
    docs = await collection.find(
        query or {},
        {"_id": 0, key_field: 1, "source_hash": 1},
    ).to_list(length=len(expected) + 1)
    if len(docs) != len(expected):
        return False
    actual = {
        str(doc.get(key_field, "")): str(doc.get("source_hash", ""))
        for doc in docs
    }
    return actual == expected


async def _master_runtime_is_current(
    catalogue_rows: list[dict[str, Any]],
    economy_rows: list[dict[str, Any]],
) -> bool:
    """Verify master-runtime identity before deciding whether to re-import.

    Catalogue/economy are verified row-by-row through their deterministic
    source_hash.  Larger workbook projections use their immutable source SHA,
    exact row counts and completion manifests, which are written only after a
    successful import.  This preserves fail-safe reconciliation on drift while
    keeping ordinary Render starts lightweight.
    """
    catalogue_expected = {row["code"]: row["source_hash"] for row in catalogue_rows}
    economy_expected = {row["code"]: row["source_hash"] for row in economy_rows}

    if not await _source_hashes_match(
        db.academy_catalogue_master,
        catalogue_expected,
    ):
        return False
    if not await _source_hashes_match(
        db.academy_economy_master,
        economy_expected,
    ):
        return False
    if not await _source_hashes_match(
        db.academy_requirement_registry,
        catalogue_expected,
        query={"family": "CATALOGUE_2D"},
    ):
        return False
    if not await _source_hashes_match(
        db.academy_requirement_registry,
        economy_expected,
        query={"family": "ECONOMY_3D"},
    ):
        return False

    cartography_manifest = await db.academy_cartography_2d_manifest.find_one(
        {"kind": "CARTOGRAPHY_2D_WORKBOOK"},
        {"_id": 0, "source_workbook_sha256": 1, "runtime_rows": 1},
    )
    if not cartography_manifest:
        return False
    if cartography_manifest.get("source_workbook_sha256") != CARTOGRAPHY_SOURCE_SHA256:
        return False
    if cartography_manifest.get("runtime_rows") != CARTOGRAPHY_EXPECTED_ROWS:
        return False
    if (
        await db.academy_cartography_2d_rows.count_documents(
            {"source.workbook_sha256": CARTOGRAPHY_SOURCE_SHA256}
        )
        != CARTOGRAPHY_EXPECTED_ROWS
    ):
        return False
    if (
        await db.academy_requirement_registry.count_documents(
            {
                "family": "CARTOGRAPHY_2D",
                "source.workbook_sha256": CARTOGRAPHY_SOURCE_SHA256,
            }
        )
        != CARTOGRAPHY_EXPECTED_ROWS
    ):
        return False

    protocol_rows = load_protocol_workbook_rows()
    protocol_source_sha = protocol_rows[0]["source"]["workbook_sha256"]
    protocol_manifest = await db.academy_protocol_manifest.find_one(
        {"kind": "PROTOCOL_MASTER_WORKBOOK"},
        {
            "_id": 0,
            "source_workbook_sha256": 1,
            "workbook_runtime_rows": 1,
            "runtime_controls": 1,
        },
    )
    if not protocol_manifest:
        return False
    if protocol_manifest.get("source_workbook_sha256") != protocol_source_sha:
        return False
    if protocol_manifest.get("workbook_runtime_rows") != PROTOCOL_EXPECTED_WORKBOOK_ROWS:
        return False
    if protocol_manifest.get("runtime_controls") != PROTOCOL_EXPECTED_CONTROLS:
        return False
    if (
        await db.academy_protocol_workbook_rows.count_documents(
            {"source.workbook_sha256": protocol_source_sha}
        )
        != PROTOCOL_EXPECTED_WORKBOOK_ROWS
    ):
        return False
    if (
        await db.academy_protocol_controls.count_documents(
            {"source.workbook_sha256": protocol_source_sha}
        )
        != PROTOCOL_EXPECTED_CONTROLS
    ):
        return False
    if (
        await db.academy_requirement_registry.count_documents(
            {
                "family": "PROTOCOL_MASTER",
                "source.workbook_sha256": protocol_source_sha,
            }
        )
        != PROTOCOL_EXPECTED_CONTROLS
    ):
        return False

    return True


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
    await db.formations.update_many(
        {"content_status": {"$exists": False}}, {"$set": {"content_status": "published"}}
    )

    # Master truth reconciliation can involve several thousand remote writes.
    # On ordinary web boots the source/runtime identity is verified first and
    # unchanged projections are left untouched.  A missing, partial or drifted
    # projection deliberately falls back to the existing importers below.
    catalogue_rows = load_catalogue_rows()
    economy_rows = load_economy_rows()
    if await _master_runtime_is_current(catalogue_rows, economy_rows):
        logger.info("master runtime current; skipping unchanged master imports")
    else:
        logger.info("master runtime drift/incomplete; reconciling master imports")
        await import_catalogue_master(db, catalogue_rows)
        await import_economy_master(db, economy_rows)
        await sync_master_requirements(db)

        # Complete Cartographie 2D workbook projection: 11 sheets / 1,884 rows.
        await import_cartography_2d_runtime(db)

        # Complete Protocol Master: Excel rows 3..229 = 227 executable controls.
        # Source NOT_CREATED/PARTIAL is never converted into external approval;
        # runtime gates are fail-closed and evidence/authority aware.
        await import_protocol_master_runtime(db)

    if await db.badges.count_documents({}) == 0:
        await db.badges.insert_many(BADGES)
    if await db.missions.count_documents({}) == 0:
        await db.missions.insert_many(MISSIONS)
    await db.poles.delete_many({})
    await db.poles.insert_many(POLES)
