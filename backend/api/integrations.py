"""Ecosystem integration status — what docs/INTEGRATIONS_REPORT.md and the
Admin dashboard both read to show what's configured vs. still pending
credentials (rule 9)."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends

from auth import require_role
from models import ADMIN_ROLES, User
from services.integrations import all_integrations

router = APIRouter(prefix="/integrations", tags=["integrations"])


@router.get("")
async def get_integrations(
    current: User = Depends(require_role(*ADMIN_ROLES)),
) -> List[dict]:
    return all_integrations()
