from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

import services.economy_checkout as economy_checkout
from commerce.catalog import OFFERS, get_offer
from services.economy_workbook_runtime import (
    SHEETS,
    UNIT_OFFER_PRODUCT,
    evaluate_offer_phase,
    evaluate_offer_unit_economics,
    import_economy_workbook_runtime,
    load_economy_workbook_rows,
    load_unit_economics,
    set_phase_state,
)


def test_complete_economy_workbook_has_15_runtime_source_sheets():
    workbook = load_economy_workbook_rows()
    assert set(workbook) == set(SHEETS)
    assert len(workbook) == 15
    assert len(workbook["Mapping_812"]) == 813
    assert all(
        row["source_hash"]
        for rows in workbook.values()
        for row in rows
    )
    assert all(
        row["source_file_sha256"]
        for rows in workbook.values()
        for row in rows
    )


def test_all_18_unit_economics_products_match_commerce_runtime():
    source = load_unit_economics()
    assert len(source) == 18
    mapped_offers = [
        offer
        for offer in OFFERS
        if offer.offer_id in UNIT_OFFER_PRODUCT
    ]
    assert len(mapped_offers) == 18
    for offer in mapped_offers:
        decision = evaluate_offer_unit_economics(offer)
        assert decision["allowed"] is True, decision
        assert decision["source_gate"] == "PASS"
        assert (
            decision["computed_margin_pct"]
            >= decision["margin_floor_pct"]
        )


def test_unit_economics_blocks_runtime_drift_or_margin_regression():
    offer = get_offer("academy-access")
    assert offer is not None
    drifted = offer.model_copy(
        update={"variable_cost_eur": offer.variable_cost_eur + 20.0}
    )
    decision = evaluate_offer_unit_economics(drifted)
    assert decision["allowed"] is False
    assert "variable_cost_eur" in decision["drift_fields"]


@pytest.mark.asyncio
async def test_full_workbook_import_is_line_complete_and_idempotent():
    client = AsyncMongoMockClient()
    db = client["economy_workbook_test"]
    expected = load_economy_workbook_rows()
    expected_total = sum(len(rows) for rows in expected.values())

    first = await import_economy_workbook_runtime(db)
    second = await import_economy_workbook_runtime(db)
    assert first["sheets"] == 15
    assert first["runtime_rows"] == expected_total
    assert second["runtime_rows"] == expected_total
    assert (
        await db.academy_economy_workbook_rows.count_documents({})
        == expected_total
    )


@pytest.mark.asyncio
async def test_phase_2_and_3_are_fail_closed_until_evidence_activation():
    client = AsyncMongoMockClient()
    db = client["economy_phase_test"]

    blocked = await evaluate_offer_phase(db, "b2b-enterprise")
    assert blocked["allowed"] is False
    assert blocked["reason"] == "PHASE_NOT_ACTIVATED"
    assert blocked["phase"] == "PHASE_2"
    assert blocked["evidence_ref"] is None
    assert blocked["evidence_source_current"] is False
    assert blocked["source_file_sha256"]

    with pytest.raises(ValueError):
        await set_phase_state(
            db,
            phase="PHASE_2",
            active=True,
            evidence_ref="",
            actor_id="founder",
        )

    stored = await set_phase_state(
        db,
        phase="PHASE_2",
        active=True,
        evidence_ref="evidence:phase2-entry-gates",
        actor_id="founder",
    )
    assert stored["source_file_sha256"]

    allowed = await evaluate_offer_phase(db, "b2b-enterprise")
    assert allowed["allowed"] is True
    assert allowed["phase"] == "PHASE_2"
    assert allowed["evidence_source_current"] is True

    await db.academy_economy_phase_state.update_one(
        {"phase": "PHASE_2"},
        {"$set": {"source_file_sha256": "stale-roadmap-hash"}},
    )
    stale = await evaluate_offer_phase(db, "b2b-enterprise")
    assert stale["allowed"] is False
    assert stale["evidence_source_current"] is False


@pytest.mark.asyncio
async def test_checkout_guard_blocks_phase_before_low_level_checkout(
    monkeypatch,
):
    client = AsyncMongoMockClient()
    db = client["economy_checkout_guard_test"]
    called = {"count": 0}

    async def fake_checkout(**kwargs):
        called["count"] += 1
        return kwargs

    monkeypatch.setattr(
        economy_checkout,
        "create_payment_checkout",
        fake_checkout,
    )

    with pytest.raises(Exception) as exc_info:
        await economy_checkout.create_economy_guarded_checkout(
            db=db,
            user_id="u1",
            offer_id="b2b-enterprise",
            success_url="https://example.test/ok",
            cancel_url="https://example.test/cancel",
        )
    assert exc_info.type.__name__ == "EconomyPolicyBlockedError"
    assert called["count"] == 0

    await set_phase_state(
        db,
        phase="PHASE_2",
        active=True,
        evidence_ref="evidence:phase2",
        actor_id="founder",
    )
    result = await economy_checkout.create_economy_guarded_checkout(
        db=db,
        user_id="u1",
        offer_id="b2b-enterprise",
        success_url="https://example.test/ok",
        cancel_url="https://example.test/cancel",
    )
    assert result["offer_id"] == "b2b-enterprise"
    assert called["count"] == 1
