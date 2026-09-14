"""CVLN Academy mini-wallet models.

This bounded wallet belongs to CVLN Academy only. It tracks Academy-side JCC,
tokens, badges, rewards and history for the learner experience.

It is deliberately separate from:
- ``models.User.cc_credits`` (pedagogical progression credits), and
- the group-level ``CVLN-Wallet`` product / financial core.

Nothing in this module makes the Academy mini-wallet the group ledger, a PSP,
or a production payment rail.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import List, Literal, Optional

from pydantic import BaseModel, Field

TransactionType = Literal[
    "badge_earned", "jcc_earned", "token_earned", "reward_redeemed", "payment"
]


def _uid() -> str:
    return str(uuid.uuid4())


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class WalletTransaction(BaseModel):
    """Append-only Academy mini-wallet history entry — a wallet's balance is
    always the sum of its transactions, never mutated directly.

    ``effect_key`` (WAL-01, Audit Chirurgical 2026-09-07) is the real
    idempotency key: a deterministic string naming the real-world
    Academy-side business effect being paid out (e.g. ``"badge:BADGE-
    CODE"``, ``"certification-pass:<attempt_id>"``). ``wallet.service.
    credit()`` requires every caller to supply one — a compound
    ``(user_id, effect_key)`` partial unique index (``infra_indexes.py``,
    scoped to documents where ``effect_key`` is an actual string, so it
    never collides on legacy rows that predate this field) makes a
    retried or duplicated call for the same event a safe no-op: it
    returns the original transaction instead of minting a second one.
    ``Optional`` only so this model can still deserialize an older,
    pre-this-fix ledger row that has no such key (read-compatibility,
    never a new write path — ``credit()`` itself always sets it).

    ``wallet_accounts`` is only a cached read model, rebuilt from this
    history on every read (see ``service._reconcile_account``); the
    transaction history here is the auditable source used to explain and
    rebuild Academy-side balances.
    """

    id: str = Field(default_factory=_uid)
    user_id: str
    type: TransactionType
    amount: float
    currency: Literal["jcc", "token", "eur"] = "jcc"
    effect_key: Optional[str] = None
    ref: Optional[str] = None  # badge_code / certification_code / mission_code
    description: str = ""
    created_at: str = Field(default_factory=_now)


class WalletAccount(BaseModel):
    user_id: str
    jcc_balance: float = 0.0
    token_balance: float = 0.0
    badges: List[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=_now)
    updated_at: str = Field(default_factory=_now)


class WalletSummary(BaseModel):
    account: WalletAccount
    recent_transactions: List[WalletTransaction]
