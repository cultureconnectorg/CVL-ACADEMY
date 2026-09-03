"""Pure unit tests for the FMS import engine — parser, module-map
dependency extraction, validators, and the ZIP-extraction step of
importer.py. No DB required (those pieces don't touch Mongo); the
DB-writing half of import_fms_zip is exercised by the live-server E2E
suite instead.

Fixtures below mirror the real FMS ZIP's convention (numbered filenames,
no frontmatter) reconciled after `FMS_Chantier_Complet_20260822.zip`
arrived — see fms_import/models.py and fms_import/parser.py module
docstrings for the full story.
"""

from __future__ import annotations

import zipfile
from io import BytesIO

from fms_import.importer import _apply_module_map_dependencies
from fms_import.module_map import extract_module_prerequisites
from fms_import.parser import parse_markdown_file
from fms_import.validators import validate_batch

MODULE_CONTENU_MD = """# Poser son univers artistique

Contenu du module, mentionne FMS01-B1 et FMS01-B2 dans le corps.
"""

BLUEPRINT_MD = """# FMS-01 — MODULE M01 — BLUEPRINT PÉDAGOGIQUE
## Introduction au métier d'Artist Development

Contrat pédagogique de M01. Cite FMS01-A1.
"""

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
| **Prérequis** | Aucun |

## M02 — Comprendre le diagnostic artistique

| Champ | Contenu |
|---|---|
| **ID** | FMS01-M02 |
| **Prérequis** | M01 |

## M11 — Roadmap & trajectoire de développement

| Champ | Contenu |
|---|---|
| **ID** | FMS01-M11 |
| **Prérequis** | M07, M08, M09, M10 (cas fil rouge cumulatif) |

## A01 — Assessment certificatif FMS-01

| Champ | Contenu |
|---|---|
| **ID** | FMS01-A01 |
| **Prérequis** | M12 (obligatoire) ; M13/M14 recommandés ; M15 jamais requis |
"""

INDEX_MD = """# FMS — INDEX DE L'ARCHIVE

