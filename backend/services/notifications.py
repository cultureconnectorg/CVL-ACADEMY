"""Notifications integration layer.

Same "decoupled interface, local fallback" pattern as frek_core.py and
agent_factory.py: CVLN Academy never talks to a mail/SMS provider directly
from route handlers — everything goes through this one boundary. Until a
real transport is configured (SMTP, SES, Postmark, ...), messages are
logged and archived to `db.notification_outbox` so anything that "would
have sent an email" (password reset, email verification, invitations) is
still inspectable — useful for local dev and for tests.

Public methods:
    send_password_reset(email, token, lang) -> None
    send_email_verification(email, token, lang) -> None
    send_invitation(email, code, org_name, lang) -> None
    is_remote_enabled() -> bool
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, Optional

from db import db, utc_now_iso

logger = logging.getLogger("cvln.notifications")

NOTIFICATIONS_PROVIDER_URL = os.environ.get(
    "NOTIFICATIONS_PROVIDER_URL"
)  # e.g. SES/Postmark base URL
NOTIFICATIONS_API_KEY = os.environ.get("NOTIFICATIONS_API_KEY")

APP_PUBLIC_URL = os.environ.get("APP_PUBLIC_URL", "http://localhost:3000")


class NotificationService:
    def is_remote_enabled(self) -> bool:
        return bool(NOTIFICATIONS_PROVIDER_URL)

    async def _dispatch(self, kind: str, email: str, payload: Dict[str, Any]) -> None:
        """Local fallback: log + archive. Swap for a real provider call once
        NOTIFICATIONS_PROVIDER_URL / NOTIFICATIONS_API_KEY are configured —
        no caller of send_* needs to change."""
        logger.info("notification[%s] -> %s: %s", kind, email, payload)
        await db.notification_outbox.insert_one(
            {
                "kind": kind,
                "to": email,
                "payload": payload,
                "sent_via": "local_log" if not self.is_remote_enabled() else "remote",
                "created_at": utc_now_iso(),
            }
        )

    async def send_password_reset(
        self, email: str, token: str, lang: str = "fr"
    ) -> None:
        link = f"{APP_PUBLIC_URL}/reset-password?token={token}"
        await self._dispatch("password_reset", email, {"link": link, "lang": lang})

    async def send_email_verification(
        self, email: str, token: str, lang: str = "fr"
    ) -> None:
        link = f"{APP_PUBLIC_URL}/verify-email?token={token}"
        await self._dispatch("email_verification", email, {"link": link, "lang": lang})

    async def send_invitation(
        self, email: str, code: str, org_name: Optional[str] = None, lang: str = "fr"
    ) -> None:
        link = f"{APP_PUBLIC_URL}/invite/{code}"
        await self._dispatch(
            "invitation", email, {"link": link, "org_name": org_name, "lang": lang}
        )


notifications = NotificationService()
