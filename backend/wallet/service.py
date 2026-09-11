"""Academy mini-wallet ledger — credit/debit + balance/history reads.

The append-only transaction history is the auditable source of truth for the
mini-wallet. ``wallet_accounts`` is a cached read model rebuilt from history on
reads, so a crash between ledger insertion and cache update cannot permanently
drift the displayed balance.
"""

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
    return WalletAccount(**doc)


async def credit(
    user_id: str,
    transaction_type: TransactionType,
    amount: float,
    currency: Currency = "jcc",
    ref: Optional[str] = None,
    description: str = "",
    badge_code: Optional[str] = None,
    effect_key: Optional[str] = None,
) -> WalletTransaction:
    """Record one Academy-side balance movement.

    ``effect_key`` should be stable for retryable business effects. Reusing the
    same key for the same learner returns the original transaction and does not
    apply the balance movement twice.
    """
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
        if not effect_key:
            raise
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
