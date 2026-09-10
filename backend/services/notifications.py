"""Notifications integration layer.

CVLN Academy never talks to a mail/SMS provider directly from route handlers or
domain services. Every notification crosses this single boundary and every dispatch
keeps an honest tracked outcome: LOCAL_ONLY when no provider exists, otherwise the
real HTTP attempt determines SENT/FAILED.

Token-bearing auth links are redacted in logs/outbox but remain intact in the real
provider request. Generic operational notifications contain no authentication secret
and are persisted exactly as supplied for auditability.
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

NOTIFICATIONS_PROVIDER_URL = os.environ.get("NOTIFICATIONS_PROVIDER_URL")
NOTIFICATIONS_API_KEY = os.environ.get("NOTIFICATIONS_API_KEY")
APP_PUBLIC_URL = os.environ.get("APP_PUBLIC_URL", "http://localhost:3000")

NotificationStatus = Literal["QUEUED", "SENDING", "SENT", "FAILED", "LOCAL_ONLY"]
_TOKEN_QUERY_RE = re.compile(r"([?&]token=)[^&]+")
_INVITE_PATH_RE = re.compile(r"(/invite/)[^/?#]+")


def _redact_link(link: str) -> str:
    link = _TOKEN_QUERY_RE.sub(r"\1[REDACTED]", link)
    return _INVITE_PATH_RE.sub(r"\1[REDACTED]", link)


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
        outbox_id = str(uuid.uuid4())
        safe_payload = _redact_payload(payload)
        logger.info("notification[%s] queued -> %s: %s", kind, email, safe_payload)
        await db.notification_outbox.insert_one(
            {
                "id": outbox_id,
                "kind": kind,
                "to": email,
                "payload": safe_payload,
                "status": "QUEUED",
                "created_at": utc_now_iso(),
                "updated_at": utc_now_iso(),
            }
        )
        if not self.is_remote_enabled():
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
                response = await client.post(
                    f"{NOTIFICATIONS_PROVIDER_URL}/send",
                    json={"kind": kind, "to": email, **payload},
                    headers=headers,
                )
            status = "SENT" if response.status_code < 400 else "FAILED"
        except Exception as exc:
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

    async def send_operational_event(
        self,
        *,
        kind: str,
        email: str,
        subject: str,
        data: Dict[str, Any],
        lang: str = "fr",
    ) -> Dict[str, Any]:
        """Single generic boundary for governed domain notifications."""
        if not kind.strip() or not email.strip() or not subject.strip():
            raise ValueError("kind, email and subject are required")
        return await self._dispatch(
            kind.strip().lower(),
            email.strip(),
            {"subject": subject.strip(), "data": data, "lang": lang},
        )


notifications = NotificationService()
