"""Threshold-badge auto-award logic.

Shared by onboarding, quiz submission and mission submission — anywhere a
user's CC balance changes, this checks whether a new badge threshold was
crossed and awards it (idempotently) plus emits the FREK-CERT signal.
"""

from __future__ import annotations

import uuid

from db import db, utc_now_iso
from services.frek_core import frek_core
from wallet import credit as wallet_credit

BADGE_JCC_REWARD = 10.0


async def award_threshold_badges(user_id: str, cc: int) -> None:
    badges = await db.badges.find({"cc_threshold": {"$lte": cc}}, {"_id": 0}).to_list(
        200
    )
    for b in badges:
        exists = await db.user_badges.find_one(
            {"user_id": user_id, "badge_code": b["code"]}
        )
        if not exists:
            await db.user_badges.insert_one(
                {
                    "id": str(uuid.uuid4()),
                    "user_id": user_id,
                    "badge_code": b["code"],
                    "earned_at": utc_now_iso(),
                }
            )
            await frek_core.emit_signal(user_id, "FREK-CERT", {"badge": b["code"]})
            await wallet_credit(
                user_id,
                "badge_earned",
                BADGE_JCC_REWARD,
                currency="jcc",
                ref=b["code"],
                description=f"Badge « {b.get('name', b['code'])} » débloqué",
                badge_code=b["code"],
            )
