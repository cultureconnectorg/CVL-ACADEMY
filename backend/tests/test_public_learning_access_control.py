"""AUTH-01 (Audit Chirurgical 2026-09-07) — public discovery vs.
protected learning, swept across every route, not just the quiz the
audit named by example.

Real, exploitable gaps this suite closes and proves closed:

  - `GET /formations/{code}/modules/{code}/quiz` had no auth dependency
    at all — questions/choices and the full module object were
    reachable with no session (correct answers were already hidden).
  - `api/fms.py`'s legacy search/lookup/navigation/dependency-graph
    surface (`db.fms_resources`, the pre-canonical ZIP-import pipeline)
    had *no* auth dependency *and* no audience filtering at all —
    `banque_n1`/`banque_n2`/`cas_inedit`/`sujet_officiel`/`grille_
    certificative`/`guide_jury`/`guide_correcteur` (real exam/grading
    material) were reachable by anyone who could guess or full-text-
    search for a resource, worse than the quiz gap since it needed no
    session and no code guessing (the search endpoint enumerates).
  - `certification.py`'s rubric endpoints (exact grading criteria —
    weights, eliminatory skills, mention caps) had no auth dependency.

DB-backed pieces run against `mongomock_motor.AsyncMongoMockClient` —
same convention as every other suite in this repo.
"""

from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

import api.fms as fms_api_module
import fms_import.indexer as fms_indexer_module
from auth import get_current_user
from models import User


def _requires_authentication(route) -> bool:
    """True if `get_current_user` appears anywhere in the route's
    dependency tree — directly (`Depends(get_current_user)`) or nested
    (`Depends(require_role(...))`'s own internal
    `Depends(get_current_user)`)."""

    def search(dependant) -> bool:
        for dep in dependant.dependencies:
            if dep.call is get_current_user:
                return True
            if search(dep):
                return True
        return False

    return search(route.dependant)


# --------------------------------------------------------------------
# Declarative: every route on these three routers requires a session.
# --------------------------------------------------------------------


@pytest.mark.parametrize(
    "path",
    [
        "/formations/{formation_code}/modules/{module_code}/quiz",
        "/formations/{formation_code}/modules/{module_code}/quiz/submit",
    ],
)
def test_quiz_routes_require_authentication(path):
    from api.quizzes import router

    route = next(r for r in router.routes if r.path == path)
    assert _requires_authentication(route), f"{path} has no auth dependency"


@pytest.mark.parametrize(
    "path",
    [
        "/fms/resources",
        "/fms/resources/{code}",
        "/fms/formations/{formation_code}/navigation",
        "/fms/formations/{formation_code}/dependency-graph",
    ],
)
def test_fms_resource_routes_require_authentication(path):
    from api.fms import router

    route = next(r for r in router.routes if r.path == path)
    assert _requires_authentication(route), f"{path} has no auth dependency"


@pytest.mark.parametrize(
    "path", ["/certifications/rubrics", "/certifications/{certification_code}/rubric"]
)
def test_rubric_routes_require_authentication(path):
    from api.certification import router

    route = next(r for r in router.routes if r.path == path)
    assert _requires_authentication(route), f"{path} has no auth dependency"


# --------------------------------------------------------------------
# Functional: the fms.py audience filter actually works, not just
# "some auth dependency is declared".
# --------------------------------------------------------------------


