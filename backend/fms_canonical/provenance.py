"""ACA-0006 — exhaustive ZIP provenance (Founder blocking correction,
2026-09-03: `ALL_ZIP_FILES_ACCOUNTED_FOR = TRUE`, `ZERO_SILENT_FILE_LOSS
= TRUE`, `SOURCE_TRACEABILITY = TRUE`).

Two real gaps this closes in the existing (untouched) `fms_import`
pipeline:

1. **No hash/size/path integrity record exists anywhere.**
   `fms_import`'s own `FmsResource` never stores the source file's raw
   size or a hash of its content — nothing today can *prove* which byte-
   for-byte source produced a given `db.fms_resources` document.
2. **A file the classifier can't type is silently never persisted.**
   `fms_import/parser.py::parse_markdown_file` returns `(None, [warning
   issue])` for an unrecognized file — `importer.py` records the warning
   in the `ImportReport`, but the file itself never becomes a
   `db.fms_resources` document. For the one real archive this session
   verified (`FMS_Chantier_Complet_20260822.zip`) this never actually
   triggers — see the runtime binding report's ZIP accounting: 223/223
   files matched a known type, 0 warnings, 0 errors — but the *pipeline*
   itself has no safety net against it for a future archive.

This module builds a full, independent inventory straight from the raw
ZIP bytes — every entry, not just the ones `.md`-filtered/classified —
and records one `FileProvenance` row per real file, `parsed` or not.
**Deliberately reuses `fms_import.parser.parse_markdown_file` itself**
(the exact function `importer.py` calls) rather than reimplementing
classification — this stays a true independent *accounting* of what the
real pipeline did/would do, never a second, potentially-diverging
implementation.
"""

from __future__ import annotations

import hashlib
import logging
import zipfile
from datetime import datetime, timezone
from io import BytesIO
from typing import List, Optional, Tuple

from db import db
from fms_import.parser import MODULE_NUM_RE, parse_markdown_file

from .models import CANONICAL_VERSION_CURRENT, FileProvenance, resource_audience

logger = logging.getLogger("cvln.fms_canonical.provenance")

COLLECTION = "fms_resource_provenance"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _module_number(filename: str) -> Optional[str]:
    m = MODULE_NUM_RE.search(filename)
    return f"M{m.group(1)}" if m else None


def count_zip_files(raw_zip: bytes) -> int:
    """Independent ground truth for `ALL_ZIP_FILES_ACCOUNTED_FOR`: counts
    real (non-directory) entries straight off `zipfile.infolist()`,
    deliberately *not* sharing any code path with `build_zip_inventory`
    below — so a bug in that function's own iteration can't silently pass
    its own self-check."""
    try:
        zf = zipfile.ZipFile(BytesIO(raw_zip))
    except zipfile.BadZipFile:
        return 0
    return sum(1 for i in zf.infolist() if not (i.is_dir() or i.filename.endswith("/")))


def build_zip_inventory(
    raw_zip: bytes, *, canonical_version: str = CANONICAL_VERSION_CURRENT
) -> List[FileProvenance]:
    """Pure, read-only. Every real (non-directory) ZIP entry becomes
    exactly one record — parsed or not, never dropped."""
    records: List[FileProvenance] = []
    try:
        zf = zipfile.ZipFile(BytesIO(raw_zip))
    except zipfile.BadZipFile:
        return records

    for info in zf.infolist():
        if info.is_dir() or info.filename.endswith("/"):
            continue  # a directory entry has no content to hash/classify

        original_path = info.filename
        original_filename = original_path.rsplit("/", 1)[-1]

        try:
            raw_bytes = zf.read(original_path)
        except (KeyError, zipfile.BadZipFile) as exc:
            records.append(
                FileProvenance(
                    original_path=original_path,
                    original_filename=original_filename,
                    sha256="",
                    byte_size=info.file_size,
                    canonical_version=canonical_version,
                    parsing_status="unparsed_error",
                    parsing_note=f"Lecture impossible depuis l'archive : {exc}",
                )
            )
            continue

        sha256 = hashlib.sha256(raw_bytes).hexdigest()
        byte_size = len(raw_bytes)

        try:
            text = raw_bytes.decode("utf-8")
        except UnicodeDecodeError:
            records.append(
                FileProvenance(
                    original_path=original_path,
                    original_filename=original_filename,
                    sha256=sha256,
                    byte_size=byte_size,
                    canonical_version=canonical_version,
                    parsing_status="unparsed_error",
                    parsing_note="Encodage non-UTF-8.",
                )
            )
            continue

        resource, issues = parse_markdown_file(
            original_path, text, import_id="provenance-scan"
        )

        if resource is None:
            note = "; ".join(i.message for i in issues) or "Type non reconnu."
            records.append(
                FileProvenance(
                    original_path=original_path,
                    original_filename=original_filename,
                    sha256=sha256,
                    byte_size=byte_size,
                    canonical_version=canonical_version,
                    parsing_status="unparsed_no_type_match",
                    parsing_note=note,
                )
            )
            continue

        records.append(
            FileProvenance(
                original_path=original_path,
                original_filename=original_filename,
                sha256=sha256,
                byte_size=byte_size,
                resource_type=resource.type,
                formation_code=resource.formation_code,
                module_number=(
                    _module_number(original_filename)
                    if resource.type == "module"
                    else None
                ),
                audience=resource_audience(resource.type),
                canonical_version=canonical_version,
                parsing_status="parsed",
            )
        )

    return records


async def store_zip_provenance(
    raw_zip: bytes, *, canonical_version: str = CANONICAL_VERSION_CURRENT
) -> Tuple[List[FileProvenance], int, int]:
    """Idempotent by `original_path` + `canonical_version`: re-running
    against the same archive version overwrites each record with the
    same (or corrected classifier) data — it never duplicates. Returns
    (records, inserted_count, updated_count)."""
    records = build_zip_inventory(raw_zip, canonical_version=canonical_version)
    inserted = 0
    updated = 0
    now = _now()
    for record in records:
        payload = record.model_dump()
        payload["imported_at"] = now
        result = await db[COLLECTION].update_one(
            {
                "original_path": record.original_path,
                "canonical_version": canonical_version,
            },
            {"$set": payload},
            upsert=True,
        )
        if result.upserted_id is not None:
            inserted += 1
        else:
            updated += 1
    return records, inserted, updated


async def list_zip_provenance(
    *, canonical_version: str = CANONICAL_VERSION_CURRENT
) -> List[FileProvenance]:
    docs = (
        await db[COLLECTION]
        .find({"canonical_version": canonical_version}, {"_id": 0})
        .to_list(1000)
    )
    return [FileProvenance(**d) for d in docs]
