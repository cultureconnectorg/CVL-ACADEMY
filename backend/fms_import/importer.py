"""ZIP import orchestration — the engine behind "Importer un métier FMS".

Flow: validate it's a real ZIP -> parse every .md file inside -> derive
module prerequisites from any Master Module Map in the batch (module_map.py)
-> run referential validation across the batch -> upsert the resources
that parsed cleanly -> ensure the search index -> persist + return an
ImportReport. A corrupt/empty ZIP writes nothing at all; within a valid
ZIP, one bad resource is skipped and reported, it never blocks the rest
of the batch.
"""

from __future__ import annotations

import uuid
import zipfile
from io import BytesIO
from typing import Dict, List, Literal, Optional, Tuple

from db import db

from .indexer import ensure_search_index
from .models import FmsResource, ImportIssue, ImportReport
from .module_map import extract_module_prerequisites
from .parser import parse_markdown_file
from .validators import validate_batch

# P0-I (Audit Chirurgical 2026-09-07) — ZIP-bomb / upload-abuse
# protections. `api/fms.py`'s own `MAX_ZIP_BYTES` (50 MB) only bounds
# the *compressed* upload — it says nothing about what `zf.read(name)`
# decompresses to in memory. A ZIP's central directory carries each
# entry's real (`file_size`) and compressed (`compress_size`) byte
# counts WITHOUT decompressing anything, so every check below runs
# before a single byte of content is ever read — a crafted archive
# never gets the chance to exhaust memory before being rejected.
# Bounds are deliberately generous for a real métier archive (223 real
# files, none anywhere near these sizes — see the provenance reports
# already committed) while still being finite:
MAX_ZIP_ENTRIES = 5000  # a real métier batch is ~20-30 files
MAX_ENTRY_UNCOMPRESSED_BYTES = 10 * 1024 * 1024  # 10 MB — no real
# Markdown lesson/quiz/rubric file in this corpus approaches 1 MB
MAX_TOTAL_UNCOMPRESSED_BYTES = 300 * 1024 * 1024  # 300 MB aggregate
# across every .md entry in one archive — catches "many merely-large
# files" bombs a single per-entry cap alone would miss
MAX_COMPRESSION_RATIO = 100  # file_size / compress_size; real prose
# Markdown compresses ~2-6x — a crafted bomb (e.g. run-length-encodable
# filler) compresses at ratios in the thousands. Only applied to
# entries already past a minimum absolute size, so a tiny file's
# naturally noisy ratio never false-positives.
RATIO_CHECK_MIN_BYTES = 4096

# `zf.read()` never writes to disk (parsed content goes straight to
# `parse_markdown_file`, in memory) and `source_file` is stored purely
# as display/provenance metadata (grep-confirmed: no code path anywhere
# in this repo uses it to build a filesystem path) — so a path-
# traversal entry name (`../../etc/passwd`) has no exploitable target
# here and is deliberately not treated as a rejection case, unlike the
# size/ratio bounds above.


