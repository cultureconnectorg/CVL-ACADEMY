"""Focused reconciliation layer for Academy workbook runtimes.

The current application remains authoritative. Historical #24 contributes only
source-backed workbook projections, imported idempotently when persisted counts
drift from their evidence contracts.
"""
from __future__ import annotations

from typing import Any

from services.cartography_2d_runtime import (
    TOTAL_NONEMPTY_ROWS,
    import_cartography_2d_runtime,
)
from services.economy_workbook_runtime import (
    import_economy_workbook_runtime,
    load_economy_workbook_rows,
)
from services.protocol_master_runtime import (
    EXPECTED_ROWS,
    EXPECTED_WORKBOOK_ROWS,
    import_protocol_master_runtime,
)


def expected_economy_rows() -> int:
    return sum(len(rows) for rows in load_economy_workbook_rows().values())


async def workbook_runtime_summary(db: Any) -> dict[str, Any]:
    economy_expected = expected_economy_rows()
    economy_actual = await db.academy_economy_workbook_rows.count_documents({})
    cartography_actual = await db.academy_cartography_2d_rows.count_documents({})
    protocol_controls_actual = await db.academy_protocol_controls.count_documents({})
    protocol_rows_actual = await db.academy_protocol_workbook_rows.count_documents({})
    return {
        "economy": {
            "expected_rows": economy_expected,
            "actual_rows": economy_actual,
            "ready": economy_actual == economy_expected,
        },
        "cartography_2d": {
            "expected_rows": TOTAL_NONEMPTY_ROWS,
            "actual_rows": cartography_actual,
            "ready": cartography_actual == TOTAL_NONEMPTY_ROWS,
        },
        "protocol_master": {
            "expected_controls": EXPECTED_ROWS,
            "actual_controls": protocol_controls_actual,
            "expected_workbook_rows": EXPECTED_WORKBOOK_ROWS,
            "actual_workbook_rows": protocol_rows_actual,
            "ready": (
                protocol_controls_actual == EXPECTED_ROWS
                and protocol_rows_actual == EXPECTED_WORKBOOK_ROWS
            ),
        },
    }


async def ensure_workbook_runtimes(db: Any) -> dict[str, Any]:
    before = await workbook_runtime_summary(db)
    imported: dict[str, Any] = {}

    if not before["economy"]["ready"]:
        imported["economy"] = await import_economy_workbook_runtime(db)
    if not before["cartography_2d"]["ready"]:
        imported["cartography_2d"] = await import_cartography_2d_runtime(db)
    if not before["protocol_master"]["ready"]:
        imported["protocol_master"] = await import_protocol_master_runtime(db)

    after = await workbook_runtime_summary(db)
    after["all_ready"] = all(section["ready"] for section in after.values())
    after["imported"] = imported
    return after
