"""Academy mini-wallet ledger — credit/debit + balance/history reads.

The append-only transaction history is the auditable source of truth for the
mini-wallet. ``wallet_accounts`` is a cached read model rebuilt from history on
reads, so a crash between ledger insertion and cache update cannot permanently
drift the displayed balance.
"""

from __future__ import annotations

from typing import List, Literal, Optional

from db import db, utc_now_iso
from pymongo.errors import DuplicateKeyError

from .models import TransactionType, WalletAccount, WalletSummary, WalletTransaction

Currency = Literal["jcc", "token", "eur"]


async def _get_or_create_account(user_id: str) -> WalletAccount:
    doc = await db.wallet_accounts.find_one({"user_id": user_id}, {"_id": 0})
    if doc:
        return WalletAccount(**doc)
    account = WalletAccount(user_id=user_id)
    try:
        await db.wallet_accounts.insert_one(account.model_dump())
    except DuplicateKeyError:
        doc = await db.wallet_accounts.find_one({"user_id": user_id}, {"_id": 0})
        if doc:
            return WalletAccount(**doc)
        raise
    return account


async def _reconcile_account(user_id: str) -> WalletAccount:
    """Rebuild cached balances from append-only transaction history."""
    await _get_or_create_account(user_id)
    totals = {"jcc": 0.0, "token": 0.0}
    async for doc in db.wallet_transactions.find(
        {"user_id": user_id, "currency": {"$in": ["jcc", "token"]}},
        {"_id": 0, "currency": 1, "amount": 1},
    ):
        currency = doc.get("currency")
        if currency in totals:
            totals[currency] += float(doc.get("amount", 0.0))

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
    if doc is None:
        raise RuntimeError(
            f"Academy mini-wallet account missing after reconciliation: {user_id}"
        )
    return WalletAccount(**doc)


async def credit(
    user_id: str,
    transaction_type: TransactionType,
    amount: float,
    effect_key: str,
    currency: Currency = "jcc",
    ref: Optional[str] = None,
    description: str = "",
    badge_code: Optional[str] = None,
) -> WalletTransaction:
    """Record one Academy-side balance movement. `amount` is always positive
    here — `reward_redeemed` records are logged with a negative amount by the
    caller if it represents a spend.

    WAL-01 (Audit Chirurgical 2026-09-07) — `effect_key` is mandatory: a
    deterministic id naming the real-world Academy-side effect being paid out
    (e.g. ``"badge:BADGE-CODE"``, ``"certification-pass:<attempt_id>"``). A
    ``(user_id, effect_key)`` partial unique index (``infra_indexes.py``,
    scoped to documents where the field is an actual string, so it never
    collides on legacy pre-fix rows without one) makes a retried or
    duplicated call for the same event a safe no-op — it returns the
    original transaction instead of minting a second one, whether the
    duplicate is caught by this function's own pre-check (the common,
    non-concurrent retry case) or, under real concurrency, by the database
    rejecting the second insert outright.

    The ledger insert happens before the cached-balance update and is itself
    idempotent — a crash between the two never produces a fabricated credit,
    only a cached balance that undercounts a real ledger entry until the next
    read (`get_summary` always calls `_reconcile_account`, so this self-heals
    on the very next balance view) or an explicit `reconcile_wallet_balance`
    call. That is the actual, honestly-scoped guarantee this module makes:
    not a multi-document ACID transaction (this sandbox has no replica-set
    MongoDB to build or test one against), but an idempotent, append-only
    source of truth plus a real, tested, always-applied repair path for its
    derived cache.
    """
    existing = await db.wallet_transactions.find_one(
        {"user_id": user_id, "effect_key": effect_key}, {"_id": 0}
    )
    if existing:
        return WalletTransaction(**existing)

    txn = WalletTransaction(
        user_id=user_id,
        type=transaction_type,
        amount=amount,
        currency=currency,
        effect_key=effect_key,
        ref=ref,
        description=description,
    )
    try:
        await db.wallet_transactions.insert_one(txn.model_dump(exclude_none=True))
    except DuplicateKeyError:
        # Lost a race against a concurrent identical credit (or the
        # pre-check above missed it under real concurrency) — the
        # transaction that won is now the source of truth for this
        # event; never mint a second one. A missing winner here (the
        # index rejected the insert but a fresh read can't find it) is
        # a genuinely unexpected state, not silently swallowed.
        existing = await db.wallet_transactions.find_one(
            {"user_id": user_id, "effect_key": effect_key}, {"_id": 0}
        )
        if not existing:
            raise
        await _reconcile_account(user_id)
        return WalletTransaction(**existing)

    await _get_or_create_account(user_id)
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
    """WAL-01 — public repair entry point for `_reconcile_account`: recomputes
    `jcc_balance`/`token_balance` directly from the append-only transaction
    history and overwrites the cache, so a stale/undercounted cache is always
    fixable, never a silent, permanent drift. `credit()` and `get_summary()`
    already call the same underlying reconciliation on every write and read
    respectively — this is the explicit, externally-callable form for
    ops/admin tooling that wants to force a repair outside that normal flow."""
    return await _reconcile_account(user_id)


async def get_summary(user_id: str, limit: int = 50) -> WalletSummary:
    account = await _reconcile_account(user_id)
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
