"""Canonical importer for the CVLN Academy 2D catalogue master.

Evidence First: the CSV is the source artefact; runtime records retain source
path, row number and a deterministic content hash. CANDIDATE rows stay
CANDIDATE and are never promoted to published formations by this importer.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

EXPECTED_MASTER_ROWS = 812
CATALOGUE_SOURCE = (
    Path(__file__).resolve().parents[2]
    / "docs/cvln_academy_master/10_PORTFOLIO/raw/Master_Catalogue.csv"
)
REQUIRED_COLUMNS = {
    "Domaine",
    "Code",
    "Intitulé",
    "Dimension",
    "Contexte",
    "Type",
    "Statut",
    "Notes",
}


def _clean(value: Any) -> str:
    return "" if value is None else str(value).strip()


def _hash_payload(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def load_catalogue_rows(path: Path = CATALOGUE_SOURCE) -> list[dict[str, Any]]:
    """Parse and strictly validate the 2D master without mutating runtime state."""
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - headers
        if missing:
            raise ValueError(f"catalogue master missing columns: {sorted(missing)}")

        rows: list[dict[str, Any]] = []
        seen: set[str] = set()
        for row_number, raw in enumerate(reader, start=2):
            code = _clean(raw.get("Code"))
            if not code:
                raise ValueError(f"catalogue master row {row_number}: empty Code")
            if code in seen:
                raise ValueError(f"catalogue master duplicate Code: {code}")
            seen.add(code)

            payload: dict[str, Any] = {
                "domain": _clean(raw.get("Domaine")),
                "code": code,
                "title": _clean(raw.get("Intitulé")),
                "dimension": _clean(raw.get("Dimension")),
                "context": _clean(raw.get("Contexte")),
                "type": _clean(raw.get("Type")),
                "status": _clean(raw.get("Statut")),
                "notes": _clean(raw.get("Notes")),
            }
            if not payload["domain"] or not payload["title"]:
                raise ValueError(
                    f"catalogue master row {row_number}: domain/title required"
                )
            payload["source"] = {
                "kind": "MASTER_CATALOGUE_2D",
                "path": str(path.relative_to(Path(__file__).resolve().parents[2])),
                "row": row_number,
            }
            payload["source_hash"] = _hash_payload(payload)
            rows.append(payload)

    if len(rows) != EXPECTED_MASTER_ROWS:
        raise ValueError(
            f"catalogue master row count mismatch: expected {EXPECTED_MASTER_ROWS}, got {len(rows)}"
        )
    return rows


async def import_catalogue_master(
    db: Any, rows: Iterable[dict[str, Any]] | None = None
) -> dict[str, int]:
    """Idempotently upsert all catalogue rows into the runtime master collection."""
    parsed = list(rows) if rows is not None else load_catalogue_rows()
    if len(parsed) != EXPECTED_MASTER_ROWS:
        raise ValueError(f"refusing partial catalogue import: {len(parsed)} rows")

    matched = modified = upserted = 0
    for row in parsed:
        result = await db.academy_catalogue_master.update_one(
            {"code": row["code"]},
            {"$set": row},
            upsert=True,
        )
        matched += int(getattr(result, "matched_count", 0) or 0)
        modified += int(getattr(result, "modified_count", 0) or 0)
        upserted += int(getattr(result, "upserted_id", None) is not None)

    await db.academy_catalogue_master.create_index("code", unique=True)
    await db.academy_catalogue_master.create_index([("domain", 1), ("status", 1)])
    return {
        "rows": len(parsed),
        "matched": matched,
        "modified": modified,
        "upserted": upserted,
    }
