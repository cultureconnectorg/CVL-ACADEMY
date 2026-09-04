"""Server-side import of the real `docs/klt/kltXX/` tree into
`db.klt_resources` — the one new, additive collection this whole
package writes to. **Never writes to `db.formations`, `seed_data.py`,
`db.progress`, or any legacy route.**

Unlike FMS (a ZIP a human uploads), the Kiltikonet corpus already lives
unpacked in this repo (`docs/klt/`) — so "import" here means "scan the
real filesystem tree and persist a structured read model of it",
triggered by an admin action, not a file upload. Re-running it is
idempotent (upsert by `source_file`) — it never duplicates.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from db import db

from .models import KLT_CANONICAL_VERSION_CURRENT, KltCanonicalImportResult
from .parser import (classify_resource_type, formation_code_from_path,
                     parse_module_file, parse_skill_registry)
from .provenance import default_docs_dir, list_real_files, store_klt_provenance

COLLECTION = "klt_resources"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


async def _persist_resource(
    *,
    relative_path: str,
    resource_type: str,
    formation_code: Optional[str],
    text: str,
    canonical_version: str,
) -> None:
    payload: dict = {
        "source_file": relative_path,
        "type": resource_type,
        "formation_code": formation_code,
        "canonical_version": canonical_version,
        "body_markdown": text,
        "updated_at": _now(),
    }
    if resource_type == "module":
        parsed = parse_module_file(relative_path, text)
        payload.update(
            {
                "module_code": parsed["module_code"],
                "title": parsed["title"],
                "competency_id": parsed["competency_id"],
                "competency_label": parsed["competency_label"],
                "prerequisites_raw": parsed["prerequisites_raw"],
                "assessment_level": parsed["assessment_level"],
                "kiltikonet_dependency": parsed["kiltikonet_dependency"],
                "role_boundaries": parsed["role_boundaries"],
                "frek_proof_mapping": parsed["frek_proof_mapping"],
                "origin": parsed["origin"],
            }
        )
    elif resource_type == "skill_id_registry":
        payload["skill_rows"] = parse_skill_registry(text)

    await db[COLLECTION].update_one(
        {"source_file": relative_path, "canonical_version": canonical_version},
        {"$set": payload},
        upsert=True,
    )


async def import_klt_docs(
    docs_dir: Optional[Path] = None,
    *,
    canonical_version: str = KLT_CANONICAL_VERSION_CURRENT,
    created_by: Optional[str] = None,
) -> KltCanonicalImportResult:
    docs_dir = docs_dir or default_docs_dir()
    files = list_real_files(docs_dir)

    parsed_count = 0
    formations_found: set = set()

    for path in files:
        relative_path = str(path.relative_to(docs_dir)).replace("\\", "/")
        resource_type = classify_resource_type(relative_path)
        if resource_type is None:
            continue
        try:
            text = path.read_bytes().decode("utf-8")
        except UnicodeDecodeError:
            continue
        formation_code = formation_code_from_path(relative_path)
        if formation_code:
            formations_found.add(formation_code)
        await _persist_resource(
            relative_path=relative_path,
            resource_type=resource_type,
            formation_code=formation_code,
            text=text,
            canonical_version=canonical_version,
        )
        parsed_count += 1

    provenance_records, _inserted, _updated = await store_klt_provenance(
        docs_dir, canonical_version=canonical_version
    )
    total_files = len(provenance_records)
    unparsed_count = total_files - parsed_count

    import_id = str(uuid.uuid4())
    await db.klt_imports.insert_one(
        {
            "id": import_id,
            "canonical_version": canonical_version,
            "docs_dir": str(docs_dir),
            "total_files": total_files,
            "parsed_count": parsed_count,
            "unparsed_count": unparsed_count,
            "formations_found": sorted(formations_found),
            "created_by": created_by,
            "created_at": _now(),
        }
    )

    return KltCanonicalImportResult(
        import_id=import_id,
        docs_dir=str(docs_dir),
        total_files=total_files,
        parsed_count=parsed_count,
        unparsed_count=unparsed_count,
        formations_found=sorted(formations_found),
        all_files_accounted_for=(total_files == len(files)),
    )
