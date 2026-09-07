"""P0-G (Audit Chirurgical 2026-09-07) — CAN-01/CAN-02: canonical FMS
convergence.

Real gap this suite closes and proves closed: `services/
canonical_convergence.py`'s aggregation logic (the actual new code —
each domain's own `list_canonical_*_formations()`/`get_user_*_progress()`
read model is already covered by its own test suite and is stubbed
here, not re-tested). Proves:

  - A learner with zero legacy `db.progress` activity but real
    `content_viewed_at` records across FMS/KLT/KOR shows up as real,
    non-zero progress once the three domains are summed.
  - "viewed" is never relabeled "completed" — the returned shape only
    ever exposes `canonical_modules_viewed`/`canonical_progress_pct`,
    distinctly named from the legacy `modules_completed`/`global_pct`
    fields these values are merged alongside in api/progression.py and
    api/learning.py (checked directly on those two files' responses
    below, against mongomock_motor for the legacy side).
  - A formation with zero total modules never raises a
    ZeroDivisionError (empty corpus edge case).
"""

from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

import api.learning as learning_module
import api.progression as progression_module
import fms_canonical
import klt_canonical
import kor_canonical
from fms_canonical.models import CanonicalFormation, CanonicalModuleProgress
from klt_canonical.models import CanonicalKltFormation, CanonicalKltModuleProgress
from kor_canonical.models import CanonicalKorFormation
from models import User


def _fms_formation(code: str, name: str, count: int) -> CanonicalFormation:
    return CanonicalFormation(
        canonical_formation_code=code,
        metier_number=code.split("-")[-1],
        metier_name=name,
        module_codes_in_order=[f"{code.replace('-', '')}-M{i+1}" for i in range(count)],
        module_count=count,
    )


def _klt_formation(code: str, title: str, count: int) -> CanonicalKltFormation:
    return CanonicalKltFormation(
        klt_formation_code=code,
        title=title,
        structural_status="COMPLETE",
        fully_complete=True,
        module_codes_in_order=[f"{code}-M{i+1}" for i in range(count)],
        module_count=count,
    )


def _kor_formation(code: str, title: str, count: int) -> CanonicalKorFormation:
    return CanonicalKorFormation(
        kor_formation_code=code,
        title=title,
        fully_complete=True,
        module_codes_in_order=[f"{code}-M{i+1}" for i in range(count)],
        module_count=count,
    )


@pytest.fixture
def stub_canonical(monkeypatch):
    """Stubs all three domains' read model + progress getters — the
    convergence module's own aggregation logic is what this suite
    tests, not each domain's already-separately-tested read model."""

    async def fms_formations(**_kw):
        return [_fms_formation("FMS-01", "Métier Un", 3)]

    async def fms_progress(user_id, **_kw):
        return [
            CanonicalModuleProgress(
                user_id=user_id,
                canonical_formation_code="FMS-01",
                canonical_module_code="FMS01-M01",
                content_viewed_at="2026-09-01T00:00:00+00:00",
            ),
            CanonicalModuleProgress(
                user_id=user_id,
                canonical_formation_code="FMS-01",
                canonical_module_code="FMS01-M02",
                content_viewed_at=None,  # recorded but not yet viewed
            ),
        ]

    async def klt_formations():
        return [_klt_formation("KLT-06", "Analyste Observatory", 5)]

    async def klt_progress(user_id, **_kw):
        return [
            CanonicalKltModuleProgress(
                user_id=user_id,
                klt_formation_code="KLT-06",
                module_code="KLT-06-M01",
                content_viewed_at="2026-09-02T00:00:00+00:00",
            )
        ]

    async def kor_formations():
        return [_kor_formation("KOR-01", "Podcast & Audio Production", 4)]

    async def kor_progress(user_id, **_kw):
        return []  # no KOR activity at all for this user

    monkeypatch.setattr(fms_canonical, "list_canonical_formations", fms_formations)
    monkeypatch.setattr(fms_canonical, "get_user_canonical_progress", fms_progress)
    monkeypatch.setattr(klt_canonical, "list_canonical_klt_formations", klt_formations)
    monkeypatch.setattr(klt_canonical, "get_user_klt_progress", klt_progress)
    monkeypatch.setattr(kor_canonical, "list_canonical_kor_formations", kor_formations)
    monkeypatch.setattr(kor_canonical, "get_user_kor_progress", kor_progress)


