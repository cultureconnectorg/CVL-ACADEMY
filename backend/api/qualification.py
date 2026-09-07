"""Qualification Engine API — RAIL 2 ("Master -> Runtime Academy",
Founder, 2026-09-06). Definitions are admin-configured; issuance is
never a direct API call (it only ever happens inside
`certification/service.py::grade_attempt`) — this router exposes
reads, plus the admin registration endpoint.
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException

from auth import get_current_user, require_role
from models import ADMIN_ROLES, User
from qualification import (Qualification, QualificationDefinition,
                           QualificationDefinitionInput, get_definition,
                           list_definitions, list_user_qualifications,
                           register_definition)

router = APIRouter(prefix="/qualifications", tags=["qualification"])


@router.post("/definitions/{code}", response_model=QualificationDefinition)
async def create_or_update_definition(
    code: str,
    inp: QualificationDefinitionInput,
    current: User = Depends(require_role(*ADMIN_ROLES)),
):
    return await register_definition(code, inp)


@router.get("/definitions", response_model=List[QualificationDefinition])
async def list_all_definitions(current: User = Depends(get_current_user)):
    return await list_definitions()


@router.get("/definitions/{code}", response_model=QualificationDefinition)
async def read_definition(code: str, current: User = Depends(get_current_user)):
    definition = await get_definition(code)
    if not definition:
        raise HTTPException(status_code=404, detail="Qualification introuvable")
    return definition


@router.get("/mine", response_model=List[Qualification])
async def my_qualifications(current: User = Depends(get_current_user)):
    return await list_user_qualifications(current.id)
