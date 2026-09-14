"""ACA-0020 — real N1/N2/A01 assessment-chain runtime binding, FRK
(FREK, fourth domain) proof. See `frk_canonical/rubric_import.py`'s own
docstring for the real corpus shape variance this parser was written
against (named-competency shape vs. single global grille shape) and
the explicit formative-only exclusion (FRK-10/14/73)."""

from __future__ import annotations

from pathlib import Path

import pytest
from mongomock_motor import AsyncMongoMockClient

import frk_canonical.rubric_import as rubric_import_module
from certification.models import Rubric
from certification.scoring import compute_scores
from frk_canonical.rubric_import import (
    FRK_RUBRIC_PASS_THRESHOLD_PCT,
    certification_code_for,
    import_rubric_for_formation,
    parse_rubric_criteria,
)

REAL_FRK_DOCS = Path(__file__).resolve().parents[2] / "docs" / "frk"

# Every real formation confirmed (by filesystem sweep) to have a built
# ASSESSMENT_AND_RUBRIC.md, whatever its shape.
ALL_REAL_FRK_RUBRIC_FILES = sorted(
    p.parent.name for p in REAL_FRK_DOCS.glob("frk*/ASSESSMENT_AND_RUBRIC.md")
)

# The 3 real formations that explicitly state they are formative-only /
# not yet certifiable (NEEDS_EXPERT_REVIEW unresolved) — confirmed by
# grep sweep, never assumed rare.
NOT_CERTIFIABLE_YET = {"frk10", "frk14", "frk73"}

REAL_FRK09_RUBRIC = (
    REAL_FRK_DOCS / "frk09" / "ASSESSMENT_AND_RUBRIC.md"
).read_text()
REAL_FRK23_RUBRIC = (
    REAL_FRK_DOCS / "frk23" / "ASSESSMENT_AND_RUBRIC.md"
).read_text()
REAL_FRK14_RUBRIC = (
    REAL_FRK_DOCS / "frk14" / "ASSESSMENT_AND_RUBRIC.md"
).read_text()


def test_at_least_50_real_files_confirmed():
    # Sanity floor so a future filesystem regression can't silently
    # shrink the corpus this suite exercises.
    assert len(ALL_REAL_FRK_RUBRIC_FILES) >= 50


# ---------------- parser correctness against every real file ----------------


@pytest.mark.parametrize("dirname", ALL_REAL_FRK_RUBRIC_FILES)
def test_parses_every_real_frk_rubric_file(dirname):
    path = REAL_FRK_DOCS / dirname / "ASSESSMENT_AND_RUBRIC.md"
    criteria = parse_rubric_criteria(path.read_text())
    if dirname in NOT_CERTIFIABLE_YET:
        # These are still parseable as text (the parser itself doesn't
        # know about certifiability), but import_rubric_for_formation
        # must refuse them — see the dedicated tests below.
        return
    assert len(criteria) >= 1, f"{dirname}: expected at least 1 criterion"
    assert all(c.max_score == 4.0 for c in criteria)
    assert all(c.bloc == "A01" for c in criteria)
    assert all(c.is_eliminatory is True for c in criteria)


def test_named_competency_shape_frk09():
    criteria = parse_rubric_criteria(REAL_FRK09_RUBRIC)
    assert len(criteria) == 2
    assert criteria[0].id == "C1"
    assert criteria[1].id == "C2"


def test_single_global_grille_shape_frk23():
    """FRK-23 has no named competency table at all — one shared 0-4
    grille for the whole formation, which must reduce to exactly one
    criterion, never zero and never a fabricated multi-row split."""
    criteria = parse_rubric_criteria(REAL_FRK23_RUBRIC)
    assert len(criteria) == 1
    assert criteria[0].id == "C1"
    assert criteria[0].max_score == 4.0
    assert criteria[0].is_eliminatory is True


def test_certification_code_convention():
    assert certification_code_for("FRK-09") == "FRK09-A01"
    assert certification_code_for("FRK-23") == "FRK23-A01"


# ---------------- real import into db.certification_rubrics ----------------


