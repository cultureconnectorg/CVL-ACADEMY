"""Notifications integration layer.

CVLN Academy never talks to a mail/SMS provider directly from route handlers or
domain services. Every notification crosses this single boundary and every dispatch
keeps an honest tracked outcome: LOCAL_ONLY when no provider exists, otherwise the
real HTTP attempt determines SENT/FAILED.

Token-bearing auth links are redacted in logs/outbox but remain intact in the real
provider request. Generic operational notifications contain no authentication secret
and are persisted exactly as supplied for auditability.

RECONCILE-4 (2026-09-15) — two real remote backends now, not one. `main`'s own
history independently built a concrete, production-ready Resend integration for
the three real auth-link kinds (password_reset/email_verification/invitation),
with actual localized (fr/en) HTML+text email content — never merged into the
NOTIF-01/NOTIF-02 fix this file otherwise carries, so it was rediscovered and
restored here rather than left to bit-rot on `main`. When `RESEND_API_KEY` +
`EMAIL_FROM` are configured, those three kinds render and send a real rendered
email via Resend's real API. `NOTIFICATIONS_PROVIDER_URL` remains the generic,
provider-agnostic fallback (used as-is by `send_operational_event`'s governed,
non-auth-link notifications, and by the three auth-link kinds too when Resend
isn't configured but a generic provider is) — same "decoupled interface, local
fallback" pattern as `frek_core.py`/`agent_factory.py`, just with two concrete
backends instead of one. Neither backend changes NOTIF-01's honest status
machine or NOTIF-02's redaction discipline below.
"""

from __future__ import annotations

import html
import logging
import os
import re
import uuid
from typing import Any, Dict, Literal, Optional, Tuple

import httpx

from db import db, utc_now_iso

logger = logging.getLogger("cvln.notifications")

NOTIFICATIONS_PROVIDER_URL = os.environ.get("NOTIFICATIONS_PROVIDER_URL")
NOTIFICATIONS_API_KEY = os.environ.get("NOTIFICATIONS_API_KEY")
RESEND_API_URL = os.environ.get("RESEND_API_URL", "https://api.resend.com/emails")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
EMAIL_FROM = os.environ.get("EMAIL_FROM")
APP_PUBLIC_URL = os.environ.get("APP_PUBLIC_URL", "http://localhost:3000").rstrip("/")

NotificationStatus = Literal["QUEUED", "SENDING", "SENT", "FAILED", "LOCAL_ONLY"]
_TOKEN_QUERY_RE = re.compile(r"([?&]token=)[^&]+")
_INVITE_PATH_RE = re.compile(r"(/invite/)[^/?#]+")

# The only three kinds Resend's real templates below know how to render —
# everything else (send_operational_event's governed notifications) always
# uses the generic NOTIFICATIONS_PROVIDER_URL passthrough, never Resend.
_RESEND_TEMPLATED_KINDS = {"password_reset", "email_verification", "invitation"}


def _redact_link(link: str) -> str:
    link = _TOKEN_QUERY_RE.sub(r"\1[REDACTED]", link)
    return _INVITE_PATH_RE.sub(r"\1[REDACTED]", link)


def _redact_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    safe = dict(payload)
    if isinstance(safe.get("link"), str):
        safe["link"] = _redact_link(safe["link"])
    return safe


def _resend_subject(kind: str, lang: str) -> str:
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


def _resend_render(kind: str, payload: Dict[str, Any]) -> Tuple[str, str]:
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
            f"Tu as été invité·e à rejoindre {org_name} sur CVLN Academy."
            if org_name
            else "Tu as été invité·e à rejoindre CVLN Academy."
        )
        cta = "Accepter l'invitation"

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


class NotificationService:
    def is_resend_enabled(self) -> bool:
        return bool(RESEND_API_KEY and EMAIL_FROM)

    def is_remote_enabled(self) -> bool:
        return bool(NOTIFICATIONS_PROVIDER_URL) or self.is_resend_enabled()

    async def _send_resend(self, *, kind: str, email: str, payload: Dict[str, Any]) -> str:
        """Real Resend API call with real rendered content. Returns the
        real outcome status — never assumed. Raises on transport/HTTP
        failure so `_dispatch` records a real FAILED, same discipline
        as the generic provider path below."""
        lang = payload.get("lang", "fr")
        html_body, text_body = _resend_render(kind, payload)
        body = {
            "from": EMAIL_FROM,
            "to": [email],
            "subject": _resend_subject(kind, lang),
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
            # Never log the response/request body: it carries the real,
            # credential-bearing link.
            logger.warning(
                "notification[%s] Resend delivery to %s failed: HTTP %s",
                kind,
                email,
                response.status_code,
            )
            raise RuntimeError(f"Resend returned HTTP {response.status_code}")
        return "SENT"

    async def _send_generic_provider(self, *, kind: str, email: str, payload: Dict[str, Any]) -> str:
        headers = (
            {"Authorization": f"Bearer {NOTIFICATIONS_API_KEY}"} if NOTIFICATIONS_API_KEY else {}
        )
        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.post(
                f"{NOTIFICATIONS_PROVIDER_URL}/send",
                json={"kind": kind, "to": email, **payload},
                headers=headers,
            )
        return "SENT" if response.status_code < 400 else "FAILED"

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
            # Real Resend content is only used for the three kinds it
            # actually has templates for; everything else (including a
            # templated kind when Resend isn't configured but a generic
            # provider is) uses the provider-agnostic passthrough.
            if kind in _RESEND_TEMPLATED_KINDS and self.is_resend_enabled():
                status = await self._send_resend(kind=kind, email=email, payload=payload)
            elif NOTIFICATIONS_PROVIDER_URL:
                status = await self._send_generic_provider(kind=kind, email=email, payload=payload)
            else:
                # is_remote_enabled() was True only via Resend, but this
                # kind has no Resend template and no generic provider is
                # configured either -- nothing real to send to.
                status = "FAILED"
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
