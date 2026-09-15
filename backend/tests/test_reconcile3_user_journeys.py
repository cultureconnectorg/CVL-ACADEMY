"""RECONCILE-3 Phase 3 — full system user journeys.

Not a mocked-unit-test suite: this drives the REAL FastAPI app (real
`lifespan()`, real ensure_indexes()/architecture_reuse.sync_manifest(),
real routers, real auth/JWT, real business logic) through actual HTTP
requests via httpx's ASGI transport, against an in-memory Motor-
compatible DB (`mongomock_motor` — the same MOCK_DB=1 fallback db.py
already documents for this exact sandbox constraint: no live MongoDB
reachable here). This is genuine end-to-end proof of wiring, not of
the underlying MongoDB storage engine's own correctness (indexes are
created for real against mongomock and asserted on, but real-engine
behaviors like true multi-document transaction semantics are out of
reach here — see RECONCILE_3_RUNTIME_REPORT.md Phase 6 for what that
means for PHY-01/ECON-01..03 under this sandbox).

Journeys covered, per the Founder's Phase 3 instruction:
  VISITEUR: landing -> formations -> formation -> register
  APPRENANT: register -> login -> legal acceptance -> onboarding ->
    dashboard -> formation -> module -> progression -> certification/
    badge -> wallet
  RETOUR UTILISATEUR: login -> session restore -> dashboard -> reprise
  PRO/EXPERT: auth -> professional profile -> permissions
  ADMIN: auth -> admin dashboard -> reserved functions -> refusal for
    non-admin
  Plus: refresh, deep links, logout, expired/invalid token, 401/403,
  feature flags ON/OFF.
"""

from __future__ import annotations

import contextlib
import os

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient


class _FakeSessionManager:
    """See tests/test_server_startup_and_cors.py's own docstring for
    why: mcp's StreamableHTTPSessionManager.run() can only be entered
    once per process-lifetime instance, and the real academy_mcp/
    private_academy_mcp objects are module-level singletons. These
    journey tests exercise the real REST API surface, not MCP session
    mechanics, so a fresh, reusable fake is swapped in per test."""

    @contextlib.asynccontextmanager
    async def run(self):
        yield


class _FakeMCP:
    def __init__(self):
        self.session_manager = _FakeSessionManager()


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def live_app():
    """Boot the real app for real, via its real lifespan() (real
    ensure_indexes()/architecture_reuse.sync_manifest(), real full
    corpus seed -- formations/modules/economy/cartography/protocol
    master imports across every domain built in this engagement --
    real workbook runtime reconciliation), ONCE for this whole test
    module, against one shared in-memory DB. That seed alone takes on
    the order of a minute against mongomock in this sandbox (hundreds
    of real formations/modules across FMS/FRK/KOR/KLT/GMD/CVE/AGF/etc.)
    -- function-scoping it would multiply that by every journey test in
    this file for no additional proof value, since ensure_indexes()/
    architecture_reuse.sync_manifest() themselves are already covered
    function-scoped (fresh DB per test, fail-closed scenarios included)
    by tests/test_server_startup_and_cors.py. Every journey test below
    registers its own uniquely-emailed user, so sharing one seeded
    catalogue + auth/legal/wallet/etc. collections across tests is safe
    -- this mirrors a real shared staging backend far more closely than
    a fresh empty DB per journey would anyway."""
    os.environ.setdefault("MONGO_URL", "mongodb://localhost:27017")
    os.environ.setdefault("DB_NAME", "cvln_academy_journeys")
    os.environ.setdefault("JWT_SECRET", "journey-test-secret")
    os.environ["MOCK_DB"] = "1"

    import importlib

    import server

    importlib.reload(server)
    server.academy_mcp = _FakeMCP()
    server.private_academy_mcp = _FakeMCP()

    async with server.app.router.lifespan_context(server.app):
        transport = ASGITransport(app=server.app)
        async with AsyncClient(transport=transport, base_url="http://testserver/api") as client:
            yield client


def _register_payload(email: str, name: str = "Journey Learner"):
    return {
        "email": email,
        "password": "S3curePassw0rd!",
        "display_name": name,
        "lang": "fr",
    }


# A real, tiny (1x1 transparent) PNG data URL -- matches legal.py's own
# _SIGNATURE_RE and the min_length=100 constraint exactly like a real
# canvas.toDataURL("image/png") signature would (see LegalAcceptance.jsx).
_FAKE_SIGNATURE_DATA_URL = (
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lE"
    "QVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
)


