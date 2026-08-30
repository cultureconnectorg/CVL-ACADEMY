"""Wallet ledger — credit/debit + balance/history reads."""

from __future__ import annotations

from typing import List, Literal, Optional

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
    currency: Currency = "jcc",
    ref: Optional[str] = None,
    description: str = "",
    badge_code: Optional[str] = None,
) -> WalletTransaction:
    """Records a ledger entry and updates the cached balance. `amount` is
    always positive here — `reward_redeemed` records are logged with a
    negative amount by the caller if it represents a spend."""
    txn = WalletTransaction(
        user_id=user_id,
        type=transaction_type,
        amount=amount,
        currency=currency,
        ref=ref,
        description=description,
    )
    await db.wallet_transactions.insert_one(txn.model_dump())

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
