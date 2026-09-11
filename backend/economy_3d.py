"""Canonical Economy 3D traceability runtime.

This module exposes the line-by-line traceability snapshot derived from
CVLN_Academy_Master_Economie_3D_DECIDE_V1.xlsx / Mapping_812!A1:Y813.

The workbook remains the canonical source. The repository snapshot is a
verifiable projection containing one entry per source row plus a SHA-256 hash
of the full 25-column row. It is intentionally fail-closed: malformed,
incomplete, duplicated or policy-inconsistent data raises immediately.
"""

from __future__ import annotations

import base64
import gzip
import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Iterable, List

DATA_PATH = Path(__file__).parent / "data" / "economy_3d_traceability_v1.json.gz.b64"
EXPECTED_RECORD_COUNT = 812
EXPECTED_WORKBOOK_SHA256 = (
    "be41260e722ac3daa1974ef52fb0f48f8c31536a8be420469b139755bb9c6bc0"
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


class Economy3DError(RuntimeError):
    """Raised when the Economy 3D projection violates its canonical contract."""


@lru_cache(maxsize=1)
def load_manifest() -> Dict[str, Any]:
    encoded = DATA_PATH.read_text(encoding="utf-8").strip()
    try:
        payload = gzip.decompress(base64.b64decode(encoded, validate=True))
        manifest = json.loads(payload.decode("utf-8"))
    except Exception as exc:  # pragma: no cover - defensive corruption guard
        raise Economy3DError("Economy 3D traceability snapshot is unreadable") from exc
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
    nature = record["nature_economique"]
    if nature == "Marché":
        return "PUBLIC_MARKET"
    if nature == "Cross-ecosystem":
        return "CROSS_ECOSYSTEM_PROGRAM"
    if nature in {"Interne", "Interne restreint", "Interne privilégié"}:
        return "INTERNAL_NOT_FOR_SALE"
    if nature == "Bridge":
        return "BUNDLED_BRIDGE"
    if nature == "Hold":
        return "HOLD_FROM_SALE"
    raise Economy3DError(f"Unknown economic nature: {nature!r}")


def validate_record(record: Dict[str, Any], index: int) -> None:
    expected_id = f"ACA-ECO-{index:04d}"
    expected_row = index + 1
    if record.get("requirement_id") != expected_id:
        raise Economy3DError(
            f"record {index}: expected {expected_id}, got {record.get('requirement_id')!r}"
        )
    if record.get("source_row") != expected_row:
        raise Economy3DError(
            f"{expected_id}: expected source row {expected_row}, "
            f"got {record.get('source_row')!r}"
        )
    code = record.get("code")
    if not isinstance(code, str) or not code.strip():
        raise Economy3DError(f"{expected_id}: code is missing")
    row_hash = record.get("row_sha256")
    if not isinstance(row_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", row_hash):
        raise Economy3DError(f"{expected_id}: invalid source-row SHA-256")
    if record.get("pricing_status") != "DECIDED_V1":
        raise Economy3DError(f"{expected_id}: pricing_status is not DECIDED_V1")

    nature = record.get("nature_economique")
    price = record.get("prix_public_v1")
    public = record.get("public")
    package = record.get("packaging_v1")
    gate = record.get("activation_gate")
    channel = record.get("canal")
    recognition = record.get("revenue_recognition")
    status = record.get("economic_status")

    if nature == "Marché":
        expected = (
            price == "€990 path / subscription"
            and public == "OUI"
            and package == "INCLUDED_PRO + ELIGIBLE_PATH"
            and gate == "CANONICALIZED"
            and channel == "B2C+B2B+B2G"
            and recognition == "External revenue"
            and status == "DECIDED_V1"
        )
        if not expected:
            raise Economy3DError(f"{expected_id}: public-market policy drift")
    elif nature == "Cross-ecosystem":
        expected = (
            price == "B2B/B2G/Enterprise bundle"
            and public == "SÉLECTIF"
            and package == "CROSS_CVLN_PROGRAM"
            and gate == "VERTICALS_CANONICALIZED + HANDOFF_VERIFIED"
            and channel == "B2B/B2G/Internal"
            and recognition == "Program/enterprise revenue"
            and status == "DECIDED_V1"
        )
        if not expected:
            raise Economy3DError(f"{expected_id}: cross-ecosystem policy drift")
    elif nature == "Interne":
        expected = (
            price == "NOT_FOR_SALE"
            and public == "NON"
            and package == "INTERNAL_QUALIFICATION"
            and gate == "PRODUCT_VERIFIED + ROLE_DEFINED"
            and channel == "Internal"
            and recognition == "Internal value"
            and status == "DECIDED_V1"
        )
        if not expected:
            raise Economy3DError(f"{expected_id}: internal policy drift")
    elif nature == "Interne restreint":
        expected = (
            price == "NOT_FOR_SALE"
            and public == "NON"
            and package == "RESTRICTED_INTERNAL"
            and gate == "PRODUCT_VERIFIED + NEED_TO_KNOW + APPROVAL"
            and channel == "Internal restricted"
            and recognition == "Internal value"
            and status == "DECIDED_V1"
        )
        if not expected:
            raise Economy3DError(f"{expected_id}: restricted-internal policy drift")
    elif nature == "Interne privilégié":
        expected = (
            price == "NOT_FOR_SALE"
            and public == "NON"
            and package == "PRIVILEGED_INTERNAL"
            and gate == "PRODUCT_VERIFIED + PRIVILEGED_APPROVAL + AUDIT"
            and channel == "Internal privileged"
            and recognition == "Internal value"
            and status == "DECIDED_V1"
        )
        if not expected:
            raise Economy3DError(f"{expected_id}: privileged-internal policy drift")
    elif nature == "Bridge":
        expected = (
            price == "€0 standalone"
            and public == "SÉLECTIF"
            and package == "BUNDLED_BRIDGE"
            and gate == "CANONICALIZED + ELIGIBILITY_RULES"
            and channel == "Career+B2B/B2G"
            and recognition == "Bundled/program revenue"
            and status == "DECIDED_V1"
        )
        if not expected:
            raise Economy3DError(f"{expected_id}: bridge policy drift")
    elif nature == "Hold":
        expected = (
            price == "NOT_FOR_SALE"
            and public == "NON"
            and package == "HOLD_FROM_SALE"
            and gate == "RECONCILIATION_REQUIRED"
            and channel == "None"
            and recognition == "None"
            and status == "DECIDED_HOLD"
        )
        if not expected:
            raise Economy3DError(f"{expected_id}: hold policy drift")
    else:
        raise Economy3DError(f"{expected_id}: unknown economic nature {nature!r}")


def validate_manifest(manifest: Dict[str, Any]) -> None:
    if manifest.get("schema_version") != "1.0.0":
        raise Economy3DError("unsupported Economy 3D traceability schema")
    if manifest.get("source_workbook") != "CVLN_Academy_Master_Economie_3D_DECIDE_V1.xlsx":
        raise Economy3DError("unexpected source workbook")
    if manifest.get("source_sheet") != "Mapping_812":
        raise Economy3DError("unexpected source sheet")
    if manifest.get("source_range") != "A1:Y813":
        raise Economy3DError("unexpected source range")
    if manifest.get("source_workbook_sha256") != EXPECTED_WORKBOOK_SHA256:
        raise Economy3DError("canonical workbook SHA-256 drift")

    items = manifest.get("records")
    if not isinstance(items, list) or len(items) != EXPECTED_RECORD_COUNT:
        raise Economy3DError(
            f"expected {EXPECTED_RECORD_COUNT} Economy 3D records, "
            f"got {len(items) if isinstance(items, list) else 'non-list'}"
        )

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