def _extract_markdown_files(
    raw_zip: bytes,
) -> Tuple[List[Tuple[str, str]], List[ImportIssue]]:
    issues: List[ImportIssue] = []
    files: List[Tuple[str, str]] = []
    try:
        zf = zipfile.ZipFile(BytesIO(raw_zip))
    except zipfile.BadZipFile:
        issues.append(
            ImportIssue(
                level="error", file="<archive>", message="ZIP invalide ou corrompu."
            )
        )
        return [], issues

    if len(zf.infolist()) > MAX_ZIP_ENTRIES:
        issues.append(
            ImportIssue(
                level="error",
                file="<archive>",
                message=(
                    f"Archive rejetée : {len(zf.infolist())} entrées, "
                    f"maximum {MAX_ZIP_ENTRIES}."
                ),
            )
        )
        return [], issues

    bad_entry = zf.testzip()
    if bad_entry:
        issues.append(
            ImportIssue(
                level="error",
                file=bad_entry,
                message="Entrée ZIP corrompue (CRC invalide).",
            )
        )

    md_infos = [
        info
        for info in zf.infolist()
        if info.filename.lower().endswith(".md") and not info.filename.endswith("/")
    ]
    if not md_infos:
        issues.append(
            ImportIssue(
                level="error",
                file="<archive>",
                message="Aucun fichier .md trouvé dans le ZIP.",
            )
        )
        return [], issues

    total_uncompressed = sum(info.file_size for info in md_infos)
    if total_uncompressed > MAX_TOTAL_UNCOMPRESSED_BYTES:
        issues.append(
            ImportIssue(
                level="error",
                file="<archive>",
                message=(
                    f"Archive rejetée : {total_uncompressed} octets décompressés "
                    f"au total, maximum {MAX_TOTAL_UNCOMPRESSED_BYTES}."
                ),
            )
        )
        return [], issues

    for info in md_infos:
        name = info.filename
        if info.file_size > MAX_ENTRY_UNCOMPRESSED_BYTES:
            issues.append(
                ImportIssue(
                    level="error",
                    file=name,
                    message=(
                        f"Fichier ignoré : {info.file_size} octets décompressés, "
                        f"maximum {MAX_ENTRY_UNCOMPRESSED_BYTES}."
                    ),
                )
            )
            continue
        if (
            info.file_size >= RATIO_CHECK_MIN_BYTES
            and info.file_size > info.compress_size * MAX_COMPRESSION_RATIO
        ):
            issues.append(
                ImportIssue(
                    level="error",
                    file=name,
                    message=(
                        "Fichier ignoré : taux de compression anormal "
                        f"({info.file_size}/{max(info.compress_size, 1)}), "
                        "signature typique d'une ZIP bomb."
                    ),
                )
            )
            continue

        try:
            raw = zf.read(name)
        except (KeyError, zipfile.BadZipFile) as e:
            issues.append(
                ImportIssue(
                    level="error", file=name, message=f"Lecture impossible : {e}"
                )
            )
            continue
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            issues.append(
                ImportIssue(
                    level="error",
                    file=name,
                    message="Encodage non-UTF-8 — fichier ignoré.",
                )
            )
            continue
        files.append((name, text))

    return files, issues


def _apply_module_map_dependencies(resources: List[FmsResource]) -> None:
    """Mutates `module` resources in place: sets `.prerequisites` from
    their métier's Master Module Map, when one was included in this batch.
    See module_map.py for exactly what is and isn't extracted."""
    module_maps = [r for r in resources if r.type == "module_map" and r.formation_code]
    for module_map in module_maps:
        deps = extract_module_prerequisites(module_map.body_markdown)
        if not deps:
            continue
        formation_code = module_map.formation_code
        for r in resources:
            if r.type != "module" or r.formation_code != formation_code:
                continue
            # A module's own code is "<formation_code>-M07" — match its
            # trailing "M07" against the map's keys.
            module_num = r.code.rsplit("-", 1)[-1]
            if module_num in deps:
                r.prerequisites = [f"{formation_code}-{m}" for m in deps[module_num]]


async def import_fms_zip(
    raw_zip: bytes, filename: str, created_by: Optional[str] = None
) -> ImportReport:
    all_issues: List[ImportIssue] = []
    md_files, extract_issues = _extract_markdown_files(raw_zip)
    all_issues.extend(extract_issues)

    if not md_files:
        report = ImportReport(
            filename=filename,
            status="failed",
            issues=all_issues,
            created_by=created_by,
        )
        await db.fms_imports.insert_one(report.model_dump())
        return report

    import_id = str(uuid.uuid4())

    resources: List[FmsResource] = []
    for name, content in md_files:
        resource, parse_issues = parse_markdown_file(name, content, import_id)
        all_issues.extend(parse_issues)
        if resource:
            resources.append(resource)

    _apply_module_map_dependencies(resources)

    batch_issues = validate_batch(resources)
    all_issues.extend(batch_issues)

    # A per-resource error (e.g. a module missing formation_code) skips
    # only that resource — the rest of the batch still imports. Archive-
    # level errors (bad zip, no markdown) already returned above.
    files_with_errors = {i.file for i in all_issues if i.level == "error"}
    resources_to_persist = [
        r for r in resources if r.source_file not in files_with_errors
    ]

    for r in resources_to_persist:
        await db.fms_resources.update_one(
            {"code": r.code}, {"$set": r.model_dump()}, upsert=True
        )

    await ensure_search_index()

    resources_by_type: Dict[str, int] = {}
    for r in resources_to_persist:
        resources_by_type[r.type] = resources_by_type.get(r.type, 0) + 1

    status: Literal["success", "partial", "failed"]
    if not resources_to_persist:
        status = "failed"
    elif any(i.level == "error" for i in all_issues):
        status = "partial"
    else:
        status = "success"

    report = ImportReport(
        id=import_id,
        filename=filename,
        status=status,
        resources_created=len(resources_to_persist),
        resources_by_type=resources_by_type,
        issues=all_issues,
        created_by=created_by,
    )
    await db.fms_imports.insert_one(report.model_dump())
    return report
