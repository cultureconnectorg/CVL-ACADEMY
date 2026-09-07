"""Server-side import of the real `docs/frk/frkNN/` tree into
`db.frk_resources` — the one new, additive collection this whole
package writes to. **Never writes to `db.formations`, `seed_data.py`,
`db.progress`, or any legacy route.**

Same shape as `kor_canonical/import_pipeline.py`/
`klt_canonical/import_pipeline.py`: the corpus already lives unpacked
in this repo, so "import" means "scan the real filesystem tree and
persist a structured read model of it", triggered by an admin action
(or the MOCK_DB preview auto-import in `server.py`), not a file
upload. Re-running it is idempotent (upsert by `source_file` +
`canonical_version`) — it never duplicates.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from db import db

from .models import FRK_CANONICAL_VERSION_CURRENT, FrkCanonicalImportResult
from .parser import classify_resource_type, extract_heading_title, formation_code_from_path, parse_referential
from .provenance import default_docs_dir, list_real_files, store_frk_provenance

COLLECTION = "frk_resources"


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
        "title": extract_heading_title(text),
        "updated_at": _now(),
    }
    if resource_type == "referential":
        parsed = parse_referential(relative_path, text)
        payload.update(
            {
                "title": parsed["title"],
                "status": parsed["status"],
                "needs_expert_review": parsed["needs_expert_review"],
                "prerequisites": parsed["prerequisites"],
                "objectives": parsed["objectives"],
                "assessment_summary": parsed["assessment_summary"],
                "modules": parsed["modules"],
            }
        )

    await db[COLLECTION].update_one(
        {"source_file": relative_path, "canonical_version": canonical_version},
        {"$set": payload},
        upsert=True,
    )


async def import_frk_docs(
    docs_dir: Optional[Path] = None,
    *,
    canonical_version: str = FRK_CANONICAL_VERSION_CURRENT,
    created_by: Optional[str] = None,
) -> FrkCanonicalImportResult:
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
        # A formation is only ever considered "found" (importable as a
        # real, learner-visible formation) when its REFERENTIAL.md is
        # present — the 10 GAP.md-only formations (BLOCKED_PRODUCT_
        # DEPENDENCY) never populate this set, matching read_model.py's
        # own gate.
        if formation_code and resource_type == "referential":
            formations_found.add(formation_code)
        await _persist_resource(
            relative_path=relative_path,
            resource_type=resource_type,
            formation_code=formation_code,
            text=text,
            canonical_version=canonical_version,
        )
        parsed_count += 1

    provenance_records, _inserted, _updated = await store_frk_provenance(
        docs_dir, canonical_version=canonical_version
    )
    total_files = len(provenance_records)
    unparsed_count = total_files - parsed_count

    import_id = str(uuid.uuid4())
    await db.frk_imports.insert_one(
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

    return FrkCanonicalImportResult(
        import_id=import_id,
        docs_dir=str(docs_dir),
        total_files=total_files,
        parsed_count=parsed_count,
        unparsed_count=unparsed_count,
        formations_found=sorted(formations_found),
        all_files_accounted_for=(total_files == len(files)),
    )
