"""P0-J (Audit Chirurgical 2026-09-07) — OPS-01 (startup fail-closed)
and OPS-02 (production CORS allowlist).

RECONCILE-3 Phase 1 — real gap found and closed: r35l31's original
`on_startup()` ran `ensure_indexes()` and `architecture_reuse.
sync_manifest()` outside any try/except (a raise there is a fatal ASGI
`lifespan.startup.failed` — the app never accepts a connection). When
this file's CORS section was reconciled onto the modern `lifespan()`/
readiness-gate structure (main's own contribution — `app.state.
startup_ready`/`startup_error` exposed via `/health` for orchestrator
probes), that fail-closed half of the historical contract was not
restored: `ensure_indexes()` ended up inside the same broad
`except Exception: log-and-continue` as the genuinely non-critical
seed calls, and `architecture_reuse.sync_manifest()` was dropped from
startup entirely (it still exists, tested, reachable only via the
admin-triggered `POST /production-gates/architecture/sync`).
`server.py`'s `lifespan()` now runs both, again, outside that
try/except — this suite proves it.

`ENVIRONMENT`/`CORS_ORIGINS` are read at module import time, so the
CORS tests reload `server` under monkeypatched env vars via
`importlib.reload` rather than re-invoking a function — that IS the
code path that actually runs at real process boot. The private
module-level name is `_cors_origins` (leading underscore, intentional
— see server.py's own reconciliation comment on that line).

Startup/shutdown tests drive the real `lifespan()` async context
manager via FastAPI's `TestClient` (which only runs ASGI lifespan
inside a `with TestClient(app) as client:` block — a bare `client.get()`
does not, which is how the pre-fix gap went unnoticed by every other
test in this file's original form). The slow, non-critical seed steps
(`seed_if_empty`/`seed_default_definitions`/`seed_initial_matrix`/
`ensure_workbook_runtimes`) are monkeypatched to no-ops so this suite
stays fast; `ensure_indexes()` and `architecture_reuse.sync_manifest()`
— the two invariants under test — run for real against a fresh
`mongomock_motor` database per test, proving they actually execute
end-to-end, not just that they were called. `infra_indexes.py` and
`services/architecture_reuse.py` each did their own `from db import
db`, so the mock DB is patched onto each of those modules directly
(patching only `server.db` would leave them pointed at the real,
unreachable Motor client)."""

from __future__ import annotations

import contextlib
import importlib

import pytest
from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient

import infra_indexes
from services import architecture_reuse


class _FakeSessionManager:
    """`mcp.server.streamable_http_manager.StreamableHTTPSessionManager.
    run()` can only be entered once per instance for the lifetime of the
    process (a real, intentional limitation of that package — see its
    own docstring). The real `academy_mcp`/`private_academy_mcp` are
    module-level singletons in mcp_server.py/mcp_private.py, so the
    first test in this file to fully enter+exit `lifespan()` for real
    would permanently exhaust them for every test after it. What this
    suite is actually testing is the OPS-01 fail-closed contract and
    the startup_ready/startup_error readiness state — not MCP session
    manager mechanics (covered separately by test_mcp_oauth_contract.py)
    — so tests that need a successful, repeatable boot swap in this
    reusable fake instead."""

    @contextlib.asynccontextmanager
    async def run(self):
        yield


class _FakeMCP:
    def __init__(self):
        self.session_manager = _FakeSessionManager()


def _use_fake_mcp(monkeypatch, server):
    monkeypatch.setattr(server, "academy_mcp", _FakeMCP())
    monkeypatch.setattr(server, "private_academy_mcp", _FakeMCP())


def _fresh_mock_db(monkeypatch, server, name: str):
    """Point every module that resolved its own `db` reference at
    import time (`infra_indexes`, `services.architecture_reuse`,
    `server` itself) at the same fresh in-memory database, so
    ensure_indexes()/sync_manifest() actually read and write it."""
    mock_db = AsyncMongoMockClient()[name]
    monkeypatch.setattr(infra_indexes, "db", mock_db)
    monkeypatch.setattr(architecture_reuse, "db", mock_db)
    monkeypatch.setattr(server, "db", mock_db)
    return mock_db


def _quiet_seed_steps(monkeypatch, server):
    """Neutralize the slow, non-critical seed/reconciliation calls so
    startup/shutdown tests stay fast and focused on the OPS-01
    fail-closed contract, not on exercising the full real corpus seed
    (already covered by `test_mcp_oauth_contract.py`'s own full-app
    boot and by manual MOCK_DB=1 verification)."""

    async def _noop():
        return None

    async def _matrix():
        return (0, 0)

    async def _workbook_ready(_db):
        return {"all_ready": True, "imported": []}

    monkeypatch.setattr(server, "register_integration_subscribers", lambda: None)
    monkeypatch.setattr(server, "ensure_mcp_indexes", _noop)
    monkeypatch.setattr(server, "seed_if_empty", _noop)
    monkeypatch.setattr(server, "seed_default_definitions", _noop)
    monkeypatch.setattr(server, "seed_initial_matrix", _matrix)
    monkeypatch.setattr(server, "ensure_workbook_runtimes", _workbook_ready)


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
    assert server._cors_origins == ["*"]


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
    assert server._cors_origins == [
        "https://academy.cvln.example",
        "https://admin.cvln.example",
    ]


