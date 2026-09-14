"""Exhaustive, read-only inventory of every real file under
`docs/kor/korXX/` — same discipline `fms_canonical/provenance.py` and
`klt_canonical/provenance.py` already apply: every file is accounted
for, parsed or not, never silently dropped.
"""

from __future__ import annotations

import hashlib
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Tuple

from db import db

from .models import (KOR_CANONICAL_VERSION_CURRENT, KorFileProvenance,
                     resource_audience)
from .parser import (classify_resource_type, formation_code_from_path,
                     module_number_from_filename)

COLLECTION = "kor_resource_provenance"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def default_docs_dir() -> Path:
    """`backend/kor_canonical/provenance.py` -> repo root -> `docs/kor`.
    Overridable via `KOR_DOCS_DIR` for deployments where the docs tree
    isn't a sibling of `backend/`."""
    override = os.environ.get("KOR_DOCS_DIR")
    if override:
        return Path(override)
    return Path(__file__).resolve().parent.parent.parent / "docs" / "kor"


def list_real_files(docs_dir: Path) -> List[Path]:
    """Every real file under `docs_dir`, `korXX/` subtrees only — the
    root `README.md` is real but out of scope for this inventory (it's
    a corpus-level status summary, not a kor-formation-scoped resource)."""
    if not docs_dir.is_dir():
        return []
    files: List[Path] = []
    for entry in sorted(docs_dir.iterdir()):
        if entry.is_dir() and entry.name.startswith("kor"):
            for path in sorted(entry.rglob("*")):
                if path.is_file():
                    files.append(path)
    return files


def build_kor_inventory(
    docs_dir: Optional[Path] = None,
    *,
    canonical_version: str = KOR_CANONICAL_VERSION_CURRENT,
) -> List[KorFileProvenance]:
    """Pure, read-only. Every real file under `docs/kor/korXX/` becomes
    exactly one record — parsed or not, never dropped."""
    docs_dir = docs_dir or default_docs_dir()
    records: List[KorFileProvenance] = []

    for path in list_real_files(docs_dir):
        relative_path = str(path.relative_to(docs_dir)).replace(os.sep, "/")
        raw_bytes = path.read_bytes()
        sha256 = hashlib.sha256(raw_bytes).hexdigest()
        byte_size = len(raw_bytes)

        try:
            raw_bytes.decode("utf-8")
        except UnicodeDecodeError:
            records.append(
                KorFileProvenance(
                    original_path=relative_path,
                    original_filename=path.name,
                    sha256=sha256,
                    byte_size=byte_size,
                    canonical_version=canonical_version,
                    parsing_status="unparsed_error",
                    parsing_note="Encodage non-UTF-8.",
                )
            )
            continue

        resource_type = classify_resource_type(relative_path)
        formation_code = formation_code_from_path(relative_path)

        if resource_type is None:
            records.append(
                KorFileProvenance(
                    original_path=relative_path,
                    original_filename=path.name,
                    sha256=sha256,
                    byte_size=byte_size,
                    formation_code=formation_code,
                    canonical_version=canonical_version,
                    parsing_status="unparsed_no_type_match",
                    parsing_note=(
                        "Fichier réel, hors convention de classification "
                        "confirmée (voir parser.py::classify_resource_type — "
                        "seule la convention KOR-01 est reconnue à ce stade)."
                    ),
                )
            )
            continue

        module_number = (
            module_number_from_filename(path.name)
            if resource_type == "module"
            else None
        )

        records.append(
            KorFileProvenance(
                original_path=relative_path,
                original_filename=path.name,
                sha256=sha256,
                byte_size=byte_size,
                resource_type=resource_type,
                formation_code=formation_code,
                module_number=module_number,
                audience=resource_audience(resource_type),
                canonical_version=canonical_version,
                parsing_status="parsed",
            )
        )

    return records


async def store_kor_provenance(
    docs_dir: Optional[Path] = None,
    *,
    canonical_version: str = KOR_CANONICAL_VERSION_CURRENT,
) -> Tuple[List[KorFileProvenance], int, int]:
    """Idempotent by `original_path` + `canonical_version` — re-running
    against the same docs tree overwrites each record, never
    duplicates. Returns (records, inserted_count, updated_count)."""
    records = build_kor_inventory(docs_dir, canonical_version=canonical_version)
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


async def list_kor_provenance(
    *, canonical_version: str = KOR_CANONICAL_VERSION_CURRENT
) -> List[KorFileProvenance]:
    docs = (
        await db[COLLECTION]
        .find({"canonical_version": canonical_version}, {"_id": 0})
        .to_list(1000)
    )
    return [KorFileProvenance(**d) for d in docs]
