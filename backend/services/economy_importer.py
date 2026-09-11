"""Canonical importer and policy helpers for the CVLN Academy 3D economy master."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

EXPECTED_MASTER_ROWS = 812
ECONOMY_SOURCE = (
    Path(__file__).resolve().parents[2]
    / "docs/cvln_academy_master/100_ECONOMY/raw/Mapping_812.csv"
)
REQUIRED_COLUMNS = {
    "Domaine", "Code", "Intitulé", "Dimension", "Contexte", "Type", "Statut 2D",
    "Nature économique", "Moteur primaire", "Acheteur", "Public ?", "Monétisation V1",
    "Certification", "Mission", "Valeur interne", "Pricing status", "Décision économique",
    "Packaging V1", "Prix public V1", "Activation gate", "Canal", "Revenue recognition",
    "Economic status",
}


def _clean(value: Any) -> str:
    return "" if value is None else str(value).strip()


def _hash_payload(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def load_economy_rows(path: Path = ECONOMY_SOURCE) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - headers
        if missing:
            raise ValueError(f"economy master missing columns: {sorted(missing)}")

        rows: list[dict[str, Any]] = []
        seen: set[str] = set()
        for row_number, raw in enumerate(reader, start=2):
            code = _clean(raw.get("Code"))
            if not code:
                raise ValueError(f"economy master row {row_number}: empty Code")
            if code in seen:
                raise ValueError(f"economy master duplicate Code: {code}")
            seen.add(code)
            payload = {
                "domain": _clean(raw.get("Domaine")),
                "code": code,
                "title": _clean(raw.get("Intitulé")),
                "dimension": _clean(raw.get("Dimension")),
                "context": _clean(raw.get("Contexte")),
                "type": _clean(raw.get("Type")),
                "catalogue_status": _clean(raw.get("Statut 2D")),
                "catalogue_notes": _clean(raw.get("Notes 2D")),
                "economic_nature": _clean(raw.get("Nature économique")),
                "primary_engine": _clean(raw.get("Moteur primaire")),
                "buyer": _clean(raw.get("Acheteur")),
                "public": _clean(raw.get("Public ?")),
                "monetization_v1": _clean(raw.get("Monétisation V1")),
                "certification": _clean(raw.get("Certification")),
                "mission": _clean(raw.get("Mission")),
                "internal_value": _clean(raw.get("Valeur interne")),
                "pricing_status": _clean(raw.get("Pricing status")),
                "economic_decision": _clean(raw.get("Décision économique")),
                "comment": _clean(raw.get("Commentaire")),
                "packaging_v1": _clean(raw.get("Packaging V1")),
                "public_price_v1": _clean(raw.get("Prix public V1")),
                "activation_gate": _clean(raw.get("Activation gate")),
                "channel": _clean(raw.get("Canal")),
                "revenue_recognition": _clean(raw.get("Revenue recognition")),
                "economic_status": _clean(raw.get("Economic status")),
            }
            payload["sale_policy"] = "NOT_FOR_SALE" if payload["public_price_v1"].upper() == "NOT_FOR_SALE" else "GATED"
            payload["source"] = {
                "kind": "MASTER_ECONOMY_3D",
                "path": str(path.relative_to(Path(__file__).resolve().parents[2])),
                "row": row_number,
            }
            payload["source_hash"] = _hash_payload(payload)
            rows.append(payload)

    if len(rows) != EXPECTED_MASTER_ROWS:
        raise ValueError(
            f"economy master row count mismatch: expected {EXPECTED_MASTER_ROWS}, got {len(rows)}"
        )
    return rows


async def import_economy_master(db: Any, rows: Iterable[dict[str, Any]] | None = None) -> dict[str, int]:
    parsed = list(rows) if rows is not None else load_economy_rows()
    if len(parsed) != EXPECTED_MASTER_ROWS:
        raise ValueError(f"refusing partial economy import: {len(parsed)} rows")

    matched = modified = upserted = 0
    for row in parsed:
        result = await db.academy_economy_master.update_one(
            {"code": row["code"]},
            {"$set": row},
            upsert=True,
        )
        matched += int(getattr(result, "matched_count", 0) or 0)
        modified += int(getattr(result, "modified_count", 0) or 0)
        upserted += int(getattr(result, "upserted_id", None) is not None)

    await db.academy_economy_master.create_index("code", unique=True)
    await db.academy_economy_master.create_index([("economic_status", 1), ("sale_policy", 1)])
    return {"rows": len(parsed), "matched": matched, "modified": modified, "upserted": upserted}


def evaluate_sale_policy(record: dict[str, Any], satisfied_gates: set[str] | None = None) -> dict[str, Any]:
    """Return a machine-readable allow/deny decision without inventing business authority."""
    if record.get("sale_policy") == "NOT_FOR_SALE":
        return {"allowed": False, "reason": "NOT_FOR_SALE", "required_gates": []}

    gate_expr = _clean(record.get("activation_gate"))
    required = [part.strip() for part in gate_expr.split("+") if part.strip()]
    satisfied = satisfied_gates or set()
    missing = [gate for gate in required if gate not in satisfied]
    if missing:
        return {"allowed": False, "reason": "ACTIVATION_GATE", "required_gates": required, "missing_gates": missing}
    return {"allowed": True, "reason": "POLICY_SATISFIED", "required_gates": required}