# --------------------------------------------------------------------
# OPS-01 — startup fails closed on an index/invariant failure
# --------------------------------------------------------------------


@pytest.mark.asyncio
async def test_startup_normal_boots_ready_with_real_indexes_and_manifest(monkeypatch):
    """Scenario: normal startup. ensure_indexes() and architecture_reuse.
    sync_manifest() run for real against an in-memory Motor-compatible
    DB (not mocked out — only the slow seed steps are); the app reaches
    startup_ready=True and real indexes exist afterward."""
    import server

    mock_db = _fresh_mock_db(monkeypatch, server, "ops01_normal")
    _quiet_seed_steps(monkeypatch, server)
    _use_fake_mcp(monkeypatch, server)

    with TestClient(server.app) as client:
        assert server.app.state.startup_ready is True
        assert server.app.state.startup_error is None
        indexes = await mock_db.users.index_information()
        assert len(indexes) > 1  # more than just the default _id_ index
        assert client.get("/api/health/live").status_code == 200


@pytest.mark.asyncio
async def test_startup_db_unavailable_refuses_to_boot(monkeypatch):
    """Scenario: DB unavailable. A connection-level failure inside
    ensure_indexes() (simulating an unreachable/down Mongo) must abort
    ASGI startup, not degrade to "serving without indexes"."""
    import server

    async def _connection_refused():
        raise OSError("simulated: connection refused (mongod unreachable)")

    monkeypatch.setattr(server, "ensure_indexes", _connection_refused)
    _quiet_seed_steps(monkeypatch, server)

    with pytest.raises(OSError, match="connection refused"):
        with TestClient(server.app):
            pytest.fail("TestClient entered successfully despite DB being down")


@pytest.mark.asyncio
async def test_startup_index_creation_failure_refuses_to_boot(monkeypatch):
    """Scenario: index creation failure (e.g. a conflicting index
    already exists with different options). This is the exact
    regression this suite exists to prevent: an app that starts and
    serves traffic while ECON-01/02/03 and PHY-01's atomicity
    guarantees are not actually enforced at the DB layer."""
    import server

    async def _boom():
        raise RuntimeError("simulated index creation failure")

    monkeypatch.setattr(server, "ensure_indexes", _boom)
    _quiet_seed_steps(monkeypatch, server)

    with pytest.raises(RuntimeError, match="simulated index creation failure"):
        with TestClient(server.app):
            pytest.fail("TestClient entered successfully despite index failure")


@pytest.mark.asyncio
async def test_startup_manifest_not_locked_refuses_to_boot(monkeypatch):
    """The second half of the same fail-closed contract: a PG-13
    architecture manifest that fails to lock (e.g. a conflicting
    build-decision record already stored) must abort startup exactly
    like an index failure does — same invariant, same seriousness."""
    import server

    _fresh_mock_db(monkeypatch, server, "ops01_manifest_conflict")

    async def _not_locked(*, actor_id):
        return {"status": "CONFLICT", "reason": "simulated manifest conflict"}

    monkeypatch.setattr(server.architecture_reuse, "sync_manifest", _not_locked)
    _quiet_seed_steps(monkeypatch, server)

    with pytest.raises(RuntimeError, match="PG-13 deduplication manifest failed to lock"):
        with TestClient(server.app):
            pytest.fail("TestClient entered successfully despite an unlocked manifest")


@pytest.mark.asyncio
async def test_startup_survives_seed_failures(monkeypatch):
    """Seed data is NOT a correctness/security invariant — a failure
    there must stay logged-and-continue, never fatal, unlike
    ensure_indexes() and the PG-13 manifest above. The app still
    reaches startup_ready=True: real indexes + manifest succeeded,
    only the best-effort seed step failed."""
    import server

    _fresh_mock_db(monkeypatch, server, "ops01_seed_failure")

    async def _ok():
        return None

    async def _boom():
        raise RuntimeError("simulated seed failure")

    async def _matrix():
        return (0, 0)

    async def _workbook_ready(_db):
        return {"all_ready": True, "imported": []}

    monkeypatch.setattr(server, "register_integration_subscribers", lambda: None)
    monkeypatch.setattr(server, "ensure_mcp_indexes", _ok)
    monkeypatch.setattr(server, "seed_if_empty", _boom)
    monkeypatch.setattr(server, "seed_default_definitions", _ok)
    monkeypatch.setattr(server, "seed_initial_matrix", _matrix)
    monkeypatch.setattr(server, "ensure_workbook_runtimes", _workbook_ready)
    _use_fake_mcp(monkeypatch, server)

    # ensure_indexes()/architecture_reuse.sync_manifest() (the OPS-01
    # correctness invariants) ran outside the try/except and succeeded;
    # only the best-effort seed_if_empty() inside it failed, so the app
    # still accepts the connection (lifespan did not raise) rather than
    # refusing to boot for a non-critical failure. app.state.startup_error
    # is populated so the failure is visible (e.g. via a readiness probe
    # or /health), while app.state.startup_ready reflects that this
    # particular boot did not reach a fully-clean end-to-end state —
    # r35l31's original contract only required this path to not raise.
    with TestClient(server.app) as client:
        assert server.app.state.startup_ready is False
        assert "simulated seed failure" in server.app.state.startup_error
        assert client.get("/api/health/live").status_code == 200


