"""ECON-03/WAL-01 (Audit Chirurgical 2026-09-07) — CC/wallet/badge
atomicity.

Real, exploitable gaps this suite closes and proves closed:

  - `wallet.service.credit()` had no idempotency key at all
    (`economic_event_id`) — a retried or duplicated call for the same
    real-world event minted a second ledger transaction and
    double-incremented the cached balance.
  - `wallet.service.credit()` inserted the ledger row then updated the
    cached balance in two separate operations with no reconciliation
    path — a crash between them left `ledger != balance` with no way
    to repair it.
  - `badges_engine.award_threshold_badges()` did a plain
    find_one-then-insert with no atomic guard — two concurrent calls
    could both see "not exists" and both insert (the pre-existing
    unique index on (user_id, badge_code) made the double-insert itself
    impossible, but the resulting DuplicateKeyError on the losing call
    went uncaught, surfacing as a crash instead of a safe no-op).

DB-backed pieces run against `mongomock_motor.AsyncMongoMockClient` —
same convention as every other suite in this repo. Unlike production
(where `infra_indexes.ensure_indexes()` runs once at startup), the
unique indexes these guarantees actually rely on are created
explicitly in each fixture below — the guarantee under test is real DB
behavior, not this module's own bookkeeping.
"""

from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

import badges_engine as badges_module
import services.events as events_module
import services.frek_core as frek_core_module
import wallet.service as wallet_service_module
from badges_engine import award_threshold_badges
from wallet.service import credit, reconcile_wallet_balance


