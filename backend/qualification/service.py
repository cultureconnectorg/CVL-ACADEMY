"""Qualification Engine orchestration — the DB-touching half. See
`models.py`'s module docstring for the chain this closes.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, List, Optional

from db import db, utc_now_iso
from skills.progression import get_user_progress

from .models import Qualification, QualificationDefinition, QualificationDefinitionInput


def _hash_issuance(payload: Dict[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()


async def register_definition(
    code: str, inp: QualificationDefinitionInput
) -> QualificationDefinition:
    """Idempotent by `code` — re-registering the same code updates its
    fields (admin correcting a typo, adding a certification path) rather
    than erroring or duplicating."""
    definition = QualificationDefinition(code=code, **inp.model_dump())
    await db.qualification_definitions.update_one(
        {"code": code}, {"$set": definition.model_dump()}, upsert=True
    )
    return definition


async def get_definition(code: str) -> Optional[QualificationDefinition]:
    doc = await db.qualification_definitions.find_one({"code": code}, {"_id": 0})
    return QualificationDefinition(**doc) if doc else None


async def list_definitions() -> List[QualificationDefinition]:
    docs = await db.qualification_definitions.find({}, {"_id": 0}).to_list(500)
    return [QualificationDefinition(**d) for d in docs]


async def _definitions_for_certification(
    certification_code: str,
) -> List[QualificationDefinition]:
    docs = await db.qualification_definitions.find(
        {"certification_codes": certification_code}, {"_id": 0}
    ).to_list(500)
    return [QualificationDefinition(**d) for d in docs]


async def _has_all_required_skills(user_id: str, skill_ids: List[str]) -> bool:
    if not skill_ids:
        return True
    progress = await get_user_progress(user_id)
    acquired = {p.skill.id for p in progress if p.state == "acquired"}
    return all(sid in acquired for sid in skill_ids)


async def maybe_issue_qualification(
    user_id: str, certification_code: str, attempt_id: str
) -> List[Qualification]:
    """Called from `certification/service.py::grade_attempt`'s `if
    passed:` block, once per graded, passing attempt. A no-op — returns
    `[]` — whenever no `QualificationDefinition` names this certification
    code, so every pre-existing certification flow (FMS, GMD, WAL, ...)
    that never registers a definition is completely unaffected.

    Idempotent per (user_id, qualification_code): a candidate who
    re-passes the same certification on a later attempt (e.g. a retake
    after an initial fail elsewhere) is never issued a second copy of
    the same qualification."""
    definitions = await _definitions_for_certification(certification_code)
    issued: List[Qualification] = []
    for definition in definitions:
        existing = await db.qualifications.find_one(
            {"user_id": user_id, "qualification_code": definition.code}, {"_id": 0}
        )
        if existing:
            issued.append(Qualification(**existing))
            continue
        if not await _has_all_required_skills(user_id, definition.required_skill_ids):
            continue

        issued_at = utc_now_iso()
        payload = {
            "user_id": user_id,
            "qualification_code": definition.code,
            "source_certification_code": certification_code,
            "source_attempt_id": attempt_id,
            "ts": issued_at,
        }
        qualification = Qualification(
            user_id=user_id,
            qualification_code=definition.code,
            formation_code=definition.formation_code,
            source_certification_code=certification_code,
            source_attempt_id=attempt_id,
            sha256=_hash_issuance(payload),
            issued_at=issued_at,
        )
        await db.qualifications.insert_one(qualification.model_dump())
        issued.append(qualification)
    return issued


async def list_user_qualifications(user_id: str) -> List[Qualification]:
    docs = (
        await db.qualifications.find({"user_id": user_id}, {"_id": 0})
        .sort("issued_at", -1)
        .to_list(500)
    )
    return [Qualification(**d) for d in docs]


async def is_qualified(user_id: str, qualification_code: str) -> bool:
    doc = await db.qualifications.find_one(
        {"user_id": user_id, "qualification_code": qualification_code}, {"_id": 0, "id": 1}
    )
    return doc is not None


async def has_any_of(user_id: str, qualification_codes: List[str]) -> bool:
    """Used by the Mission eligibility view (the Opportunity chain
    link) — True when `qualification_codes` is empty (open to all, the
    default/backward-compatible case) or when the user holds at least
    one of the named qualifications."""
    if not qualification_codes:
        return True
    count = await db.qualifications.count_documents(
        {"user_id": user_id, "qualification_code": {"$in": qualification_codes}}
    )
    return count > 0
