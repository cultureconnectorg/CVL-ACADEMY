from __future__ import annotations

import pytest
from fastapi import HTTPException

import services.frek_oidc as frek_oidc_module
from services.frek_oidc import FrekOIDCClient, _pkce_pair


def test_pkce_pair_is_non_empty_and_distinct():
    verifier, challenge = _pkce_pair()
    assert verifier
    assert challenge
    assert verifier != challenge
    assert "=" not in verifier
    assert "=" not in challenge


def test_frek_oidc_not_configured_without_issuer(monkeypatch):
    monkeypatch.setattr(frek_oidc_module, "FREK_CORE_ISSUER_URL", "")
    monkeypatch.setattr(frek_oidc_module, "FREK_CORE_CLIENT_ID", "cvln-academy")
    monkeypatch.setattr(
        frek_oidc_module,
        "FREK_CORE_REDIRECT_URI",
        "https://academy.example/auth/frek/callback",
    )
    assert FrekOIDCClient().is_configured() is False


def test_frek_oidc_configured_with_required_fields(monkeypatch):
    monkeypatch.setattr(frek_oidc_module, "FREK_CORE_ISSUER_URL", "https://id.cvln.test")
    monkeypatch.setattr(frek_oidc_module, "FREK_CORE_CLIENT_ID", "cvln-academy")
    monkeypatch.setattr(
        frek_oidc_module,
        "FREK_CORE_REDIRECT_URI",
        "https://academy.example/auth/frek/callback",
    )
    assert FrekOIDCClient().is_configured() is True


@pytest.mark.asyncio
async def test_discovery_fails_closed_when_unconfigured(monkeypatch):
    monkeypatch.setattr(frek_oidc_module, "FREK_CORE_ISSUER_URL", "")
    monkeypatch.setattr(frek_oidc_module, "FREK_CORE_CLIENT_ID", "")
    monkeypatch.setattr(frek_oidc_module, "FREK_CORE_REDIRECT_URI", "")

    with pytest.raises(HTTPException) as exc:
        await FrekOIDCClient().discovery()

    assert exc.value.status_code == 503
    assert "non configuré" in exc.value.detail