@pytest.fixture
async def wal_db(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_wallet_econ03_test"]
    await mock_db.wallet_transactions.create_index(
        [("user_id", 1), ("economic_event_id", 1)], unique=True
    )
    await mock_db.user_badges.create_index(
        [("user_id", 1), ("badge_code", 1)], unique=True
    )
    # ACA-0029 — award_threshold_badges now also publishes a real
    # academy_badge_awarded event (services/events.py), which writes to
    # db.event_log — needs the same mock db as everything else here,
    # or it reaches for a real (absent) MongoDB and hangs/times out.
    for module in (
        wallet_service_module,
        badges_module,
        frek_core_module,
        events_module,
    ):
        monkeypatch.setattr(module, "db", mock_db)
    return mock_db


# --------------------------------------------------------------------
# WAL-01 — credit() idempotency
# --------------------------------------------------------------------


@pytest.mark.asyncio
async def test_credit_creates_transaction_and_updates_balance(wal_db):
    txn = await credit(
        "u1", "jcc_earned", 15.0, economic_event_id="ev-1", currency="jcc"
    )
    assert txn.amount == 15.0
    account = await wal_db.wallet_accounts.find_one({"user_id": "u1"}, {"_id": 0})
    assert account["jcc_balance"] == 15.0


@pytest.mark.asyncio
async def test_credit_x100_same_event_id_credits_exactly_once(wal_db):
    """The audit's own required proof pattern, applied to the wallet
    ledger directly."""
    results = [
        await credit("u1", "jcc_earned", 15.0, economic_event_id="ev-1", currency="jcc")
        for _ in range(100)
    ]
    assert all(r.id == results[0].id for r in results)  # same transaction returned

    count = await wal_db.wallet_transactions.count_documents(
        {"user_id": "u1", "economic_event_id": "ev-1"}
    )
    assert count == 1
    account = await wal_db.wallet_accounts.find_one({"user_id": "u1"}, {"_id": 0})
    assert account["jcc_balance"] == 15.0  # not 15*100


@pytest.mark.asyncio
async def test_credit_different_event_ids_both_apply(wal_db):
    """Not over-blocking — two genuinely different events for the same
    user both credit."""
    await credit("u1", "jcc_earned", 10.0, economic_event_id="ev-a", currency="jcc")
    await credit("u1", "jcc_earned", 20.0, economic_event_id="ev-b", currency="jcc")
    account = await wal_db.wallet_accounts.find_one({"user_id": "u1"}, {"_id": 0})
    assert account["jcc_balance"] == 30.0


@pytest.mark.asyncio
async def test_credit_event_ids_are_scoped_per_user(wal_db):
    """The same economic_event_id string for two different users must
    not collide — the unique index is compound on (user_id, event_id)."""
    await credit(
        "u1", "jcc_earned", 10.0, economic_event_id="ev-shared", currency="jcc"
    )
    await credit(
        "u2", "jcc_earned", 10.0, economic_event_id="ev-shared", currency="jcc"
    )
    acc1 = await wal_db.wallet_accounts.find_one({"user_id": "u1"}, {"_id": 0})
    acc2 = await wal_db.wallet_accounts.find_one({"user_id": "u2"}, {"_id": 0})
    assert acc1["jcc_balance"] == 10.0
    assert acc2["jcc_balance"] == 10.0


# --------------------------------------------------------------------
# WAL-01 — reconciliation (the repair path for the crash-between-
# ledger-and-cache window)
# --------------------------------------------------------------------


@pytest.mark.asyncio
async def test_reconcile_repairs_a_desynced_cached_balance(wal_db):
    """Simulates the exact crash window credit()'s own docstring names:
    the ledger entries exist (source of truth) but the cached balance
    was never updated to match — reconcile must fix it."""
    await wal_db.wallet_accounts.insert_one(
        {"user_id": "u1", "jcc_balance": 0.0, "token_balance": 0.0}
    )
    # Real ledger rows inserted directly (as if credit() crashed right
    # after the insert, before its own $inc ran).
    await wal_db.wallet_transactions.insert_one(
        {
            "id": "t1",
            "user_id": "u1",
            "type": "jcc_earned",
            "amount": 15.0,
            "currency": "jcc",
            "economic_event_id": "ev-1",
        }
    )
    await wal_db.wallet_transactions.insert_one(
        {
            "id": "t2",
            "user_id": "u1",
            "type": "jcc_earned",
            "amount": 10.0,
            "currency": "token",
            "economic_event_id": "ev-2",
        }
    )

    account = await reconcile_wallet_balance("u1")
    assert account.jcc_balance == 15.0
    assert account.token_balance == 10.0


@pytest.mark.asyncio
async def test_reconcile_is_idempotent(wal_db):
    await credit("u1", "jcc_earned", 5.0, economic_event_id="ev-1", currency="jcc")
    first = await reconcile_wallet_balance("u1")
    second = await reconcile_wallet_balance("u1")
    assert first.jcc_balance == second.jcc_balance == 5.0


# --------------------------------------------------------------------
# ECON-03 — badge award atomicity
# --------------------------------------------------------------------


@pytest.mark.asyncio
async def test_award_threshold_badges_awards_exactly_once(wal_db):
    await wal_db.badges.insert_one(
        {"code": "BADGE-1", "name": "Découverte", "cc_threshold": 0}
    )
    await wal_db.users.insert_one({"id": "u1"})

    for _ in range(100):
        await award_threshold_badges("u1", 50)

    count = await wal_db.user_badges.count_documents(
        {"user_id": "u1", "badge_code": "BADGE-1"}
    )
    assert count == 1

    txn_count = await wal_db.wallet_transactions.count_documents(
        {"user_id": "u1", "economic_event_id": "badge:BADGE-1"}
    )
    assert txn_count == 1
    account = await wal_db.wallet_accounts.find_one({"user_id": "u1"}, {"_id": 0})
    assert account["jcc_balance"] == 10.0  # BADGE_JCC_REWARD, not 10*100


@pytest.mark.asyncio
async def test_award_threshold_badges_skips_below_threshold(wal_db):
    await wal_db.badges.insert_one(
        {"code": "BADGE-HIGH", "name": "Senior", "cc_threshold": 500}
    )
    await wal_db.users.insert_one({"id": "u1"})

    await award_threshold_badges("u1", 50)

    count = await wal_db.user_badges.count_documents({"user_id": "u1"})
    assert count == 0