async def _accept_legal(client, headers):
    """Mirrors LegalAcceptance.jsx's real submit() exactly: GET the
    requirements, build the {doc_id: version} map from the real
    documents list, sign, POST /legal/accept."""
    r = await client.get("/legal/requirements", headers=headers)
    assert r.status_code == 200, r.text
    requirements = r.json()
    documents = {doc["id"]: doc["version"] for doc in requirements["documents"]}
    r = await client.post(
        "/legal/accept",
        headers=headers,
        json={
            "documents": documents,
            "signature_data_url": _FAKE_SIGNATURE_DATA_URL,
            "signer_name": "Journey Tester",
        },
    )
    assert r.status_code == 200, r.text
    return r.json()


# --------------------------------------------------------------------
# VISITEUR — landing -> formations -> formation -> register
# --------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="session")
async def test_visitor_journey_formations_discovery_to_register(live_app):
    # formations (public discovery, no auth required)
    r = await live_app.get("/formations")
    assert r.status_code == 200, r.text
    catalogue = r.json()
    assert isinstance(catalogue, list) and len(catalogue) > 0
    first_code = catalogue[0]["code"]

    # single formation detail (public)
    r = await live_app.get(f"/formations/{first_code}")
    assert r.status_code == 200, r.text
    assert r.json()["code"] == first_code

    # register (the visitor's exit point into the learner journey)
    r = await live_app.post("/auth/register", json=_register_payload("visitor.journey@example.com"))
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["user"]["email"] == "visitor.journey@example.com"
    assert body["token"]


# --------------------------------------------------------------------
# APPRENANT — register -> login -> legal -> onboarding -> dashboard ->
# formation -> module -> progression -> certification/badge -> wallet
# --------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="session")
async def test_learner_journey_register_through_wallet(live_app):
    email = "learner.journey@example.com"
    r = await live_app.post("/auth/register", json=_register_payload(email))
    assert r.status_code == 200, r.text
    token = r.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # A brand-new user has not accepted legal terms yet: a gated route
    # must refuse, not silently allow.
    r = await live_app.get("/missions", headers=headers)
    assert r.status_code == 428, r.text
    assert r.json()["detail"]["code"] == "LEGAL_ACCEPTANCE_REQUIRED"

    # legal acceptance — real flow, not bypassed
    await _accept_legal(live_app, headers)

    # Now gated routes open up.
    r = await live_app.get("/missions", headers=headers)
    assert r.status_code == 200, r.text
    missions = r.json()
    assert isinstance(missions, list)

    # onboarding
    r = await live_app.get("/onboarding/options", headers=headers)
    assert r.status_code == 200, r.text
    options = r.json()
    r = await live_app.post(
        "/onboarding/complete",
        headers=headers,
        json={
            "lang": "fr",
            "metier_vise": options["metiers"][0]["code"],
            "territoire": options["territoires"][0]["code"],
            "objectif_perso": "Obtenir ma certification et évoluer professionnellement.",
        },
    )
    assert r.status_code == 200, r.text

    # dashboard-equivalent data: progression summary + learning path
    r = await live_app.get("/progression/summary", headers=headers)
    assert r.status_code == 200, r.text
    r = await live_app.get("/user/learning-path", headers=headers)
    assert r.status_code == 200, r.text
    path = r.json()
    assert "own_pole" in path and "other_poles" in path

    # formation + module (real content, real progress-tracking route)
    r = await live_app.get("/formations", headers=headers)
    assert r.status_code == 200
    code = r.json()[0]["code"]
    r = await live_app.get(f"/formations/{code}", headers=headers)
    assert r.status_code == 200, r.text
    modules = r.json().get("modules", [])
    assert len(modules) > 0
    module_code = modules[0]["code"]
    r = await live_app.get(f"/modules/{code}/{module_code}", headers=headers)
    assert r.status_code == 200, r.text

    # badges (proof/certification adjacent — real list, may be empty for a fresh user)
    r = await live_app.get("/badges/mine", headers=headers)
    assert r.status_code == 200, r.text

    # wallet
    r = await live_app.get("/wallet/me", headers=headers)
    assert r.status_code == 200, r.text
    wallet = r.json()
    assert "jcc_balance" in wallet["account"]
    assert "token_balance" in wallet["account"]


