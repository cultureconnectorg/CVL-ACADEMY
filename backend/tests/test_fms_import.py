"""Pure unit tests for the FMS import engine — parser, validators, and the
ZIP-extraction step of importer.py. No DB required (those pieces don't
touch Mongo); the DB-writing half of import_fms_zip is exercised by the
live-server E2E suite instead.
"""

from __future__ import annotations

import zipfile
from io import BytesIO

from fms_import.importer import _extract_markdown_files
from fms_import.parser import parse_markdown_file
from fms_import.validators import validate_batch

MODULE_MD = """---
type: module
code: FMS-01-M01
formation_code: FMS-01
title: Poser son univers artistique
prerequisites: []
skill_ids: [FMS.N1.B1.S1]
version: "1.0"
---
# Poser son univers artistique

Contenu du module...
"""

QCM_MD = """---
type: qcm
code: FMS-01-M01-QCM
formation_code: FMS-01
title: QCM — Poser son univers artistique
prerequisites: [FMS-01-M01]
---
1. Question...
"""


def _zip_bytes(files: dict) -> bytes:
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for name, content in files.items():
            zf.writestr(name, content)
    return buf.getvalue()


class TestParser:
    def test_parses_frontmatter_and_body(self):
        resource, issues = parse_markdown_file("FMS-01-M01.md", MODULE_MD, "import-1")
        assert issues == []
        assert resource is not None
        assert resource.type == "module"
        assert resource.code == "FMS-01-M01"
        assert resource.formation_code == "FMS-01"
        assert resource.skill_ids == ["FMS.N1.B1.S1"]
        assert "Contenu du module" in resource.body_markdown

    def test_infers_type_from_filename_when_missing(self):
        content = "---\ncode: FMS-01-GUIDE-01\n---\n# Guide"
        resource, issues = parse_markdown_file(
            "fms-01-guide-formateur.md", content, "import-1"
        )
        assert resource is not None
        assert resource.type == "guide"
        # No `title:` in frontmatter -> falls back to the code, with a warning.
        assert len(issues) == 1 and issues[0].level == "warning"

    def test_unrecognizable_file_yields_warning_not_crash(self):
        resource, issues = parse_markdown_file(
            "random-notes.md", "no frontmatter here", "import-1"
        )
        assert resource is None
        assert len(issues) == 1
        assert issues[0].level == "warning"

    def test_malformed_yaml_falls_back_to_no_frontmatter(self):
        content = "---\n: not valid yaml: [\n---\nBody"
        resource, issues = parse_markdown_file("broken.md", content, "import-1")
        # No usable frontmatter -> type can't be inferred from content, but
        # filename has no hint either -> warning, no crash.
        assert resource is None
        assert issues[0].level == "warning"

    def test_missing_title_defaults_to_code_with_warning(self):
        content = "---\ntype: guide\ncode: FMS-01-G01\n---\nBody"
        resource, issues = parse_markdown_file("g.md", content, "import-1")
        assert resource is not None
        assert resource.title == "FMS-01-G01"
        assert any("title" in i.message for i in issues)


class TestValidateBatch:
    def test_clean_batch_has_no_errors(self):
        mod, _ = parse_markdown_file("m.md", MODULE_MD, "i1")
        qcm, _ = parse_markdown_file("q.md", QCM_MD, "i1")
        issues = validate_batch([mod, qcm])
        assert not any(i.level == "error" for i in issues)

    def test_module_without_formation_code_is_error(self):
        content = "---\ntype: module\ncode: FMS-01-M99\n---\nBody"
        mod, _ = parse_markdown_file("m99.md", content, "i1")
        issues = validate_batch([mod])
        assert any(i.level == "error" and "formation_code" in i.message for i in issues)

    def test_dangling_prerequisite_is_warning_not_error(self):
        content = "---\ntype: module\ncode: FMS-01-M02\nformation_code: FMS-01\nprerequisites: [FMS-01-M01]\n---\nBody"
        mod, _ = parse_markdown_file("m2.md", content, "i1")
        issues = validate_batch([mod])  # FMS-01-M01 not in this batch
        assert any(i.level == "warning" and "Prérequis" in i.message for i in issues)
        assert not any(i.level == "error" for i in issues)

    def test_duplicate_codes_flagged(self):
        mod1, _ = parse_markdown_file("m.md", MODULE_MD, "i1")
        mod2, _ = parse_markdown_file("m-copy.md", MODULE_MD, "i1")
        issues = validate_batch([mod1, mod2])
        assert any("présent 2 fois" in i.message for i in issues)


class TestExtractMarkdownFiles:
    def test_extracts_all_md_files(self):
        raw = _zip_bytes({"a.md": MODULE_MD, "b.md": QCM_MD, "readme.txt": "ignore me"})
        files, issues = _extract_markdown_files(raw)
        assert issues == []
        assert {name for name, _ in files} == {"a.md", "b.md"}

    def test_bad_zip_reports_error(self):
        files, issues = _extract_markdown_files(b"not a zip at all")
        assert files == []
        assert issues[0].level == "error"

    def test_zip_with_no_markdown_reports_error(self):
        raw = _zip_bytes({"readme.txt": "hello"})
        files, issues = _extract_markdown_files(raw)
        assert files == []
        assert any("Aucun fichier .md" in i.message for i in issues)
