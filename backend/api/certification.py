"""Certification engine API — rubrics, attempts, jury grading, attestations."""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel

import physical_delivery
from auth import get_current_user, require_role
from certification import (
    CertificationAttempt,
    GradeInput,
    PhysicalAssessmentRequirement,
    PhysicalAssessmentRequirementInput,
    Rubric,
    RubricInput,
    generate_attestation_pdf,
    get_physical_assessment_requirement,
    get_rubric,
    grade_attempt,
    list_pending_attempts,
    list_physical_assessment_requirements,
    list_user_attempts,
    set_physical_assessment_requirement,
    start_attempt,
    start_practical_attempt,
    submit_attempt,
)
from certification.service import get_user_display_info
from db import db
from models import ADMIN_ROLES, STAFF_ROLES, User

router = APIRouter(prefix="/certifications", tags=["certification"])

JURY_ROLES = ("jury", "corrector", *ADMIN_ROLES)


class PracticalAttemptInput(BaseModel):
    session_id: str


async def _can_grade(attempt: CertificationAttempt, current: User) -> bool:
    """RBAC must be explicit (Founder decision, PHYSICAL/HYBRID
    assessment architecture, 2026-09-07) — jury/corrector/admin-tier
    keep exactly the same grading authority they already have over any
    "certification"-kind attempt (JURY_ROLES, unchanged). A "practical"
    attempt ADDITIONALLY admits the one trainer this specific physical
    session was assigned to (`TrainingSession.trainer_user_id`) — never
    every trainer, and never a corrector/jury automatically gaining
    trainer-side access or vice versa."""
    if current.role in JURY_ROLES:
        return True
    if attempt.assessment_kind == "practical" and current.role == "trainer" and attempt.session_id:
        session = await physical_delivery.get_session(attempt.session_id)
        return bool(session and session.trainer_user_id == current.id)
    return False


@router.post("/rubrics", response_model=Rubric)
async def create_rubric(
    certification_code: str,
    inp: RubricInput,
    current: User = Depends(require_role(*ADMIN_ROLES)),
):
    existing = await db.certification_rubrics.find_one(
        {"certification_code": certification_code}
    )
    if existing:
        raise HTTPException(
            status_code=400, detail="Un référentiel existe déjà pour ce code"
        )
    rubric = Rubric(certification_code=certification_code, **inp.model_dump())
    await db.certification_rubrics.insert_one(rubric.model_dump())
    return rubric


@router.get("/rubrics", response_model=List[Rubric])
async def list_rubrics(current: User = Depends(get_current_user)):
    """AUTH-01 sweep (Audit Chirurgical 2026-09-07) — a rubric names the
    exact grading criteria (weights, eliminatory skills, mention caps):
    real, protected certification content, not catalogue metadata. Any
    signed-in user (not staff-only — a candidate legitimately consults
    what they'll be graded on), never an anonymous visitor."""
    docs = await db.certification_rubrics.find({}, {"_id": 0}).to_list(200)
    return [Rubric(**d) for d in docs]


@router.get("/{certification_code}/rubric", response_model=Rubric)
async def read_rubric(
    certification_code: str, current: User = Depends(get_current_user)
):
    return await get_rubric(certification_code)


@router.get("/attempts/pending", response_model=List[CertificationAttempt])
async def pending_attempts(current: User = Depends(require_role(*STAFF_ROLES))):
    """RBAC must be explicit — jury/corrector/admin-tier see the full
    queue (every attempt, unchanged); a trainer sees ONLY "practical"
    attempts awaiting grading at a session they were personally
    assigned to, never the full queue and never a "certification"-kind
    attempt (that grading authority stays with jury/corrector/admin)."""
    pending = await list_pending_attempts()
    if current.role in JURY_ROLES:
        return pending
    if current.role == "trainer":
        visible = []
        for attempt in pending:
            if attempt.assessment_kind == "practical" and attempt.session_id:
                session = await physical_delivery.get_session(attempt.session_id)
                if session and session.trainer_user_id == current.id:
                    visible.append(attempt)
        return visible
    return []


