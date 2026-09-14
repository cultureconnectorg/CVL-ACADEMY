"""ACA-0020 — real N1/N2/A01 assessment-chain runtime binding, KLT
(second-domain) proof. See `tests/test_kor_rubric_import.py`'s own
docstring for the shared reasoning; this suite is the same contract
against the KLT domain, plus one thing KOR alone didn't cover: KLT's
own eliminatory-cell wording variant (`"**oui si absent**"`, never
seen in KOR's files), the exact reason `_is_eliminatory_cell` matches
the `"**oui"` prefix rather than an enumerated string set.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from mongomock_motor import AsyncMongoMockClient

import klt_canonical.rubric_import as rubric_import_module
from certification.models import Rubric
from certification.scoring import compute_scores
from klt_canonical.rubric_import import (
    KLT_RUBRIC_PASS_THRESHOLD_PCT,
    certification_code_for,
    import_rubric_for_formation,
    parse_rubric_criteria,
)

REAL_KLT_DOCS = Path(__file__).resolve().parents[2] / "docs" / "klt"
# The 10 real formations confirmed (by filesystem sweep) to carry an
# assessments/RUBRIC.md — KLT-09..12/14..17/19/20 do not, and are not
# claimed to by this suite.
REAL_KLT_RUBRIC_FORMATIONS = [
    "01",
    "02",
    "03",
    "04",
    "05",
    "06",
    "07",
    "08",
    "13",
    "18",
]
REAL_KLT05_RUBRIC = (REAL_KLT_DOCS / "klt05" / "assessments" / "RUBRIC.md").read_text()


# ---------------- parser correctness against every real file ----------------


@pytest.mark.parametrize("suffix", REAL_KLT_RUBRIC_FORMATIONS)
def test_parses_every_real_klt_rubric_file(suffix):
    path = REAL_KLT_DOCS / f"klt{suffix}" / "assessments" / "RUBRIC.md"
    assert path.exists(), f"real fixture missing: {path}"
    criteria = parse_rubric_criteria(path.read_text())
    assert len(criteria) >= 6
    assert all(c.max_score == 4.0 for c in criteria)
    assert all(c.bloc == "A01" for c in criteria)
    assert [c.id for c in criteria] == [f"C{i}" for i in range(1, len(criteria) + 1)]


def test_klt05_matches_the_real_document_by_hand():
    """KLT-05 was chosen for the hand cross-check specifically because
    it's the first formation using the `"**oui si absent**"` wording
    (KLT-01..04 use `"**oui si non conforme**"`, same as KOR)."""
    criteria = parse_rubric_criteria(REAL_KLT05_RUBRIC)
    # Real file: criterion 2 is "Accès/rôle respecté... | ≥3 | **oui**",
    # a later one uses the "si absent" qualifier — both must resolve to
    # is_eliminatory=True.
    assert criteria[1].id == "C2"
    assert criteria[1].is_eliminatory is True
    elim_ids = {c.id for c in criteria if c.is_eliminatory}
    assert len(elim_ids) >= 1


def test_certification_code_matches_real_document_heading():
    assert certification_code_for("KLT-06") == "KLT06-A01"
    real_klt06 = (REAL_KLT_DOCS / "klt06" / "assessments" / "RUBRIC.md").read_text()
    assert real_klt06.startswith("# KLT06-A01")


def test_eliminatory_prefix_matches_both_real_klt_wordings():
    """The exact regression this parser had to be generalized against:
    KOR's own rubrics never use "si absent"; KLT's do, for over half
    its rubrics (KLT-05/06/07/08/13/18). Both must be detected."""
    from klt_canonical.rubric_import import _is_eliminatory_cell

    assert _is_eliminatory_cell("**oui**") is True
    assert _is_eliminatory_cell("**oui si non conforme**") is True
    assert _is_eliminatory_cell("**oui si absent**") is True
    assert _is_eliminatory_cell("non") is False


# ---------------- real import into db.certification_rubrics ----------------


@pytest.fixture
async def klt_resources_db(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_aca0020_klt_rubric_test"]
    monkeypatch.setattr(rubric_import_module, "db", mock_db)
    await mock_db.klt_resources.insert_one(
        {
            "source_file": "klt05/assessments/RUBRIC.md",
            "type": "rubric",
            "formation_code": "KLT-05",
            "canonical_version": "test",
            "body_markdown": REAL_KLT05_RUBRIC,
        }
    )
    return mock_db


@pytest.mark.asyncio
async def test_import_creates_real_rubric_document(klt_resources_db):
    result = await import_rubric_for_formation("KLT-05")
    assert result is not None
    assert result.formation_code == "KLT-05"
    assert result.pass_threshold_pct == KLT_RUBRIC_PASS_THRESHOLD_PCT

    stored = await klt_resources_db.certification_rubrics.find_one(
        {"certification_code": "KLT05-A01"}, {"_id": 0}
    )
    assert stored is not None
    assert stored["formation_code"] == "KLT-05"


@pytest.mark.asyncio
async def test_import_returns_none_for_formation_without_rubric(klt_resources_db):
    # KLT-09 genuinely has no assessments/RUBRIC.md (confirmed by sweep).
    result = await import_rubric_for_formation("KLT-09")
    assert result is None


# ---------------- the resulting Rubric is genuinely gradable ----------------


@pytest.mark.asyncio
async def test_imported_rubric_is_scored_by_the_real_engine(klt_resources_db):
    await import_rubric_for_formation("KLT-05")
    stored = await klt_resources_db.certification_rubrics.find_one(
        {"certification_code": "KLT05-A01"}, {"_id": 0}
    )
    rubric = Rubric(**stored)

    raw_scores = {c.id: 4.0 for c in rubric.criteria}
    raw_scores["C2"] = 0.0  # the real eliminatory criterion in KLT-05
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
    assert "C2" in (eliminated_reason or "")
    assert score_global > KLT_RUBRIC_PASS_THRESHOLD_PCT
