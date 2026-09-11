"""Canonical Economy 3D line-by-line traceability runtime.

Source of truth:
CVLN_Academy_Master_Economie_3D_DECIDE_V1.xlsx / Mapping_812!A1:Y813.

The workbook stays authoritative. This repository stores one plain-text line
per canonical item (Code|economic-class), plus frozen SHA-256 identifiers for
the workbook and full Mapping_812 source data. All pricing, public/private,
packaging, activation, channel and revenue rules below are the invariants found
in the canonical workbook for each economic class.

This module proves Economy 3D source decisions are present and queryable. It
does NOT claim checkout, payment, invoice, subscription or entitlement runtime.
"""

from __future__ import annotations

import hashlib
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Iterable, List

DATA_PATH = Path(__file__).parent / "data" / "economy_3d_classes_v1.txt"
EXPECTED_RECORD_COUNT = 812
EXPECTED_WORKBOOK_SHA256 = (
    "be41260e722ac3daa1974ef52fb0f48f8c31536a8be420469b139755bb9c6bc0"
)
EXPECTED_MAPPING_SHA256 = (
    "03c512d7cf8644030612e8f70d890fd997735db3789f3ea06608d050143d010a"
)
EXPECTED_CLASS_PROJECTION_SHA256 = (
    "3a20b4c76890c70e628f87bd5a013eaa63812b4c4964e0e02fdb83c819f3152f"
)
EXPECTED_SEGMENTS = {
    "Marché": 437,
    "Cross-ecosystem": 153,
    "Interne": 152,
    "Interne restreint": 53,
    "Interne privilégié": 15,
    "Bridge": 1,
    "Hold": 1,
}
EXPECTED_PRICE_BUCKETS = {
    "€990 path / subscription": 437,
    "B2B/B2G/Enterprise bundle": 153,
    "NOT_FOR_SALE": 221,
    "€0 standalone": 1,
}

CLASS_POLICY: Dict[str, Dict[str, str]] = {
    "M": {
        "nature_economique": "Marché",
        "moteur_primaire": "B2C Learning",
        "public": "OUI",
        "pricing_status": "DECIDED_V1",
        "packaging_v1": "INCLUDED_PRO + ELIGIBLE_PATH",
        "prix_public_v1": "€990 path / subscription",
        "activation_gate": "CANONICALIZED",
        "canal": "B2C+B2B+B2G",
        "revenue_recognition": "External revenue",
        "economic_status": "DECIDED_V1",
    },
    "X": {
        "nature_economique": "Cross-ecosystem",
        "moteur_primaire": "B2B Workforce/Learning-to-Work",
        "public": "SÉLECTIF",
        "pricing_status": "DECIDED_V1",
        "packaging_v1": "CROSS_CVLN_PROGRAM",
        "prix_public_v1": "B2B/B2G/Enterprise bundle",
        "activation_gate": "VERTICALS_CANONICALIZED + HANDOFF_VERIFIED",
        "canal": "B2B/B2G/Internal",
        "revenue_recognition": "Program/enterprise revenue",
        "economic_status": "DECIDED_V1",
    },
    "I": {
        "nature_economique": "Interne",
        "moteur_primaire": "Internal Value",
        "public": "NON",
        "pricing_status": "DECIDED_V1",
        "packaging_v1": "INTERNAL_QUALIFICATION",
        "prix_public_v1": "NOT_FOR_SALE",
        "activation_gate": "PRODUCT_VERIFIED + ROLE_DEFINED",
        "canal": "Internal",
        "revenue_recognition": "Internal value",
        "economic_status": "DECIDED_V1",
    },
    "R": {
        "nature_economique": "Interne restreint",
        "moteur_primaire": "Internal Value",
        "public": "NON",
        "pricing_status": "DECIDED_V1",
        "packaging_v1": "RESTRICTED_INTERNAL",
        "prix_public_v1": "NOT_FOR_SALE",
        "activation_gate": "PRODUCT_VERIFIED + NEED_TO_KNOW + APPROVAL",
        "canal": "Internal restricted",
        "revenue_recognition": "Internal value",
        "economic_status": "DECIDED_V1",
    },
    "P": {
        "nature_economique": "Interne privilégié",
        "moteur_primaire": "Internal Value",
        "public": "NON",
        "pricing_status": "DECIDED_V1",
        "packaging_v1": "PRIVILEGED_INTERNAL",
        "prix_public_v1": "NOT_FOR_SALE",
        "activation_gate": "PRODUCT_VERIFIED + PRIVILEGED_APPROVAL + AUDIT",
        "canal": "Internal privileged",
        "revenue_recognition": "Internal value",
        "economic_status": "DECIDED_V1",
    },
    "B": {
        "nature_economique": "Bridge",
        "moteur_primaire": "Learning-to-Work",
        "public": "SÉLECTIF",
        "pricing_status": "DECIDED_V1",
        "packaging_v1": "BUNDLED_BRIDGE",
        "prix_public_v1": "€0 standalone",
        "activation_gate": "CANONICALIZED + ELIGIBILITY_RULES",
        "canal": "Career+B2B/B2G",
        "revenue_recognition": "Bundled/program revenue",
        "economic_status": "DECIDED_V1",
    },
    "H": {
        "nature_economique": "Hold",
        "moteur_primaire": "None",
        "public": "NON",
        "pricing_status": "DECIDED_V1",
        "packaging_v1": "HOLD_FROM_SALE",
        "prix_public_v1": "NOT_FOR_SALE",
        "activation_gate": "RECONCILIATION_REQUIRED",
        "canal": "None",
        "revenue_recognition": "None",
        "economic_status": "DECIDED_HOLD",
    },
}


