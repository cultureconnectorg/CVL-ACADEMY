"""Line-by-line verification for the canonical Economy 3D master.

Every Mapping_812 source row is one independent pytest case. A green test
therefore means the 812-line projection is present, ordered, uniquely keyed,
source-hashed and policy-consistent. It does NOT claim checkout/payment
implementation; those remain separate commercial-runtime gates.
"""

from __future__ import annotations

from collections import Counter

import pytest

from economy_3d import (
    EXPECTED_PRICE_BUCKETS,
    EXPECTED_RECORD_COUNT,
    EXPECTED_SEGMENTS,
    commercial_class,
    load_manifest,
    record_by_code,
    record_by_requirement_id,
    records,
    validate_record,
)

MANIFEST = load_manifest()
RECORDS = records()


def test_economy_3d_manifest_has_exactly_812_unique_lines():
    assert MANIFEST["record_count"] == EXPECTED_RECORD_COUNT
    assert len(RECORDS) == EXPECTED_RECORD_COUNT
    assert len({r["requirement_id"] for r in RECORDS}) == EXPECTED_RECORD_COUNT
    assert len({r["code"] for r in RECORDS}) == EXPECTED_RECORD_COUNT


def test_economy_3d_source_identity_is_frozen():
    assert (
        MANIFEST["source_workbook"] == "CVLN_Academy_Master_Economie_3D_DECIDE_V1.xlsx"
    )
    assert MANIFEST["sheet"] == "Mapping_812"
    assert MANIFEST["workbook_sha256"]
    assert MANIFEST["mapping_sha256"]
    assert MANIFEST["projection_sha256"]


def test_economy_3d_segment_counts_match_source():
    counts = Counter(r["nature_economique"] for r in RECORDS)
    assert counts == Counter(EXPECTED_SEGMENTS)


def test_economy_3d_price_buckets_match_source():
    counts = Counter(r["prix_public_v1"] for r in RECORDS)
    assert counts == Counter(EXPECTED_PRICE_BUCKETS)


@pytest.mark.parametrize(
    "record", RECORDS, ids=[record["requirement_id"] for record in RECORDS]
)
def test_every_economy_3d_source_line(record):
    validate_record(record)
    by_requirement = record_by_requirement_id(record["requirement_id"])
    by_code = record_by_code(record["code"])
    assert by_requirement == record
    assert by_code == record
    assert commercial_class(record) in {
        "PUBLIC_MARKET",
        "CROSS_ECOSYSTEM_PROGRAM",
        "INTERNAL_NOT_FOR_SALE",
        "BUNDLED_BRIDGE",
        "HOLD_FROM_SALE",
    }
