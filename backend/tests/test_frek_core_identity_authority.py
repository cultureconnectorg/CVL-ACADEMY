from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

import services.frek_core as frek_module
from services.frek_core import (
    FrekCoreClient,
    FrekCoreConfigurationError,
    FrekCoreUnavailableError,
)


@pytest.mark.asyncio
async def test_frekcore_authority_requires_remote_url(monkeypatch):
    monkeypatch.setattr(frek_module, "FREK_CORE_IDENTITY_AUTHORITY", "frekcore")
    monkeypatch.setattr(frek_module, "FREK_CORE_BASE_URL", "")

    client = FrekCoreClient()

    with pytest.raises(FrekCoreConfigurationError):
        await client.mint_frek_id()


@pytest.mark.asyncio
async def test_frekcore_authority_never_falls_back_when_remote_fails(monkeypatch):
    monkeypatch.setattr(frek_module, "FREK_CORE_IDENTITY_AUTHORITY", "frekcore")
    monkeypatch.setattr(frek_module, "FREK_CORE_BASE_URL", "https://frekcore.test")

    client = FrekCoreClient()
    remote_post = AsyncMock(return_value=None)
    monkeypatch.setattr(client, "_remote_post", remote_post)

    with pytest.raises(FrekCoreUnavailableError):
        await client.mint_frek_id()

    remote_post.assert_awaited_once_with("/mint", {})


@pytest.mark.asyncio
async def test_frekcore_authority_returns_remote_identity(monkeypatch):
    monkeypatch.setattr(frek_module, "FREK_CORE_IDENTITY_AUTHORITY", "frekcore")
    monkeypatch.setattr(frek_module, "FREK_CORE_BASE_URL", "https://frekcore.test")

    client = FrekCoreClient()
    remote_post = AsyncMock(return_value={"frek_id": "FREK-4242"})
    monkeypatch.setattr(client, "_remote_post", remote_post)

    assert await client.mint_frek_id() == "FREK-4242"


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

    client = FrekCoreClient()
    remote_post = AsyncMock(return_value={"frek_id": "FREK-REMOTE"})
    monkeypatch.setattr(client, "_remote_post", remote_post)

    assert await client.mint_frek_id() == "FREK-042"
    remote_post.assert_not_awaited()


def test_invalid_identity_authority_is_rejected(monkeypatch):
    monkeypatch.setattr(frek_module, "FREK_CORE_IDENTITY_AUTHORITY", "academy")

    with pytest.raises(FrekCoreConfigurationError):
        FrekCoreClient().identity_authority()
