"""ACA-0006 — Canonical FMS runtime binding tests.

Uses a small synthetic ZIP fixture (same convention as
`tests/test_fms_import.py`'s fixtures) rather than the real
`FMS_Chantier_Complet_20260822.zip` — that archive lives only in this
session's uploads (`/root/.claude/uploads/...`), outside the repository,
so a committed pytest can't depend on it being present in a future
environment. The real archive was independently verified by hand this
session (see `docs/ACADEMY_FMS_CANONICAL_RUNTIME_BINDING_REPORT.md`'s
ZIP accounting section: 223/223 files parsed, 95 modules, 83 Skill IDs,
6 métiers, 0 unparsed) — this suite proves the *mechanism* is correct on
a small, portable fixture that deliberately includes one unrecognized
file (to exercise the `unparsed_no_type_match` path the real archive
never triggers) and one staff-only resource (to prove it never leaks).

DB-backed pieces run against `mongomock_motor.AsyncMongoMockClient`, same
rationale as `test_fms_lineage.py`: no live MongoDB in this sandbox, and
several guarantees here (idempotent upsert, unique-index-free coexistence
of legacy/canonical progress) are genuinely database behaviors.
"""

from __future__ import annotations

import zipfile
from io import BytesIO

import pytest
from mongomock_motor import AsyncMongoMockClient

import fms_canonical.import_pipeline as import_pipeline_module
import fms_canonical.progress as progress_module
import fms_canonical.provenance as provenance_module
import fms_canonical.read_model as read_model_module
import fms_import.importer as fms_importer_module
import fms_import.indexer as fms_indexer_module
from fms_canonical.import_pipeline import import_canonical_fms_zip
from fms_canonical.models import STAFF_ONLY_TYPES, is_learner_facing, resource_audience
from fms_canonical.progress import get_user_canonical_progress, record_content_viewed
from fms_canonical.provenance import build_zip_inventory, count_zip_files
from fms_canonical.read_model import (
    get_canonical_formation,
    get_canonical_module,
    list_canonical_formations,
    list_canonical_modules,
    list_canonical_skill_definitions,
)

REFERENTIEL_MD = """# FMS — MÉTIER A : ARTIST DEVELOPMENT
## Fiche de référence unique — Version 1.0

Contenu du référentiel.
"""

MODULE_MAP_MD = """# FMS-01 — ARTIST DEVELOPMENT
## Master Module Map — Version 1.0

## M01 — Introduction au métier d'Artist Development

| Champ | Contenu |
|---|---|
| **ID** | FMS01-M01 |
| **Titre** | Introduction au métier d'Artist Development |
| **Bloc de compétence** | Transversal |
| **Niveau de progression** | Découverte |
| **Prérequis** | Aucun |
| **N1 associé** | QCM de 10 questions |
| **N2 associé** | Aucun à ce niveau |
| **Préparation N3** | Aucune |

## M02 — Comprendre le diagnostic artistique

| Champ | Contenu |
|---|---|
| **ID** | FMS01-M02 |
| **Titre** | Comprendre le diagnostic artistique |
| **Bloc de compétence** | A — Diagnostic artistique |
| **Niveau de progression** | Découverte |
| **Prérequis** | M01 |

## M03 — Module sans prérequis déclaré

| Champ | Contenu |
|---|---|
| **ID** | FMS01-M03 |
| **Titre** | Module sans prérequis déclaré |
"""

MODULE_M01_MD = """# FMS-01 — MODULE M01

## Introduction au métier d'Artist Development

Contenu réel du module M01. Cite FMS01-A1 et FMS01-B1. Mentionne aussi le
code de certification FMS01-A01, qui n'est pas un Skill ID.
"""

MODULE_M02_MD = """# FMS-01 — MODULE M02

## Comprendre le diagnostic artistique

Contenu réel du module M02. Cite FMS01-A2.
"""

CAS_FIL_ROUGE_MD = """# FMS-01 — ARTIST DEVELOPMENT
## Cas Fil Rouge — Version 1.0

Le cas Anaïs Solaine accompagne l'apprenant.
"""

