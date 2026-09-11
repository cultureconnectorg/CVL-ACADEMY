"""Fail-fast synchronization of the Academy Excel-derived runtime masters.

This module is deliberately an orchestrator, not a new source of truth. The
individual importers own parsing/provenance semantics. We validate every source
before the first database write so a malformed workbook projection cannot leave
a half-refreshed runtime.
"""
from __future__ import annotations

from typing import Any

from services.catalogue_importer import import_catalogue_master, load_catalogue_rows
from services.cartography_2d_runtime import (
    SHEET_ROW_COUNTS,
    import_cartography_2d_runtime,
    load_cartography_2d,
)
from services.economy_importer import import_economy_master, load_economy_rows
from services.protocol_master_runtime import (
    EXPECTED_ROWS as EXPECTED_PROTOCOL_ROWS,
    import_protocol_master_runtime,
    load_protocol_master_runtime,
)
from services.requirement_registry import sync_master_requirements


def validate_master_sources() -> dict[str, Any]:
    """Parse every authoritative projection and cross-check shared identities."""
    catalogue = load_catalogue_rows()
    economy = load_economy_rows()
    cartography = load_cartography_2d()
    protocols = load_protocol_master_runtime()

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

    cartography_counts = {sheet: len(rows) for sheet, rows in cartography.items()}
    if cartography_counts != SHEET_ROW_COUNTS:
        raise ValueError(
            f"cartography 2D row-count drift: expected={SHEET_ROW_COUNTS} "
            f"actual={cartography_counts}"
        )
    if len(protocols) != EXPECTED_PROTOCOL_ROWS:
        raise ValueError(
            f"protocol master row-count drift: expected={EXPECTED_PROTOCOL_ROWS} "
            f"actual={len(protocols)}"
        )

    return {
        "valid": True,
        "catalogue_rows": len(catalogue),
        "economy_rows": len(economy),
        "shared_codes": len(catalogue_codes),
        "cartography_2d_rows": sum(cartography_counts.values()),
        "cartography_2d_sheets": len(cartography_counts),
        "protocol_rows": len(protocols),
    }


async def sync_all_masters(db: Any) -> dict[str, Any]:
    """Validate first, then idempotently refresh all currently coded masters."""
    validation = validate_master_sources()

    catalogue = await import_catalogue_master(db)
    economy = await import_economy_master(db)
    cartography = await import_cartography_2d_runtime(db)
    protocols = await import_protocol_master_runtime(db)
    requirements = await sync_master_requirements(db)

    return {
        "validation": validation,
        "imports": {
            "catalogue": catalogue,
            "economy": economy,
            "cartography_2d": cartography,
            "protocol_master": protocols,
            "requirements": requirements,
        },
    }