@router.post("/{certification_code}/attempts", response_model=CertificationAttempt)
async def create_attempt(
    certification_code: str, current: User = Depends(get_current_user)
):
    return await start_attempt(current.id, certification_code)


@router.post(
    "/{certification_code}/practical-attempts", response_model=CertificationAttempt
)
async def create_practical_attempt(
    certification_code: str,
    inp: PracticalAttemptInput,
    current: User = Depends(get_current_user),
):
    """ATTENDANCE != ASSESSMENT: this only ever gates on a real,
    server-recorded AttendanceRecord for `inp.session_id` — see
    `certification.service.start_practical_attempt`."""
    return await start_practical_attempt(current.id, certification_code, inp.session_id)


@router.get("/attempts/mine", response_model=List[CertificationAttempt])
async def my_attempts(current: User = Depends(get_current_user)):
    return await list_user_attempts(current.id)


@router.post("/attempts/{attempt_id}/submit", response_model=CertificationAttempt)
async def submit(attempt_id: str, current: User = Depends(get_current_user)):
    return await submit_attempt(attempt_id, current.id)


@router.post("/attempts/{attempt_id}/grade", response_model=CertificationAttempt)
async def grade(
    attempt_id: str, inp: GradeInput, current: User = Depends(get_current_user)
):
    doc = await db.certification_attempts.find_one({"id": attempt_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Tentative introuvable")
    attempt = CertificationAttempt(**doc)
    if not await _can_grade(attempt, current):
        raise HTTPException(status_code=403, detail="Accès refusé")
    return await grade_attempt(attempt_id, current.id, inp)


@router.get("/attempts/{attempt_id}/attestation.pdf")
async def attestation_pdf(attempt_id: str, current: User = Depends(get_current_user)):
    doc = await db.certification_attempts.find_one({"id": attempt_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Tentative introuvable")
    attempt = CertificationAttempt(**doc)
    if attempt.user_id != current.id and current.role not in STAFF_ROLES:
        raise HTTPException(status_code=403, detail="Accès refusé")
    if not attempt.passed:
        raise HTTPException(
            status_code=400, detail="Attestation disponible uniquement après réussite"
        )

    user_info = await get_user_display_info(attempt.user_id)
    formation = await db.formations.find_one(
        {"code": attempt.formation_code}, {"_id": 0}
    )
    pdf_bytes = generate_attestation_pdf(
        attempt,
        user_display_name=(user_info or {}).get("display_name", "—"),
        user_frek_id=(user_info or {}).get("frek_id", "—"),
        formation_name=(formation or {}).get("name", attempt.formation_code),
    )
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{attempt.certification_code}-{attempt.id}.pdf"'
        },
    )


# --------------------------------------------------------------------
# PHYSICAL/HYBRID assessment architecture — PhysicalAssessmentRequirement
# admin config. `POST` is ADMIN_ROLES-only (a real staff decision naming
# a real practical rubric); `GET` is any authenticated user (a candidate
# legitimately needs to know a practical assessment is required, same
# rationale as `list_rubrics` above).
# --------------------------------------------------------------------


@router.post(
    "/{certification_code}/physical-assessment-requirement",
    response_model=PhysicalAssessmentRequirement,
)
async def set_physical_requirement(
    certification_code: str,
    inp: PhysicalAssessmentRequirementInput,
    current: User = Depends(require_role(*ADMIN_ROLES)),
):
    return await set_physical_assessment_requirement(certification_code, inp, current.id)


@router.get(
    "/{certification_code}/physical-assessment-requirement",
    response_model=Optional[PhysicalAssessmentRequirement],
)
async def read_physical_requirement(
    certification_code: str, current: User = Depends(get_current_user)
):
    return await get_physical_assessment_requirement(certification_code)


@router.get(
    "/admin/physical-assessment-requirements",
    response_model=List[PhysicalAssessmentRequirement],
)
async def list_physical_requirements(
    current: User = Depends(require_role(*ADMIN_ROLES)),
):
    return await list_physical_assessment_requirements()
