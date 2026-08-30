"""Skill progression engine — records evidence, recomputes state.

v1 rule (documented, deliberately simple — tune once real usage data
exists): a skill needs 2 pieces of evidence to be "acquired", or a single
`certification` evidence entry (a jury sign-off is authoritative on its
own). `progression_pct` is evidence_count/2 capped at 100, except a
certification entry jumps straight to 100.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, List, Optional

from db import db, utc_now_iso

from .models import (
    EvidenceEntry,
    EvidenceType,
    Skill,
    SkillProgressSummary,
    SkillState,
    UserSkill,
)

ACQUIRED_AT_EVIDENCE_COUNT = 2


def _hash_evidence(payload: Dict[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()


async def register_skill(
    skill_id: str, metier: str, niveau: str, bloc: str, label: str
) -> Skill:
    existing = await db.skills.find_one({"id": skill_id}, {"_id": 0})
    if existing:
        return Skill(**existing)
    skill = Skill(id=skill_id, metier=metier, niveau=niveau, bloc=bloc, label=label)
    await db.skills.insert_one(skill.model_dump())
    return skill


async def record_evidence(
    user_id: str,
    skill_id: str,
    evidence_type: EvidenceType,
    ref: str,
    detail: Optional[str] = None,
) -> EvidenceEntry:
    payload: Dict[str, Any] = {
        "user_id": user_id,
        "skill_id": skill_id,
        "evidence_type": evidence_type,
        "ref": ref,
        "detail": detail,
        "ts": utc_now_iso(),
    }
    entry = EvidenceEntry(
        user_id=user_id,
        skill_id=skill_id,
        evidence_type=evidence_type,
        ref=ref,
        detail=detail,
        sha256=_hash_evidence(payload),
    )
    await db.skill_evidence.insert_one(entry.model_dump())
    await _recompute_user_skill(user_id, skill_id)
    return entry


async def _recompute_user_skill(user_id: str, skill_id: str) -> UserSkill:
    entries = await db.skill_evidence.find(
        {"user_id": user_id, "skill_id": skill_id}, {"_id": 0}
    ).to_list(1000)
    count = len(entries)
    has_certification = any(e["evidence_type"] == "certification" for e in entries)

    state: SkillState
    pct: int
    if count == 0:
        state, pct = "not_started", 0
    elif has_certification or count >= ACQUIRED_AT_EVIDENCE_COUNT:
        state, pct = "acquired", 100
    else:
        state, pct = "in_progress", int(count / ACQUIRED_AT_EVIDENCE_COUNT * 100)

    user_skill = UserSkill(
        user_id=user_id,
        skill_id=skill_id,
        state=state,
        progression_pct=pct,
        evidence_count=count,
    )
    await db.user_skills.update_one(
        {"user_id": user_id, "skill_id": skill_id},
        {"$set": user_skill.model_dump()},
        upsert=True,
    )
    return user_skill


async def get_user_progress(
    user_id: str, metier: Optional[str] = None
) -> List[SkillProgressSummary]:
    skill_filter: Dict[str, Any] = {"metier": metier} if metier else {}
    skills = await db.skills.find(skill_filter, {"_id": 0}).to_list(1000)
    progress_docs = await db.user_skills.find({"user_id": user_id}, {"_id": 0}).to_list(
        1000
    )
    progress_by_skill = {p["skill_id"]: p for p in progress_docs}

    summaries = []
    for s in skills:
        skill = Skill(**s)
        p = progress_by_skill.get(skill.id)
        summaries.append(
            SkillProgressSummary(
                skill=skill,
                state=p["state"] if p else "not_started",
                progression_pct=p["progression_pct"] if p else 0,
                evidence_count=p["evidence_count"] if p else 0,
            )
        )
    return summaries
