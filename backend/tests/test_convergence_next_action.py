"""CONVERGENCE_RUNTIME (reconciliation 2026-09-07, ACA-0019) — a
learner whose legacy path has nothing actionable must see a real
canonical next-action instead of an empty one, and `GET /user/
learning-path` must never make the caller guess which of the three
canonical frontend route prefixes (`/canonical`, `/kiltikonet-
canonical`, `/kora-canonical`) applies.

Real gap this closes: `next_action` in `api/learning.py::
user_learning_path` was computed from legacy `db.formations`/
`db.progress` only — a learner with no legacy formation unlocked (or
none assigned) got `next_action: null` regardless of real canonical
work available, and even a caller that DID know about canonical
content would have had to hardcode which of three route prefixes to
use per domain.
"""

from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

import api.learning as learning_module
import fms_canonical
import frk_canonical
import klt_canonical
import kor_canonical
from fms_canonical.models import CanonicalFormation, CanonicalModule, CanonicalModuleProgress
from klt_canonical.models import CanonicalKltFormation, CanonicalKltModule
from models import User


def _fms_formation(code="FMS-01", name="Métier Un", modules=("FMS01-M01", "FMS01-M02")):
    return CanonicalFormation(
        canonical_formation_code=code,
        metier_number=code.split("-")[-1],
        metier_name=name,
        module_codes_in_order=list(modules),
        module_count=len(modules),
    )


def _fms_module(formation_code, module_code, title):
    return CanonicalModule(
        canonical_formation_code=formation_code,
        canonical_module_code=module_code,
        order_index=0,
        title=title,
        prerequisites={"status": "UNSPECIFIED"},
    )


@pytest.fixture
def empty_canonical(monkeypatch):
    """Every domain has no formations at all — the honest "nothing to
    fall back to" case."""

    async def empty_list(*_a, **_kw):
        return []

    async def empty_progress(*_a, **_kw):
        return []

    for module, fn_names in (
        (fms_canonical, ("list_canonical_formations", "get_user_canonical_progress")),
        (klt_canonical, ("list_canonical_klt_formations", "get_user_klt_progress")),
        (kor_canonical, ("list_canonical_kor_formations", "get_user_kor_progress")),
        (frk_canonical, ("list_canonical_frk_formations", "get_user_frk_progress")),
    ):
        monkeypatch.setattr(module, fn_names[0], empty_list)
        monkeypatch.setattr(module, fn_names[1], empty_progress)


@pytest.fixture
def fms_has_unviewed_module(monkeypatch):
    """FMS-01 has one viewed module (M01) and one unviewed (M02) — the
    real "resume here" case, domain-first (FMS tried before KLT/KOR)."""

    async def fms_formations(**_kw):
        return [_fms_formation()]

    async def fms_progress(user_id, **_kw):
        return [
            CanonicalModuleProgress(
                user_id=user_id,
                canonical_formation_code="FMS-01",
                canonical_module_code="FMS01-M01",
                content_viewed_at="2026-09-01T00:00:00+00:00",
            )
        ]

    async def fms_module(formation_code, module_code, **_kw):
        return _fms_module(formation_code, module_code, "Module Deux")

    monkeypatch.setattr(fms_canonical, "list_canonical_formations", fms_formations)
    monkeypatch.setattr(fms_canonical, "get_user_canonical_progress", fms_progress)
    monkeypatch.setattr(fms_canonical, "get_canonical_module", fms_module)

    async def empty_list(*_a, **_kw):
        return []

    async def empty_progress(*_a, **_kw):
        return []

    monkeypatch.setattr(klt_canonical, "list_canonical_klt_formations", empty_list)
    monkeypatch.setattr(klt_canonical, "get_user_klt_progress", empty_progress)
    monkeypatch.setattr(kor_canonical, "list_canonical_kor_formations", empty_list)
    monkeypatch.setattr(kor_canonical, "get_user_kor_progress", empty_progress)
    monkeypatch.setattr(frk_canonical, "list_canonical_frk_formations", empty_list)
    monkeypatch.setattr(frk_canonical, "get_user_frk_progress", empty_progress)


