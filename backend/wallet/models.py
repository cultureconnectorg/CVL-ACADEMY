"""CVLN Wallet — a user's JCC/token balance, badges, rewards, history.

Deliberately separate from the CC-credits/stade progression system
(models.User.cc_credits) — CC credits are Academy's own pedagogical
currency; the Wallet is the cross-CVLN-ecosystem ledger (rule 10) that
badges, certifications, and eventually payments feed into.
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
    """Append-only ledger entry — a wallet's balance is always the sum of
    its transactions, never mutated directly.

    `economic_event_id` (WAL-01, Audit Chirurgical 2026-09-07): the real
    idempotency key. `wallet.service.credit()` requires every caller to
    supply one — a deterministic string naming the real-world event
    being paid out (e.g. `"badge:BADGE-CODE"`,
    `"certification-pass:<attempt_id>"`), unique per user via a compound
    `(user_id, economic_event_id)` index. A retried or duplicated call
    for the same event returns the original transaction instead of
    minting a second one — the actual guarantee that closes the
    "ledger != balance from a crash mid-credit, or the same event
    credited twice" risk the audit named. `Optional` only so this model
    can still deserialize an older, pre-this-fix ledger row that has no
    such key (read-compatibility, never a new write path)."""

    id: str = Field(default_factory=_uid)
    user_id: str
    type: TransactionType
    amount: float
    currency: Literal["jcc", "token", "eur"] = "jcc"
    ref: Optional[str] = None  # badge_code / certification_code / mission_code
    description: str = ""
    economic_event_id: Optional[str] = None
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
