"""Certification engine API — rubrics, attempts, jury grading, attestations."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response

from auth import get_current_user, require_role
from certification import (
    CertificationAttempt,
    GradeInput,
    Rubric,
    RubricInput,
    generate_attestation_pdf,
    get_rubric,
    grade_attempt,
    list_pending_attempts,
    list_user_attempts,
    start_attempt,
    submit_attempt,
)
from certification.service import get_user_display_info
from db import db
from models import ADMIN_ROLES, STAFF_ROLES, User

router = APIRouter(prefix="/certifications", tags=["certification"])

JURY_ROLES = ("jury", "corrector", *ADMIN_ROLES)


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
async def list_rubrics():
    docs = await db.certification_rubrics.find({}, {"_id": 0}).to_list(200)
    return [Rubric(**d) for d in docs]


@router.get("/{certification_code}/rubric", response_model=Rubric)
async def read_rubric(certification_code: str):
    return await get_rubric(certification_code)


@router.get("/attempts/pending", response_model=List[CertificationAttempt])
async def pending_attempts(current: User = Depends(require_role(*JURY_ROLES))):
    return await list_pending_attempts()


@router.post("/{certification_code}/attempts", response_model=CertificationAttempt)
async def create_attempt(
    certification_code: str, current: User = Depends(get_current_user)
):
    return await start_attempt(current.id, certification_code)


@router.get("/attempts/mine", response_model=List[CertificationAttempt])
async def my_attempts(current: User = Depends(get_current_user)):
    return await list_user_attempts(current.id)


@router.post("/attempts/{attempt_id}/submit", response_model=CertificationAttempt)
async def submit(attempt_id: str, current: User = Depends(get_current_user)):
    return await submit_attempt(attempt_id, current.id)


@router.post("/attempts/{attempt_id}/grade", response_model=CertificationAttempt)
async def grade(
    attempt_id: str, inp: GradeInput, current: User = Depends(require_role(*JURY_ROLES))
):
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
