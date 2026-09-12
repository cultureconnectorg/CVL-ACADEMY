from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services.cartography_2d_runtime import TOTAL_NONEMPTY_ROWS, load_cartography_2d
from services.economy_workbook_runtime import SHEETS, load_economy_workbook_rows
from services.protocol_master_runtime import (
    EXPECTED_ROWS,
    EXPECTED_WORKBOOK_ROWS,
    load_protocol_controls,
    load_protocol_workbook_rows,
)
from services.workbook_runtime import ensure_workbook_runtimes


def test_economy_workbook_projects_all_15_sheets_and_812_mapping_rows():
    workbook = load_economy_workbook_rows()
    assert set(workbook) == set(SHEETS)
    assert len(workbook) == 15
    assert len(workbook["Mapping_812"]) == 813
    assert all(row["source_hash"] for rows in workbook.values() for row in rows)


def test_cartography_2d_projects_exact_1884_source_rows():
    workbook = load_cartography_2d()
    assert sum(len(rows) for rows in workbook.values()) == TOTAL_NONEMPTY_ROWS == 1884
    assert len(workbook["Master_Catalogue"]) == 812
    assert len({row["normalized"]["code"] for row in workbook["Master_Catalogue"]}) == 812


def test_protocol_master_projects_227_controls_and_328_workbook_rows():
    controls = load_protocol_controls()
    rows = load_protocol_workbook_rows()
    assert len(controls) == EXPECTED_ROWS == 227
    assert len(rows) == EXPECTED_WORKBOOK_ROWS == 328
    assert len({control["control_id"] for control in controls}) == 227
    assert len({control["behavior_fingerprint"] for control in controls}) == 227


@pytest.mark.asyncio
async def test_runtime_reconciliation_is_complete_and_idempotent():
    client = AsyncMongoMockClient()
    db = client["workbook_runtime_reconciliation"]

    first = await ensure_workbook_runtimes(db)
    assert first["all_ready"] is True
    assert set(first["imported"]) == {
        "economy",
        "cartography_2d",
        "protocol_master",
    }
    assert first["economy"]["ready"] is True
    assert first["cartography_2d"]["actual_rows"] == 1884
    assert first["protocol_master"]["actual_controls"] == 227
    assert first["protocol_master"]["actual_workbook_rows"] == 328

    second = await ensure_workbook_runtimes(db)
    assert second["all_ready"] is True
    assert second["imported"] == {}
