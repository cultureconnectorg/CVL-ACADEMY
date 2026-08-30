"""Skill engine API — registry + a user's own progression."""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends

from auth import get_current_user
from db import db
from models import User
from skills import Skill, SkillProgressSummary, get_user_progress

router = APIRouter(prefix="/skills", tags=["skills"])


@router.get("", response_model=List[Skill])
async def list_skills(metier: Optional[str] = None):
    skill_filter = {"metier": metier} if metier else {}
    docs = await db.skills.find(skill_filter, {"_id": 0}).to_list(1000)
    return [Skill(**d) for d in docs]


@router.get("/mine", response_model=List[SkillProgressSummary])
async def my_skills(
    metier: Optional[str] = None, current: User = Depends(get_current_user)
):
    return await get_user_progress(current.id, metier)