@pytest.fixture
def only_klt_has_unviewed_module(monkeypatch):
    """FMS fully viewed (so FMS contributes nothing); KLT has one
    unviewed module — proves domain fallthrough (FMS -> KLT)."""

    async def fms_formations(**_kw):
        return [_fms_formation(modules=("FMS01-M01",))]

    async def fms_progress(user_id, **_kw):
        return [
            CanonicalModuleProgress(
                user_id=user_id,
                canonical_formation_code="FMS-01",
                canonical_module_code="FMS01-M01",
                content_viewed_at="2026-09-01T00:00:00+00:00",
            )
        ]

    monkeypatch.setattr(fms_canonical, "list_canonical_formations", fms_formations)
    monkeypatch.setattr(fms_canonical, "get_user_canonical_progress", fms_progress)

    async def klt_formations():
        return [
            CanonicalKltFormation(
                klt_formation_code="KLT-06",
                title="Analyste Observatory",
                structural_status="COMPLETE",
                fully_complete=True,
                module_codes_in_order=["KLT-06-M01"],
                module_count=1,
            )
        ]

    async def klt_progress(user_id, **_kw):
        return []

    async def klt_module(formation_code, module_code, **_kw):
        return CanonicalKltModule(
            klt_formation_code=formation_code,
            module_code=module_code,
            order_index=0,
            title="Observation Module",
        )

    monkeypatch.setattr(klt_canonical, "list_canonical_klt_formations", klt_formations)
    monkeypatch.setattr(klt_canonical, "get_user_klt_progress", klt_progress)
    monkeypatch.setattr(klt_canonical, "get_canonical_klt_module", klt_module)

    async def empty_list(*_a, **_kw):
        return []

    async def empty_progress(*_a, **_kw):
        return []

    monkeypatch.setattr(kor_canonical, "list_canonical_kor_formations", empty_list)
    monkeypatch.setattr(kor_canonical, "get_user_kor_progress", empty_progress)
    monkeypatch.setattr(frk_canonical, "list_canonical_frk_formations", empty_list)
    monkeypatch.setattr(frk_canonical, "get_user_frk_progress", empty_progress)


# --------------------------------------------------------------------
# get_first_unviewed_canonical_module — the pure convergence logic
# --------------------------------------------------------------------


@pytest.mark.asyncio
async def test_returns_none_when_no_canonical_content_exists(empty_canonical):
    from services.canonical_convergence import get_first_unviewed_canonical_module

    assert await get_first_unviewed_canonical_module("user-1") is None


@pytest.mark.asyncio
async def test_finds_first_unviewed_fms_module(fms_has_unviewed_module):
    from services.canonical_convergence import get_first_unviewed_canonical_module

    result = await get_first_unviewed_canonical_module("user-1")
    assert result is not None
    assert result["domain"] == "FMS"
    assert result["formation_code"] == "FMS-01"
    assert result["module_code"] == "FMS01-M02"
    assert result["module_name"] == "Module Deux"
    assert result["route"] == "/canonical/FMS-01/FMS01-M02"


@pytest.mark.asyncio
async def test_falls_through_to_klt_when_fms_exhausted(only_klt_has_unviewed_module):
    from services.canonical_convergence import get_first_unviewed_canonical_module

    result = await get_first_unviewed_canonical_module("user-1")
    assert result is not None
    assert result["domain"] == "KLT"
    assert result["formation_code"] == "KLT-06"
    assert result["module_code"] == "KLT-06-M01"
    assert result["route"] == "/kiltikonet-canonical/KLT-06/KLT-06-M01"


# --------------------------------------------------------------------
# user_learning_path — wired end-to-end (mongomock for the legacy side)
# --------------------------------------------------------------------


def _user() -> User:
    return User(
        frek_id="FREK-1",
        email="learner@example.com",
        display_name="Learner",
        password_hash="x",
        role="student",
        metier_vise="FMS",
    )


@pytest.fixture
async def empty_legacy_db(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_convergence_next_action_test"]
    monkeypatch.setattr(learning_module, "db", mock_db)
    return mock_db


@pytest.mark.asyncio
async def test_next_action_falls_back_to_canonical_when_legacy_empty(
    empty_legacy_db, fms_has_unviewed_module
):
    """No legacy formations at all (empty db.formations) -> next_action
    must come from the canonical fallback, not stay null."""
    result = await learning_module.user_learning_path(current=_user())
    assert result["next_action"] is not None
    assert result["next_action"]["source"] == "FMS"
    assert result["next_action"]["route"] == "/canonical/FMS-01/FMS01-M02"
    assert result["own_pole"] == []


@pytest.mark.asyncio
async def test_next_action_stays_legacy_when_legacy_has_something(
    empty_legacy_db, fms_has_unviewed_module
):
    """Legacy stays authoritative whenever it has a real next step —
    the canonical fallback must never override a genuine legacy
    next_action."""
    await empty_legacy_db.formations.insert_one(
        {
            "code": "KOR-01",
            "name": "Legacy Formation",
            "pole": "FMS",
            "duration_h": 10,
            "cc": 5,
            "modules": [{"code": "KOR-01-M01", "name": "Legacy Module"}],
        }
    )
    result = await learning_module.user_learning_path(current=_user())
    assert result["next_action"] is not None
    assert result["next_action"]["source"] == "legacy"
    assert result["next_action"]["formation_code"] == "KOR-01"


@pytest.mark.asyncio
async def test_next_action_stays_null_when_nothing_anywhere(
    empty_legacy_db, empty_canonical
):
    result = await learning_module.user_learning_path(current=_user())
    assert result["next_action"] is None
