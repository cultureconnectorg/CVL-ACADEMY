"""Canonical Kiltikonet runtime binding tests — "branchage complet de
Kiltikonet" (Founder, 2026-09-04).

Unlike `test_fms_canonical.py`'s synthetic ZIP fixture, this suite runs
the import pipeline directly against the **real** `docs/klt/` tree
already committed in this repo (no upload step exists for KLT — see
`import_pipeline.py`'s module docstring) — so this is both a mechanism
test and a live content verification in one, closer to what ACA-0006's
own by-hand ZIP accounting did for the real FMS archive.

DB-backed pieces run against `mongomock_motor.AsyncMongoMockClient`
(no live MongoDB in this sandbox), same rationale as `test_fms_
canonical.py`.
"""

from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

import klt_canonical.import_pipeline as import_pipeline_module
import klt_canonical.progress as progress_module
import klt_canonical.provenance as provenance_module
import klt_canonical.read_model as read_model_module
from klt_canonical.import_pipeline import import_klt_docs
from klt_canonical.models import KLT_FORMATION_CODES, is_learner_facing
from klt_canonical.parser import parse_skill_registry
from klt_canonical.progress import (get_user_klt_progress,
                                    record_klt_content_viewed)
from klt_canonical.provenance import default_docs_dir, list_real_files
from klt_canonical.read_model import (get_canonical_klt_formation,
                                      get_canonical_klt_module,
                                      list_canonical_klt_formations,
                                      list_canonical_klt_modules,
                                      list_canonical_klt_skills)

# Ground truth, independently recomputed from the real files on disk —
# never copied from a prior report — so a regression in either the repo
# content or the parser shows up as a real assertion failure.
DOCS_DIR = default_docs_dir()
_REAL_FILE_COUNT = len(list_real_files(DOCS_DIR))


