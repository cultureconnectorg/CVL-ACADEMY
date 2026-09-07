"""Canonical FREK (FRK) runtime binding — "raccorder ces corpus au
même runtime/funnel Academy" (Founder instruction, 2026-09-07).

Gate this suite proves: the real `docs/frk/` corpus (75 real
candidates, 57 with importable content — 54 `PACKAGE_COMPLETE` + 3
`MODULE_CONTENT_DRAFTED`/`NEEDS_EXPERT_REVIEW`, 10 `GAP.md`-only
`BLOCKED_PRODUCT_DEPENDENCY`, 8 codes with no directory at all
`EXTEND_EXISTING`) imports correctly, is readable through
`frk_canonical`'s own read model, tracks real per-learner progress, and
is wired — additively, without disturbing FMS/KLT/KOR — into
`services/canonical_convergence.py`'s next_action/progress-summary
convergence.

No `import_kor_docs`-style fixture corpus here: same rationale as
`test_klt_canonical.py`/`test_rail2_kor01_e2e.py` — the real `docs/frk/`
tree already lives unpacked in this repo, so these tests import it
directly rather than fabricating a synthetic one.
"""

from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

import frk_canonical.import_pipeline as frk_import_pipeline_module
import frk_canonical.progress as frk_progress_module
import frk_canonical.provenance as frk_provenance_module
import frk_canonical.read_model as frk_read_model_module
from frk_canonical.import_pipeline import import_frk_docs
from frk_canonical.models import FRK_FORMATION_CODES
from frk_canonical.parser import (canonical_module_code, classify_resource_type,
                                  extract_formation_title, extract_status,
                                  formation_code_from_path, parse_modules_section)
from frk_canonical.progress import get_user_frk_progress, record_content_viewed
from frk_canonical.provenance import list_real_files
from frk_canonical.read_model import (get_canonical_frk_formation,
                                      get_canonical_frk_module,
                                      list_canonical_frk_formations,
                                      list_canonical_frk_modules)


# --------------------------------------------------------------------
# Parser — pure functions, read directly against real docs/frk/ files
# --------------------------------------------------------------------


def _read(rel_path: str) -> str:
    from frk_canonical.provenance import default_docs_dir

    return (default_docs_dir() / rel_path).read_text(encoding="utf-8")


def test_formation_code_from_path():
    assert formation_code_from_path("frk01/REFERENTIAL.md") == "FRK-01"
    assert formation_code_from_path("frk75/GUIDE_JURY.md") == "FRK-75"
    assert formation_code_from_path("README.md") is None


def test_classify_resource_type_recognizes_every_real_filename():
    assert classify_resource_type("frk01/REFERENTIAL.md") == "referential"
    assert classify_resource_type("frk01/BANQUE_N1.md") == "n1_question_bank"
    assert classify_resource_type("frk01/BANQUE_N2.md") == "n2_evaluations"
    assert classify_resource_type("frk01/ASSESSMENT_AND_RUBRIC.md") == "assessment_and_rubric"
    assert classify_resource_type("frk01/EVIDENCE_MODEL.md") == "evidence_model"
    assert classify_resource_type("frk01/GUIDE_CANDIDAT.md") == "candidate_guide"
    assert classify_resource_type("frk01/GUIDE_CORRECTEUR.md") == "corrector_guide"
    assert classify_resource_type("frk01/GUIDE_JURY.md") == "jury_guide"
    assert classify_resource_type("frk01/INTEGRATION_NOTE.md") == "integration_note"
    assert classify_resource_type("frk19/GAP.md") == "gap"
    assert classify_resource_type("frk01/UNKNOWN_FILE.md") is None


def test_canonical_module_code():
    assert canonical_module_code("FRK-01", 2) == "FRK01-M02"
    assert canonical_module_code("FRK-75", 10) == "FRK75-M10"


def test_parse_frk01_referential_flagship():
    text = _read("frk01/REFERENTIAL.md")
    assert extract_formation_title(text).startswith("FREK Foundations")
    status, needs_review = extract_status(text)
    assert status == "PACKAGE_COMPLETE"
    assert needs_review is False
    modules = parse_modules_section(text)
    assert len(modules) == 4
    assert modules[0]["order_index"] == 1
    assert modules[0]["title"] == "System map"
    assert modules[0]["description"]