@pytest.mark.asyncio
async def test_startup_in_production_configuration_still_fails_closed(monkeypatch):
    """Configuration: production. OPS-01 (fail-closed on index/manifest
    failure) and OPS-02 (CORS allowlist) are independent gates — a
    correctly-configured production CORS allowlist must not weaken the
    index/manifest fail-closed behavior."""
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("CORS_ORIGINS", "https://academy.cvln.example")
    import server

    importlib.reload(server)
    assert server._cors_origins == ["https://academy.cvln.example"]

    async def _boom():
        raise RuntimeError("simulated index creation failure in production")

    monkeypatch.setattr(server, "ensure_indexes", _boom)
    _quiet_seed_steps(monkeypatch, server)

    with pytest.raises(RuntimeError, match="simulated index creation failure in production"):
        with TestClient(server.app):
            pytest.fail("production TestClient entered despite index failure")


@pytest.mark.asyncio
async def test_startup_in_development_configuration_still_fails_closed(monkeypatch):
    """Configuration: development/test (the default — no ENVIRONMENT
    set). The wildcard CORS default is intentional here, but that must
    not be conflated with a weaker index/manifest guarantee."""
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    monkeypatch.delenv("CORS_ORIGINS", raising=False)
    import server

    importlib.reload(server)
    assert server._cors_origins == ["*"]

    async def _boom():
        raise RuntimeError("simulated index creation failure in development")

    monkeypatch.setattr(server, "ensure_indexes", _boom)
    _quiet_seed_steps(monkeypatch, server)

    with pytest.raises(RuntimeError, match="simulated index creation failure in development"):
        with TestClient(server.app):
            pytest.fail("development TestClient entered despite index failure")


@pytest.mark.asyncio
async def test_shutdown_closes_db_client_and_stops_mcp_session_managers(monkeypatch):
    """Scenario: shutdown. On a clean exit from the lifespan context,
    startup_ready must revert to False (an orchestrator's readiness
    probe must see the instance as no longer ready) and the Mongo
    client must be closed exactly once."""
    import server

    _fresh_mock_db(monkeypatch, server, "ops01_shutdown")
    _quiet_seed_steps(monkeypatch, server)
    _use_fake_mcp(monkeypatch, server)

    close_calls = []
    real_client = server.client

    class _TrackingClient:
        def close(self):
            close_calls.append(True)
            return real_client.close()

    # `server.py`'s lifespan() only ever calls `client.close()` in its
    # `finally` block, and `client` is the module-level name imported
    # from db.py (`from db import client, db`) — Motor's AsyncIOMotorClient
    # itself doesn't allow rebinding a method on the instance (`.close` is
    # a non-settable descriptor), so the module-level name is replaced
    # with a minimal proxy instead.
    monkeypatch.setattr(server, "client", _TrackingClient())

    with TestClient(server.app) as client:
        assert server.app.state.startup_ready is True
        client.get("/api/health/live")

    assert server.app.state.startup_ready is False
    assert close_calls == [True]


@pytest.mark.asyncio
async def test_restart_boots_cleanly_a_second_time(monkeypatch):
    """Scenario: restart. Entering and fully exiting the lifespan twice
    in a row (simulating a process restart, or two TestClient-driven
    requests in a test suite reusing the same `app` object) must
    succeed both times with no leaked state from the first run."""
    import server

    _fresh_mock_db(monkeypatch, server, "ops01_restart")
    _quiet_seed_steps(monkeypatch, server)
    _use_fake_mcp(monkeypatch, server)

    with TestClient(server.app) as client:
        assert server.app.state.startup_ready is True
        assert client.get("/api/health/live").status_code == 200
    assert server.app.state.startup_ready is False

    # Second boot — same app object, same monkeypatched fast seed path.
    with TestClient(server.app) as client:
        assert server.app.state.startup_ready is True
        assert server.app.state.startup_error is None
        assert client.get("/api/health/live").status_code == 200
    assert server.app.state.startup_ready is False