SKILL_IDS_REGISTRY_MD = """# FMS-01 — Skill IDs Registry

| ID | Nom |
|---|---|
| FMS01-A1 | Diagnostic |
| FMS01-A2 | Diagnostic autonome |
| FMS01-B1 | Univers |
"""

GUIDE_CORRECTEUR_MD = """# FMS-01 — Guide Correcteur

Instructions de notation confidentielles — ne jamais montrer à l'apprenant.
Cite FMS01-A1 pour le barème.
"""


def _zip_bytes(files: dict) -> bytes:
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for name, content in files.items():
            zf.writestr(name, content)
    return buf.getvalue()


FIXTURE_FILES = {
    "FMS_Fixture/01_FMS-A_Referentiel_Artist_Development.md": REFERENTIEL_MD,
    "FMS_Fixture/09_FMS01_Master_Module_Map.md": MODULE_MAP_MD,
    "FMS_Fixture/14_FMS01_M01_Contenu_Complet.md": MODULE_M01_MD,
    "FMS_Fixture/17_FMS01_M02_Contenu_Complet.md": MODULE_M02_MD,
    "FMS_Fixture/10_FMS01_Cas_Fil_Rouge_Anais_Solaine.md": CAS_FIL_ROUGE_MD,
    "FMS_Fixture/27_FMS01_Skill_IDs_Registry.md": SKILL_IDS_REGISTRY_MD,
    "FMS_Fixture/55_FMS01_Guide_Correcteur.md": GUIDE_CORRECTEUR_MD,
    # Deliberately unrecognizable — no FILENAME_TYPE_HINTS substring
    # matches "mystere" — exercises the unparsed path the real archive
    # never triggers.
    "FMS_Fixture/999_FMS01_Mystere.md": "# Contenu non classifiable\n\nTexte.",
}

FIXTURE_ZIP = _zip_bytes(FIXTURE_FILES)


