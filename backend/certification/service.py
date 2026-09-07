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

import physical_delivery
from db import db, utc_now_iso
from lx import compute_status
from qualification import maybe_issue_qualification
from services.canonical_convergence import get_canonical_authority
from services.events import events
from services.frek_core import frek_core
from skills.models import EvidenceType
from skills.progression import record_evidence
from wallet import credit as wallet_credit

from .attestation import make_jury_signature
from .models import (
    CertificationAttempt,
    GradeInput,
    PhysicalAssessmentRequirement,
    PhysicalAssessmentRequirementInput,
    Rubric,
)
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


# --------------------------------------------------------------------
# PHYSICAL/HYBRID assessment architecture (Founder decision, 2026-09-07)
#
# ATTENDANCE != ASSESSMENT != SKILL_VALIDATION != CERTIFICATION.
# EXISTING_RUBRIC_ENGINE = REUSE_WHERE_SEMANTICALLY_COMPATIBLE;
# NEW_PARALLEL_RUBRIC_SYSTEM = FORBIDDEN — a "practical" attempt below
# is a real `CertificationAttempt` against a real `Rubric`, graded by
# the exact same `grade_attempt`/`compute_scores` this file already
# has. The only new thing is what gates *starting* one (real attendance,
# not module completion) and how its pass composes into a FINAL
# ("certification"-kind) attempt's eligibility — never instead of it,
# never auto-granting it (AUTO_CERTIFICATION = FORBIDDEN).
# --------------------------------------------------------------------


async def _digital_content_exists(formation_code: str) -> bool:
    """Whether `formation_code` has ANY real digital (legacy or
    canonical) content at all — existence only, not completion. Lets
    `check_full_eligibility` tell a genuine physical-only formation
    (this returns False — the digital leg simply does not apply) apart
    from a hybrid formation with real digital content the candidate
    just hasn't finished (this returns True — the digital leg must
    still be checked for real completion, per HYBRID_DOUBLE_CREDIT =
    FORBIDDEN: a practical pass alone can never cover for unfinished
    digital content when both channels are real)."""
    if await db.formations.find_one({"code": formation_code}, {"_id": 0, "code": 1}):
        return True
    if await fms_canonical.get_canonical_formation(formation_code):
        return True
    if await klt_canonical.get_canonical_klt_formation(formation_code):
        return True
    if await kor_canonical.get_canonical_kor_formation(formation_code):
        return True
    return False


async def get_physical_assessment_requirement(
    certification_code: str,
) -> Optional[PhysicalAssessmentRequirement]:
    doc = await db.physical_assessment_requirements.find_one(
        {"certification_code": certification_code}, {"_id": 0}
    )
    return PhysicalAssessmentRequirement(**doc) if doc else None


async def set_physical_assessment_requirement(
    certification_code: str, inp: PhysicalAssessmentRequirementInput, created_by: str
) -> PhysicalAssessmentRequirement:
    """Staff-only (see api/certification.py's RBAC). Validates both
    certification_codes are real, already-created rubrics, and that the
    named practical rubric really is `assessment_kind == "practical"` —
    never lets a requirement point at a rubric that doesn't exist or
    isn't actually a practical one, which would silently make the gate
    below unsatisfiable or meaningless."""
    final_rubric = await get_rubric(certification_code)
    practical_rubric = await get_rubric(inp.practical_certification_code)
    if practical_rubric.assessment_kind != "practical":
        raise HTTPException(
            status_code=400,
            detail=(
                f"« {inp.practical_certification_code} » n'est pas un référentiel "
                "d'évaluation pratique (assessment_kind != 'practical')."
            ),
        )
    requirement = PhysicalAssessmentRequirement(
        certification_code=certification_code,
        formation_code=final_rubric.formation_code,
        practical_certification_code=inp.practical_certification_code,
        required=inp.required,
        created_by=created_by,
    )
    await db.physical_assessment_requirements.update_one(
        {"certification_code": certification_code},
        {"$set": requirement.model_dump()},
        upsert=True,
    )
    return requirement


async def list_physical_assessment_requirements() -> List[PhysicalAssessmentRequirement]:
    docs = await db.physical_assessment_requirements.find({}, {"_id": 0}).to_list(500)
    return [PhysicalAssessmentRequirement(**d) for d in docs]


async def _passed_practical_attempt(user_id: str, practical_certification_code: str) -> bool:
    doc = await db.certification_attempts.find_one(
        {
            "user_id": user_id,
            "certification_code": practical_certification_code,
            "status": "passed",
        },
        {"_id": 0, "id": 1},
    )
    return doc is not None


