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
    assert MANIFEST["source_sheet"] == "Mapping_812"
    assert MANIFEST["source_range"] == "A1:Y813"
    assert MANIFEST["source_workbook_sha256"] == (
        "be41260e722ac3daa1974ef52fb0f48f8c31536a8be420469b139755bb9c6bc0"
    )


@pytest.mark.parametrize(
    "index,record",
    list(enumerate(RECORDS, start=1)),
    ids=[r["requirement_id"] for r in RECORDS],
)
def test_each_economy_3d_line_is_traceable_and_policy_consistent(index, record):
    """812 distinct tests: one test for one canonical Mapping_812 row."""

    validate_record(record, index)
    assert record_by_requirement_id(record["requirement_id"])["code"] == record["code"]
    assert record_by_code(record["code"])["requirement_id"] == record["requirement_id"]
    assert commercial_class(record) in {
        "PUBLIC_MARKET",
        "CROSS_ECOSYSTEM_PROGRAM",
        "INTERNAL_NOT_FOR_SALE",
        "BUNDLED_BRIDGE",
        "HOLD_FROM_SALE",
    }


def test_economy_3d_segment_totals_match_the_workbook():
    assert Counter(r["nature_economique"] for r in RECORDS) == Counter(
        EXPECTED_SEGMENTS
    )


def test_economy_3d_price_buckets_match_the_workbook():
    assert Counter(r["prix_public_v1"] for r in RECORDS) == Counter(
        EXPECTED_PRICE_BUCKETS
    )


def test_not_for_sale_is_never_publicly_sellable():
    rows = [r for r in RECORDS if r["prix_public_v1"] == "NOT_FOR_SALE"]
    assert len(rows) == 221
    for record in rows:
        assert record["public"] == "NON"
        assert record["packaging_v1"] in {
            "INTERNAL_QUALIFICATION",
            "RESTRICTED_INTERNAL",
            "PRIVILEGED_INTERNAL",
            "HOLD_FROM_SALE",
        }


def test_public_market_rows_are_all_canonicalized_before_sale():
    rows = [r for r in RECORDS if r["nature_economique"] == "Marché"]
    assert len(rows) == 437
    assert {r["activation_gate"] for r in rows} == {"CANONICALIZED"}
    assert {r["prix_public_v1"] for r in rows} == {"€990 path / subscription"}


def test_cross_ecosystem_is_program_only_not_b2c_microcourse():
    rows = [r for r in RECORDS if r["nature_economique"] == "Cross-ecosystem"]
    assert len(rows) == 153
    assert {r["packaging_v1"] for r in rows} == {"CROSS_CVLN_PROGRAM"}
    assert {r["prix_public_v1"] for r in rows} == {"B2B/B2G/Enterprise bundle"}


def test_special_bridge_and_hold_rows_are_explicit():
    bridge = record_by_requirement_id("ACA-ECO-0353")
    hold = record_by_requirement_id("ACA-ECO-0675")
    assert bridge["code"] == "SAY-LAB"
    assert commercial_class(bridge) == "BUNDLED_BRIDGE"
    assert bridge["prix_public_v1"] == "€0 standalone"
    assert hold["code"] == "HOS-GAP"
    assert commercial_class(hold) == "HOLD_FROM_SALE"
    assert hold["economic_status"] == "DECIDED_HOLD"