@pytest.fixture
async def canon_db(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_canonical_test"]
    for module in (
        fms_importer_module,
        fms_indexer_module,
        import_pipeline_module,
        provenance_module,
        read_model_module,
        progress_module,
    ):
        monkeypatch.setattr(module, "db", mock_db)
    return mock_db


async def _import_fixture(**kwargs):
    return await import_canonical_fms_zip(
        FIXTURE_ZIP, "FMS_Fixture.zip", created_by="test", **kwargs
    )


# ---------------------------------------------------------------------
# 1-3. Canonical read model
# ---------------------------------------------------------------------


async def test_canonical_formation_read(canon_db):
    await _import_fixture()
    formation = await get_canonical_formation("FMS-01")
    assert formation is not None
    assert formation.metier_name == "Artist Development"
    assert formation.pedagogical_source == "CANONICAL"
    assert formation.pedagogical_case_title == "Anais Solaine"


async def test_canonical_module_read(canon_db):
    await _import_fixture()
    module = await get_canonical_module("FMS-01", "FMS01-M01")
    assert module is not None
    assert module.title == "Introduction au métier d'Artist Development"
    assert "Contenu réel du module M01" in module.content_markdown


async def test_module_order(canon_db):
    await _import_fixture()
    modules = await list_canonical_modules("FMS-01")
    assert [m.canonical_module_code for m in modules] == [
        "FMS01-M01",
        "FMS01-M02",
        "FMS01-M03",
    ]
    assert [m.order_index for m in modules] == [0, 1, 2]


# ---------------------------------------------------------------------
# 4-5. Prerequisites: real, never invented
# ---------------------------------------------------------------------


async def test_real_prerequisites_extracted(canon_db):
    await _import_fixture()
    m02 = await get_canonical_module("FMS-01", "FMS01-M02")
    assert m02.prerequisites.status == "DEFINED"
    assert m02.prerequisites.required_module_codes == ["FMS01-M01"]


async def test_missing_prerequisites_not_invented(canon_db):
    await _import_fixture()
    m01 = await get_canonical_module("FMS-01", "FMS01-M01")
    assert m01.prerequisites.status == "NONE"  # explicit "Aucun"

    m03 = await get_canonical_module("FMS-01", "FMS01-M03")
    assert m03.prerequisites.status == "UNSPECIFIED"  # no Prérequis field at all
    assert m03.prerequisites.required_module_codes == []


# ---------------------------------------------------------------------
# 6-7. Codes preserved exactly
# ---------------------------------------------------------------------


async def test_canonical_code_preserved_exactly(canon_db):
    await _import_fixture()
    modules = await list_canonical_modules("FMS-01")
    for m in modules:
        assert m.canonical_module_code.startswith("FMS01-M")
        assert (
            "FMS-01-M" not in m.canonical_module_code
        )  # never the legacy hyphenated form


def test_legacy_code_format_untouched_by_this_package():
    # fms_import's own normalization (untouched, read-only input to this
    # package) still produces the legacy-shaped code — proves this
    # package didn't change that behavior.
    from fms_import.parser import parse_markdown_file

    resource, _ = parse_markdown_file(
        "14_FMS01_M01_Contenu_Complet.md", MODULE_M01_MD, "import-1"
    )
    assert resource.code == "FMS-01-M01"


# ---------------------------------------------------------------------
# 8-9. Legacy/canonical progress coexistence, no mutation
# ---------------------------------------------------------------------


async def test_legacy_and_canonical_progress_coexist(canon_db):
    await _import_fixture()
    legacy_doc = {
        "id": "p1",
        "user_id": "u1",
        "formation_code": "FMS-01",
        "module_code": "FMS-01-M01",
        "completed": True,
        "score": 1.0,
    }
    await canon_db.progress.insert_one(dict(legacy_doc))

    await record_content_viewed("u1", "FMS-01", "FMS01-M01")

    stored_legacy = await canon_db.progress.find_one({"id": "p1"}, {"_id": 0})
    assert stored_legacy == legacy_doc  # byte-for-byte unchanged
    assert await canon_db.progress.count_documents({}) == 1
    assert await canon_db.canonical_progress.count_documents({}) == 1

    canon_progress = await get_user_canonical_progress("u1")
    assert len(canon_progress) == 1
    assert canon_progress[0].canonical_module_code == "FMS01-M01"


async def test_no_legacy_progress_mutation_across_full_pipeline(canon_db):
    legacy_doc = {
        "id": "p1",
        "user_id": "u1",
        "formation_code": "FMS-01",
        "module_code": "FMS-01-M01",
        "completed": True,
        "score": 0.5,
    }
    await canon_db.progress.insert_one(dict(legacy_doc))

    await _import_fixture()
    await list_canonical_formations()
    await record_content_viewed("u1", "FMS-01", "FMS01-M02")

    stored = await canon_db.progress.find_one({"id": "p1"}, {"_id": 0})
    assert stored == legacy_doc


# ---------------------------------------------------------------------
# 10-11. No positional/automatic credit — structural, not just tested
# ---------------------------------------------------------------------


def test_no_automatic_skill_crediting_code_exists():
    """Structural guarantee: nothing in fms_canonical/ references the
    collections that actually credit a skill/badge to a user."""
    import pathlib

    pkg_dir = pathlib.Path(__file__).parent.parent / "fms_canonical"
    forbidden = ["db.user_skills", "db.user_badges", "db.skill_evidence"]
    for path in pkg_dir.glob("*.py"):
        text = path.read_text(encoding="utf-8")
        for term in forbidden:
            assert (
                term not in text
            ), f"{path.name} references {term} — would credit a user"


async def test_content_viewed_never_infers_skill_completion(canon_db):
    await _import_fixture()
    progress = await record_content_viewed("u1", "FMS-01", "FMS01-M01")
    assert progress.content_viewed_at is not None
    # The progress record itself carries no skill/credit fields at all.
    assert not hasattr(progress, "skills_awarded")


# ---------------------------------------------------------------------
# 12-13. Full scale — proven by hand against the real archive (see the
# runtime binding report's ZIP accounting); this fixture proves the
# counting *mechanism* on a small, portable subset (3 of 95 modules, 1
# of 6 métiers).
# ---------------------------------------------------------------------


async def test_module_count_and_metier_scale_mechanism(canon_db):
    await _import_fixture()
    formation = await get_canonical_formation("FMS-01")
    assert formation.module_count == 3  # this fixture's real count
    assert len(formation.module_codes_in_order) == 3


# ---------------------------------------------------------------------
# 14. Staff-only resources never leak to a learner
# ---------------------------------------------------------------------


async def test_staff_resource_never_leaks_as_module_content(canon_db):
    await _import_fixture()
    module = await get_canonical_module("FMS-01", "FMS01-M01")
    assert module.content_markdown is not None
    assert "confidentielles" not in module.content_markdown
    assert "barème" not in module.content_markdown


def test_guide_correcteur_is_not_learner_facing():
    assert is_learner_facing("guide_correcteur") is False
    assert "guide_correcteur" in STAFF_ONLY_TYPES
    assert "LEARNER" not in resource_audience("guide_correcteur")


def test_unrecognized_type_defaults_to_staff_only():
    assert is_learner_facing("some_future_type_nobody_registered") is False


# ---------------------------------------------------------------------
# 15-16. Skill definitions
# ---------------------------------------------------------------------


async def test_skill_definitions_extraction(canon_db):
    await _import_fixture()
    skills = await list_canonical_skill_definitions("FMS-01")
    skill_ids = {s.skill_id for s in skills}
    assert {"FMS01-A1", "FMS01-A2", "FMS01-B1"}.issubset(skill_ids)
    # The certification code FMS01-A01 (2 digits) must never be treated
    # as a skill ID.
    assert "FMS01-A01" not in skill_ids


async def test_skill_registry_source_is_marked(canon_db):
    await _import_fixture()
    skills = {s.skill_id: s for s in await list_canonical_skill_definitions("FMS-01")}
    assert skills["FMS01-A1"].source == "skill_ids_registry"


# ---------------------------------------------------------------------
# 17. N1/N2/N3 distinction
# ---------------------------------------------------------------------


async def test_n1_n2_n3_distinction(canon_db):
    await _import_fixture()
    m01 = await get_canonical_module("FMS-01", "FMS01-M01")
    assert m01.assessment.n1_reference == "QCM de 10 questions"
    assert m01.assessment.n2_reference == "Aucun à ce niveau"
    assert m01.assessment.n3_reference == "Aucune"


# ---------------------------------------------------------------------
# 18. Pedagogical case != product mission (structural — no such merge
# exists in this package at all)
# ---------------------------------------------------------------------


def test_no_mission_pedagogical_case_merge_code_exists():
    import pathlib

    pkg_dir = pathlib.Path(__file__).parent.parent / "fms_canonical"
    for path in pkg_dir.glob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "db.missions" not in text
        assert "db.user_missions" not in text


# ---------------------------------------------------------------------
# 19. Certification safeguards — this pass adds no canonical
# certification-attempt code at all (see runtime binding report §"what's
# left"); the existing engine's own safeguards are untouched.
# ---------------------------------------------------------------------


def test_no_canonical_certification_attempt_code_exists():
    import pathlib

    pkg_dir = pathlib.Path(__file__).parent.parent / "fms_canonical"
    for path in pkg_dir.glob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "db.certification_attempts" not in text


# ---------------------------------------------------------------------
# 20. module_lineage still functional (regression against ACA-0005)
# ---------------------------------------------------------------------


async def test_module_lineage_still_functional(canon_db, monkeypatch):
    import fms_lineage.initial_matrix as lineage_initial_matrix_module
    import fms_lineage.service as lineage_service_module
    from fms_lineage.service import get_lineage_for_legacy_module

    monkeypatch.setattr(lineage_service_module, "db", canon_db)
    monkeypatch.setattr(lineage_initial_matrix_module, "db", canon_db)

    from fms_lineage.initial_matrix import seed_initial_matrix

    inserted, _ = await seed_initial_matrix()
    assert inserted == 53
    records = await get_lineage_for_legacy_module("FMS-01", "FMS-01-M01")
    assert len(records) == 1
    assert records[0].relation == "NO_EQUIVALENCE"


# ---------------------------------------------------------------------
# 21. Legacy routes/data still functional — proven by the full pre-
# existing pure-unit suite staying green (see runtime binding report
# §"regression"), not duplicated here.
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
# 22. API auth/RBAC
# ---------------------------------------------------------------------


def _allowed_roles(dependency_callable):
    freevars = dependency_callable.__code__.co_freevars
    if "allowed" not in freevars:
        return None
    idx = freevars.index("allowed")
    return dependency_callable.__closure__[idx].cell_contents


def test_import_route_requires_admin_roles():
    from api.canonical import router
    from models import ADMIN_ROLES

    route = next(r for r in router.routes if r.path == "/canonical/import")
    roles = next(
        (
            _allowed_roles(dep.call)
            for dep in route.dependant.dependencies
            if _allowed_roles(dep.call)
        ),
        None,
    )
    assert roles == ADMIN_ROLES


def test_provenance_route_requires_staff_roles():
    from api.canonical import router
    from models import STAFF_ROLES

    route = next(r for r in router.routes if r.path == "/canonical/provenance")
    roles = next(
        (
            _allowed_roles(dep.call)
            for dep in route.dependant.dependencies
            if _allowed_roles(dep.call)
        ),
        None,
    )
    assert roles == STAFF_ROLES


def test_read_routes_require_real_authentication():
    from api.canonical import router
    from auth import get_current_user

    route = next(r for r in router.routes if r.path == "/canonical/formations")
    # get_current_user itself (not require_role(...)) must be the
    # dependency — no get_current_user_optional anywhere in this router
    # (mission: PUBLIC_DISCOVERY_ACTIVATION = OUT_OF_SCOPE).
    calls = [dep.call for dep in route.dependant.dependencies]
    assert get_current_user in calls


# ---------------------------------------------------------------------
# 23. Idempotent canonical import/read model
# ---------------------------------------------------------------------


async def test_import_is_idempotent(canon_db):
    report1, prov1, inserted1, updated1 = await _import_fixture()
    assert report1.resources_created == 7  # 7 real types, 1 unparsed excluded
    assert inserted1 == 8  # all 8 real ZIP entries get a provenance row
    assert updated1 == 0

    report2, prov2, inserted2, updated2 = await _import_fixture()
    assert report2.resources_created == 7
    assert inserted2 == 0
    assert updated2 == 8  # same 8 rows re-written, never duplicated

    assert await canon_db.fms_resources.count_documents({}) == 7
    assert await canon_db.fms_resource_provenance.count_documents({}) == 8


# ---------------------------------------------------------------------
# Provenance — the Founder's blocking correction
# ---------------------------------------------------------------------


def test_zip_inventory_accounts_for_every_file_including_unparsed():
    records = build_zip_inventory(FIXTURE_ZIP)
    assert len(records) == 8  # every real entry in FIXTURE_FILES, none dropped
    assert count_zip_files(FIXTURE_ZIP) == len(records)

    unparsed = [r for r in records if r.parsing_status != "parsed"]
    assert len(unparsed) == 1
    assert unparsed[0].original_filename == "999_FMS01_Mystere.md"
    assert unparsed[0].resource_type is None
    assert unparsed[0].parsing_note  # a real reason, not silence


def test_every_provenance_record_has_hash_and_size():
    records = build_zip_inventory(FIXTURE_ZIP)
    for r in records:
        assert len(r.sha256) == 64  # real sha256 hex digest
        assert r.byte_size > 0


async def test_provenance_never_overwritten_by_import_report_gap(canon_db):
    """Even the file the resource pipeline drops (unparsed) still has a
    permanent provenance record after a real import — mission's
    'un fichier non interprété doit être conservé comme ressource
    canonique... avec son statut de parsing'."""
    await _import_fixture()
    all_prov = await canon_db.fms_resource_provenance.find({}, {"_id": 0}).to_list(100)
    assert len(all_prov) == 8
    mystere = next(
        p for p in all_prov if p["original_filename"] == "999_FMS01_Mystere.md"
    )
    assert mystere["parsing_status"] == "unparsed_no_type_match"
    assert mystere["resource_type"] is None


def test_audience_classification_covers_every_real_type():
    from fms_canonical.models import RESOURCE_AUDIENCE
    from fms_import.models import FmsResourceType

    for real_type in FmsResourceType.__args__:
        assert real_type in RESOURCE_AUDIENCE, f"{real_type} has no audience mapping"