@pytest.mark.asyncio
async def test_summary_sums_across_all_three_domains(stub_canonical):
    from services.canonical_convergence import get_canonical_progress_summary

    summary = await get_canonical_progress_summary("user-1")

    assert summary["canonical_modules_total"] == 3 + 5 + 4
    assert summary["canonical_modules_viewed"] == 1 + 1 + 0
    assert summary["canonical_progress_pct"] == int((2 / 12) * 100)
    domains = {f["domain"] for f in summary["canonical_formations"]}
    assert domains == {"FMS", "KLT", "KOR"}
    fms_entry = next(
        f for f in summary["canonical_formations"] if f["domain"] == "FMS"
    )
    assert fms_entry["modules_total"] == 3
    assert fms_entry["modules_viewed"] == 1


@pytest.mark.asyncio
async def test_summary_never_labels_viewed_as_completed(stub_canonical):
    """AUTO_PEDAGOGICAL_EQUIVALENCE = FORBIDDEN — the returned shape
    must never claim a stronger word than the domains themselves do."""
    from services.canonical_convergence import get_canonical_progress_summary

    summary = await get_canonical_progress_summary("user-1")
    assert "completed" not in str(summary).lower()


@pytest.mark.asyncio
async def test_empty_corpus_never_divides_by_zero(monkeypatch):
    async def empty_list(*_a, **_kw):
        return []

    async def empty_progress(*_a, **_kw):
        return []

    monkeypatch.setattr(fms_canonical, "list_canonical_formations", empty_list)
    monkeypatch.setattr(fms_canonical, "get_user_canonical_progress", empty_progress)
    monkeypatch.setattr(klt_canonical, "list_canonical_klt_formations", empty_list)
    monkeypatch.setattr(klt_canonical, "get_user_klt_progress", empty_progress)
    monkeypatch.setattr(kor_canonical, "list_canonical_kor_formations", empty_list)
    monkeypatch.setattr(kor_canonical, "get_user_kor_progress", empty_progress)

    from services.canonical_convergence import get_canonical_progress_summary

    summary = await get_canonical_progress_summary("user-1")
    assert summary["canonical_modules_total"] == 0
    assert summary["canonical_progress_pct"] == 0


# --------------------------------------------------------------------
# Wired end-to-end into the two real progression surfaces + the
# learning-path surface, against mongomock_motor for the legacy side —
# proves the convergence actually reaches the response, additively.
# --------------------------------------------------------------------


def _user() -> User:
    return User(
        frek_id="FREK-1",
        email="learner@example.com",
        display_name="Learner",
        password_hash="x",
        role="student",
        metier_vise="FMS",
        stade="graine",
        cc_credits=0,
    )


@pytest.fixture
async def legacy_db(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_convergence_test"]
    monkeypatch.setattr(progression_module, "db", mock_db)
    monkeypatch.setattr(learning_module, "db", mock_db)
    return mock_db


@pytest.mark.asyncio
async def test_progression_summary_carries_canonical_key(
    legacy_db, stub_canonical
):
    result = await progression_module.progression_summary(current=_user())
    assert "canonical" in result
    assert result["canonical"]["canonical_modules_viewed"] == 2
    # Legacy fields stay exactly as before — untouched shape.
    assert result["completed_modules"] == 0
    assert result["total_modules"] == 0


@pytest.mark.asyncio
async def test_frek_profile_carries_canonical_key(legacy_db, stub_canonical):
    result = await progression_module.frek_profile(current=_user())
    assert "canonical" in result
    assert result["canonical"]["canonical_modules_viewed"] == 2
    assert result["modules_completed"] == 0


@pytest.mark.asyncio
async def test_learning_path_carries_canonical_key(legacy_db, stub_canonical):
    result = await learning_module.user_learning_path(current=_user())
    assert "canonical" in result
    assert result["canonical"]["canonical_modules_total"] == 12
    # Legacy shape untouched.
    assert result["own_pole"] == []
    assert result["other_poles"] == []
