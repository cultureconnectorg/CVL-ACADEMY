"""Threshold-badge auto-award logic.

Shared by onboarding, quiz submission and mission submission — anywhere a
user's CC balance changes, this checks whether a new badge threshold was
crossed and awards it (idempotently) plus emits the FREK-CERT signal.
"""

from __future__ import annotations

import uuid

from db import db, utc_now_iso
from pymongo.errors import DuplicateKeyError
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
        newly_awarded = False
        if not exists:
            try:
                await db.user_badges.insert_one(
                    {
                        "id": str(uuid.uuid4()),
                        "user_id": user_id,
                        "badge_code": b["code"],
                        "earned_at": utc_now_iso(),
                    }
                )
                newly_awarded = True
            except DuplicateKeyError:
                # A concurrent request awarded the same badge first.
                pass

        if newly_awarded:
            await frek_core.emit_signal(user_id, "FREK-CERT", {"badge": b["code"]})

        # Always retry the Academy mini-wallet effect. Its stable effect key
        # makes this safe and also heals the case where badge insertion
        # succeeded but a previous process crashed before crediting the wallet.
        await wallet_credit(
            user_id,
            "badge_earned",
            BADGE_JCC_REWARD,
            currency="jcc",
            ref=b["code"],
            description=f"Badge « {b.get('name', b['code'])} » débloqué",
            badge_code=b["code"],
            effect_key=f"badge:{b['code']}",
        )
