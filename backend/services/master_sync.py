"""Fail-fast synchronization of the Academy Excel-derived runtime masters."""
from __future__ import annotations

from typing import Any

from services.catalogue_importer import import_catalogue_master, load_catalogue_rows
from services.cartography_2d_runtime import (
    SHEET_ROW_COUNTS,
    import_cartography_2d_runtime,
    load_cartography_2d,
)
from services.economy_importer import import_economy_master, load_economy_rows
from services.economy_runtime import sync_economy_runtime_links
from services.economy_workbook_runtime import (
    SHEETS as ECONOMY_WORKBOOK_SHEETS,
    import_economy_workbook_runtime,
    load_economy_workbook_rows,
    load_unit_economics,
)
from services.protocol_master_runtime import (
    EXPECTED_ROWS as EXPECTED_PROTOCOL_ROWS,
    import_protocol_master_runtime,
    load_protocol_controls,
)
from services.requirement_registry import sync_master_requirements


def validate_master_sources() -> dict[str, Any]:
    """Parse every authoritative projection and cross-check shared identities."""
    catalogue = load_catalogue_rows()
    economy = load_economy_rows()
    economy_workbook = load_economy_workbook_rows()
    unit_economics = load_unit_economics()
    cartography = load_cartography_2d()
    protocols = load_protocol_controls()

    catalogue_codes = {row["code"] for row in catalogue}
    economy_codes = {row["code"] for row in economy}
    if catalogue_codes != economy_codes:
        missing_economy = sorted(catalogue_codes - economy_codes)
        missing_catalogue = sorted(economy_codes - catalogue_codes)
        raise ValueError(
            "catalogue/economy code drift: "
            f"missing_economy={missing_economy[:20]} "
            f"missing_catalogue={missing_catalogue[:20]}"
        )

    if set(economy_workbook) != set(ECONOMY_WORKBOOK_SHEETS):
        raise ValueError("Economy workbook sheet projection is incomplete")
    if len(unit_economics) != 18:
        raise ValueError("Economy workbook Unit_Economics must contain 18 products")

    cartography_counts = {sheet: len(rows) for sheet, rows in cartography.items()}
    if cartography_counts != SHEET_ROW_COUNTS:
        raise ValueError(
            "cartography 2D row-count drift: "
            f"expected={SHEET_ROW_COUNTS} actual={cartography_counts}"
        )
    if len(protocols) != EXPECTED_PROTOCOL_ROWS:
        raise ValueError(
            "protocol master row-count drift: "
            f"expected={EXPECTED_PROTOCOL_ROWS} actual={len(protocols)}"
        )

    return {
        "valid": True,
        "catalogue_rows": len(catalogue),
        "economy_rows": len(economy),
        "economy_workbook_sheets": len(economy_workbook),
        "economy_workbook_runtime_rows": sum(
            len(rows) for rows in economy_workbook.values()
        ),
        "unit_economics_products": len(unit_economics),
        "shared_codes": len(catalogue_codes),
        "cartography_2d_rows": sum(cartography_counts.values()),
        "cartography_2d_sheets": len(cartography_counts),
        "protocol_rows": len(protocols),
    }


async def sync_all_masters(db: Any) -> dict[str, Any]:
    """Validate first, then idempotently refresh all coded masters and bindings."""
    validation = validate_master_sources()

    catalogue = await import_catalogue_master(db)
    economy = await import_economy_master(db)
    economy_workbook = await import_economy_workbook_runtime(db)
    cartography = await import_cartography_2d_runtime(db)
    protocols = await import_protocol_master_runtime(db)
    requirements = await sync_master_requirements(db)
    economy_runtime = await sync_economy_runtime_links(db)

    return {
        "validation": validation,
        "imports": {
            "catalogue": catalogue,
            "economy": economy,
            "economy_workbook": economy_workbook,
            "economy_runtime": economy_runtime,
            "cartography_2d": cartography,
            "protocol_master": protocols,
            "requirements": requirements,
        },
    }
