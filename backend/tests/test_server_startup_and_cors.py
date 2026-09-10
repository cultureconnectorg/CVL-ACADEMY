"""P0-J (Audit Chirurgical 2026-09-07) — OPS-01 (startup fail-closed)
and OPS-02 (production CORS allowlist).

Real gaps this suite closes and proves closed:
  - `on_startup()` used to wrap `ensure_indexes()` — which creates
    every unique/partial index this session's atomicity fixes actually
    depend on — in the same broad `try/except: log-and-continue` as
    the (genuinely non-critical) seed calls. An index that failed to
    create logged an exception and let the app boot anyway, serving
    real traffic with none of those DB-enforced guarantees in place.
  - `CORS_ORIGINS` defaulted straight to `"*"` with `allow_credentials
    =True` and no distinction between a local/preview checkout (fine)
    and a real production deployment (a real security
    misconfiguration) — the app would boot and serve regardless.

`ENVIRONMENT`/`CORS_ORIGINS` are read at module import time, so the
CORS tests reload `server` under monkeypatched env vars via
`importlib.reload` rather than re-invoking a function — that IS the
code path that actually runs at real process boot.
"""

from __future__ import annotations

import importlib

import pytest


@pytest.fixture(autouse=True)
def _restore_server_module():
    """Every test in this file may `importlib.reload(server)` under a
    monkeypatched env — reload it back to the real, unpatched env once
    more afterward so other test files (and pytest-xdist workers
    reusing this process) see the normal dev-mode module."""
    yield
    import server

    importlib.reload(server)


# --------------------------------------------------------------------
# OPS-02 — production CORS allowlist
# --------------------------------------------------------------------


def test_development_default_stays_wildcard(monkeypatch):
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    monkeypatch.delenv("CORS_ORIGINS", raising=False)
    import server

    importlib.reload(server)
    assert server.cors_origins == ["*"]


def test_production_with_wildcard_cors_refuses_to_boot(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("CORS_ORIGINS", "*")
    import server

    with pytest.raises(RuntimeError, match="CORS_ORIGINS"):
        importlib.reload(server)


def test_production_with_unset_cors_refuses_to_boot(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.delenv("CORS_ORIGINS", raising=False)
    import server

    with pytest.raises(RuntimeError, match="CORS_ORIGINS"):
        importlib.reload(server)


def test_production_with_real_allowlist_boots_fine(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv(
        "CORS_ORIGINS", "https://academy.cvln.example,https://admin.cvln.example"
    )
    import server

    importlib.reload(server)
    assert server.cors_origins == [
        "https://academy.cvln.example",
        "https://admin.cvln.example",
    ]


# --------------------------------------------------------------------
# OPS-01 — startup fails closed on an index/invariant failure
# --------------------------------------------------------------------


@pytest.mark.asyncio
async def test_startup_raises_when_ensure_indexes_fails(monkeypatch):
    import server

    monkeypatch.setattr(server, "register_integration_subscribers", lambda: None)

    async def _boom():
        raise RuntimeError("simulated index creation failure")

    monkeypatch.setattr(server, "ensure_indexes", _boom)

    with pytest.raises(RuntimeError, match="simulated index creation failure"):
        await server.on_startup()


@pytest.mark.asyncio
async def test_startup_survives_seed_failures(monkeypatch):
    """Seed data is NOT a correctness/security invariant — a failure
    there must stay logged-and-continue, never fatal, unlike
    ensure_indexes() and the PG-13 manifest above."""
    import server

    monkeypatch.setattr(server, "register_integration_subscribers", lambda: None)

    async def _ok():
        return None

    async def _boom():
        raise RuntimeError("simulated seed failure")

    async def _locked_manifest(*, actor_id):
        assert actor_id == "SYSTEM_STARTUP"
        return {"status": "LOCKED"}

    monkeypatch.setattr(server, "ensure_indexes", _ok)
    monkeypatch.setattr(server.architecture_reuse, "sync_manifest", _locked_manifest)
    monkeypatch.setattr(server, "seed_if_empty", _boom)
    monkeypatch.setattr(server, "seed_default_definitions", _ok)

    async def _matrix():
        return (0, 0)

    monkeypatch.setattr(server, "seed_initial_matrix", _matrix)
    monkeypatch.delenv("MOCK_DB", raising=False)

    # Must NOT raise — the seed failure is caught and logged.
    await server.on_startup()
