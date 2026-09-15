"""NOTIF-01/NOTIF-02 (Audit Chirurgical 2026-09-07) — real notification
delivery status and no raw-token leakage.

Real gaps this suite closes and proves closed:
  - `is_remote_enabled()` could be True (a provider URL configured)
    while `_dispatch()` never made any network call at all — `sent_via`
    could read "remote" with nothing ever actually sent.
  - The raw token embedded in a password-reset / email-verification /
    invitation link was archived in `db.notification_outbox` and
    written to the application log in cleartext.

DB-backed pieces run against `mongomock_motor.AsyncMongoMockClient` —
same convention as every other suite in this repo. The real HTTP
attempt (when a provider is configured) is exercised against
`httpx.MockTransport` — a real `httpx.AsyncClient` request/response
cycle, not a call recorded and merely trusted.
"""

from __future__ import annotations

import json

import httpx
import pytest
from mongomock_motor import AsyncMongoMockClient

import services.notifications as notifications_module
from services.notifications import NotificationService


@pytest.fixture
async def notif_db(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_notifications_test"]
    monkeypatch.setattr(notifications_module, "db", mock_db)
    return mock_db


def _mock_transport(status_code: int = 200, capture: list | None = None):
    def handler(request: httpx.Request) -> httpx.Response:
        if capture is not None:
            capture.append(json.loads(request.content))
        return httpx.Response(status_code, json={"ok": status_code < 400})

    return httpx.MockTransport(handler)


class _MockAsyncClient(httpx.AsyncClient):
    """Same shape as the real `httpx.AsyncClient(timeout=8.0)` call the
    implementation makes — only the transport is swapped, so this is a
    real request/response round trip, not a bypassed call."""

    _transport_factory = None

    def __init__(self, *args, **kwargs):
        kwargs["transport"] = self._transport_factory()
        super().__init__(*args, **kwargs)


def _install_mock_transport(monkeypatch, status_code=200, capture=None):
    cls = type(
        "_InstalledMockAsyncClient",
        (_MockAsyncClient,),
        {"_transport_factory": staticmethod(lambda: _mock_transport(status_code, capture))},
    )
    monkeypatch.setattr(notifications_module.httpx, "AsyncClient", cls)


# --------------------------------------------------------------------
# NOTIF-01 — no provider configured -> honest LOCAL_ONLY, never "sent"
# --------------------------------------------------------------------


@pytest.mark.asyncio
async def test_no_provider_configured_is_local_only_never_sent(notif_db, monkeypatch):
    monkeypatch.setattr(notifications_module, "NOTIFICATIONS_PROVIDER_URL", None)
    svc = NotificationService()
    assert svc.is_remote_enabled() is False

    result = await svc.send_password_reset("user@example.com", "raw-token-abc123")
    assert result["status"] == "LOCAL_ONLY"

    stored = await notif_db.notification_outbox.find_one({"id": result["id"]}, {"_id": 0})
    assert stored["status"] == "LOCAL_ONLY"


# --------------------------------------------------------------------
# NOTIF-01 — provider configured -> a real request happens, real status
# --------------------------------------------------------------------


@pytest.mark.asyncio
async def test_provider_configured_and_healthy_reaches_sent(notif_db, monkeypatch):
    monkeypatch.setattr(
        notifications_module, "NOTIFICATIONS_PROVIDER_URL", "https://fake-provider.test"
    )
    captured = []
    _install_mock_transport(monkeypatch, status_code=200, capture=captured)

    svc = NotificationService()
    assert svc.is_remote_enabled() is True

    result = await svc.send_password_reset("user@example.com", "raw-token-abc123")
    assert result["status"] == "SENT"

    # A real request really happened, carrying the real (unredacted)
    # token — that's the actual email link recipients need.
    assert len(captured) == 1
    assert "raw-token-abc123" in captured[0]["link"]

    stored = await notif_db.notification_outbox.find_one({"id": result["id"]}, {"_id": 0})
    assert stored["status"] == "SENT"


@pytest.mark.asyncio
async def test_provider_configured_but_errors_reaches_failed(notif_db, monkeypatch):
    monkeypatch.setattr(
        notifications_module, "NOTIFICATIONS_PROVIDER_URL", "https://fake-provider.test"
    )
    _install_mock_transport(monkeypatch, status_code=500)

    svc = NotificationService()
    result = await svc.send_password_reset("user@example.com", "raw-token-xyz")
    assert result["status"] == "FAILED"

    stored = await notif_db.notification_outbox.find_one({"id": result["id"]}, {"_id": 0})
    assert stored["status"] == "FAILED"


@pytest.mark.asyncio
async def test_provider_configured_but_network_raises_reaches_failed_not_crash(
    notif_db, monkeypatch
):
    monkeypatch.setattr(
        notifications_module, "NOTIFICATIONS_PROVIDER_URL", "https://fake-provider.test"
    )

    def raising_handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectTimeout("simulated network failure")

    cls = type(
        "_RaisingMockAsyncClient",
        (_MockAsyncClient,),
        {"_transport_factory": staticmethod(lambda: httpx.MockTransport(raising_handler))},
    )
    monkeypatch.setattr(notifications_module.httpx, "AsyncClient", cls)

    svc = NotificationService()
    # Must not raise — a provider outage is a real, handled FAILED
    # status, never an unhandled exception surfacing to the caller
    # (e.g. crashing a registration request).
    result = await svc.send_password_reset("user@example.com", "raw-token-neterr")
    assert result["status"] == "FAILED"


# --------------------------------------------------------------------
# NOTIF-02 — raw token never persisted or logged
# --------------------------------------------------------------------


@pytest.mark.asyncio
async def test_raw_token_never_stored_in_outbox_password_reset(notif_db, monkeypatch):
    monkeypatch.setattr(notifications_module, "NOTIFICATIONS_PROVIDER_URL", None)
    svc = NotificationService()
    result = await svc.send_password_reset("user@example.com", "SUPER-SECRET-RESET-TOKEN")

    stored = await notif_db.notification_outbox.find_one({"id": result["id"]}, {"_id": 0})
    assert "SUPER-SECRET-RESET-TOKEN" not in json.dumps(stored)
    assert "[REDACTED]" in stored["payload"]["link"]


@pytest.mark.asyncio
async def test_raw_token_never_stored_in_outbox_email_verification(notif_db, monkeypatch):
    monkeypatch.setattr(notifications_module, "NOTIFICATIONS_PROVIDER_URL", None)
    svc = NotificationService()
    result = await svc.send_email_verification("user@example.com", "SUPER-SECRET-VERIFY-TOKEN")

    stored = await notif_db.notification_outbox.find_one({"id": result["id"]}, {"_id": 0})
    assert "SUPER-SECRET-VERIFY-TOKEN" not in json.dumps(stored)


@pytest.mark.asyncio
async def test_raw_invite_code_never_stored_in_outbox(notif_db, monkeypatch):
    monkeypatch.setattr(notifications_module, "NOTIFICATIONS_PROVIDER_URL", None)
    svc = NotificationService()
    result = await svc.send_invitation(
        "user@example.com", "SECRET-INVITE-CODE-123", org_name="CVLN Test Org"
    )

    stored = await notif_db.notification_outbox.find_one({"id": result["id"]}, {"_id": 0})
    assert "SECRET-INVITE-CODE-123" not in json.dumps(stored)
    assert "[REDACTED]" in stored["payload"]["link"]
    # Non-sensitive context (org name) is still preserved.
    assert stored["payload"]["org_name"] == "CVLN Test Org"


@pytest.mark.asyncio
async def test_raw_token_never_logged(notif_db, monkeypatch, caplog):
    import logging

    monkeypatch.setattr(notifications_module, "NOTIFICATIONS_PROVIDER_URL", None)
    svc = NotificationService()
    with caplog.at_level(logging.INFO, logger="cvln.notifications"):
        await svc.send_password_reset("user@example.com", "LOGGED-SECRET-TOKEN")

    assert "LOGGED-SECRET-TOKEN" not in caplog.text


# --------------------------------------------------------------------
# RECONCILE-4 — real Resend backend (recovered from `main`, real
# rendered content, same NOTIF-01/NOTIF-02 discipline as the generic
# provider path above)
# --------------------------------------------------------------------


@pytest.mark.asyncio
async def test_resend_not_configured_is_local_only(notif_db, monkeypatch):
    monkeypatch.setattr(notifications_module, "NOTIFICATIONS_PROVIDER_URL", None)
    monkeypatch.setattr(notifications_module, "RESEND_API_KEY", None)
    monkeypatch.setattr(notifications_module, "EMAIL_FROM", None)
    svc = NotificationService()
    assert svc.is_resend_enabled() is False
    assert svc.is_remote_enabled() is False

    result = await svc.send_password_reset("user@example.com", "raw-token-abc123")
    assert result["status"] == "LOCAL_ONLY"


@pytest.mark.asyncio
async def test_resend_configured_sends_real_rendered_content(notif_db, monkeypatch):
    monkeypatch.setattr(notifications_module, "NOTIFICATIONS_PROVIDER_URL", None)
    monkeypatch.setattr(notifications_module, "RESEND_API_KEY", "re_fake_key")
    monkeypatch.setattr(notifications_module, "EMAIL_FROM", "CVLN Academy <academy@cvln.test>")
    captured = []
    _install_mock_transport(monkeypatch, status_code=200, capture=captured)

    svc = NotificationService()
    assert svc.is_resend_enabled() is True
    assert svc.is_remote_enabled() is True

    result = await svc.send_password_reset("user@example.com", "raw-token-abc123", lang="fr")
    assert result["status"] == "SENT"

    # A real Resend request really happened, with real rendered content
    # (subject/html/text), carrying the real (unredacted) token -- the
    # actual link recipients need to click.
    assert len(captured) == 1
    body = captured[0]
    assert body["from"] == "CVLN Academy <academy@cvln.test>"
    assert body["to"] == ["user@example.com"]
    assert "Réinitialise ton mot de passe" in body["subject"]
    assert "raw-token-abc123" in body["html"]
    assert "raw-token-abc123" in body["text"]

    # NOTIF-02 discipline still holds: the outbox never gets the raw token.
    stored = await notif_db.notification_outbox.find_one({"id": result["id"]}, {"_id": 0})
    assert "raw-token-abc123" not in json.dumps(stored)
    assert stored["status"] == "SENT"


@pytest.mark.asyncio
async def test_resend_configured_but_errors_reaches_failed(notif_db, monkeypatch):
    monkeypatch.setattr(notifications_module, "NOTIFICATIONS_PROVIDER_URL", None)
    monkeypatch.setattr(notifications_module, "RESEND_API_KEY", "re_fake_key")
    monkeypatch.setattr(notifications_module, "EMAIL_FROM", "academy@cvln.test")
    _install_mock_transport(monkeypatch, status_code=500)

    svc = NotificationService()
    result = await svc.send_email_verification("user@example.com", "raw-token-xyz")
    assert result["status"] == "FAILED"

    stored = await notif_db.notification_outbox.find_one({"id": result["id"]}, {"_id": 0})
    assert stored["status"] == "FAILED"


@pytest.mark.asyncio
async def test_resend_preferred_over_generic_provider_for_templated_kinds(notif_db, monkeypatch):
    """When both backends are configured, the three real-templated auth-
    link kinds go through Resend (real content), not the generic
    passthrough (which has no template and would send raw JSON)."""
    monkeypatch.setattr(notifications_module, "NOTIFICATIONS_PROVIDER_URL", "https://fake-provider.test")
    monkeypatch.setattr(notifications_module, "RESEND_API_KEY", "re_fake_key")
    monkeypatch.setattr(notifications_module, "EMAIL_FROM", "academy@cvln.test")
    captured = []
    _install_mock_transport(monkeypatch, status_code=200, capture=captured)

    svc = NotificationService()
    result = await svc.send_invitation("user@example.com", "SECRET-CODE", org_name="CVLN Test Org")
    assert result["status"] == "SENT"
    assert len(captured) == 1
    # Resend's real request shape (from/to/subject/html/text), not the
    # generic provider's raw {"kind":..., "to":..., **payload}.
    assert "from" in captured[0] and "html" in captured[0]
    assert "CVLN Test Org" in captured[0]["html"]


@pytest.mark.asyncio
async def test_operational_event_never_uses_resend_even_when_configured(notif_db, monkeypatch):
    """send_operational_event's governed, non-auth-link notifications
    have no Resend template -- they always use the generic provider,
    even when Resend is configured for the three auth-link kinds."""
    monkeypatch.setattr(notifications_module, "NOTIFICATIONS_PROVIDER_URL", "https://fake-provider.test")
    monkeypatch.setattr(notifications_module, "RESEND_API_KEY", "re_fake_key")
    monkeypatch.setattr(notifications_module, "EMAIL_FROM", "academy@cvln.test")
    captured = []
    _install_mock_transport(monkeypatch, status_code=200, capture=captured)

    svc = NotificationService()
    result = await svc.send_operational_event(
        kind="legal_deadline",
        email="owner@example.com",
        subject="Test deadline",
        data={"deadline_id": "d1"},
    )
    assert result["status"] == "SENT"
    assert len(captured) == 1
    # Generic provider's real request shape, not Resend's.
    assert captured[0]["kind"] == "legal_deadline"
    assert "from" not in captured[0]