def test_parse_frk10_needs_expert_review_plain_sentence_modules():
    """FRK-10's real "## Modules" items carry no bold title — the
    parser's fallback path (whole sentence -> title, description=None)
    must never fabricate a split that isn't there."""
    text = _read("frk10/REFERENTIAL.md")
    status, needs_review = extract_status(text)
    assert status == "MODULE_CONTENT_DRAFTED"
    assert needs_review is True
    modules = parse_modules_section(text)
    assert len(modules) == 3
    assert modules[0]["title"] == "eIDAS2/EUDI Wallet regulatory framework (EU-specific)."
    assert modules[0]["description"] is None


# --------------------------------------------------------------------
# Provenance — every real file under docs/frk/ accounted for
# --------------------------------------------------------------------


def test_list_real_files_finds_the_real_corpus():
    from frk_canonical.provenance import default_docs_dir

    files = list_real_files(default_docs_dir())
    assert len(files) > 0
    # frk19 is a real, GAP.md-only BLOCKED_PRODUCT_DEPENDENCY formation
    # — its one real file must still be inventoried (provenance's
    # "parsed or not, never dropped" discipline), even though it never
    # becomes a formation (see the import-pipeline test below).
    assert any(p.name == "GAP.md" and "frk19" in str(p) for p in files)


# --------------------------------------------------------------------
# Import pipeline + read model — end-to-end against the real corpus
# --------------------------------------------------------------------


