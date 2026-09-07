"""Wallet ledger — credit/debit + balance/history reads."""

from __future__ import annotations

from typing import List, Literal, Optional

from pymongo.errors import DuplicateKeyError

from db import db, utc_now_iso

from .models import TransactionType, WalletAccount, WalletSummary, WalletTransaction

Currency = Literal["jcc", "token", "eur"]


async def _get_or_create_account(user_id: str) -> WalletAccount:
    doc = await db.wallet_accounts.find_one({"user_id": user_id}, {"_id": 0})
    if doc:
        return WalletAccount(**doc)
    account = WalletAccount(user_id=user_id)
    await db.wallet_accounts.insert_one(account.model_dump())
    return account


async def credit(
    user_id: str,
    transaction_type: TransactionType,
    amount: float,
    economic_event_id: str,
    currency: Currency = "jcc",
    ref: Optional[str] = None,
    description: str = "",
    badge_code: Optional[str] = None,
) -> WalletTransaction:
    """Records a ledger entry and updates the cached balance. `amount` is
    always positive here — `reward_redeemed` records are logged with a
    negative amount by the caller if it represents a spend.

    WAL-01 (Audit Chirurgical 2026-09-07) — `economic_event_id` is
    mandatory: a deterministic id naming the real-world event being
    paid out (e.g. `"badge:BADGE-CODE"`, `"certification-pass:<attempt_
    id>"`). A `(user_id, economic_event_id)` unique index
    (infra_indexes.py) makes a retried or duplicated call for the same
    event a safe no-op — it returns the original transaction instead of
    minting a second one, whether the duplicate is caught by this
    function's own pre-check or, under real concurrency, by the
    database rejecting the second insert outright.

    The ledger insert happens before the cached-balance update and is
    itself idempotent — a crash between the two never produces a
    fabricated credit, only a cached balance that undercounts a real
    ledger entry until `reconcile_wallet_balance()` (below) recomputes
    it. That is the actual, honestly-scoped guarantee this module
    makes: not a multi-document ACID transaction (this sandbox has no
    replica-set MongoDB to build or test one against), but an
    idempotent, append-only source of truth plus a real, tested repair
    path for its derived cache.
    """
    existing = await db.wallet_transactions.find_one(
        {"user_id": user_id, "economic_event_id": economic_event_id}, {"_id": 0}
    )
    if existing:
        return WalletTransaction(**existing)

    txn = WalletTransaction(
        user_id=user_id,
        type=transaction_type,
        amount=amount,
        currency=currency,
        ref=ref,
        description=description,
        economic_event_id=economic_event_id,
    )
    try:
        await db.wallet_transactions.insert_one(txn.model_dump())
    except DuplicateKeyError:
        # Lost a race against a concurrent identical credit — the
        # transaction that won is now the source of truth for this
        # event; never mint a second one.
        winner = await db.wallet_transactions.find_one(
            {"user_id": user_id, "economic_event_id": economic_event_id}, {"_id": 0}
        )
        return WalletTransaction(**winner) if winner else txn

    await _get_or_create_account(user_id)  # ensure the account doc exists
    update: dict = {"updated_at": utc_now_iso()}
    inc: dict = {}
    if currency == "jcc":
        inc["jcc_balance"] = amount
    elif currency == "token":
        inc["token_balance"] = amount

    mongo_update: dict = {"$set": update}
    if inc:
        mongo_update["$inc"] = inc
    if badge_code:
        mongo_update["$addToSet"] = {"badges": badge_code}
    await db.wallet_accounts.update_one({"user_id": user_id}, mongo_update)

    return txn


async def reconcile_wallet_balance(user_id: str) -> WalletAccount:
    """WAL-01 — the repair path for the one real gap `credit()`'s
    ledger-then-cache ordering leaves open: a crash between the ledger
    insert and the cached-balance update. The ledger
    (`wallet_transactions`) is this module's own documented source of
    truth ("a wallet's balance is always the sum of its transactions,
    never mutated directly" — models.py); this recomputes
    `jcc_balance`/`token_balance` directly from it and overwrites the
    cache, so a stale/undercounted cache is always fixable, never a
    silent, permanent drift."""
    await _get_or_create_account(user_id)
    totals = {"jcc": 0.0, "token": 0.0}
    async for row in db.wallet_transactions.aggregate(
        [
            {"$match": {"user_id": user_id}},
            {"$group": {"_id": "$currency", "total": {"$sum": "$amount"}}},
        ]
    ):
        if row["_id"] in totals:
            totals[row["_id"]] = row["total"]
    await db.wallet_accounts.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "jcc_balance": totals["jcc"],
                "token_balance": totals["token"],
                "updated_at": utc_now_iso(),
            }
        },
    )
    doc = await db.wallet_accounts.find_one({"user_id": user_id}, {"_id": 0})
    return WalletAccount(**doc)


async def get_summary(user_id: str, limit: int = 50) -> WalletSummary:
    account = await _get_or_create_account(user_id)
    txn_docs = (
        await db.wallet_transactions.find({"user_id": user_id}, {"_id": 0})
        .sort("created_at", -1)
        .to_list(limit)
    )
    return WalletSummary(
        account=account, recent_transactions=[WalletTransaction(**t) for t in txn_docs]
    )


async def list_transactions(user_id: str, limit: int = 200) -> List[WalletTransaction]:
    docs = (
        await db.wallet_transactions.find({"user_id": user_id}, {"_id": 0})
        .sort("created_at", -1)
        .to_list(limit)
    )
    return [WalletTransaction(**d) for d in docs]