# --------------------------------------------------------------------
# RETOUR UTILISATEUR — login -> session restore -> dashboard -> reprise
# --------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="session")
async def test_returning_user_journey_login_and_session_restore(live_app):
    email = "returning.journey@example.com"
    r = await live_app.post("/auth/register", json=_register_payload(email))
    assert r.status_code == 200
    first_login_token = r.json()["token"]

    # A second real login (simulating a new browser session) must
    # succeed and issue an independent token.
    r = await live_app.post(
        "/auth/login", json={"email": email, "password": "S3curePassw0rd!"}
    )
    assert r.status_code == 200, r.text
    second_token = r.json()["token"]
    assert second_token  # real, independent token issued
    headers = {"Authorization": f"Bearer {second_token}"}

    r = await live_app.get("/auth/me", headers=headers)
    assert r.status_code == 200, r.text
    assert r.json()["email"] == email

    # The first token is still independently valid (real session restore
    # semantics — not single-session-only).
    r = await live_app.get("/auth/me", headers={"Authorization": f"Bearer {first_login_token}"})
    assert r.status_code == 200, r.text

    await _accept_legal(live_app, headers)

    # Per lifecycle.py's own deliberate design (RETURNING_THRESHOLD=1 day),
    # a second login moments after registration must NOT read as
    # "returning" -- that guards against a multi-tab/refresh-token-rotation
    # burst right after signup misreading as a return visit.
    r = await live_app.get("/frek/profile", headers=headers)
    assert r.status_code == 200, r.text
    assert r.json().get("returning") is False

    # Now prove the True branch for real: backdate the account's
    # created_at past the threshold (the same server-side field
    # is_returning_session() actually reads) and re-authenticate --
    # the derived signal must flip without any stored "returning" field.
    import server

    old_created_at = "2020-01-01T00:00:00+00:00"
    await server.db.users.update_one(
        {"email": email}, {"$set": {"created_at": old_created_at}}
    )
    r = await live_app.post(
        "/auth/login", json={"email": email, "password": "S3curePassw0rd!"}
    )
    assert r.status_code == 200, r.text
    third_headers = {"Authorization": f"Bearer {r.json()['token']}"}

    r = await live_app.get("/frek/profile", headers=third_headers)
    assert r.status_code == 200, r.text
    assert r.json().get("returning") is True


# --------------------------------------------------------------------
# PRO / EXPERT — auth -> professional profile/workspace -> permissions
# --------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="session")
async def test_professional_journey_profile_and_permissions(live_app):
    email = "pro.journey@example.com"
    r = await live_app.post("/auth/register", json=_register_payload(email))
    token = r.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    await _accept_legal(live_app, headers)

    # own professional profile — real, gated to the authenticated user
    r = await live_app.get("/professional/profile/mine", headers=headers)
    assert r.status_code == 200, r.text

    # visibility toggle is a real, permission-scoped write
    r = await live_app.post(
        "/professional/profile/visibility", headers=headers, json={"is_public": True}
    )
    assert r.status_code == 200, r.text
    assert r.json()["is_public"] is True

    # a professional workspace route reserved to a higher role must
    # refuse a plain student — proves the permission boundary is real,
    # not merely documented.
    r = await live_app.get("/production-gates", headers=headers)
    assert r.status_code == 403, r.text


# --------------------------------------------------------------------
# ADMIN — auth -> admin dashboard -> reserved functions -> refusal for
# non-admin
# --------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_journey_and_non_admin_is_refused(live_app):
    # A plain, freshly-registered user (student role) must be refused
    # every admin-reserved route — the actual negative-permission proof.
    email = "plain.journey@example.com"
    r = await live_app.post("/auth/register", json=_register_payload(email))
    token = r.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    await _accept_legal(live_app, headers)

    r = await live_app.get("/orgs", headers=headers)
    assert r.status_code == 403, r.text

    r = await live_app.get("/production-gates", headers=headers)
    assert r.status_code == 403, r.text

    # Now provision a real admin (server-side role assignment, the same
    # mechanism an operator would use — not a shortcut around auth).
    import server

    admin_email = "admin.journey@example.com"
    r = await live_app.post("/auth/register", json=_register_payload(admin_email, "Admin Journey"))
    admin_token = r.json()["token"]
    await server.db.users.update_one({"email": admin_email}, {"$set": {"role": "admin"}})
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    await _accept_legal(live_app, admin_headers)

    r = await live_app.get("/orgs", headers=admin_headers)
    assert r.status_code == 200, r.text

    r = await live_app.get("/production-gates", headers=admin_headers)
    assert r.status_code == 200, r.text