async def check_full_eligibility(user_id: str, certification_code: str) -> Tuple[bool, str]:
    """The real, composed gate `start_attempt` uses for a FINAL
    (`assessment_kind == "certification"`) rubric.

    - No `PhysicalAssessmentRequirement` configured for this
      certification_code -> byte-identical to `check_certification_
      eligibility` alone (every rubric that predates this decision,
      and every rubric nobody has explicitly gated with a practical
      requirement, is completely unaffected).
    - A requirement IS configured and `required` -> HYBRID composition,
      AND not OR: the candidate must clear every leg that actually
      applies —
        * digital leg: only applies when the formation has any real
          digital content at all (`_digital_content_exists`); when it
          does, the real existing eligibility check still runs in
          full — a passed practical assessment never substitutes for
          real, unfinished digital content.
        * physical leg: a real, server-recorded PASSED
          `CertificationAttempt` against the configured
          `practical_certification_code` — never inferred from
          attendance alone (ATTENDANCE != CERTIFICATION).
    """
    rubric = await get_rubric(certification_code)
    requirement = await get_physical_assessment_requirement(certification_code)
    if not requirement or not requirement.required:
        return await check_certification_eligibility(user_id, rubric.formation_code)

    if await _digital_content_exists(rubric.formation_code):
        eligible, reason = await check_certification_eligibility(
            user_id, rubric.formation_code
        )
        if not eligible:
            return False, reason

    if not await _passed_practical_attempt(
        user_id, requirement.practical_certification_code
    ):
        return (
            False,
            "Évaluation pratique requise non validée avant cette certification.",
        )

    return True, ""


async def start_practical_attempt(
    user_id: str, certification_code: str, session_id: str
) -> CertificationAttempt:
    """Starts a "practical"-kind attempt — gated on real, server-
    recorded attendance at the named physical session, never on module
    completion (a practical rubric has nothing to do with digital
    content). ATTENDANCE != ASSESSMENT still holds: attendance only
    unlocks being observed/graded, it is not itself the evidence — the
    evidence is whatever `grade_attempt` records once a jury/trainer
    actually grades this attempt."""
    rubric = await get_rubric(certification_code)
    if rubric.assessment_kind != "practical":
        raise HTTPException(
            status_code=400,
            detail=(
                f"« {certification_code} » n'est pas un référentiel d'évaluation "
                "pratique — utilisez le parcours de certification standard."
            ),
        )
    session = await physical_delivery.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session physique introuvable.")
    if session.formation_code != rubric.formation_code:
        raise HTTPException(
            status_code=400,
            detail="Cette session ne correspond pas à la formation de ce référentiel.",
        )
    attended = await db.physical_attendance.find_one(
        {"session_id": session_id, "user_id": user_id, "present": True},
        {"_id": 0, "id": 1},
    )
    if not attended:
        raise HTTPException(
            status_code=403,
            detail=(
                "Présence non constatée pour cette session — l'évaluation "
                "pratique nécessite une présence réelle enregistrée."
            ),
        )
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
        assessment_kind="practical",
        session_id=session_id,
    )
    await db.certification_attempts.insert_one(attempt.model_dump())
    return attempt


async def start_attempt(user_id: str, certification_code: str) -> CertificationAttempt:
    rubric = await get_rubric(certification_code)
    if rubric.assessment_kind == "practical":
        raise HTTPException(
            status_code=400,
            detail=(
                f"« {certification_code} » est un référentiel d'évaluation "
                "pratique — utilisez le parcours d'évaluation physique "
                "(session requise)."
            ),
        )
    eligible, reason = await check_full_eligibility(user_id, certification_code)
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

    # PHYSICAL/HYBRID assessment architecture (Founder decision,
    # 2026-09-07) — "do not confuse delivery evidence with
    # certification": a "practical" attempt's evidence is recorded
    # under its own `evidence_type` ("physical_assessment"), which
    # `skills/progression.py`'s `_recompute_user_skill` does NOT treat
    # as an automatic jump to "acquired" the way "certification" does
    # (AUTO_SKILL_AWARD = FORBIDDEN) — a graded practical pass is real
    # evidence, never itself the authoritative sign-off a final
    # certification's grading already is. Every existing call site
    # (a "certification"-kind attempt) is byte-for-byte unchanged.
    is_practical = attempt.assessment_kind == "practical"
    evidence_type: EvidenceType = "physical_assessment" if is_practical else "certification"
    for c in rubric.criteria:
        if c.skill_id and score_by_competency.get(c.id, 0) >= rubric.pass_threshold_pct:
            await record_evidence(
                user_id=attempt.user_id,
                skill_id=c.skill_id,
                evidence_type=evidence_type,
                ref=attempt_id,
                detail=f"{attempt.certification_code} — {c.label}",
            )

    # AUTO_CERTIFICATION = FORBIDDEN: a passed "practical" attempt is a
    # real prerequisite `check_full_eligibility` can later require for a
    # FINAL certification_code (via PhysicalAssessmentRequirement) — it
    # never itself emits the FREK-CERT signal, credits the certification
    # JCC reward, or issues a qualification. Those effects stay scoped
    # to an actual "certification"-kind pass, exactly as before this
    # architecture existed.
    if passed and not is_practical:
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
