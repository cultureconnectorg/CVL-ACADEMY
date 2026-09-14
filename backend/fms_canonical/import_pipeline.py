"""ACA-0006 §12 — canonical import command.

A thin, additive wrapper over the existing `fms_import.import_fms_zip` —
reused exactly as-is, not reimplemented. `fms_import`'s own
`db.fms_resources.update_one({"code": r.code}, {"$set": ...}, upsert=True)`
(see `fms_import/importer.py`) already makes the underlying write
idempotent by resource code: re-running an import of the same archive
overwrites each resource with the same content, it never duplicates.

What this wrapper adds: a canonical-version tag on the report (so a
future archive version is distinguishable in `db.fms_imports` history),
a single, clearly named entrypoint for "import the canonical FMS
archive" as opposed to "import an arbitrary FMS ZIP" — same underlying
mechanism, clearer intent at the call site (mission asks for "une
commande/admin operation claire pour déploiement") — and, per the
Founder's blocking correction (2026-09-03), a full `FileProvenance`
inventory of every entry the archive actually contains
(`provenance.py::store_zip_provenance`), run unconditionally alongside
the resource import so an import can never silently account for fewer
files than the archive holds.

**This wrapper does not by itself prove a real, persistent MongoDB
import** — see `docs/ACADEMY_FMS_CANONICAL_RUNTIME_BINDING_REPORT.md`
§12 for the explicit `CODE_PATH_VERIFIED` vs `REAL_MONGO_IMPORT_VERIFIED`
distinction. No live MongoDB is available in this sandbox.
"""

from __future__ import annotations

from typing import Optional, Tuple

from db import db
from fms_import import ImportReport, import_fms_zip

from .models import CANONICAL_VERSION_CURRENT, FileProvenance
from .provenance import store_zip_provenance


async def import_canonical_fms_zip(
    raw_zip: bytes,
    filename: str,
    *,
    canonical_version: str = CANONICAL_VERSION_CURRENT,
    created_by: Optional[str] = None,
) -> Tuple[ImportReport, list[FileProvenance], int, int]:
    """Returns `(import_report, provenance_records, provenance_inserted,
    provenance_updated)`. `ALL_ZIP_FILES_ACCOUNTED_FOR` is only true when
    `len(provenance_records)` matches the archive's real, independently
    counted file total — this pass verified that equality by hand for
    `FMS_Chantier_Complet_20260822.zip` (223 == 223, see the runtime
    binding report's ZIP accounting) rather than asserting it in code,
    since a *different* archive's true file count isn't something this
    function can know in advance to check itself against."""
    report = await import_fms_zip(raw_zip, filename, created_by=created_by)
    # Additive tag only — never rewrites what import_fms_zip already
    # persisted to db.fms_resources; just records which canonical
    # version this particular import run was declared to be.
    await db.fms_imports.update_one(
        {"id": report.id}, {"$set": {"canonical_version": canonical_version}}
    )
    provenance_records, inserted, updated = await store_zip_provenance(
        raw_zip, canonical_version=canonical_version
    )
    return report, provenance_records, inserted, updated
