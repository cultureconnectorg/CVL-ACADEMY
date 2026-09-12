"""Complete runtime projection of the CVLN Academy Cartographie 2D workbook.

Evidence First:
- Master_Catalogue (812 rows) is the canonical catalogue source.
- External_Market, Internal_CVLN and Cross_Ecosystem are exact materialized
  views of Master_Catalogue by Dimension.
- Operator_Roles, Habilitations, Access_Levels, Missions_Pipelines,
  Coverage_Gaps, Taxonomy and Dashboard are preserved in runtime_snapshot.json.
- CANDIDATE never means published.
- Certification never grants a habilitation.
- Academy never auto-assigns executive authority.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from services.catalogue_importer import load_catalogue_rows

ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT_PATH = (
    ROOT
    / "docs/cvln_academy_master/10_PORTFOLIO/raw/cartography_2d_workbook/runtime_snapshot.json"
)

SOURCE_WORKBOOK = "CVLN_Academy_Cartographie_2D_Master(2).xlsx"
SOURCE_WORKBOOK_SHA256 = (
    "43a0885dff4177249fa83fb1e7754d48c871df150309d931349c381954fa6bf2"
)
SHEET_ROW_COUNTS = {
    "Master_Catalogue": 812,
    "External_Market": 437,
    "Internal_CVLN": 220,
    "Cross_Ecosystem": 153,
    "Operator_Roles": 130,
    "Habilitations": 71,
    "Access_Levels": 7,
    "Missions_Pipelines": 10,
    "Coverage_Gaps": 6,
    "Taxonomy": 9,
    "Dashboard": 29,
}
TOTAL_NONEMPTY_ROWS = 1884
CLASSIFICATION_EXCEPTIONS = {"HOS-GAP", "SAY-LAB"}
DERIVED_DIMENSIONS = {
    "External_Market": "MARKET",
    "Internal_CVLN": "SYSTEM_CVLN",
    "Cross_Ecosystem": "CROSS_ECOSYSTEM",
}
STATIC_MAPPINGS = {
    "Habilitations": {
        "Domaine": "domain",
        "Habilitation": "habilitation",
        "Sensibilité": "sensitivity",
        "Principe": "principle",
        "Statut": "status",
    },
    "Access_Levels": {
        "Niveau": "level",
        "Nom": "name",
        "Définition": "definition",
    },
    "Missions_Pipelines": {
        "Type": "kind",
        "Nom": "name",
        "Chaîne": "chain",
        "Objectif / règle": "objective_rule",
    },
    "Coverage_Gaps": {
        "Domaine": "domain",
        "Écart / dépendance": "gap_dependency",
        "Action": "action",
        "Règle": "rule",
    },
    "Taxonomy": {
        "Code": "code",
        "Catégorie": "category",
        "Définition": "definition",
    },
    "Dashboard": {
        "col_1": "col_1",
        "col_2": "col_2",
        "col_3": "col_3",
        "col_4": "col_4",
        "col_5": "col_5",
        "col_6": "col_6",
        "col_7": "col_7",
        "col_8": "col_8",
    },
}


def _hash_payload(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _runtime_row(
    sheet: str,
    excel_row: int,
    fields: dict[str, str],
    normalized: dict[str, str],
    path: str,
) -> dict[str, Any]:
    source = {
        "kind": "CARTOGRAPHY_2D_WORKBOOK",
        "workbook": SOURCE_WORKBOOK,
        "workbook_sha256": SOURCE_WORKBOOK_SHA256,
        "sheet": sheet,
        "excel_row": excel_row,
        "path": path,
    }
    payload = {
        "sheet": sheet,
        "excel_row": excel_row,
        "fields": fields,
        "source": source,
    }
    return {
        "sheet": sheet,
        "excel_row": excel_row,
        "row_id": f"{sheet}:{excel_row}",
        "fields": fields,
        "normalized": normalized,
        "source": source,
        "source_hash": _hash_payload(payload),
    }


def _load_snapshot() -> dict[str, Any]:
    with SNAPSHOT_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _master_rows() -> list[dict[str, Any]]:
    rows = []
    source_path = "docs/cvln_academy_master/10_PORTFOLIO/raw/Master_Catalogue.csv"
    for item in load_catalogue_rows():
        fields = {
            "Domaine": item["domain"],
            "Code": item["code"],
            "Intitulé": item["title"],
            "Dimension": item["dimension"],
            "Contexte": item["context"],
            "Type": item["type"],
            "Statut": item["status"],
            "Notes": item["notes"],
        }
        normalized = {
            "domain": item["domain"],
            "code": item["code"],
            "title": item["title"],
            "dimension": item["dimension"],
            "context": item["context"],
            "type": item["type"],
            "status": item["status"],
            "notes": item["notes"],
        }
        rows.append(
            _runtime_row(
                "Master_Catalogue",
                item["source"]["row"],
                fields,
                normalized,
                source_path,
            )
        )
    return rows


def _derived_view(sheet: str, master: list[dict[str, Any]]) -> list[dict[str, Any]]:
    dimension = DERIVED_DIMENSIONS[sheet]
    selected = [row for row in master if row["normalized"]["dimension"] == dimension]
    return [
        _runtime_row(
            sheet,
            excel_row,
            dict(source_row["fields"]),
            dict(source_row["normalized"]),
            source_row["source"]["path"],
        )
        for excel_row, source_row in enumerate(selected, start=2)
    ]


def _operator_role_rows(
    snapshot: dict[str, Any], master: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    by_code = {row["normalized"]["code"]: row for row in master}
    codes = snapshot["OPERATOR_ROLE_CODES"]
    if len(codes) != 130 or len(set(codes)) != 130:
        raise ValueError("Operator_Roles must contain 130 unique codes")
    missing = set(codes) - set(by_code)
    if missing:
        raise ValueError(f"Operator_Roles contains unknown codes: {sorted(missing)}")
    return [
        _runtime_row(
            "Operator_Roles",
            excel_row,
            dict(by_code[code]["fields"]),
            dict(by_code[code]["normalized"]),
            str(SNAPSHOT_PATH.relative_to(ROOT)),
        )
        for excel_row, code in enumerate(codes, start=2)
    ]


def _static_rows(snapshot: dict[str, Any], sheet: str) -> list[dict[str, Any]]:
    block = snapshot[sheet]
    headers = block["headers"]
    mapping = STATIC_MAPPINGS[sheet]
    if headers != list(mapping.keys()):
        raise ValueError(f"{sheet}: snapshot headers drifted")
    rows = []
    seen_excel_rows = set()
    for item in block["rows"]:
        excel_row = int(item["excel_row"])
        if excel_row in seen_excel_rows:
            raise ValueError(f"{sheet}: duplicate Excel row {excel_row}")
        seen_excel_rows.add(excel_row)
        values = item["values"]
        if len(values) != len(headers):
            raise ValueError(f"{sheet} row {excel_row}: wrong value count")
        fields = {
            header: str(value) if value is not None else ""
            for header, value in zip(headers, values)
        }
        normalized = {target: fields[source] for source, target in mapping.items()}
        rows.append(
            _runtime_row(
                sheet,
                excel_row,
                fields,
                normalized,
                str(SNAPSHOT_PATH.relative_to(ROOT)),
            )
        )
    return rows


def load_cartography_2d() -> dict[str, list[dict[str, Any]]]:
    snapshot = _load_snapshot()
    master = _master_rows()
    workbook: dict[str, list[dict[str, Any]]] = {"Master_Catalogue": master}

    for sheet in DERIVED_DIMENSIONS:
        workbook[sheet] = _derived_view(sheet, master)
    workbook["Operator_Roles"] = _operator_role_rows(snapshot, master)
    for sheet in STATIC_MAPPINGS:
        workbook[sheet] = _static_rows(snapshot, sheet)

    for sheet, expected in SHEET_ROW_COUNTS.items():
        actual = len(workbook[sheet])
        if actual != expected:
            raise ValueError(f"{sheet}: expected {expected} rows, got {actual}")

    total = sum(len(rows) for rows in workbook.values())
    if total != TOTAL_NONEMPTY_ROWS:
        raise ValueError(
            f"cartography 2D total mismatch: expected {TOTAL_NONEMPTY_ROWS}, got {total}"
        )

    master_set = {row["normalized"]["code"] for row in master}
    if len(master_set) != 812:
        raise ValueError("Master_Catalogue is not 812 unique codes")

    view_sets = {
        sheet: {row["normalized"]["code"] for row in workbook[sheet]}
        for sheet in DERIVED_DIMENSIONS
    }
    union = set().union(*view_sets.values())
    if master_set - union != CLASSIFICATION_EXCEPTIONS:
        raise ValueError("2D classification exceptions drifted")
    if (
        view_sets["External_Market"] & view_sets["Internal_CVLN"]
        or view_sets["External_Market"] & view_sets["Cross_Ecosystem"]
        or view_sets["Internal_CVLN"] & view_sets["Cross_Ecosystem"]
    ):
        raise ValueError("External/Internal/Cross classification views overlap")

    habilitation_pairs = [
        (row["normalized"]["domain"], row["normalized"]["habilitation"])
        for row in workbook["Habilitations"]
    ]
    if len(habilitation_pairs) != len(set(habilitation_pairs)):
        raise ValueError("Habilitations contains duplicate domain+habilitation pairs")

    for sheet, key in (
        ("Access_Levels", "level"),
        ("Missions_Pipelines", "name"),
        ("Coverage_Gaps", "domain"),
        ("Taxonomy", "code"),
    ):
        values = [row["normalized"][key] for row in workbook[sheet]]
        if len(values) != len(set(values)):
            raise ValueError(f"{sheet} contains duplicate {key} values")
    return workbook


async def import_cartography_2d_runtime(db: Any) -> dict[str, Any]:
    """Upsert all 1,884 rows and one proof-registry identity per Excel row."""
    workbook = load_cartography_2d()
    imported = 0

    for sheet, rows in workbook.items():
        for row in rows:
            await db.academy_cartography_2d_rows.update_one(
                {"row_id": row["row_id"]},
                {"$set": row},
                upsert=True,
            )
            requirement_id = f"CARTOGRAPHY_2D:{sheet}:{row['excel_row']}"
            await db.academy_requirement_registry.update_one(
                {"requirement_id": requirement_id},
                {
                    "$set": {
                        "requirement_id": requirement_id,
                        "family": "CARTOGRAPHY_2D",
                        "sheet": sheet,
                        "excel_row": row["excel_row"],
                        "source": row["source"],
                        "source_hash": row["source_hash"],
                        "runtime_collection": "academy_cartography_2d_rows",
                        "runtime_key": {"row_id": row["row_id"]},
                        "runtime_importer": (
                            "services.cartography_2d_runtime."
                            "import_cartography_2d_runtime"
                        ),
                        "test_ref": "backend/tests/test_cartography_2d_runtime.py",
                    },
                    "$setOnInsert": {
                        "status": "INGESTED_RUNTIME",
                        "verified": False,
                    },
                },
                upsert=True,
            )
            imported += 1

    await db.academy_cartography_2d_rows.create_index("row_id", unique=True)
    await db.academy_cartography_2d_rows.create_index(
        [("sheet", 1), ("excel_row", 1)], unique=True
    )
    await db.academy_cartography_2d_rows.create_index(
        [("sheet", 1), ("normalized.code", 1)]
    )
    await db.academy_requirement_registry.create_index("requirement_id", unique=True)
    await db.academy_cartography_2d_manifest.update_one(
        {"kind": "CARTOGRAPHY_2D_WORKBOOK"},
        {
            "$set": {
                "kind": "CARTOGRAPHY_2D_WORKBOOK",
                "source_workbook": SOURCE_WORKBOOK,
                "source_workbook_sha256": SOURCE_WORKBOOK_SHA256,
                "runtime_rows": imported,
                "sheet_row_counts": {
                    sheet: len(rows) for sheet, rows in workbook.items()
                },
            }
        },
        upsert=True,
    )
    return {
        "rows": imported,
        "sheets": len(workbook),
        "sheet_row_counts": {sheet: len(rows) for sheet, rows in workbook.items()},
        "source_workbook_sha256": SOURCE_WORKBOOK_SHA256,
    }
