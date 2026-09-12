"""Runtime proof for Economy 3D -> Academy order -> CVLN Wallet -> entitlement."""

from __future__ import annotations

from types import SimpleNamespace

import api.commercial as api_commercial
import commercial as commercial_module
import pytest
from api.commercial import OrderCreate
from fastapi import HTTPException
from mongomock_motor import AsyncMongoMockClient
from services.integrations.cvln_wallet import (
    CVLNWalletAmbiguousResult,
    CVLNWalletIntegration,
)


@pytest.fixture
async def commercial_db(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_commercial_test"]
    monkeypatch.setattr(api_commercial, "db", mock_db)
    monkeypatch.setattr(commercial_module, "db", mock_db)
    return mock_db


@pytest.fixture
def learner():
    return SimpleNamespace(id="user-1", frek_id="FREK-001")


async def test_offer_endpoint_returns_canonical_server_price(learner):
    offer = await api_commercial.get_offer("FMS-07", "path", learner)
    assert offer["amount_eur"] == 990.0
    assert offer["currency"] == "EUR"
    assert offer["requirement_id"] == "ACA-ECO-0013"
    assert offer["source_sheet"] == "Mapping_812"


async def test_create_order_snapshots_economy_price_and_wallet_rate(
    commercial_db, learner, monkeypatch
):
    async def fake_entity_info():
        return {"entity_id": "ent_cvln_academy", "rate_eur": 1.5}

    monkeypatch.setattr(api_commercial.cvln_wallet, "entity_info", fake_entity_info)
    order = await api_commercial.create_order(
        OrderCreate(economy_code="FMS-07", offer_kind="path"), learner
    )

    assert order["status"] == "PENDING_PAYMENT"
    assert order["amount_eur"] == 990.0
    assert order["wallet_rate_eur_per_jcc"] == 1.5
    assert order["wallet_amount_jcc"] == 660.0
    assert order["wallet_entity_id"] == "ent_cvln_academy"


async def test_wallet_payment_grants_exact_entitlement_once(
    commercial_db, learner, monkeypatch
):
    calls = []

    async def fake_entity_info():
        return {"entity_id": "ent_cvln_academy", "rate_eur": 1.5}

    async def fake_charge(frek_id, amount_cc, note, idempotency_key=None):
        calls.append((frek_id, amount_cc, note, idempotency_key))
        return {"ok": True, "frek_id": frek_id, "amount": amount_cc}

    monkeypatch.setattr(api_commercial.cvln_wallet, "entity_info", fake_entity_info)
    monkeypatch.setattr(api_commercial.cvln_wallet, "charge", fake_charge)

    order = await api_commercial.create_order(
        OrderCreate(economy_code="FMS-07"), learner
    )
    paid = await api_commercial.pay_order_with_wallet(order["order_id"], learner)
    replay = await api_commercial.pay_order_with_wallet(order["order_id"], learner)

    assert paid["status"] == "PAID"
    assert replay["status"] == "PAID"
    assert len(calls) == 1
    assert calls[0][3].startswith("pay_")
    entitlement = await commercial_db.academy_entitlements.find_one(
        {"user_id": "user-1", "economy_code": "FMS-07", "status": "ACTIVE"},
        {"_id": 0},
    )
    assert entitlement is not None
    assert entitlement["source"] == "CVLN_WALLET"


async def test_ambiguous_wallet_outcome_is_never_auto_retried(
    commercial_db, learner, monkeypatch
):
    calls = 0

    async def fake_entity_info():
        return {"entity_id": "ent_cvln_academy", "rate_eur": 1.5}

    async def ambiguous_charge(frek_id, amount_cc, note, idempotency_key=None):
        nonlocal calls
        calls += 1
        raise CVLNWalletAmbiguousResult("unknown remote outcome")

    monkeypatch.setattr(api_commercial.cvln_wallet, "entity_info", fake_entity_info)
    monkeypatch.setattr(api_commercial.cvln_wallet, "charge", ambiguous_charge)

    order = await api_commercial.create_order(
        OrderCreate(economy_code="FMS-07"), learner
    )
    with pytest.raises(HTTPException) as exc:
        await api_commercial.pay_order_with_wallet(order["order_id"], learner)
    assert exc.value.detail == "REQUIRES_REVIEW"

    with pytest.raises(HTTPException) as second:
        await api_commercial.pay_order_with_wallet(order["order_id"], learner)
    assert second.value.detail == "REQUIRES_REVIEW"
    assert calls == 1


def test_wallet_client_builds_entity_and_idempotency_headers(monkeypatch):
    monkeypatch.setenv("CVLN_WALLET_URL", "https://wallet.example")
    monkeypatch.setenv("CVLN_WALLET_API_KEY", "test-key")
    client = CVLNWalletIntegration()
    assert client._headers("pay_123") == {
        "X-API-Key": "test-key",
        "Idempotency-Key": "pay_123",
    }


async def test_paid_entitlement_opens_commercial_gate(
    commercial_db, learner, monkeypatch
):
    monkeypatch.setenv("ACADEMY_COMMERCIAL_ENTITLEMENTS_ENFORCED", "true")
    assert await commercial_module.has_commercial_access(learner.id, "FMS-07") is False
    await commercial_db.academy_entitlements.insert_one(
        {
            "entitlement_id": "ent-test",
            "user_id": learner.id,
            "economy_code": "FMS-07",
            "status": "ACTIVE",
        }
    )
    assert await commercial_module.has_commercial_access(learner.id, "FMS-07") is True
