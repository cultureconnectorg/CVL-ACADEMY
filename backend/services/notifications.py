"""Notifications integration layer.

Same "decoupled interface, local fallback" pattern as frek_core.py and
agent_factory.py: CVLN Academy never talks to a mail/SMS provider directly
from route handlers — everything goes through this one boundary.

NOTIF-01/NOTIF-02 (Audit Chirurgical 2026-09-07) — two real gaps this
version closes:

  - "Provider configured" is no longer conflated with "message sent".
    Every dispatch gets a real, tracked `status`: `QUEUED` -> (if a
    remote provider is configured) `SENDING` -> `SENT`/`FAILED` from an
    actual network attempt's real outcome, or (if none is configured)
    `LOCAL_ONLY` — the honest, `BLOCKED_BY_ENVIRONMENT` state for this
    sandbox today: no `NOTIFICATIONS_PROVIDER_URL`/`NOTIFICATIONS_API_KEY`
    secret exists here, so nothing claiming "remote" would be true.
    Wiring a real provider only ever needs `NOTIFICATIONS_PROVIDER_URL`
    set — no caller of `send_*` changes.
  - The raw token embedded in a password-reset / email-verification /
    invitation link is never logged or archived in cleartext anymore.
    The real link (with its real, working token) still goes out in the
    actual outbound request to a real provider when one is configured —
    only this module's own local log line and `db.notification_outbox`
    record get the redacted form.

Public methods:
    send_password_reset(email, token, lang) -> dict (status)
    send_email_verification(email, token, lang) -> dict (status)
    send_invitation(email, code, org_name, lang) -> dict (status)
    is_remote_enabled() -> bool
"""

from __future__ import annotations

import logging
import os
import re
import uuid
from typing import Any, Dict, Literal, Optional

import httpx

from db import db, utc_now_iso

logger = logging.getLogger("cvln.notifications")

NOTIFICATIONS_PROVIDER_URL = os.environ.get(
    "NOTIFICATIONS_PROVIDER_URL"
)  # e.g. SES/Postmark base URL
NOTIFICATIONS_API_KEY = os.environ.get("NOTIFICATIONS_API_KEY")

APP_PUBLIC_URL = os.environ.get("APP_PUBLIC_URL", "http://localhost:3000")

NotificationStatus = Literal["QUEUED", "SENDING", "SENT", "FAILED", "LOCAL_ONLY"]

# NOTIF-02 — matches the two real token-bearing shapes `send_*` below
# builds (`?token=...` for reset/verify, `/invite/<code>` for
# invitations). Redaction is applied only to what this module persists
# or logs locally — never to what's actually posted to a real provider.
_TOKEN_QUERY_RE = re.compile(r"([?&]token=)[^&]+")
_INVITE_PATH_RE = re.compile(r"(/invite/)[^/?#]+")


def _redact_link(link: str) -> str:
    link = _TOKEN_QUERY_RE.sub(r"\1[REDACTED]", link)
    link = _INVITE_PATH_RE.sub(r"\1[REDACTED]", link)
    return link


def _redact_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    safe = dict(payload)
    if isinstance(safe.get("link"), str):
        safe["link"] = _redact_link(safe["link"])
    return safe


class NotificationService:
    def is_remote_enabled(self) -> bool:
        return bool(NOTIFICATIONS_PROVIDER_URL)

    async def _dispatch(
        self, kind: str, email: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Real state machine: QUEUED always first; then either
        LOCAL_ONLY (no provider configured — nothing left this
        process) or SENDING -> SENT/FAILED from a real HTTP attempt.
        Returns `{"id": ..., "status": ...}` — the final, real outcome,
        never assumed."""
        outbox_id = str(uuid.uuid4())
        safe_payload = _redact_payload(payload)
        logger.info("notification[%s] queued -> %s: %s", kind, email, safe_payload)

        await db.notification_outbox.insert_one(
            {
                "id": outbox_id,
                "kind": kind,
                "to": email,
                "payload": safe_payload,  # NOTIF-02: redacted, never the raw token
                "status": "QUEUED",
                "created_at": utc_now_iso(),
                "updated_at": utc_now_iso(),
            }
        )

        if not self.is_remote_enabled():
            # BLOCKED_BY_ENVIRONMENT: real, honest state — no secret
            # configured, so nothing was or could have been sent.
            await db.notification_outbox.update_one(
                {"id": outbox_id},
                {"$set": {"status": "LOCAL_ONLY", "updated_at": utc_now_iso()}},
            )
            return {"id": outbox_id, "status": "LOCAL_ONLY"}

        await db.notification_outbox.update_one(
            {"id": outbox_id},
            {"$set": {"status": "SENDING", "updated_at": utc_now_iso()}},
        )
        status: NotificationStatus
        try:
            headers = (
                {"Authorization": f"Bearer {NOTIFICATIONS_API_KEY}"}
                if NOTIFICATIONS_API_KEY
                else {}
            )
            async with httpx.AsyncClient(timeout=8.0) as client:
                # The real, unredacted payload (with its real, working
                # token) goes to the real provider — only what this
                # module persists/logs locally is ever redacted.
                response = await client.post(
                    f"{NOTIFICATIONS_PROVIDER_URL}/send",
                    json={"kind": kind, "to": email, **payload},
                    headers=headers,
                )
            status = "SENT" if response.status_code < 400 else "FAILED"
        except Exception as exc:  # network error, timeout, DNS, ...
            status = "FAILED"
            logger.warning("notification[%s] delivery to provider failed: %s", kind, exc)

        await db.notification_outbox.update_one(
            {"id": outbox_id},
            {"$set": {"status": status, "updated_at": utc_now_iso()}},
        )
        return {"id": outbox_id, "status": status}

    async def send_password_reset(
        self, email: str, token: str, lang: str = "fr"
    ) -> Dict[str, Any]:
        link = f"{APP_PUBLIC_URL}/reset-password?token={token}"
        return await self._dispatch("password_reset", email, {"link": link, "lang": lang})

    async def send_email_verification(
        self, email: str, token: str, lang: str = "fr"
    ) -> Dict[str, Any]:
        link = f"{APP_PUBLIC_URL}/verify-email?token={token}"
        return await self._dispatch(
            "email_verification", email, {"link": link, "lang": lang}
        )

    async def send_invitation(
        self, email: str, code: str, org_name: Optional[str] = None, lang: str = "fr"
    ) -> Dict[str, Any]:
        link = f"{APP_PUBLIC_URL}/invite/{code}"
        return await self._dispatch(
            "invitation", email, {"link": link, "org_name": org_name, "lang": lang}
        )


notifications = NotificationService()