@pytest.fixture
async def klt_db(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_klt_canonical_test"]
    for module in (
        import_pipeline_module,
        provenance_module,
        read_model_module,
        progress_module,
    ):
        monkeypatch.setattr(module, "db", mock_db)
    return mock_db


# ---------------------------------------------------------------------
# 1. Real docs/klt/ accounting
# ---------------------------------------------------------------------


def test_real_docs_dir_exists_and_is_nonempty():
    assert DOCS_DIR.is_dir()
    assert _REAL_FILE_COUNT > 0


def test_every_real_file_gets_a_provenance_record():
    from klt_canonical.provenance import build_klt_inventory

    records = build_klt_inventory(DOCS_DIR)
    assert len(records) == _REAL_FILE_COUNT
    # Zero silent loss — every path on disk maps to exactly one record.
    on_disk = {
        str(p.relative_to(DOCS_DIR)).replace("\\", "/")
        for p in list_real_files(DOCS_DIR)
    }
    recorded = {r.original_path for r in records}
    assert on_disk == recorded


async def test_import_accounts_for_every_real_file(klt_db):
    result = await import_klt_docs(DOCS_DIR, created_by="test")
    assert result.total_files == _REAL_FILE_COUNT
    assert result.all_files_accounted_for is True
    assert result.formations_found == KLT_FORMATION_CODES


# ---------------------------------------------------------------------
# 2. fully_complete — the invariant this ticket exists to enforce
# ---------------------------------------------------------------------


async def test_klt01_05_are_fully_complete(klt_db):
    await import_klt_docs(DOCS_DIR, created_by="test")
    for code in ("KLT-01", "KLT-02", "KLT-03", "KLT-04", "KLT-05"):
        formation = await get_canonical_klt_formation(code)
        assert formation is not None, code
        assert formation.fully_complete is True, code
        assert formation.structural_status == "COMPLETE", code
        assert formation.blocked_skill_ids == [], code
        assert formation.certification_scope == "FULL", code


async def test_klt06_07_08_are_not_fully_complete(klt_db):
    """The exact regression this ticket must never allow: KLT-06/07/08
    silently reporting fully_complete=True. Updated 2026-09-07: their
    formerly-BLOCKED competencies are now BUILT_UNCONNECTED (real module
    + content, grounded on a verified real external schema, but no live
    Academy<->Kiltikonet-Aout2026 connection) — structural_status is now
    COMPLETE (every skill has a real module) but fully_complete stays
    False (no BUILT_UNCONNECTED skill may count toward it)."""
    await import_klt_docs(DOCS_DIR, created_by="test")

    formation_06 = await get_canonical_klt_formation("KLT-06")
    assert formation_06.fully_complete is False
    assert formation_06.structural_status == "COMPLETE"
    assert formation_06.blocked_skill_ids == []
    assert set(formation_06.unconnected_skill_ids) == {"KLT06.SKILL.C05", "KLT06.SKILL.C06"}
    assert formation_06.certification_scope == "FULL"

    formation_07 = await get_canonical_klt_formation("KLT-07")
    assert formation_07.fully_complete is False
    assert formation_07.blocked_skill_ids == []
    assert formation_07.unconnected_skill_ids == ["KLT07.SKILL.C04"]

    formation_08 = await get_canonical_klt_formation("KLT-08")
    assert formation_08.fully_complete is False
    assert formation_08.blocked_skill_ids == []
    assert formation_08.unconnected_skill_ids == ["KLT08.SKILL.C04"]


async def test_skill_counts_match_registry_ground_truth(klt_db):
    await import_klt_docs(DOCS_DIR, created_by="test")
    expected = {
        "KLT-01": (11, 0),
        "KLT-02": (11, 0),
        "KLT-03": (12, 0),
        "KLT-04": (14, 0),
        "KLT-05": (11, 0),
        "KLT-06": (7, 0),
        "KLT-07": (7, 0),
        "KLT-08": (7, 0),
    }
    for code, (built, blocked) in expected.items():
        formation = await get_canonical_klt_formation(code)
        assert formation.built_skill_count == built, code
        assert len(formation.blocked_skill_ids) == blocked, code
        assert formation.skill_count == built + blocked, code


async def test_blocked_skills_carry_no_module_and_no_content(klt_db):
    """A BLOCKED skill must never resolve to a fabricated module. Updated
    2026-09-07: KLT-06 no longer has any BLOCKED skill (C5/C6 are now
    BUILT_UNCONNECTED, with real modules) — this test now asserts the
    empty case explicitly rather than assuming a formation always has
    BLOCKED rows."""
    await import_klt_docs(DOCS_DIR, created_by="test")
    skills = await list_canonical_klt_skills("KLT-06")
    blocked = [s for s in skills if s.status == "BLOCKED"]
    assert blocked == []

    unconnected = [s for s in skills if s.status == "BUILT_UNCONNECTED"]
    assert {s.skill_id for s in unconnected} == {"KLT06.SKILL.C05", "KLT06.SKILL.C06"}
    for s in unconnected:
        # skill.module_code is the registry's short form ("M05"); module
        # docs key on the full MODULE_ID form ("KLT06-M05") — reconstruct
        # it rather than assume the two are directly comparable.
        full_module_code = f"KLT{s.klt_formation_code.split('-')[1]}-{s.module_code}"
        module = await get_canonical_klt_module("KLT-06", full_module_code)
        assert module is not None  # M05/M06 are real, written modules now
        assert module.content_markdown


# ---------------------------------------------------------------------
# 3. Module content — learner-safe, real, correctly parsed
# ---------------------------------------------------------------------


async def test_module_content_matches_real_file(klt_db):
    await import_klt_docs(DOCS_DIR, created_by="test")
    module = await get_canonical_klt_module("KLT-06", "KLT06-M01")
    assert module is not None
    assert module.title == "Qu'est-ce qu'un observatoire de données culturelles ?"
    assert module.competency_id == "C1"
    assert "Observatory" in (module.kiltikonet_dependency or "")
    assert module.content_markdown  # real body, not None
    assert is_learner_facing("module")


async def test_module_ordering_is_numeric_not_lexicographic(klt_db):
    await import_klt_docs(DOCS_DIR, created_by="test")
    modules = await list_canonical_klt_modules("KLT-04")  # 14 modules, M01..M14
    codes = [m.module_code for m in modules]
    assert codes == sorted(codes, key=lambda c: int(c.rsplit("-M", 1)[-1]))
    assert "KLT04-M14" in codes  # would sort before "KLT04-M02" lexicographically


async def test_klt06_module_list_is_now_complete(klt_db):
    """Updated 2026-09-07: KLT-06 M05/M06 are real, written modules now
    (BUILT_UNCONNECTED on the verified real Observatory schema) — the
    formation's module list is no longer missing M05/M06."""
    await import_klt_docs(DOCS_DIR, created_by="test")
    modules = await list_canonical_klt_modules("KLT-06")
    codes = {m.module_code for m in modules}
    assert codes == {
        "KLT06-M01", "KLT06-M02", "KLT06-M03", "KLT06-M04",
        "KLT06-M05", "KLT06-M06", "KLT06-M07",
    }


# ---------------------------------------------------------------------
# 4. list_canonical_klt_formations — full corpus
# ---------------------------------------------------------------------


async def test_list_all_ten_formations(klt_db):
    await import_klt_docs(DOCS_DIR, created_by="test")
    formations = await list_canonical_klt_formations()
    assert [f.klt_formation_code for f in formations] == KLT_FORMATION_CODES
    # 59 (KLT-01..05) + 21 (KLT-06/07/08, 7/7/7 modules each after
    # 2026-09-07's M05/M06/M04/M04 builds) + 5 (KLT-13) + 5 (KLT-18,
    # both built 2026-09-07 as new formations) = 90 real modules
    assert sum(f.module_count for f in formations) == 59 + 21 + 5 + 5


async def test_contexts_match_klt0008_decision(klt_db):
    await import_klt_docs(DOCS_DIR, created_by="test")
    assert (await get_canonical_klt_formation("KLT-06")).contexts == ["EXTERNAL"]
    assert (await get_canonical_klt_formation("KLT-07")).contexts == ["INTERNAL"]
    assert (await get_canonical_klt_formation("KLT-08")).contexts == ["INTERNAL"]
    assert (await get_canonical_klt_formation("KLT-13")).contexts == ["EXTERNAL"]
    assert (await get_canonical_klt_formation("KLT-18")).contexts == ["EXTERNAL"]


async def test_legacy_badge_flag_matches_corpus(klt_db):
    await import_klt_docs(DOCS_DIR, created_by="test")
    assert (await get_canonical_klt_formation("KLT-01")).has_legacy_badge is True
    assert (await get_canonical_klt_formation("KLT-06")).has_legacy_badge is False
    assert (await get_canonical_klt_formation("KLT-13")).has_legacy_badge is False
    assert (await get_canonical_klt_formation("KLT-18")).has_legacy_badge is False


async def test_klt13_and_klt18_are_new_formations_fully_built(klt_db):
    """KLT-13 and KLT-18 are net-new formations (no legacy, no BLOCKED
    competencies, no BUILT_UNCONNECTED external-system dependency) — built
    complete from construction, unlike KLT-06/07/08 which started PARTIAL
    and carry a real-but-unconnected Observatory/Network dependency.
    fully_complete is legitimately True here (same as KLT-01..05): the
    registry has zero BLOCKED and zero BUILT_UNCONNECTED rows, so the
    derivation in read_model.py computes True — there is no external
    live-connection gap for these two formations to begin with."""
    await import_klt_docs(DOCS_DIR, created_by="test")
    for code in ("KLT-13", "KLT-18"):
        formation = await get_canonical_klt_formation(code)
        assert formation.module_count == 5
        assert formation.structural_status == "COMPLETE"
        assert formation.certification_scope == "FULL"
        assert formation.blocked_skill_ids == []
        assert formation.unconnected_skill_ids == []
        assert formation.fully_complete is True


# ---------------------------------------------------------------------
# 5. Progress — separate collection, idempotent
# ---------------------------------------------------------------------


async def test_content_viewed_idempotent(klt_db):
    first = await record_klt_content_viewed("user-1", "KLT-06", "KLT06-M01")
    second = await record_klt_content_viewed("user-1", "KLT-06", "KLT06-M01")
    assert first.content_viewed_at == second.content_viewed_at

    progress = await get_user_klt_progress("user-1", klt_formation_code="KLT-06")
    assert len(progress) == 1
    assert progress[0].module_code == "KLT06-M01"


# ---------------------------------------------------------------------
# 6. Zero legacy mutation — provable, not just asserted
# ---------------------------------------------------------------------


def test_no_module_here_imports_db_formations_collection():
    """A structural, not just behavioral, guarantee: none of this
    package's real source lines ever reference `db.formations` or
    `db.progress`."""
    import pathlib

    pkg_dir = pathlib.Path(__file__).resolve().parent.parent / "klt_canonical"
    for py_file in pkg_dir.glob("*.py"):
        text = py_file.read_text()
        # ".progress." / ".formations." (attribute-access shape) rules
        # out real code usage while allowing this package's own
        # docstrings to discuss those legacy collections by name (e.g.
        # "db.progress's own (user_id, module_code) namespace").
        assert "db.formations." not in text, py_file
        assert "db.progress." not in text, py_file
        assert "from seed_data" not in text, py_file
        assert "import seed_data" not in text, py_file


def test_skill_registry_parser_matches_known_ground_truth():
    """Independent of any DB — the exact figures reported to the
    Founder in docs/KILTIKONET_MASTER_PACKAGE... reports, recomputed
    here from the real files at test time. Updated 2026-09-07: each
    formation's formerly-BLOCKED skill is now BUILT_UNCONNECTED (real
    module + content on a verified real external schema, no live
    Academy connection) — zero BLOCKED remain."""
    expected = {
        "klt06": (5, 2, 0),
        "klt07": (6, 1, 0),
        "klt08": (6, 1, 0),
    }
    for slug, (built, unconnected, blocked) in expected.items():
        text = (DOCS_DIR / slug / "skills" / "SKILL_ID_REGISTRY.md").read_text()
        rows = parse_skill_registry(text)
        assert sum(1 for r in rows if r["status"] == "BUILT") == built, slug
        assert sum(1 for r in rows if r["status"] == "BUILT_UNCONNECTED") == unconnected, slug
        assert sum(1 for r in rows if r["status"] == "BLOCKED") == blocked, slug
