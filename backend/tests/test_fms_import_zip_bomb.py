"""P0-I (Audit Chirurgical 2026-09-07) — ZIP-bomb / upload-abuse
protections.

Real gap this suite closes and proves closed: `api/fms.py`'s own
`MAX_ZIP_BYTES` (50 MB) only bounds the *compressed* upload size — a
crafted archive a few KB in size can decompress to gigabytes
(`zf.read(name)` had no bound on what it decompressed into memory), and
nothing capped entry count either. `fms_import.importer.
_extract_markdown_files` (the `.md`-only path) and
`fms_canonical.provenance.build_zip_inventory` (the every-entry path —
the more exposed of the two, since it reads entries regardless of
extension) both now reject on entry-count, per-entry uncompressed size,
aggregate uncompressed size, and compression ratio, all checked from
the ZIP central directory BEFORE a single byte is ever decompressed.

Thresholds are monkeypatched down to tiny values for these tests — the
real production bounds (10 MB/entry, 300 MB aggregate, 5000 entries)
would require gigabytes of real test fixture data to exercise
honestly; patching the same constants the production code reads keeps
this a real exercise of the actual comparison logic, not a mock of it.
"""

from __future__ import annotations

import zipfile
from io import BytesIO

import fms_canonical.provenance as provenance_module
import fms_import.importer as importer_module
from fms_canonical.provenance import build_zip_inventory
from fms_import.importer import _extract_markdown_files


def _zip_bytes(entries: dict, compress_type=zipfile.ZIP_STORED) -> bytes:
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for name, content in entries.items():
            zf.writestr(name, content, compress_type=compress_type)
    return buf.getvalue()


# --------------------------------------------------------------------
# Entry-count bomb
# --------------------------------------------------------------------


def test_too_many_entries_rejects_whole_archive(monkeypatch):
    monkeypatch.setattr(importer_module, "MAX_ZIP_ENTRIES", 2)
    raw = _zip_bytes({f"file{i}.md": "# content" for i in range(5)})

    files, issues = _extract_markdown_files(raw)
    assert files == []
    assert any("entrées" in i.message for i in issues)


def test_too_many_entries_rejects_whole_inventory(monkeypatch):
    monkeypatch.setattr(provenance_module, "MAX_ZIP_ENTRIES", 2)
    raw = _zip_bytes({f"file{i}.md": "# content" for i in range(5)})

    records = build_zip_inventory(raw)
    assert records == []


# --------------------------------------------------------------------
# Per-entry uncompressed size bomb
# --------------------------------------------------------------------


def test_oversized_entry_is_skipped_not_the_whole_archive(monkeypatch):
    monkeypatch.setattr(importer_module, "MAX_ENTRY_UNCOMPRESSED_BYTES", 50)
    raw = _zip_bytes(
        {
            "small.md": "# ok\nshort content",
            "huge.md": "X" * 500,
        }
    )

    files, issues = _extract_markdown_files(raw)
    names = {n for n, _ in files}
    assert names == {"small.md"}
    assert any(i.file == "huge.md" and "octets décompressés" in i.message for i in issues)


def test_oversized_entry_gets_an_unread_provenance_record(monkeypatch):
    monkeypatch.setattr(provenance_module, "MAX_ENTRY_UNCOMPRESSED_BYTES", 50)
    raw = _zip_bytes(
        {
            "small.md": "# ok\nshort content",
            "huge.md": "X" * 500,
        }
    )

    records = build_zip_inventory(raw)
    # ALL_ZIP_FILES_ACCOUNTED_FOR — still exactly one record per real
    # entry, the oversized one just never got decompressed to produce it.
    assert len(records) == 2
    huge = next(r for r in records if r.original_filename == "huge.md")
    assert huge.parsing_status == "unparsed_error"
    assert huge.sha256 == ""  # never hashed — never read
    assert "octets décompressés" in huge.parsing_note
    small = next(r for r in records if r.original_filename == "small.md")
    assert small.parsing_status in ("parsed", "unparsed_no_type_match")
    assert small.sha256 != ""  # a real file well under the cap IS read


# --------------------------------------------------------------------
# Aggregate uncompressed size bomb ("many merely-large files")
# --------------------------------------------------------------------


def test_aggregate_size_over_cap_rejects_whole_archive(monkeypatch):
    monkeypatch.setattr(importer_module, "MAX_ENTRY_UNCOMPRESSED_BYTES", 10_000)
    monkeypatch.setattr(importer_module, "MAX_TOTAL_UNCOMPRESSED_BYTES", 100)
    raw = _zip_bytes({f"file{i}.md": "X" * 40 for i in range(3)})  # 120 total

    files, issues = _extract_markdown_files(raw)
    assert files == []
    assert any("octets décompressés au total" in i.message for i in issues)


# --------------------------------------------------------------------
# Compression-ratio bomb — a real zip-bomb signature: a tiny compressed
# payload that inflates enormously (highly repetitive content, real
# DEFLATE compression, not a faked ratio).
# --------------------------------------------------------------------


def test_high_compression_ratio_entry_is_skipped(monkeypatch):
    monkeypatch.setattr(importer_module, "MAX_COMPRESSION_RATIO", 5)
    monkeypatch.setattr(importer_module, "RATIO_CHECK_MIN_BYTES", 100)
    raw = _zip_bytes(
        {
            # Highly repetitive -> compresses far beyond 5x with real DEFLATE.
            "bomb.md": "A" * 5000,
            # Real prose-like content -> compresses modestly, stays under 5x.
            "normal.md": (
                "Ceci est un contenu pedagogique varie avec des mots "
                "differents et une structure de phrase normale, pas "
                "une repetition simple d'un seul caractere reproduit. "
            )
            * 3,
        },
        compress_type=zipfile.ZIP_DEFLATED,
    )

    files, issues = _extract_markdown_files(raw)
    names = {n for n, _ in files}
    assert "bomb.md" not in names
    assert "normal.md" in names
    assert any(i.file == "bomb.md" and "ZIP bomb" in i.message for i in issues)


def test_high_compression_ratio_entry_gets_an_unread_provenance_record(monkeypatch):
    monkeypatch.setattr(provenance_module, "MAX_COMPRESSION_RATIO", 5)
    monkeypatch.setattr(provenance_module, "RATIO_CHECK_MIN_BYTES", 100)
    raw = _zip_bytes({"bomb.md": "A" * 5000}, compress_type=zipfile.ZIP_DEFLATED)

    records = build_zip_inventory(raw)
    assert len(records) == 1
    assert records[0].parsing_status == "unparsed_error"
    assert records[0].sha256 == ""
    assert "ZIP bomb" in records[0].parsing_note


# --------------------------------------------------------------------
# A normal, well-formed small archive is completely unaffected —
# proves these bounds don't regress the legitimate case at
# production-scale thresholds (no monkeypatching in this one).
# --------------------------------------------------------------------


def test_normal_small_archive_is_unaffected_by_production_thresholds():
    raw = _zip_bytes(
        {"module.md": "# Module\nContenu normal du module."},
        compress_type=zipfile.ZIP_DEFLATED,
    )

    files, issues = _extract_markdown_files(raw)
    assert [n for n, _ in files] == ["module.md"]
    assert not any(i.level == "error" for i in issues)

    records = build_zip_inventory(raw)
    assert len(records) == 1
    assert records[0].sha256 != ""
