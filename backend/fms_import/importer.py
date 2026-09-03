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

    bad_entry = zf.testzip()
    if bad_entry:
        issues.append(
            ImportIssue(
                level="error",
                file=bad_entry,
                message="Entrée ZIP corrompue (CRC invalide).",
            )
        )

    md_entries = [
        n for n in zf.namelist() if n.lower().endswith(".md") and not n.endswith("/")
    ]
    if not md_entries:
        issues.append(
            ImportIssue(
                level="error",
                file="<archive>",
                message="Aucun fichier .md trouvé dans le ZIP.",
            )
        )
        return [], issues

    for name in md_entries:
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
