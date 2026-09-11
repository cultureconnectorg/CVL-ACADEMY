from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

import payments.service as payment_service
from payments.service import EconomyPolicyBlockedError, ProviderNotConfiguredError, create_checkout
from services.economy_importer import load_economy_rows
from services.economy_runtime import (
    PACKAGE_OFFERS,
    evaluate_runtime_row,
    public_discovery_allowed,
    set_gate_state,
)


def _rows():
    return load_economy_rows()


def test_all_812_rows_have_executable_runtime_policy():
    rows = _rows()
    assert len(rows) == 812
    assert len({row["code"] for row in rows}) == 812
    unknown_packages = {row["packaging_v1"] for row in rows} - set(PACKAGE_OFFERS)
    assert unknown_packages == set()
    decisions = [evaluate_runtime_row(row) for row in rows]
    assert len(decisions) == 812
    assert all(decision["code"] for decision in decisions)
    assert all(decision["source_row"] >= 2 for decision in decisions)


def test_812_distribution_is_enforced_not_merely_imported():
    rows = _rows()
    assert sum(row["public"] == "OUI" for row in rows) == 437
    assert sum(row["public"] == "NON" for row in rows) == 221
    assert sum(row["public"] == "SÉLECTIF" for row in rows) == 154
    assert sum(public_discovery_allowed(row) for row in rows) == 437
    assert sum(row["public_price_v1"] == "NOT_FOR_SALE" for row in rows) == 221
    assert sum(row["economic_status"] == "DECIDED_HOLD" for row in rows) == 1


def test_external_line_requires_canonicalized_and_checks_package():
    row = next(row for row in _rows() if row["code"] == "FMS-07")
    blocked = evaluate_runtime_row(row, offer_id="parcours-metier")
    assert blocked["sale_allowed"] is False
    assert blocked["missing_gates"] == ["CANONICALIZED"]

    allowed = evaluate_runtime_row(
        row, satisfied_gates={"CANONICALIZED"}, offer_id="parcours-metier"
    )
    assert allowed["sale_allowed"] is True

    wrong_offer = evaluate_runtime_row(
        row, satisfied_gates={"CANONICALIZED"}, offer_id="internal-cvln-capability"
    )
    assert wrong_offer["sale_allowed"] is False
    assert "OFFER_NOT_ALLOWED_FOR_PACKAGE" in wrong_offer["reasons"]


def test_internal_and_hold_rows_are_hard_blocked_from_sale():
    internal = next(row for row in _rows() if row["code"] == "KLT-09")
    internal_decision = evaluate_runtime_row(
        internal, satisfied_gates={"PRODUCT_VERIFIED", "ROLE_DEFINED"}
    )
    assert internal_decision["sale_allowed"] is False
    assert internal_decision["sale_reason"] == "NOT_FOR_SALE"

    hold = next(row for row in _rows() if row["economic_status"] == "DECIDED_HOLD")
    hold_decision = evaluate_runtime_row(
        hold, satisfied_gates={"RECONCILIATION_REQUIRED"}
    )
    assert hold_decision["sale_allowed"] is False
    assert hold_decision["sale_reason"] == "DECIDED_HOLD"


@pytest.mark.asyncio
async def test_activation_gate_requires_declared_gate_and_evidence():
    client = AsyncMongoMockClient()
    db = client["economy_gate_test"]
    row = next(row for row in _rows() if row["code"] == "KLT-09")
    await db.academy_economy_master.insert_one(row)

    with pytest.raises(ValueError):
        await set_gate_state(
            db, code="KLT-09", gate="CANONICALIZED", satisfied=True,
            evidence_ref="proof", actor_id="founder"
        )
    with pytest.raises(ValueError):
        await set_gate_state(
            db, code="KLT-09", gate="ROLE_DEFINED", satisfied=True,
            evidence_ref="", actor_id="founder"
        )

    stored = await set_gate_state(
        db, code="KLT-09", gate="ROLE_DEFINED", satisfied=True,
        evidence_ref="evidence:role-1", actor_id="founder"
    )
    assert stored["satisfied"] is True
    assert stored["source_hash"] == row["source_hash"]


@pytest.fixture
async def checkout_db(monkeypatch):
    client = AsyncMongoMockClient()
    db = client["economy_checkout_test"]
    monkeypatch.setattr(payment_service, "db", db)
    monkeypatch.setattr(payment_service, "is_provider_configured", lambda: False)
    return db


@pytest.mark.asyncio
async def test_checkout_blocks_not_for_sale_before_payment_provider(checkout_db, monkeypatch):
    row = next(row for row in _rows() if row["code"] == "KLT-09")
    await checkout_db.academy_economy_master.insert_one(row)

    async def no_authority():
        return {}
    monkeypatch.setattr(payment_service, "get_canonical_authority_map", no_authority)

    with pytest.raises(EconomyPolicyBlockedError):
        await create_checkout(
            user_id="u1", offer_id="academy-pro", formation_code="KLT-09",
            success_url="https://example.test/ok", cancel_url="https://example.test/cancel"
        )
    assert await checkout_db.payment_checkout_sessions.count_documents({}) == 0


@pytest.mark.asyncio
async def test_checkout_external_line_passes_economy_then_reaches_provider_gate(checkout_db, monkeypatch):
    row = next(row for row in _rows() if row["code"] == "FMS-07")
    await checkout_db.academy_economy_master.insert_one(row)

    async def canonical_authority():
        return {"FMS-07": {"domain": "FMS", "route": "/canonical/FMS-07"}}
    monkeypatch.setattr(payment_service, "get_canonical_authority_map", canonical_authority)

    with pytest.raises(ProviderNotConfiguredError):
        await create_checkout(
            user_id="u1", offer_id="parcours-metier", formation_code="FMS-07",
            success_url="https://example.test/ok", cancel_url="https://example.test/cancel"
        )
    stored = await checkout_db.payment_checkout_sessions.find_one({"user_id": "u1"})
    assert stored["formation_code"] == "FMS-07"
    assert stored["economy_decision"]["sale_allowed"] is True
