"""ACA-0020 — real N1/N2/A01 assessment-chain runtime binding, FMS-07..18
(specialization formations) proof. See `fms_canonical/spec_rubric_
import.py`'s own docstring for why this domain needed a different
import path than KOR/KLT (reads the real filesystem directly, not
`db.fms_resources` — that collection never gets these 9 files, since
`fms_import`'s own filename classifier doesn't recognize
`ASSESSMENT_AND_RUBRIC.md`, confirmed before writing this module)."""

from __future__ import annotations

from pathlib import Path

import pytest
from mongomock_motor import AsyncMongoMockClient

import fms_canonical.spec_rubric_import as spec_rubric_import_module
from certification.models import Rubric
from certification.scoring import compute_scores
from fms_canonical.spec_rubric_import import (
    FMS_SPEC_FORMATION_CODES,
    FMS_SPEC_RUBRIC_PASS_THRESHOLD_PCT,
    certification_code_for,
    import_rubric_for_formation,
    parse_rubric_criteria,
)

REAL_FMS_DOCS = Path(__file__).resolve().parents[2] / "docs" / "fms"
REAL_FMS09_RUBRIC = (REAL_FMS_DOCS / "fms09" / "ASSESSMENT_AND_RUBRIC.md").read_text()


# ---------------- parser correctness against every real file ----------------


@pytest.mark.parametrize("formation_code", FMS_SPEC_FORMATION_CODES)
def test_parses_every_real_fms_spec_rubric_file(formation_code):
    num = formation_code.split("-")[-1]
    path = REAL_FMS_DOCS / f"fms{num}" / "ASSESSMENT_AND_RUBRIC.md"
    assert path.exists(), f"real fixture missing: {path}"
    criteria = parse_rubric_criteria(path.read_text())
    assert len(criteria) >= 3
    assert all(c.max_score == 4.0 for c in criteria)
    assert all(c.bloc == "A01" for c in criteria)
    # Every competency is eliminatory-if-zero — the document's own "Seuil
    # de passage" line states this universally, not per-row.
    assert all(c.is_eliminatory is True for c in criteria)
    assert [c.id for c in criteria] == [f"C{i}" for i in range(1, len(criteria) + 1)]


def test_fms09_matches_the_real_document_by_hand():
    criteria = parse_rubric_criteria(REAL_FMS09_RUBRIC)
    assert len(criteria) == 3
    assert criteria[0].id == "C1"
    assert (
        "mix" in criteria[0].label.lower() or "mastering" in criteria[0].label.lower()
    )
    assert all(c.is_eliminatory for c in criteria)


def test_certification_code_convention():
    assert certification_code_for("FMS-09") == "FMS09-A01"
    assert certification_code_for("FMS-18") == "FMS18-A01"


def test_only_the_9_real_formations_are_recognized():
    assert FMS_SPEC_FORMATION_CODES == [
        "FMS-07",
        "FMS-08",
        "FMS-09",
        "FMS-10",
        "FMS-11",
        "FMS-12",
        "FMS-13",
        "FMS-15",
        "FMS-18",
    ]
    # FMS-14/16/17 are named in CERTIFICATION_MODEL.md's range but not
    # yet built — never silently claimed as importable.
    assert "FMS-14" not in FMS_SPEC_FORMATION_CODES
    assert "FMS-16" not in FMS_SPEC_FORMATION_CODES
    assert "FMS-17" not in FMS_SPEC_FORMATION_CODES


# ---------------- real import into db.certification_rubrics ----------------


@pytest.fixture
async def fms_rubric_db(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_aca0020_fms_spec_rubric_test"]
    monkeypatch.setattr(spec_rubric_import_module, "db", mock_db)
    return mock_db


@pytest.mark.asyncio
async def test_import_reads_real_filesystem_and_creates_rubric(fms_rubric_db):
    result = await import_rubric_for_formation("FMS-09")
    assert result is not None
    assert result.formation_code == "FMS-09"
    assert result.pass_threshold_pct == FMS_SPEC_RUBRIC_PASS_THRESHOLD_PCT
    assert len(result.criteria) == 3

    stored = await fms_rubric_db.certification_rubrics.find_one(
        {"certification_code": "FMS09-A01"}, {"_id": 0}
    )
    assert stored is not None
    assert stored["formation_code"] == "FMS-09"


@pytest.mark.asyncio
async def test_import_is_idempotent(fms_rubric_db):
    await import_rubric_for_formation("FMS-09")
    await import_rubric_for_formation("FMS-09")
    count = await fms_rubric_db.certification_rubrics.count_documents(
        {"certification_code": "FMS09-A01"}
    )
    assert count == 1


@pytest.mark.asyncio
async def test_import_returns_none_for_formation_outside_the_real_9(fms_rubric_db):
    # FMS-14 is named in the shared range but has no built directory.
    assert await import_rubric_for_formation("FMS-14") is None
    # FMS-01 is real but belongs to the ZIP-import path, not this one.
    assert await import_rubric_for_formation("FMS-01") is None
    # Not an FMS code at all.
    assert await import_rubric_for_formation("KOR-01") is None


@pytest.mark.asyncio
async def test_import_all_9_real_formations(fms_rubric_db):
    for code in FMS_SPEC_FORMATION_CODES:
        result = await import_rubric_for_formation(code)
        assert result is not None, f"{code} should import"
        assert len(result.criteria) >= 3


# ---------------- the resulting Rubric is genuinely gradable ----------------


@pytest.mark.asyncio
async def test_imported_rubric_is_scored_by_the_real_engine(fms_rubric_db):
    await import_rubric_for_formation("FMS-09")
    stored = await fms_rubric_db.certification_rubrics.find_one(
        {"certification_code": "FMS09-A01"}, {"_id": 0}
    )
    rubric = Rubric(**stored)

    raw_scores = {c.id: 4.0 for c in rubric.criteria}
    raw_scores["C1"] = 0.0  # any competency at 0 fails, per the real doctrine
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
    assert score_global > FMS_SPEC_RUBRIC_PASS_THRESHOLD_PCT


@pytest.mark.asyncio
async def test_all_competencies_at_full_score_passes(fms_rubric_db):
    await import_rubric_for_formation("FMS-09")
    stored = await fms_rubric_db.certification_rubrics.find_one(
        {"certification_code": "FMS09-A01"}, {"_id": 0}
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
