from __future__ import annotations

import pytest

import services.frek_core as frek_module
from services.frek_core import (
    FrekCoreClient,
    FrekCoreConfigurationError,
    FrekCoreUnavailableError,
)


def _configure_remote(monkeypatch):
    monkeypatch.setattr(frek_module, "FREK_CORE_IDENTITY_AUTHORITY", "frekcore")
    monkeypatch.setattr(frek_module, "FREK_CORE_BASE_URL", "https://frekcore.test")
    monkeypatch.setattr(frek_module, "FREK_CORE_CLIENT_ID", "cvln-academy")
    monkeypatch.setattr(frek_module, "FREK_CORE_CLIENT_SECRET", "test-secret")


@pytest.mark.asyncio
async def test_frekcore_authority_requires_client_configuration(monkeypatch):
    monkeypatch.setattr(frek_module, "FREK_CORE_IDENTITY_AUTHORITY", "frekcore")
    monkeypatch.setattr(frek_module, "FREK_CORE_BASE_URL", "")
    monkeypatch.setattr(frek_module, "FREK_CORE_CLIENT_ID", "")
    monkeypatch.setattr(frek_module, "FREK_CORE_CLIENT_SECRET", "")

    with pytest.raises(FrekCoreConfigurationError):
        await FrekCoreClient().mint_frek_id("maya@example.test")


@pytest.mark.asyncio
async def test_frekcore_authority_requires_email(monkeypatch):
    _configure_remote(monkeypatch)

    with pytest.raises(FrekCoreConfigurationError):
        await FrekCoreClient().mint_frek_id()


@pytest.mark.asyncio
async def test_frekcore_uses_existing_v1_token_and_identity_emit_contract(monkeypatch):
    _configure_remote(monkeypatch)
    calls = []

    class FakeResponse:
        def __init__(self, body):
            self.body = body

        def raise_for_status(self):
            return None

        def json(self):
            return self.body

    class FakeHttpClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return None

        async def post(self, url, json=None, headers=None):
            calls.append((url, json, headers))
            if url.endswith("/api/v1/auth/token"):
                return FakeResponse({"access_token": "client-token"})
            if url.endswith("/api/v1/identity/emit"):
                return FakeResponse(
                    {"frek_id": "FREK-4242", "created": True, "stage": "GENESIS"}
                )
            raise AssertionError(f"Unexpected URL: {url}")

    monkeypatch.setattr(frek_module.httpx, "AsyncClient", FakeHttpClient)

    result = await FrekCoreClient().mint_frek_id(
        "Maya@Example.Test", metadata={"application": "cvln_academy"}
    )

    assert result == "FREK-4242"
    assert calls[0] == (
        "https://frekcore.test/api/v1/auth/token",
        {
            "client_id": "cvln-academy",
            "client_secret": "test-secret",
            "grant_type": "client_credentials",
        },
        None,
    )
    assert calls[1][0] == "https://frekcore.test/api/v1/identity/emit"
    assert calls[1][1]["email"] == "maya@example.test"
    assert calls[1][1]["source"] == "cvln_academy"
    assert calls[1][2] == {"Authorization": "Bearer client-token"}


@pytest.mark.asyncio
async def test_frekcore_authority_never_falls_back_when_remote_fails(monkeypatch):
    _configure_remote(monkeypatch)

    class FailingHttpClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return None

        async def post(self, *args, **kwargs):
            request = frek_module.httpx.Request(
                "POST", "https://frekcore.test/api/v1/auth/token"
            )
            raise frek_module.httpx.ConnectError("offline", request=request)

    monkeypatch.setattr(frek_module.httpx, "AsyncClient", FailingHttpClient)

    with pytest.raises(FrekCoreUnavailableError):
        await FrekCoreClient().mint_frek_id("maya@example.test")


@pytest.mark.asyncio
async def test_local_dev_authority_mints_only_from_local_counter(monkeypatch):
    monkeypatch.setattr(frek_module, "FREK_CORE_IDENTITY_AUTHORITY", "local_dev")
    monkeypatch.setattr(frek_module, "FREK_CORE_BASE_URL", "https://ignored.test")

    class FakeCounters:
        async def find_one_and_update(self, *args, **kwargs):
            return {"seq": 42}

    class FakeDb:
        counters = FakeCounters()

    monkeypatch.setattr(frek_module, "db", FakeDb())

    assert await FrekCoreClient().mint_frek_id("maya@example.test") == "FREK-042"


def test_invalid_identity_authority_is_rejected(monkeypatch):
    monkeypatch.setattr(frek_module, "FREK_CORE_IDENTITY_AUTHORITY", "academy")

    with pytest.raises(FrekCoreConfigurationError):
        FrekCoreClient().identity_authority()