@pytest.fixture
async def fms_db(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_fms_access_control_test"]
    # Every module in the real call chain holds its own `db` reference —
    # api/fms.py's own lookups AND fms_import.indexer's search/nav/graph
    # builders (search_resources/build_navigation/build_dependency_graph)
    # both need the mock swapped in, or the indexer calls fall through to
    # the real (disconnected) db and raise deep inside motor.
    monkeypatch.setattr(fms_api_module, "db", mock_db)
    monkeypatch.setattr(fms_indexer_module, "db", mock_db)
    await mock_db.fms_resources.insert_many(
        [
            {
                "code": "FMS-01-M01",
                "type": "module",  # LEARNER-facing
                "formation_code": "FMS-01",
                "title": "Module 1",
                "version": "1.0",
                "body_markdown": "Contenu réel du module.",
                "prerequisites": [],
            },
            {
                "code": "FMS-01-BANQUE-N1",
                "type": "banque_n1",  # CORRECTOR/JURY only — real exam bank
                "formation_code": "FMS-01",
                "title": "Banque N1",
                "version": "1.0",
                "body_markdown": "Questions et corrigé N1 — confidentiel.",
                "prerequisites": [],
            },
            {
                "code": "FMS-01-GUIDE-CORRECTEUR",
                "type": "guide_correcteur",  # CORRECTOR only
                "formation_code": "FMS-01",
                "title": "Guide Correcteur",
                "version": "1.0",
                "body_markdown": "Barème confidentiel.",
                "prerequisites": ["FMS-01-M01"],
            },
        ]
    )
    return mock_db


def _student() -> User:
    return User(
        frek_id="FREK-STUDENT",
        email="student@example.com",
        display_name="Student",
        password_hash="x",
        role="student",
    )


def _corrector() -> User:
    return User(
        frek_id="FREK-CORRECTOR",
        email="corrector@example.com",
        display_name="Corrector",
        password_hash="x",
        role="corrector",
    )


@pytest.mark.asyncio
async def test_search_hides_staff_only_resources_from_a_student(fms_db):
    from api.fms import list_resources

    # Explicit kwargs, including `resource_type` — called directly (not
    # through the FastAPI app), so its `Query(None, alias="type")`
    # default would otherwise bind as the live Query object itself, not
    # the `None` FastAPI's DI would resolve it to, silently poisoning
    # the mongo filter with a non-matching value.
    results = await list_resources(
        q="", formation_code=None, resource_type=None, limit=50, current=_student()
    )
    codes = {r["code"] for r in results}
    assert codes == {"FMS-01-M01"}


@pytest.mark.asyncio
async def test_search_shows_everything_to_staff(fms_db):
    from api.fms import list_resources

    results = await list_resources(
        q="", formation_code=None, resource_type=None, limit=50, current=_corrector()
    )
    codes = {r["code"] for r in results}
    assert codes == {"FMS-01-M01", "FMS-01-BANQUE-N1", "FMS-01-GUIDE-CORRECTEUR"}


@pytest.mark.asyncio
async def test_direct_lookup_of_staff_only_resource_404s_for_a_student(fms_db):
    from fastapi import HTTPException

    from api.fms import get_resource

    with pytest.raises(HTTPException) as exc:
        await get_resource("FMS-01-BANQUE-N1", current=_student())
    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_direct_lookup_of_staff_only_resource_succeeds_for_staff(fms_db):
    from api.fms import get_resource

    doc = await get_resource("FMS-01-BANQUE-N1", current=_corrector())
    assert doc["code"] == "FMS-01-BANQUE-N1"


@pytest.mark.asyncio
async def test_navigation_omits_staff_only_sections_for_a_student(fms_db):
    from api.fms import get_navigation

    nav = await get_navigation("FMS-01", current=_student())
    all_codes = {r["code"] for section in nav["sections"] for r in section["resources"]}
    assert all_codes == {"FMS-01-M01"}


@pytest.mark.asyncio
async def test_navigation_includes_everything_for_staff(fms_db):
    from api.fms import get_navigation

    nav = await get_navigation("FMS-01", current=_corrector())
    all_codes = {r["code"] for section in nav["sections"] for r in section["resources"]}
    assert all_codes == {"FMS-01-M01", "FMS-01-BANQUE-N1", "FMS-01-GUIDE-CORRECTEUR"}


@pytest.mark.asyncio
async def test_dependency_graph_hides_staff_only_nodes_and_their_edges(fms_db):
    from api.fms import get_dependency_graph

    graph = await get_dependency_graph("FMS-01", current=_student())
    node_codes = {n["code"] for n in graph["nodes"]}
    assert node_codes == {"FMS-01-M01"}
    # The real edge FMS-01-M01 -> FMS-01-GUIDE-CORRECTEUR must not leak
    # even indirectly once the target node itself is hidden.
    assert graph["edges"] == []


@pytest.mark.asyncio
async def test_dependency_graph_shows_real_edges_to_staff(fms_db):
    from api.fms import get_dependency_graph

    graph = await get_dependency_graph("FMS-01", current=_corrector())
    assert {"from": "FMS-01-M01", "to": "FMS-01-GUIDE-CORRECTEUR"} in graph["edges"]