Sommaire complet.
"""


def _zip_bytes(files: dict) -> bytes:
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for name, content in files.items():
            zf.writestr(name, content)
    return buf.getvalue()


class TestParser:
    def test_parses_real_module_filename(self):
        resource, issues = parse_markdown_file(
            "14_FMS01_M01_Contenu_Complet.md", MODULE_CONTENU_MD, "import-1"
        )
        assert issues == []
        assert resource is not None
        assert resource.type == "module"
        assert resource.code == "FMS-01-M01"
        assert resource.formation_code == "FMS-01"
        assert resource.title == "Poser son univers artistique"
        assert resource.skill_ids == ["FMS01-B1", "FMS01-B2"]

    def test_parses_blueprint_filename_distinct_code_from_module(self):
        resource, _ = parse_markdown_file(
            "13_FMS01_M01_Blueprint.md", BLUEPRINT_MD, "import-1"
        )
        assert resource is not None
        assert resource.type == "blueprint"
        assert resource.code == "FMS-01-M01-BLUEPRINT"
        assert resource.formation_code == "FMS-01"
        # Distinct from the module's own code -> no upsert collision.
        module, _ = parse_markdown_file(
            "14_FMS01_M01_Contenu_Complet.md", MODULE_CONTENU_MD, "import-1"
        )
        assert resource.code != module.code

    def test_referentiel_letter_maps_to_formation_via_gabarit_table(self):
        resource, _ = parse_markdown_file(
            "01_FMS-A_Referentiel_Artist_Development.md", REFERENTIEL_MD, "import-1"
        )
        assert resource is not None
        assert resource.type == "referentiel"
        assert resource.formation_code == "FMS-01"  # A -> FMS-01
        assert "ARTIST DEVELOPMENT" in resource.title

    def test_cross_metier_documents_have_no_formation_code(self):
        resource, _ = parse_markdown_file("00_INDEX.md", INDEX_MD, "import-1")
        assert resource is not None
        assert resource.type == "index"
        assert resource.formation_code is None

    def test_module_map_type_and_code(self):
        resource, _ = parse_markdown_file(
            "09_FMS01_Master_Module_Map.md", MODULE_MAP_MD, "import-1"
        )
        assert resource is not None
        assert resource.type == "module_map"
        assert resource.code == "FMS-01-MODULE-MAP"
        assert resource.formation_code == "FMS-01"

    def test_unrecognizable_file_yields_warning_not_crash(self):
        resource, issues = parse_markdown_file(
            "random-notes.md", "no heading, no hint here", "import-1"
        )
        assert resource is None
        assert len(issues) == 1
        assert issues[0].level == "warning"

    def test_legacy_frontmatter_still_honored_if_present(self):
        content = (
            "---\ntype: guide\ncode: CUSTOM-CODE\nformation_code: FMS-01\n---\n"
            "# Guide personnalisé\nCorps."
        )
        resource, _ = parse_markdown_file("anything.md", content, "import-1")
        assert resource is not None
        assert resource.type == "guide"
        assert resource.code == "CUSTOM-CODE"
        assert resource.formation_code == "FMS-01"


class TestModuleMapExtraction:
    def test_extracts_prerequisites_per_module(self):
        deps = extract_module_prerequisites(MODULE_MAP_MD)
        assert deps["M01"] == []
        assert deps["M02"] == ["M01"]
        assert deps["M11"] == ["M07", "M08", "M09", "M10"]

    def test_never_extracts_the_a0n_certification_row(self):
        deps = extract_module_prerequisites(MODULE_MAP_MD)
        assert "A01" not in deps

    def test_empty_body_returns_empty_dict(self):
        assert extract_module_prerequisites("") == {}


class TestApplyModuleMapDependencies:
    def test_module_prerequisites_populated_from_batch_module_map(self):
        module_map, _ = parse_markdown_file(
            "09_FMS01_Master_Module_Map.md", MODULE_MAP_MD, "i1"
        )
        m01, _ = parse_markdown_file(
            "14_FMS01_M01_Contenu_Complet.md", MODULE_CONTENU_MD, "i1"
        )
        m01.code = "FMS-01-M01"
        m02_content = "# Comprendre le diagnostic artistique\nCorps."
        m02, _ = parse_markdown_file(
            "17_FMS01_M02_Contenu_Complet.md", m02_content, "i1"
        )
        resources = [module_map, m01, m02]
        _apply_module_map_dependencies(resources)
        assert m01.prerequisites == []
        assert m02.prerequisites == ["FMS-01-M01"]


class TestValidateBatch:
    def test_clean_batch_has_no_errors(self):
        mod, _ = parse_markdown_file(
            "14_FMS01_M01_Contenu_Complet.md", MODULE_CONTENU_MD, "i1"
        )
        issues = validate_batch([mod])
        assert not any(i.level == "error" for i in issues)

    def test_dangling_prerequisite_is_warning_not_error(self):
        mod, _ = parse_markdown_file(
            "17_FMS01_M02_Contenu_Complet.md",
            "# Comprendre le diagnostic artistique\nCorps.",
            "i1",
        )
        mod.prerequisites = ["FMS-01-M01"]  # not in this batch
        issues = validate_batch([mod])
        assert any(i.level == "warning" and "Prérequis" in i.message for i in issues)
        assert not any(i.level == "error" for i in issues)

    def test_duplicate_codes_flagged(self):
        mod1, _ = parse_markdown_file(
            "14_FMS01_M01_Contenu_Complet.md", MODULE_CONTENU_MD, "i1"
        )
        mod2, _ = parse_markdown_file(
            "14b_FMS01_M01_Contenu_Complet.md", MODULE_CONTENU_MD, "i1"
        )
        issues = validate_batch([mod1, mod2])
        assert any("présent 2 fois" in i.message for i in issues)


class TestExtractMarkdownFiles:
    def test_extracts_all_md_files(self):
        from fms_import.importer import _extract_markdown_files

        raw = _zip_bytes(
            {
                "14_FMS01_M01_Contenu_Complet.md": MODULE_CONTENU_MD,
                "13_FMS01_M01_Blueprint.md": BLUEPRINT_MD,
                "readme.txt": "ignore me",
            }
        )
        files, issues = _extract_markdown_files(raw)
        assert issues == []
        assert {name for name, _ in files} == {
            "14_FMS01_M01_Contenu_Complet.md",
            "13_FMS01_M01_Blueprint.md",
        }

    def test_bad_zip_reports_error(self):
        from fms_import.importer import _extract_markdown_files

        files, issues = _extract_markdown_files(b"not a zip at all")
        assert files == []
        assert issues[0].level == "error"

    def test_zip_with_no_markdown_reports_error(self):
        from fms_import.importer import _extract_markdown_files

        raw = _zip_bytes({"readme.txt": "hello"})
        files, issues = _extract_markdown_files(raw)
        assert files == []
        assert any("Aucun fichier .md" in i.message for i in issues)
