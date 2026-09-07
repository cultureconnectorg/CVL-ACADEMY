"""Certification Engine orchestration — the DB-touching half.

scoring.py and attestation.py are pure; this module is what api/certification.py
calls: start an attempt, submit it, have a jury grade it (which scores it,
signs it, records skill evidence, and — once passed — emits the FREK
signal that Rule 11 asks for).
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import fms_canonical
import klt_canonical
import kor_canonical
from fastapi import HTTPException

from db import db, utc_now_iso
from lx import compute_status
from qualification import maybe_issue_qualification
from services.canonical_convergence import get_canonical_authority
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


async def _check_legacy_eligibility(
    user_id: str, formation_code: str
) -> Optional[Tuple[bool, str]]:
    """Returns `None` if `formation_code` isn't a legacy formation at
    all (caller should try the canonical domains next); otherwise the
    real (eligible, reason) verdict for this exact user."""
    form = await db.formations.find_one({"code": formation_code}, {"_id": 0})
    if not form:
        return None
    modules = form.get("modules", [])
    if not modules:
        return False, "Formation sans module — rien à valider avant certification."
    progress_docs = await db.progress.find(
        {"user_id": user_id}, {"_id": 0}
    ).to_list(500)
    prog_by_mod = {p["module_code"]: p for p in progress_docs}
    incomplete = [
        m["code"] for m in modules if compute_status(prog_by_mod.get(m["code"])) != "validated"
    ]
    if incomplete:
        preview = ", ".join(incomplete[:5]) + ("…" if len(incomplete) > 5 else "")
        return False, f"Modules non validés avant certification : {preview}"
    return True, ""


async def _check_canonical_eligibility(
    user_id: str, formation_code: str
) -> Optional[Tuple[bool, str]]:
    """Same contract as `_check_legacy_eligibility`, tried across the
    three canonical domains (FMS/KLT/KOR) in turn. Canonical's one
    honest, server-recorded signal today is `content_viewed_at` (see
    each domain's own progress.py docstring) — real content-viewed
    coverage of every module is the strongest gate this domain can
    honestly enforce right now; it is never relabeled "validated" or
    "completed", the words the legacy path above earns by actually
    clearing a quiz + mini-mission."""
    fms_formation = await fms_canonical.get_canonical_formation(formation_code)
    if fms_formation:
        fms_progress = await fms_canonical.get_user_canonical_progress(
            user_id, canonical_formation_code=formation_code
        )
        fms_viewed = {
            p.canonical_module_code for p in fms_progress if p.content_viewed_at
        }
        missing = [c for c in fms_formation.module_codes_in_order if c not in fms_viewed]
        if missing:
            preview = ", ".join(missing[:5]) + ("…" if len(missing) > 5 else "")
            return False, f"Modules canoniques non consultés avant certification : {preview}"
        return True, ""

    klt_formation = await klt_canonical.get_canonical_klt_formation(formation_code)
    if klt_formation:
        klt_progress = await klt_canonical.get_user_klt_progress(
            user_id, klt_formation_code=formation_code
        )
        klt_viewed = {p.module_code for p in klt_progress if p.content_viewed_at}
        missing = [c for c in klt_formation.module_codes_in_order if c not in klt_viewed]
        if missing:
            preview = ", ".join(missing[:5]) + ("…" if len(missing) > 5 else "")
            return False, f"Modules canoniques non consultés avant certification : {preview}"
        return True, ""

    kor_formation = await kor_canonical.get_canonical_kor_formation(formation_code)
    if kor_formation:
        kor_progress = await kor_canonical.get_user_kor_progress(
            user_id, kor_formation_code=formation_code
        )
        kor_viewed = {p.module_code for p in kor_progress if p.content_viewed_at}
        missing = [c for c in kor_formation.module_codes_in_order if c not in kor_viewed]
        if missing:
            preview = ", ".join(missing[:5]) + ("…" if len(missing) > 5 else "")
            return False, f"Modules canoniques non consultés avant certification : {preview}"
        return True, ""

    return None


async def check_certification_eligibility(
    user_id: str, formation_code: str
) -> Tuple[bool, str]:
    """CERT-01 (Audit Chirurgical 2026-09-07) — real, server-enforced
    eligibility gate. `start_attempt` used to check only that a rubric
    existed for `certification_code`; nothing stopped a candidate who
    had never opened a single module from starting (and, once graded,
    passing) a certification attempt. Tries the legacy formation first,
    then each canonical domain in turn; a `formation_code` that matches
    NONE of them is rejected outright rather than silently allowed —
    an unrecognized formation_code on a rubric is an admin/data error,
    never a reason to skip the gate.

    ACA-0019 (Founder decision, 2026-09-07) —
    CANONICAL_CURRICULUM_RUNTIME = AUTHORITATIVE: fixes a real gate the
    routing-authority change itself broke. For a `formation_code` with
    real canonical content (e.g. FMS-01, which also still has a legacy
    `db.formations` doc as READ_ONLY_HISTORY), `get_module_journey` now
    redirects every navigation away from the legacy 7-phase modules —
    so a learner routed exclusively through canonical content can never
    again reach the legacy quiz/mini-mission this gate used to require,
    and `_check_legacy_eligibility` returning non-None (a legacy doc
    exists) meant canonical was never even tried. Without this check,
    certification became permanently unreachable for every learner on
    an authoritative formation. Canonical authority is checked first
    and, when present, is the ONLY path consulted — never composed with
    the legacy verdict, per the same rule that governs navigation:
    canonical is the single active pedagogical source, stale legacy
    progress on that formation_code is never credited toward it."""
    authority = await get_canonical_authority(formation_code)
    if authority:
        canonical = await _check_canonical_eligibility(user_id, formation_code)
        if canonical is not None:
            return canonical
    else:
        legacy = await _check_legacy_eligibility(user_id, formation_code)
        if legacy is not None:
            return legacy
        canonical = await _check_canonical_eligibility(user_id, formation_code)
        if canonical is not None:
            return canonical
    return False, f"Formation « {formation_code} » introuvable (ni legacy, ni canonique)."


async def start_attempt(user_id: str, certification_code: str) -> CertificationAttempt:
    rubric = await get_rubric(certification_code)
    eligible, reason = await check_certification_eligibility(
        user_id, rubric.formation_code
    )
    if not eligible:
        raise HTTPException(status_code=403, detail=reason)
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

    (
        score_by_competency,
        score_by_bloc,
        score_global,
        passed,
        eliminated,
        eliminated_reason,
        mention,
    ) = compute_scores(rubric, grade.scores)
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
                "eliminated": eliminated,
                "eliminated_reason": eliminated_reason,
                "mention": mention,
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
            economic_event_id=f"certification-pass:{attempt_id}",
            currency="jcc",
            ref=attempt.certification_code,
            description=f"Certification {attempt.certification_code} réussie",
        )
        # RAIL 2 — Certification -> Qualification. A pure no-op whenever
        # no QualificationDefinition names this certification_code (the
        # case for every certification flow that predates this ticket:
        # FMS, GMD, WAL, ...) — see qualification/service.py's docstring.
        await maybe_issue_qualification(
            attempt.user_id, attempt.certification_code, attempt_id
        )

    return await _get_attempt(attempt_id)


async def list_user_attempts(user_id: str) -> List[CertificationAttempt]:
    docs = (
        await db.certification_attempts.find({"user_id": user_id}, {"_id": 0})
        .sort("created_at", -1)
        .to_list(200)
    )
    return [CertificationAttempt(**d) for d in docs]


async def list_pending_attempts() -> List[CertificationAttempt]:
    """The jury/corrector grading queue — every attempt awaiting a grade."""
    docs = (
        await db.certification_attempts.find({"status": "submitted"}, {"_id": 0})
        .sort("submitted_at", 1)
        .to_list(200)
    )
    return [CertificationAttempt(**d) for d in docs]


async def get_user_display_info(user_id: str) -> Optional[Dict[str, str]]:
    doc = await db.users.find_one(
        {"id": user_id}, {"_id": 0, "display_name": 1, "frek_id": 1}
    )
    return doc