@pytest.fixture
async def frk_resources_db(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_aca0020_frk_rubric_test"]
    monkeypatch.setattr(rubric_import_module, "db", mock_db)
    await mock_db.frk_resources.insert_many(
        [
            {
                "source_file": "frk09/ASSESSMENT_AND_RUBRIC.md",
                "type": "assessment_and_rubric",
                "formation_code": "FRK-09",
                "body_markdown": REAL_FRK09_RUBRIC,
            },
            {
                "source_file": "frk23/ASSESSMENT_AND_RUBRIC.md",
                "type": "assessment_and_rubric",
                "formation_code": "FRK-23",
                "body_markdown": REAL_FRK23_RUBRIC,
            },
            {
                "source_file": "frk14/ASSESSMENT_AND_RUBRIC.md",
                "type": "assessment_and_rubric",
                "formation_code": "FRK-14",
                "body_markdown": REAL_FRK14_RUBRIC,
            },
        ]
    )
    return mock_db


@pytest.mark.asyncio
async def test_import_creates_real_rubric_named_competency_shape(frk_resources_db):
    result = await import_rubric_for_formation("FRK-09")
    assert result is not None
    assert result.formation_code == "FRK-09"
    assert result.pass_threshold_pct == FRK_RUBRIC_PASS_THRESHOLD_PCT
    assert len(result.criteria) == 2

    stored = await frk_resources_db.certification_rubrics.find_one(
        {"certification_code": "FRK09-A01"}, {"_id": 0}
    )
    assert stored is not None


@pytest.mark.asyncio
async def test_import_creates_real_rubric_grille_shape(frk_resources_db):
    result = await import_rubric_for_formation("FRK-23")
    assert result is not None
    assert len(result.criteria) == 1


@pytest.mark.asyncio
async def test_import_refuses_formative_only_formation(frk_resources_db):
    """FRK-14 explicitly states no certification can be delivered yet
    (NEEDS_EXPERT_REVIEW unresolved) — importing a live gradable Rubric
    for it would contradict the document's own stated status."""
    result = await import_rubric_for_formation("FRK-14")
    assert result is None

    stored = await frk_resources_db.certification_rubrics.find_one(
        {"certification_code": "FRK14-A01"}
    )
    assert stored is None


@pytest.mark.asyncio
async def test_import_returns_none_for_unimported_formation(frk_resources_db):
    assert await import_rubric_for_formation("FRK-99") is None  # not a real code
    assert await import_rubric_for_formation("FRK-01") is None  # real, not imported here
    assert await import_rubric_for_formation("KOR-01") is None  # wrong domain


@pytest.mark.asyncio
async def test_import_is_idempotent(frk_resources_db):
    await import_rubric_for_formation("FRK-09")
    await import_rubric_for_formation("FRK-09")
    count = await frk_resources_db.certification_rubrics.count_documents(
        {"certification_code": "FRK09-A01"}
    )
    assert count == 1


# ---------------- the resulting Rubric is genuinely gradable ----------------


@pytest.mark.asyncio
async def test_imported_rubric_is_scored_by_the_real_engine(frk_resources_db):
    await import_rubric_for_formation("FRK-09")
    stored = await frk_resources_db.certification_rubrics.find_one(
        {"certification_code": "FRK09-A01"}, {"_id": 0}
    )
    rubric = Rubric(**stored)

    raw_scores = {c.id: 4.0 for c in rubric.criteria}
    raw_scores["C1"] = 0.0
    (
        _by_competency,
        _by_bloc,
        score_global,
        passed,
        eliminated,
        eliminated_reason,
        _mention,
    ) = compute_scores(rubric, raw_scores)

    assert eliminated is True
    assert passed is False
    assert "C1" in (eliminated_reason or "")
    # 2 criteria, one at 0 / one at max — the raw average alone (50%)
    # would already fail the 62.5% threshold, but the elimination flag
    # is what actually fails the attempt (not the average), which is
    # the real point of this assertion.
    assert eliminated_reason is not None


@pytest.mark.asyncio
async def test_grille_shape_single_criterion_full_score_passes(frk_resources_db):
    await import_rubric_for_formation("FRK-23")
    stored = await frk_resources_db.certification_rubrics.find_one(
        {"certification_code": "FRK23-A01"}, {"_id": 0}
    )
    rubric = Rubric(**stored)

    raw_scores = {c.id: 4.0 for c in rubric.criteria}
    (
        _by_competency,
        _by_bloc,
        score_global,
        passed,
        eliminated,
        _eliminated_reason,
        _mention,
    ) = compute_scores(rubric, raw_scores)

    assert eliminated is False
    assert passed is True
    assert score_global == 100.0
