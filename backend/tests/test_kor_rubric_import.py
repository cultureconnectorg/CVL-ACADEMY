"""ACA-0020 — real N1/N2/A01 assessment-chain runtime binding, KOR proof.

Real gap this closes: `certification/service.py`'s eligibility check
already reads real canonical KOR progress (RAIL 2), but zero `Rubric`
documents ever existed for any canonical formation — every canonical
certification attempt 404'd on `get_rubric` before eligibility was even
reached. `kor_canonical/rubric_import.py` converts the real, already-
imported `assessments/RUBRIC.md` markdown (parsed into `db.kor_resources`
by `import_pipeline.py`) into a real, gradable `Rubric`.

This suite proves two separate things:
1. **The parser is correct against the real files**, not a synthetic
   fixture that happens to match the parser's own assumptions — every
   one of the 15 real `docs/kor/korXX/assessments/RUBRIC.md` files is
   read directly off disk and parsed.
2. **The resulting `Rubric` is genuinely gradable** by the existing,
   unmodified `certification.scoring.compute_scores` — an eliminatory
   criterion scoring 0 fails the attempt exactly as it would for a
   legacy FMS rubric, proving this isn't just a data-shape match but a
   real, working grading path.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from mongomock_motor import AsyncMongoMockClient

import kor_canonical.rubric_import as rubric_import_module
from certification.models import Rubric
from certification.scoring import compute_scores
from kor_canonical.rubric_import import (
    KOR_RUBRIC_PASS_THRESHOLD_PCT,
    certification_code_for,
    import_rubric_for_formation,
    parse_rubric_criteria,
)

REAL_KOR_DOCS = Path(__file__).resolve().parents[2] / "docs" / "kor"
REAL_KOR09_RUBRIC = (REAL_KOR_DOCS / "kor09" / "assessments" / "RUBRIC.md").read_text()


# ---------------- parser correctness against every real file ----------------


@pytest.mark.parametrize("n", range(1, 16))
def test_parses_every_real_kor_rubric_file(n):
    path = REAL_KOR_DOCS / f"kor{n:02d}" / "assessments" / "RUBRIC.md"
    assert path.exists(), f"real fixture missing: {path}"
    criteria = parse_rubric_criteria(path.read_text())
    # Every real file carries at least a handful of real criteria — a
    # parser regression (e.g. a header wording change breaking the
    # regex) would show up as 0, not a plausible real number.
    assert len(criteria) >= 8
    assert all(c.max_score == 4.0 for c in criteria)
    assert all(c.bloc == "A01" for c in criteria)
    assert all(c.skill_id is None for c in criteria)
    # ids are unique and match the real markdown's own numbering
    assert [c.id for c in criteria] == [f"C{i}" for i in range(1, len(criteria) + 1)]


def test_kor09_matches_the_real_document_by_hand():
    """One file cross-checked by hand against the real markdown text
    (reproduced in the module docstring of kor_canonical/rubric_import.py
    and this file's own docstring) — not just "the parser agrees with
    itself" but "the parser agrees with what a human reading the real
    file would conclude"."""
    criteria = parse_rubric_criteria(REAL_KOR09_RUBRIC)
    assert len(criteria) == 11
    assert criteria[0].label == "Diagnostic basé sur données réelles"
    assert criteria[6].id == "C7"
    assert criteria[6].is_eliminatory is True  # "Rétention... | ≥3 | **oui**"
    assert criteria[9].id == "C10"
    assert (
        criteria[9].is_eliminatory is True
    )  # "...| 4 (binaire) | **oui si non conforme**"
    # every other criterion in KOR-09 is non-eliminatory
    non_elim_ids = {c.id for c in criteria if not c.is_eliminatory}
    assert non_elim_ids == {"C1", "C2", "C3", "C4", "C5", "C6", "C8", "C9", "C11"}


def test_certification_code_matches_real_document_heading():
    # The real file's own H1 is "# KOR09-A01 — Grille certificative..."
    assert certification_code_for("KOR-09") == "KOR09-A01"
    assert REAL_KOR09_RUBRIC.startswith("# KOR09-A01")


# ---------------- real import into db.certification_rubrics ----------------


@pytest.fixture
async def kor_resources_db(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_aca0020_kor_rubric_test"]
    monkeypatch.setattr(rubric_import_module, "db", mock_db)
    await mock_db.kor_resources.insert_one(
        {
            "source_file": "kor09/assessments/RUBRIC.md",
            "type": "rubric",
            "formation_code": "KOR-09",
            "canonical_version": "test",
            "body_markdown": REAL_KOR09_RUBRIC,
        }
    )
    return mock_db


@pytest.mark.asyncio
async def test_import_creates_real_rubric_document(kor_resources_db):
    result = await import_rubric_for_formation("KOR-09")
    assert result is not None
    assert len(result.criteria) == 11
    assert result.level == "A01"
    assert result.formation_code == "KOR-09"
    assert result.pass_threshold_pct == KOR_RUBRIC_PASS_THRESHOLD_PCT

    stored = await kor_resources_db.certification_rubrics.find_one(
        {"certification_code": "KOR09-A01"}, {"_id": 0}
    )
    assert stored is not None
    assert stored["formation_code"] == "KOR-09"
    assert len(stored["criteria"]) == 11


@pytest.mark.asyncio
async def test_import_is_idempotent_upsert_not_duplicate(kor_resources_db):
    await import_rubric_for_formation("KOR-09")
    await import_rubric_for_formation("KOR-09")  # re-run, e.g. after a docs update
    count = await kor_resources_db.certification_rubrics.count_documents(
        {"certification_code": "KOR09-A01"}
    )
    assert count == 1


@pytest.mark.asyncio
async def test_import_returns_none_for_unimported_formation(kor_resources_db):
    result = await import_rubric_for_formation("KOR-99")
    assert result is None


# ---------------- the resulting Rubric is genuinely gradable ----------------


@pytest.mark.asyncio
async def test_imported_rubric_is_scored_by_the_real_engine(kor_resources_db):
    """Proves this isn't just a data-shape match: the imported Rubric,
    fed into the SAME `compute_scores` every legacy FMS attempt uses,
    produces a real, correct eliminated/passed verdict."""
    await import_rubric_for_formation("KOR-09")
    stored = await kor_resources_db.certification_rubrics.find_one(
        {"certification_code": "KOR09-A01"}, {"_id": 0}
    )
    rubric = Rubric(**stored)

    # A candidate who scores well everywhere except the real eliminatory
    # criterion C7 (raw 0) must be eliminated, exactly like FMS-01's own
    # eliminatory-criterion behavior — never merely "a low score."
    raw_scores = {c.id: 4.0 for c in rubric.criteria}
    raw_scores["C7"] = 0.0
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
    assert "C7" in (eliminated_reason or "")
    # a near-perfect score everywhere else — eliminatory is the ONLY
    # reason this attempt fails, proving it isn't the average dragging
    # it down
    assert score_global > KOR_RUBRIC_PASS_THRESHOLD_PCT

    # The same candidate, scoring the same everywhere but a real (not
    # eliminatory-triggering) 4 on C7 instead, passes on the real 2,5/4
    # global threshold this rubric imports.
    raw_scores["C7"] = 4.0
    (
        _by_competency2,
        _by_bloc2,
        score_global2,
        passed2,
        eliminated2,
        _reason2,
        _mention2,
    ) = compute_scores(rubric, raw_scores)
    assert eliminated2 is False
    assert passed2 is True
    assert score_global2 == 100.0