@pytest.fixture
async def frk_db(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_frk_canonical_test"]
    for module in (
        frk_import_pipeline_module,
        frk_provenance_module,
        frk_read_model_module,
        frk_progress_module,
    ):
        monkeypatch.setattr(module, "db", mock_db)
    return mock_db


@pytest.mark.asyncio
async def test_import_frk_docs_accounts_for_every_real_file(frk_db):
    report = await import_frk_docs()
    assert report.all_files_accounted_for is True
    assert report.total_files > 0
    assert report.parsed_count > 0
    # 57 real REFERENTIAL.md-bearing formations found — the 10 GAP.md
    # only and 8 no-directory codes are never counted as "found".
    assert len(report.formations_found) == 57
    assert "FRK-01" in report.formations_found
    assert "FRK-10" in report.formations_found  # NEEDS_EXPERT_REVIEW, still real content
    assert "FRK-19" not in report.formations_found  # GAP.md only
    assert "FRK-05" not in report.formations_found  # EXTEND_EXISTING, no directory


@pytest.mark.asyncio
async def test_get_canonical_frk_formation_frk01_flagship(frk_db):
    await import_frk_docs()
    formation = await get_canonical_frk_formation("FRK-01")
    assert formation is not None
    assert formation.frk_formation_code == "FRK-01"
    assert formation.title.startswith("FREK Foundations")
    assert formation.status == "PACKAGE_COMPLETE"
    assert formation.fully_complete is True
    assert formation.needs_expert_review is False
    assert formation.module_count == 4
    assert formation.module_codes_in_order == [
        "FRK01-M01",
        "FRK01-M02",
        "FRK01-M03",
        "FRK01-M04",
    ]
    assert formation.certification_scope == "FULL"


@pytest.mark.asyncio
async def test_get_canonical_frk_formation_needs_expert_review_never_fully_complete(frk_db):
    await import_frk_docs()
    formation = await get_canonical_frk_formation("FRK-10")
    assert formation is not None
    assert formation.status == "MODULE_CONTENT_DRAFTED"
    assert formation.needs_expert_review is True
    # NEEDS_EXPERT_REVIEW = never `fully_complete`, no matter how much
    # real content exists — same discipline the corpus's own README
    # applies.
    assert formation.fully_complete is False
    assert formation.certification_scope == "PARTIAL"


@pytest.mark.asyncio
async def test_blocked_and_extend_existing_codes_never_become_formations(frk_db):
    await import_frk_docs()
    # FRK-19: real GAP.md file exists, but no REFERENTIAL.md -> never
    # fabricated as a formation.
    assert await get_canonical_frk_formation("FRK-19") is None
    # FRK-05: no directory at all (EXTEND_EXISTING, folds into a
    # sibling) -> same honest absence.
    assert await get_canonical_frk_formation("FRK-05") is None


@pytest.mark.asyncio
async def test_list_canonical_frk_formations_returns_exactly_the_57_real_ones(frk_db):
    await import_frk_docs()
    formations = await list_canonical_frk_formations()
    codes = {f.frk_formation_code for f in formations}
    assert len(codes) == 57
    assert codes <= set(FRK_FORMATION_CODES)
    assert "FRK-19" not in codes
    assert "FRK-05" not in codes


@pytest.mark.asyncio
async def test_get_canonical_frk_module_is_learner_safe_and_real(frk_db):
    await import_frk_docs()
    module = await get_canonical_frk_module("FRK-01", "FRK01-M01")
    assert module is not None
    assert module.title == "System map"
    assert "FrekCoreClient" in module.content_markdown
    assert module.content_source_file == "frk01/REFERENTIAL.md"
    assert await get_canonical_frk_module("FRK-01", "FRK01-M99") is None


@pytest.mark.asyncio
async def test_list_canonical_frk_modules_matches_formation_order(frk_db):
    await import_frk_docs()
    modules = await list_canonical_frk_modules("FRK-01")
    assert [m.module_code for m in modules] == [
        "FRK01-M01",
        "FRK01-M02",
        "FRK01-M03",
        "FRK01-M04",
    ]


# --------------------------------------------------------------------
# Progress — separate collection, idempotent content_viewed_at
# --------------------------------------------------------------------


@pytest.mark.asyncio
async def test_record_content_viewed_is_idempotent(frk_db):
    await import_frk_docs()
    first = await record_content_viewed("user-1", "FRK-01", "FRK01-M01")
    assert first.content_viewed_at is not None
    second = await record_content_viewed("user-1", "FRK-01", "FRK01-M01")
    assert second.content_viewed_at == first.content_viewed_at

    progress = await get_user_frk_progress("user-1")
    assert len(progress) == 1
    assert progress[0].frk_formation_code == "FRK-01"


# --------------------------------------------------------------------
# Convergence — additive: FMS/KLT/KOR untouched, FRK now included
# --------------------------------------------------------------------


@pytest.fixture
async def convergence_db(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_frk_convergence_test"]
    for module in (
        frk_import_pipeline_module,
        frk_provenance_module,
        frk_read_model_module,
        frk_progress_module,
    ):
        monkeypatch.setattr(module, "db", mock_db)

    import fms_canonical
    import klt_canonical
    import kor_canonical

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
    return mock_db


@pytest.mark.asyncio
async def test_convergence_summary_includes_frk(convergence_db):
    from services.canonical_convergence import get_canonical_progress_summary

    await import_frk_docs()
    summary = await get_canonical_progress_summary("user-1")
    domains = {f["domain"] for f in summary["canonical_formations"]}
    assert "FRK" in domains
    assert summary["canonical_modules_total"] > 0


@pytest.mark.asyncio
async def test_convergence_next_action_falls_through_to_frk_when_others_empty(convergence_db):
    """FMS/KLT/KOR all report empty (see fixture) -> the real convergence
    fallback must reach FRK-01's own first unviewed module — proves the
    additive wiring in `get_first_unviewed_canonical_module` actually
    reaches FRK, not just that FRK's own read model works standalone."""
    from services.canonical_convergence import get_first_unviewed_canonical_module

    await import_frk_docs()
    result = await get_first_unviewed_canonical_module("user-1")
    assert result is not None
    assert result["domain"] == "FRK"
    assert result["formation_code"] == "FRK-01"
    assert result["module_code"] == "FRK01-M01"
    assert result["route"] == "/frek-canonical/FRK-01/FRK01-M01"


@pytest.mark.asyncio
async def test_convergence_next_action_prefers_fms_over_frk_when_both_have_content(
    monkeypatch, convergence_db
):
    """FRK is tried last (see canonical_convergence.py's own docstring)
    — an existing FMS learner must never be redirected to FRK."""
    import fms_canonical
    from fms_canonical.models import CanonicalFormation, CanonicalModule
    from services.canonical_convergence import get_first_unviewed_canonical_module

    async def fms_formations(**_kw):
        return [
            CanonicalFormation(
                canonical_formation_code="FMS-01",
                metier_number="01",
                metier_name="Artist Development",
                module_codes_in_order=["FMS01-M01"],
                module_count=1,
            )
        ]

    async def fms_progress(*_a, **_kw):
        return []

    async def fms_module(formation_code, module_code, **_kw):
        return CanonicalModule(
            canonical_formation_code=formation_code,
            canonical_module_code=module_code,
            order_index=1,
            title="Module Un",
            prerequisites={"status": "UNSPECIFIED"},
        )

    monkeypatch.setattr(fms_canonical, "list_canonical_formations", fms_formations)
    monkeypatch.setattr(fms_canonical, "get_user_canonical_progress", fms_progress)
    monkeypatch.setattr(fms_canonical, "get_canonical_module", fms_module)

    await import_frk_docs()
    result = await get_first_unviewed_canonical_module("user-1")
    assert result["domain"] == "FMS"
