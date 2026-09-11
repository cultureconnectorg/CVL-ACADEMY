"""Runtime projection and executable gates for the full Economy 3D workbook."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "docs/cvln_academy_master/100_ECONOMY/raw"
SHEETS = (
    "Dashboard",
    "Offres_Economiques",
    "Mapping_812",
    "Hypotheses",
    "Unit_Economics",
    "Economie_Domaines",
    "Valeur_Interne",
    "Learning_to_Work",
    "Sources_Methodo",
    "Decisions_Fondateur",
    "Pricing_V1",
    "B2B_B2G",
    "Plan_36M",
    "Policies",
    "Roadmap_Monetisation",
)

UNIT_OFFER_PRODUCT = {
    "academy-access": "Access",
    "academy-pro": "Pro",
    "academy-career": "Career",
    "parcours-metier": "Path",
    "intensive-hybrid-week": "Intensive/learner",
    "assessment-only": "Assessment",
    "certification-academy": "Certification",
    "certification-renewal": "Renewal",
    "b2b-team": "B2B Team",
    "b2b-growth": "B2B Growth",
    "b2b-enterprise": "B2B Enterprise",
    "b2g-pilot": "B2G Pilot",
    "b2g-territory": "B2G Territory",
    "b2g-large": "B2G Large",
    "learning-to-work-client": "Mission minimum",
    "methodology-ip-licence": "Methodology/IP",
    "academy-spatial-licence": "Academy+Spatial",
    "white-label-enterprise": "White-label annual",
}

OFFER_PHASE = {
    "b2b-enterprise": "PHASE_2",
    "b2g-large": "PHASE_2",
    "methodology-ip-licence": "PHASE_2",
    "learning-to-work-client": "PHASE_2",
    "academy-spatial-licence": "PHASE_3",
    "white-label-enterprise": "PHASE_3",
}


def _sha(value: Any) -> str:
    raw = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _source_file_sha(sheet: str) -> str:
    return hashlib.sha256((RAW / f"{sheet}.csv").read_bytes()).hexdigest()


def load_economy_workbook_rows() -> dict[str, list[dict[str, Any]]]:
    workbook: dict[str, list[dict[str, Any]]] = {}
    for sheet in SHEETS:
        path = RAW / f"{sheet}.csv"
        if not path.exists():
            raise ValueError(f"Economy workbook source missing: {path.name}")
        file_sha = _source_file_sha(sheet)
        rows: list[dict[str, Any]] = []
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            for csv_row, values in enumerate(csv.reader(handle), start=1):
                cleaned = [str(value).strip() for value in values]
                if not any(cleaned):
                    continue
                payload = {
                    "sheet": sheet,
                    "csv_row": csv_row,
                    "values": cleaned,
                    "source_file": path.name,
                    "source_file_sha256": file_sha,
                }
                rows.append(
                    {
                        "row_id": f"{sheet}:{csv_row}",
                        **payload,
                        "source_hash": _sha(payload),
                    }
                )
        if not rows:
            raise ValueError(f"Economy workbook sheet empty: {sheet}")
        workbook[sheet] = rows
    if len(workbook["Mapping_812"]) != 813:
        raise ValueError(
            "Mapping_812 source projection must contain header + 812 rows"
        )
    return workbook


async def import_economy_workbook_runtime(db: Any) -> dict[str, Any]:
    workbook = load_economy_workbook_rows()
    total = 0
    for sheet, rows in workbook.items():
        row_ids = [row["row_id"] for row in rows]
        await db.academy_economy_workbook_rows.delete_many(
            {"sheet": sheet, "row_id": {"$nin": row_ids}}
        )
        for row in rows:
            await db.academy_economy_workbook_rows.update_one(
                {"row_id": row["row_id"]},
                {"$set": row},
                upsert=True,
            )
        total += len(rows)
    await db.academy_economy_workbook_rows.create_index("row_id", unique=True)
    await db.academy_economy_workbook_rows.create_index(
        [("sheet", 1), ("csv_row", 1)],
        unique=True,
    )
    counts = {sheet: len(rows) for sheet, rows in workbook.items()}
    await db.academy_economy_workbook_manifest.update_one(
        {"kind": "ECONOMY_3D_WORKBOOK"},
        {
            "$set": {
                "kind": "ECONOMY_3D_WORKBOOK",
                "sheets": list(SHEETS),
                "sheet_rows": counts,
                "runtime_rows": total,
            }
        },
        upsert=True,
    )
    return {
        "sheets": len(SHEETS),
        "runtime_rows": total,
        "sheet_rows": counts,
    }


def load_unit_economics() -> dict[str, dict[str, Any]]:
    path = RAW / "Unit_Economics.csv"
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        raw_rows = list(csv.reader(handle))
    header_index = next(
        index
        for index, row in enumerate(raw_rows)
        if row and row[0].strip() == "Produit"
    )
    header = [cell.strip() for cell in raw_rows[header_index]]
    result: dict[str, dict[str, Any]] = {}
    for excel_row, values in enumerate(
        raw_rows[header_index + 1 :],
        start=header_index + 2,
    ):
        if not values or not any(str(value).strip() for value in values):
            continue
        padded = values + [""] * (len(header) - len(values))
        row = dict(zip(header, [str(value).strip() for value in padded]))
        product = row["Produit"]
        result[product] = {
            "product": product,
            "price_eur": float(row["Prix"]),
            "variable_cost_eur": float(row["Coût variable"]),
            "gross_margin_eur": float(row["Marge brute"]),
            "margin_pct": float(row["Marge %"]),
            "margin_floor_pct": float(row["Plancher"]),
            "gate": row["Gate"],
            "status": row["Statut"],
            "source_decision": row["Source"],
            "source": {
                "sheet": "Unit_Economics",
                "csv_row": excel_row,
            },
        }
    if len(result) != 18:
        raise ValueError(
            f"Unit_Economics must contain 18 products, got {len(result)}"
        )
    return result


def evaluate_offer_unit_economics(offer: Any) -> dict[str, Any]:
    product = UNIT_OFFER_PRODUCT.get(offer.offer_id)
    if product is None:
        return {
            "allowed": True,
            "reason": "UNIT_ECONOMICS_NOT_APPLICABLE",
            "offer_id": offer.offer_id,
        }
    source = load_unit_economics()[product]
    computed_margin = offer.price_eur - offer.variable_cost_eur
    computed_margin_pct = (
        computed_margin / offer.price_eur if offer.price_eur else 0.0
    )
    drift: list[str] = []
    checks = (
        ("price_eur", offer.price_eur, source["price_eur"]),
        ("variable_cost_eur", offer.variable_cost_eur, source["variable_cost_eur"]),
        ("gross_margin_eur", offer.gross_margin_eur, source["gross_margin_eur"]),
        ("margin_floor_pct", offer.margin_floor_pct, source["margin_floor_pct"]),
    )
    for field, actual, expected in checks:
        if abs(float(actual) - float(expected)) > 1e-9:
            drift.append(field)
    allowed = (
        source["gate"] == "PASS"
        and computed_margin_pct + 1e-12 >= source["margin_floor_pct"]
        and not drift
    )
    return {
        "allowed": allowed,
        "reason": "MARGIN_GATE_PASS" if allowed else "MARGIN_GATE_BLOCKED",
        "offer_id": offer.offer_id,
        "product": product,
        "computed_margin_pct": computed_margin_pct,
        "margin_floor_pct": source["margin_floor_pct"],
        "source_gate": source["gate"],
        "source_status": source["status"],
        "source_decision": source["source_decision"],
        "source": source["source"],
        "drift_fields": drift,
    }


async def evaluate_offer_phase(db: Any, offer_id: str) -> dict[str, Any]:
    phase = OFFER_PHASE.get(offer_id)
    if phase is None:
        return {
            "allowed": True,
            "reason": "PHASE_1_OR_NOT_PHASE_GATED",
            "phase": None,
        }
    current_source_sha = _source_file_sha("Roadmap_Monetisation")
    state = await db.academy_economy_phase_state.find_one(
        {"phase": phase},
        {"_id": 0},
    )
    evidence_is_current = bool(
        state
        and state.get("source_file_sha256") == current_source_sha
    )
    allowed = bool(
        state
        and state.get("active")
        and state.get("evidence_ref")
        and evidence_is_current
    )
    return {
        "allowed": allowed,
        "reason": "PHASE_ACTIVE" if allowed else "PHASE_NOT_ACTIVATED",
        "phase": phase,
        "evidence_ref": (state or {}).get("evidence_ref"),
        "source_file_sha256": current_source_sha,
        "evidence_source_current": evidence_is_current,
    }


async def set_phase_state(
    db: Any,
    *,
    phase: str,
    active: bool,
    evidence_ref: str,
    actor_id: str,
) -> dict[str, Any]:
    if phase not in {"PHASE_2", "PHASE_3"}:
        raise ValueError(
            "Only PHASE_2 and PHASE_3 require explicit activation state"
        )
    if active and not evidence_ref.strip():
        raise ValueError(
            "evidence_ref is required to activate an economy roadmap phase"
        )
    doc = {
        "phase": phase,
        "active": active,
        "evidence_ref": evidence_ref.strip(),
        "actor_id": actor_id,
        "source_file_sha256": _source_file_sha("Roadmap_Monetisation"),
    }
    await db.academy_economy_phase_state.update_one(
        {"phase": phase},
        {"$set": doc},
        upsert=True,
    )
    await db.academy_economy_phase_state.create_index("phase", unique=True)
    return doc