class Economy3DError(RuntimeError):
    """Raised when the Economy 3D projection violates its canonical contract."""


@lru_cache(maxsize=1)
def load_manifest() -> Dict[str, Any]:
    raw = DATA_PATH.read_bytes()
    projection_hash = hashlib.sha256(raw).hexdigest()
    if projection_hash != EXPECTED_CLASS_PROJECTION_SHA256:
        raise Economy3DError("Economy 3D class projection SHA-256 drift")

    lines = raw.decode("utf-8").splitlines()
    if len(lines) != EXPECTED_RECORD_COUNT:
        raise Economy3DError(
            f"expected {EXPECTED_RECORD_COUNT} Economy 3D lines, got {len(lines)}"
        )

    parsed: List[Dict[str, Any]] = []
    for index, line in enumerate(lines, start=1):
        parts = line.split("|")
        if len(parts) != 2:
            raise Economy3DError(f"ACA-ECO-{index:04d}: malformed Code|Class line")
        code, class_code = parts
        policy = CLASS_POLICY.get(class_code)
        if not code or policy is None:
            raise Economy3DError(f"ACA-ECO-{index:04d}: unknown code or class")
        parsed.append(
            {
                "requirement_id": f"ACA-ECO-{index:04d}",
                "source_row": index + 1,
                "code": code,
                "class_code": class_code,
                **policy,
            }
        )

    manifest: Dict[str, Any] = {
        "schema_version": "1.2.0",
        "source_workbook": "CVLN_Academy_Master_Economie_3D_DECIDE_V1.xlsx",
        "source_sheet": "Mapping_812",
        "source_range": "A1:Y813",
        "source_workbook_sha256": EXPECTED_WORKBOOK_SHA256,
        "source_mapping_sha256": EXPECTED_MAPPING_SHA256,
        "class_projection_sha256": projection_hash,
        "record_count": len(parsed),
        "records": parsed,
    }
    validate_manifest(manifest)
    return manifest


def records() -> List[Dict[str, Any]]:
    return list(load_manifest()["records"])


def iter_records() -> Iterable[Dict[str, Any]]:
    return iter(load_manifest()["records"])


