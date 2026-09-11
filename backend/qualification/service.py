"""Qualification Engine orchestration — DB-touching runtime."""

from __future__ import annotations

import calendar
import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from db import db, utc_now_iso
from skills.progression import get_user_progress

from .models import (
    Qualification,
    QualificationDefinition,
    QualificationDefinitionInput,
)

VALIDITY_MONTHS = {
    "standard": 24,
    "sensitive": 12,
}


def _hash_issuance(payload: Dict[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()


def _add_months_iso(issued_at: str, months: int) -> str:
    issued = datetime.fromisoformat(issued_at.replace("Z", "+00:00"))
    month_index = issued.month - 1 + months
    year = issued.year + month_index // 12
    month = month_index % 12 + 1
    day = min(issued.day, calendar.monthrange(year, month)[1])
    return issued.replace(year=year, month=month, day=day).isoformat()


def _is_not_expired(expires_at: str | None) -> bool:
    if not expires_at:
        return False
    expiry = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
    return expiry > datetime.now(timezone.utc)


async def register_definition(
    code: str,
    inp: QualificationDefinitionInput,
) -> QualificationDefinition:
    definition = QualificationDefinition(code=code, **inp.model_dump())
    await db.qualification_definitions.update_one(
        {"code": code},
        {"$set": definition.model_dump()},
        upsert=True,
    )
    return definition


async def get_definition(code: str) -> Optional[QualificationDefinition]:
    doc = await db.qualification_definitions.find_one(
        {"code": code},
        {"_id": 0},
    )
    return QualificationDefinition(**doc) if doc else None


async def list_definitions() -> List[QualificationDefinition]:
    docs = await db.qualification_definitions.find({}, {"_id": 0}).to_list(500)
    return [QualificationDefinition(**d) for d in docs]


async def _definitions_for_certification(
    certification_code: str,
) -> List[QualificationDefinition]:
    docs = await db.qualification_definitions.find(
        {"certification_codes": certification_code},
        {"_id": 0},
    ).to_list(500)
    return [QualificationDefinition(**d) for d in docs]


async def _has_all_required_skills(
    user_id: str,
    skill_ids: List[str],
) -> bool:
    if not skill_ids:
        return True
    progress = await get_user_progress(user_id)
    acquired = {p.skill.id for p in progress if p.state == "acquired"}
    return all(sid in acquired for sid in skill_ids)


def _effective_qualification(
    doc: dict[str, Any],
    definition: QualificationDefinition | None,
) -> Qualification:
    """Apply Economy validity policy to legacy rows without mutating issuance."""
    payload = dict(doc)
    validity_class = payload.get("validity_class")
    if validity_class not in VALIDITY_MONTHS:
        validity_class = (
            definition.validity_class if definition is not None else "standard"
        )
    validity_months = VALIDITY_MONTHS[validity_class]
    expires_at = payload.get("expires_at")
    if not expires_at and payload.get("issued_at"):
        expires_at = _add_months_iso(payload["issued_at"], validity_months)
    payload["validity_class"] = validity_class
    payload["validity_months"] = validity_months
    payload["expires_at"] = expires_at
    return Qualification(**payload)


async def _latest_qualification_doc(
    user_id: str,
    qualification_code: str,
) -> dict[str, Any] | None:
    docs = await db.qualifications.find(
        {
            "user_id": user_id,
            "qualification_code": qualification_code,
        },
        {"_id": 0},
    ).sort("issued_at", -1).limit(1).to_list(1)
    return docs[0] if docs else None


async def maybe_issue_qualification(
    user_id: str,
    certification_code: str,
    attempt_id: str,
) -> List[Qualification]:
    definitions = await _definitions_for_certification(certification_code)
    issued: List[Qualification] = []
    for definition in definitions:
        existing = await _latest_qualification_doc(user_id, definition.code)
        if existing:
            effective = _effective_qualification(existing, definition)
            # A valid qualification stays idempotent. An expired qualification
            # remains historical; a new passing attempt appends requalification.
            if _is_not_expired(effective.expires_at):
                issued.append(effective)
                continue

        if not await _has_all_required_skills(
            user_id,
            definition.required_skill_ids,
        ):
            continue

        issued_at = utc_now_iso()
        validity_months = VALIDITY_MONTHS[definition.validity_class]
        expires_at = _add_months_iso(issued_at, validity_months)
        payload = {
            "user_id": user_id,
            "qualification_code": definition.code,
            "source_certification_code": certification_code,
            "source_attempt_id": attempt_id,
            "validity_class": definition.validity_class,
            "validity_months": validity_months,
            "issued_at": issued_at,
            "expires_at": expires_at,
        }
        qualification = Qualification(
            user_id=user_id,
            qualification_code=definition.code,
            formation_code=definition.formation_code,
            source_certification_code=certification_code,
            source_attempt_id=attempt_id,
            sha256=_hash_issuance(payload),
            issued_at=issued_at,
            expires_at=expires_at,
            validity_class=definition.validity_class,
            validity_months=validity_months,
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
    result: List[Qualification] = []
    for doc in docs:
        definition = await get_definition(doc["qualification_code"])
        result.append(_effective_qualification(doc, definition))
    return result


async def is_qualified(user_id: str, qualification_code: str) -> bool:
    doc = await _latest_qualification_doc(user_id, qualification_code)
    if not doc:
        return False
    definition = await get_definition(qualification_code)
    effective = _effective_qualification(doc, definition)
    return _is_not_expired(effective.expires_at)


async def has_any_of(
    user_id: str,
    qualification_codes: List[str],
) -> bool:
    if not qualification_codes:
        return True
    docs = await db.qualifications.find(
        {
            "user_id": user_id,
            "qualification_code": {"$in": qualification_codes},
        },
        {"_id": 0},
    ).sort("issued_at", -1).to_list(500)
    seen: set[str] = set()
    for doc in docs:
        code = doc["qualification_code"]
        if code in seen:
            continue
        seen.add(code)
        definition = await get_definition(code)
        effective = _effective_qualification(doc, definition)
        if _is_not_expired(effective.expires_at):
            return True
    return False
