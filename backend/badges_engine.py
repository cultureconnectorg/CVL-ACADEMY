"""Threshold-badge auto-award logic.

Shared by onboarding, quiz submission and mission submission — anywhere a
user's CC balance changes, this checks whether a new badge threshold was
crossed and awards it (idempotently) plus emits the FREK-CERT signal.
"""

from __future__ import annotations

import uuid

from pymongo.errors import DuplicateKeyError

from db import db, utc_now_iso
from services.frek_core import frek_core
from wallet import credit as wallet_credit

BADGE_JCC_REWARD = 10.0


async def award_threshold_badges(user_id: str, cc: int) -> None:
    badges = await db.badges.find({"cc_threshold": {"$lte": cc}}, {"_id": 0}).to_list(
        200
    )
    for b in badges:
        # ECON-03/WAL-01 (Audit Chirurgical 2026-09-07) — a plain
        # find_one-then-insert is a real race: two concurrent calls can
        # both see "not exists" and both insert. The pre-existing
        # unique index on (user_id, badge_code) (infra_indexes.py)
        # already made a genuine double-insert impossible — DB-level —
        # but the un-caught DuplicateKeyError it raised on the losing
        # call surfaced as a request failure instead of the safe no-op
        # this always meant. Attempting the insert directly (skipping
        # the separate find_one entirely) and treating the DB's own
        # uniqueness rejection as "already awarded" makes the
        # award-exactly-once guarantee real without a second,
        # unenforced check.
        try:
            await db.user_badges.insert_one(
                {
                    "id": str(uuid.uuid4()),
                    "user_id": user_id,
                    "badge_code": b["code"],
                    "earned_at": utc_now_iso(),
                }
            )
        except DuplicateKeyError:
            continue

        await frek_core.emit_signal(user_id, "FREK-CERT", {"badge": b["code"]})
        await wallet_credit(
            user_id,
            "badge_earned",
            BADGE_JCC_REWARD,
            economic_event_id=f"badge:{b['code']}",
            currency="jcc",
            ref=b["code"],
            description=f"Badge « {b.get('name', b['code'])} » débloqué",
            badge_code=b["code"],
        )
