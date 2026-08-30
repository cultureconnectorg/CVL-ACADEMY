"""Certification Engine orchestration — the DB-touching half.

scoring.py and attestation.py are pure; this module is what api/certification.py
calls: start an attempt, submit it, have a jury grade it (which scores it,
signs it, records skill evidence, and — once passed — emits the FREK
signal that Rule 11 asks for).
"""

from __future__ import annotations

from typing import Dict, List, Optional

from fastapi import HTTPException

from db import db, utc_now_iso
from services.events import events
from services.frek_core import frek_core
from skills.progression import record_evidence
from wallet import credit as wallet_credit

from .attestation import make_jury_signature
from .models import CertificationAttempt, GradeInput, Rubric
from .scoring import compute_scores

CERTIFICATION_JCC_REWARD = 50.0


async def get_rubric(certification_code: str) -> Rubric:
    doc = await db.certification_rubrics.find_one(
        {"certification_code": certification_code}, {"_id": 0}
    )
    if not doc:
        raise HTTPException(
            status_code=404, detail="Référentiel de certification introuvable"
        )
    return Rubric(**doc)


async def start_attempt(user_id: str, certification_code: str) -> CertificationAttempt:
    rubric = await get_rubric(certification_code)
    prior = await db.certification_attempts.count_documents(
        {"user_id": user_id, "certification_code": certification_code}
    )
    attempt = CertificationAttempt(
        user_id=user_id,
        certification_code=certification_code,
        formation_code=rubric.formation_code,
        level=rubric.level,
        rubric_version=rubric.version,
        attempt_number=prior + 1,
    )
    await db.certification_attempts.insert_one(attempt.model_dump())
    return attempt


async def _get_attempt(attempt_id: str) -> CertificationAttempt:
    doc = await db.certification_attempts.find_one({"id": attempt_id}, {"_id": 0})
    if not doc:
        raise HTTPException(
            status_code=404, detail="Tentative de certification introuvable"
        )
    return CertificationAttempt(**doc)


async def submit_attempt(attempt_id: str, user_id: str) -> CertificationAttempt:
    attempt = await _get_attempt(attempt_id)
    if attempt.user_id != user_id:
        raise HTTPException(
            status_code=403, detail="Cette tentative ne vous appartient pas"
        )
    if attempt.status != "in_progress":
        raise HTTPException(status_code=400, detail="Tentative déjà soumise")
    await db.certification_attempts.update_one(
        {"id": attempt_id},
        {"$set": {"status": "submitted", "submitted_at": utc_now_iso()}},
    )
    return await _get_attempt(attempt_id)


async def grade_attempt(
    attempt_id: str, jury_id: str, grade: GradeInput
) -> CertificationAttempt:
    attempt = await _get_attempt(attempt_id)
    if attempt.status not in ("submitted", "graded"):
        raise HTTPException(
            status_code=400, detail="Cette tentative n'est pas prête à être notée"
        )
    rubric = await get_rubric(attempt.certification_code)

    score_by_competency, score_by_bloc, score_global, passed = compute_scores(
        rubric, grade.scores
    )
    signed_at = utc_now_iso()
    signature = make_jury_signature(attempt_id, jury_id, score_by_competency, signed_at)

    await db.certification_attempts.update_one(
        {"id": attempt_id},
        {
            "$set": {
                "status": "passed" if passed else "failed",
                "raw_scores": grade.scores,
                "score_by_competency": score_by_competency,
                "score_by_bloc": score_by_bloc,
                "score_global": score_global,
                "passed": passed,
                "jury_signature": signature.model_dump(),
                "comments": grade.comments,
                "graded_at": signed_at,
            }
        },
    )

    # Record skill evidence for every criterion the candidate cleared, and
    # emit the FREK-CERT signal once the whole attempt passed.
    for c in rubric.criteria:
        if c.skill_id and score_by_competency.get(c.id, 0) >= rubric.pass_threshold_pct:
            await record_evidence(
                user_id=attempt.user_id,
                skill_id=c.skill_id,
                evidence_type="certification",
                ref=attempt_id,
                detail=f"{attempt.certification_code} — {c.label}",
            )
    if passed:
        await frek_core.emit_signal(
            attempt.user_id,
            "FREK-CERT",
            {"certification": attempt.certification_code, "score": score_global},
        )
        await events.publish(
            "academy.certification.passed",
            {
                "user_id": attempt.user_id,
                "certification_code": attempt.certification_code,
                "formation_code": attempt.formation_code,
                "score_global": score_global,
                "attempt_id": attempt_id,
            },
        )
        await wallet_credit(
            attempt.user_id,
            "jcc_earned",
            CERTIFICATION_JCC_REWARD,
            currency="jcc",
            ref=attempt.certification_code,
            description=f"Certification {attempt.certification_code} réussie",
        )

    return await _get_attempt(attempt_id)


async def list_user_attempts(user_id: str) -> List[CertificationAttempt]:
    docs = (
        await db.certification_attempts.find({"user_id": user_id}, {"_id": 0})
        .sort("created_at", -1)
        .to_list(200)
    )
    return [CertificationAttempt(**d) for d in docs]


async def get_user_display_info(user_id: str) -> Optional[Dict[str, str]]:
    doc = await db.users.find_one(
        {"id": user_id}, {"_id": 0, "display_name": 1, "frek_id": 1}
    )
    return doc
