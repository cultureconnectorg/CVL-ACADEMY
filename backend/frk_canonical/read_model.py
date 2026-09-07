"""Canonical FREK read model. Reads `db.frk_resources` (populated by
`import_pipeline.import_frk_docs`, itself a direct read of the real
`docs/frk/` tree). **Never writes to `db.frk_resources`,
`db.formations`, or `db.progress`.**

`fully_complete` is read directly from the corpus's own `## Status`
section (`status == "PACKAGE_COMPLETE"`) — see `models.py`'s module
docstring for why FRK's corpus gives this package a stronger, simpler
real signal than KOR's derived skill-registry invariant.
"""

from __future__ import annotations

from typing import List, Optional

from db import db

from .models import (FRK_CANONICAL_VERSION_CURRENT, FRK_FORMATION_CODES,
                     CanonicalFrkFormation, CanonicalFrkModule, is_learner_facing)
from .parser import canonical_module_code


async def get_canonical_frk_formation(
    formation_code: str, *, canonical_version: str = FRK_CANONICAL_VERSION_CURRENT
) -> Optional[CanonicalFrkFormation]:
    if formation_code not in FRK_FORMATION_CODES:
        return None

    referential_doc = await db.frk_resources.find_one(
        {
            "type": "referential",
            "formation_code": formation_code,
            "canonical_version": canonical_version,
        }
    )
    if not referential_doc:
        return None  # this formation hasn't been imported (or has no
        # real content at all — a BLOCKED_PRODUCT_DEPENDENCY/GAP.md-only
        # or EXTEND_EXISTING code, never fabricated as a formation)

    modules = referential_doc.get("modules") or []
    module_codes = [
        canonical_module_code(formation_code, m["order_index"]) for m in modules
    ]
    status = referential_doc.get("status")

    return CanonicalFrkFormation(
        frk_formation_code=formation_code,
        title=referential_doc.get("title") or formation_code,
        canonical_version=canonical_version,
        status=status or "UNKNOWN",
        needs_expert_review=bool(referential_doc.get("needs_expert_review")),
        fully_complete=(status == "PACKAGE_COMPLETE"),
        prerequisites=referential_doc.get("prerequisites"),
        objectives=referential_doc.get("objectives"),
        assessment_summary=referential_doc.get("assessment_summary"),
        module_codes_in_order=module_codes,
        module_count=len(module_codes),
        certification_scope="FULL" if status == "PACKAGE_COMPLETE" else "PARTIAL",
    )


async def list_canonical_frk_formations(
    *, canonical_version: str = FRK_CANONICAL_VERSION_CURRENT
) -> List[CanonicalFrkFormation]:
    results = []
    for fc in FRK_FORMATION_CODES:
        formation = await get_canonical_frk_formation(
            fc, canonical_version=canonical_version
        )
        if formation:
            results.append(formation)
    return results


async def get_canonical_frk_module(
    formation_code: str,
    module_code: str,
    *,
    canonical_version: str = FRK_CANONICAL_VERSION_CURRENT,
) -> Optional[CanonicalFrkModule]:
    """Learner-safe: a `referential` resource's module list is always
    learner-facing (see `models.py::RESOURCE_AUDIENCE`). Returns `None`
    if not found — never a partially-fabricated result."""
    if formation_code not in FRK_FORMATION_CODES:
        return None

    referential_doc = await db.frk_resources.find_one(
        {
            "type": "referential",
            "formation_code": formation_code,
            "canonical_version": canonical_version,
        }
    )
    if not referential_doc:
        return None

    for m in referential_doc.get("modules") or []:
        code = canonical_module_code(formation_code, m["order_index"])
        if code != module_code:
            continue
        return CanonicalFrkModule(
            frk_formation_code=formation_code,
            module_code=code,
            canonical_version=canonical_version,
            order_index=m["order_index"],
            title=m.get("title") or code,
            description=m.get("description"),
            content_markdown=(
                m.get("raw_text") or m.get("title") or ""
                if is_learner_facing("referential")
                else ""
            ),
            content_source_file=referential_doc.get("source_file")
            or f"{formation_code.lower().replace('-', '')}/REFERENTIAL.md",
        )
    return None


async def list_canonical_frk_modules(
    formation_code: str, *, canonical_version: str = FRK_CANONICAL_VERSION_CURRENT
) -> List[CanonicalFrkModule]:
    formation = await get_canonical_frk_formation(
        formation_code, canonical_version=canonical_version
    )
    if not formation:
        return []
    modules = []
    for code in formation.module_codes_in_order:
        module = await get_canonical_frk_module(
            formation_code, code, canonical_version=canonical_version
        )
        if module:
            modules.append(module)
    return modules