def record_by_code(code: str) -> Dict[str, Any]:
    normalized = code.strip().upper()
    for record in iter_records():
        if str(record["code"]).upper() == normalized:
            return dict(record)
    raise KeyError(code)


def record_by_requirement_id(requirement_id: str) -> Dict[str, Any]:
    normalized = requirement_id.strip().upper()
    for record in iter_records():
        if record["requirement_id"] == normalized:
            return dict(record)
    raise KeyError(requirement_id)


def commercial_class(record: Dict[str, Any]) -> str:
    class_code = record["class_code"]
    if class_code == "M":
        return "PUBLIC_MARKET"
    if class_code == "X":
        return "CROSS_ECOSYSTEM_PROGRAM"
    if class_code in {"I", "R", "P"}:
        return "INTERNAL_NOT_FOR_SALE"
    if class_code == "B":
        return "BUNDLED_BRIDGE"
    if class_code == "H":
        return "HOLD_FROM_SALE"
    raise Economy3DError(f"Unknown economic class: {class_code!r}")


def validate_record(record: Dict[str, Any], index: int) -> None:
    expected_id = f"ACA-ECO-{index:04d}"
    if record.get("requirement_id") != expected_id:
        raise Economy3DError(f"record {index}: requirement id drift")
    if record.get("source_row") != index + 1:
        raise Economy3DError(f"{expected_id}: source row drift")
    code = record.get("code")
    if not isinstance(code, str) or not code.strip():
        raise Economy3DError(f"{expected_id}: code is missing")
    class_code = record.get("class_code")
    policy = CLASS_POLICY.get(str(class_code))
    if policy is None:
        raise Economy3DError(f"{expected_id}: unknown class")
    for key, expected in policy.items():
        if record.get(key) != expected:
            raise Economy3DError(f"{expected_id}: {key} policy drift")


def validate_manifest(manifest: Dict[str, Any]) -> None:
    if manifest.get("schema_version") != "1.2.0":
        raise Economy3DError("unsupported Economy 3D traceability schema")
    if (
        manifest.get("source_workbook")
        != "CVLN_Academy_Master_Economie_3D_DECIDE_V1.xlsx"
    ):
        raise Economy3DError("unexpected source workbook")
    if manifest.get("source_sheet") != "Mapping_812":
        raise Economy3DError("unexpected source sheet")
    if manifest.get("source_range") != "A1:Y813":
        raise Economy3DError("unexpected source range")
    if manifest.get("source_workbook_sha256") != EXPECTED_WORKBOOK_SHA256:
        raise Economy3DError("canonical workbook SHA-256 drift")
    if manifest.get("source_mapping_sha256") != EXPECTED_MAPPING_SHA256:
        raise Economy3DError("canonical Mapping_812 SHA-256 drift")

    items = manifest.get("records")
    if not isinstance(items, list) or len(items) != EXPECTED_RECORD_COUNT:
        raise Economy3DError("Economy 3D record count drift")

    codes = set()
    ids = set()
    segment_counts: Dict[str, int] = {}
    price_counts: Dict[str, int] = {}
    for index, record in enumerate(items, start=1):
        validate_record(record, index)
        code = record["code"]
        req_id = record["requirement_id"]
        if code in codes:
            raise Economy3DError(f"duplicate Economy 3D code: {code}")
        if req_id in ids:
            raise Economy3DError(f"duplicate Economy 3D requirement id: {req_id}")
        codes.add(code)
        ids.add(req_id)
        nature = record["nature_economique"]
        price = record["prix_public_v1"]
        segment_counts[nature] = segment_counts.get(nature, 0) + 1
        price_counts[price] = price_counts.get(price, 0) + 1

    if segment_counts != EXPECTED_SEGMENTS:
        raise Economy3DError(f"economic segment counts drifted: {segment_counts}")
    if price_counts != EXPECTED_PRICE_BUCKETS:
        raise Economy3DError(f"price bucket counts drifted: {price_counts}")