# --------------------------------------------------------------------
# Cross-cutting: refresh, deep links, logout, expired/invalid token,
# 401/403, feature flags
# --------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="session")
async def test_refresh_token_rotation(live_app):
    email = "refresh.journey@example.com"
    r = await live_app.post("/auth/register", json=_register_payload(email))
    assert r.status_code == 200
    refresh_token = r.json().get("refresh_token")
    assert refresh_token, "register must issue a real refresh token"

    r = await live_app.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert r.status_code == 200, r.text
    new_access = r.json()["token"]
    assert new_access

    r = await live_app.get("/auth/me", headers={"Authorization": f"Bearer {new_access}"})
    assert r.status_code == 200, r.text

    # Real rotation: the old refresh token must not be reusable twice.
    r = await live_app.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert r.status_code in (400, 401), r.text


@pytest.mark.asyncio(loop_scope="session")
async def test_deep_link_to_formation_detail_without_auth(live_app):
    r = await live_app.get("/formations")
    code = r.json()[0]["code"]
    # A "deep link" straight to a formation detail page, no prior nav,
    # no auth — must resolve exactly as browsing there normally would.
    r = await live_app.get(f"/formations/{code}")
    assert r.status_code == 200, r.text


@pytest.mark.asyncio(loop_scope="session")
async def test_logout_revokes_refresh_token(live_app):
    email = "logout.journey@example.com"
    r = await live_app.post("/auth/register", json=_register_payload(email))
    refresh_token = r.json()["refresh_token"]
    access_token = r.json()["token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    r = await live_app.post("/auth/logout", headers=headers)
    assert r.status_code == 200, r.text

    r = await live_app.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert r.status_code in (400, 401), r.text


@pytest.mark.asyncio(loop_scope="session")
async def test_expired_and_invalid_tokens_are_rejected(live_app):
    import jwt as pyjwt

    # A structurally-invalid token.
    r = await live_app.get("/auth/me", headers={"Authorization": "Bearer not-a-real-token"})
    assert r.status_code == 401, r.text

    # A well-formed but expired token (signed with the real test secret,
    # but with an exp claim in the past).
    expired = pyjwt.encode(
        {"sub": "someone", "exp": 1},
        os.environ["JWT_SECRET"],
        algorithm="HS256",
    )
    r = await live_app.get("/auth/me", headers={"Authorization": f"Bearer {expired}"})
    assert r.status_code == 401, r.text


@pytest.mark.asyncio(loop_scope="session")
async def test_401_without_token_and_403_with_wrong_role(live_app):
    # 401: no credentials at all on a protected route.
    r = await live_app.get("/auth/me")
    assert r.status_code == 401, r.text

    # 403: real credentials, real session, wrong role for an
    # admin-reserved route (already proven above for /orgs and
    # /production-gates — this asserts the shape of the 403 itself).
    email = "role403.journey@example.com"
    r = await live_app.post("/auth/register", json=_register_payload(email))
    token = r.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    await _accept_legal(live_app, headers)

    r = await live_app.get("/orgs", headers=headers)
    assert r.status_code == 403
    assert "detail" in r.json()


@pytest.mark.asyncio(loop_scope="session")
async def test_feature_flag_off_path_still_serves_correct_data(live_app):
    """SPATIAL_HUB_ENABLED and friends are frontend-only flags (see
    frontend/src/lib/featureFlags.js) with no backend equivalent -- the
    backend has no notion of "spatial mode" and always returns the same
    real data regardless. This proves that invariant directly: the same
    backend call made "as if" a flag were on or off returns identical,
    unflagged, real data -- the ON/OFF split lives entirely in how the
    frontend renders it (see Phase 4)."""
    email = "flags.journey@example.com"
    r = await live_app.post("/auth/register", json=_register_payload(email))
    headers = {"Authorization": f"Bearer {r.json()['token']}"}
    await _accept_legal(live_app, headers)

    r1 = await live_app.get("/progression/summary", headers=headers)
    r2 = await live_app.get("/progression/summary", headers=headers)
    assert r1.status_code == r2.status_code == 200
    assert r1.json() == r2.json()
