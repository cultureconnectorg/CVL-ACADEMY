"""Transactional notification boundary for CVLN Academy.

Production email delivery uses Resend when configured. Every notification is
also archived to ``db.notification_outbox`` with delivery metadata so support
and observability can inspect what happened without logging secret-bearing
links or tokens.

Required production environment variables for email delivery:
    RESEND_API_KEY
    EMAIL_FROM  (example: CVLN Academy <academy@your-domain.tld>)

APP_PUBLIC_URL controls links embedded in transactional messages.
"""

from __future__ import annotations

import html
import logging
import os
from typing import Any, Dict, Optional

import httpx

from db import db, utc_now_iso

logger = logging.getLogger("cvln.notifications")

RESEND_API_URL = os.environ.get("RESEND_API_URL", "https://api.resend.com/emails")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
EMAIL_FROM = os.environ.get("EMAIL_FROM")
APP_PUBLIC_URL = os.environ.get("APP_PUBLIC_URL", "http://localhost:3000").rstrip("/")


class NotificationService:
    def is_remote_enabled(self) -> bool:
        return bool(RESEND_API_KEY and EMAIL_FROM)

    def status(self) -> Dict[str, Any]:
        return {
            "provider": "resend",
            "configured": self.is_remote_enabled(),
            "from_configured": bool(EMAIL_FROM),
            "public_url_configured": APP_PUBLIC_URL != "http://localhost:3000",
        }

    @staticmethod
    def _subject(kind: str, lang: str) -> str:
        subjects = {
            "email_verification": {
                "fr": "Vérifie ton adresse e-mail — CVLN Academy",
                "en": "Verify your email — CVLN Academy",
            },
            "password_reset": {
                "fr": "Réinitialise ton mot de passe — CVLN Academy",
                "en": "Reset your password — CVLN Academy",
            },
            "invitation": {
                "fr": "Invitation CVLN Academy",
                "en": "CVLN Academy invitation",
            },
        }
        return subjects.get(kind, {}).get(lang, subjects.get(kind, {}).get("fr", "CVLN Academy"))

    @staticmethod
    def _render(kind: str, payload: Dict[str, Any]) -> tuple[str, str]:
        link = str(payload.get("link") or "")
        safe_link = html.escape(link, quote=True)
        lang = payload.get("lang", "fr")

        if kind == "email_verification":
            title = "Vérifie ton adresse e-mail" if lang == "fr" else "Verify your email"
            body = (
                "Confirme ton adresse pour sécuriser ton compte CVLN Academy."
                if lang == "fr"
                else "Confirm your address to secure your CVLN Academy account."
            )
            cta = "Vérifier mon e-mail" if lang == "fr" else "Verify my email"
        elif kind == "password_reset":
            title = "Réinitialise ton mot de passe" if lang == "fr" else "Reset your password"
            body = (
                "Utilise ce lien pour choisir un nouveau mot de passe."
                if lang == "fr"
                else "Use this link to choose a new password."
            )
            cta = "Réinitialiser le mot de passe" if lang == "fr" else "Reset password"
        else:
            title = "Invitation CVLN Academy"
            org_name = payload.get("org_name")
            body = (
                f"Tu as été invité à rejoindre {org_name}." if org_name else "Tu as été invité à rejoindre CVLN Academy."
            )
            cta = "Accepter l’invitation"

        html_body = (
            "<div style='font-family:Arial,sans-serif;max-width:600px;margin:auto'>"
            f"<h2>{html.escape(title)}</h2>"
            f"<p>{html.escape(body)}</p>"
            f"<p><a href='{safe_link}' style='display:inline-block;padding:12px 18px;"
            "background:#111;color:#fff;text-decoration:none;border-radius:8px'>"
            f"{html.escape(cta)}</a></p>"
            "<p style='font-size:12px;color:#666'>CVLN Academy</p>"
            "</div>"
        )
        text_body = f"{title}\n\n{body}\n\n{link}\n\nCVLN Academy"
        return html_body, text_body

    async def _send_resend(
        self, *, kind: str, email: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        if not self.is_remote_enabled():
            return {"status": "queued_local", "provider": "outbox"}

        lang = payload.get("lang", "fr")
        html_body, text_body = self._render(kind, payload)
        body = {
            "from": EMAIL_FROM,
            "to": [email],
            "subject": self._subject(kind, lang),
            "html": html_body,
            "text": text_body,
        }
        headers = {
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=12.0) as client:
            response = await client.post(RESEND_API_URL, json=body, headers=headers)

        if response.is_error:
            # Never log the request body: it contains credential-bearing links.
            logger.error(
                "notification[%s] provider failure for %s: status=%s",
                kind,
                email,
                response.status_code,
            )
            raise RuntimeError(f"Email provider returned HTTP {response.status_code}")

        data = response.json()
        return {
            "status": "sent",
            "provider": "resend",
            "provider_message_id": data.get("id"),
        }

    async def _dispatch(self, kind: str, email: str, payload: Dict[str, Any]) -> None:
        now = utc_now_iso()
        record = {
            "kind": kind,
            "to": email,
            "payload": payload,
            "provider": "resend" if self.is_remote_enabled() else "outbox",
            "delivery_status": "pending",
            "created_at": now,
            "updated_at": now,
        }
        inserted = await db.notification_outbox.insert_one(record)

        try:
            result = await self._send_resend(kind=kind, email=email, payload=payload)
        except Exception as exc:  # noqa: BLE001
            await db.notification_outbox.update_one(
                {"_id": inserted.inserted_id},
                {
                    "$set": {
                        "delivery_status": "failed",
                        "provider_error": type(exc).__name__,
                        "updated_at": utc_now_iso(),
                    }
                },
            )
            raise

        await db.notification_outbox.update_one(
            {"_id": inserted.inserted_id},
            {
                "$set": {
                    "delivery_status": result["status"],
                    "provider": result["provider"],
                    "provider_message_id": result.get("provider_message_id"),
                    "updated_at": utc_now_iso(),
                }
            },
        )
        logger.info(
            "notification[%s] %s for %s via %s",
            kind,
            result["status"],
            email,
            result["provider"],
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
