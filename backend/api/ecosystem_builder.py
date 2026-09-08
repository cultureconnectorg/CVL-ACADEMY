"""ACA-0030 — Ecosystem Builder surface API.

One real, authenticated endpoint composing what `services/
ecosystem_builder.py`'s module docstring scopes: portfolio, verified
proofs, missions completed, credentials, professional identity, and
ecosystem history — plus the derived `stage` (consumer/learner/
professional/builder). No public route here, unlike `professional_
profile.py`'s `GET /public/{frek_id}` — that's the deliberate public
surface; this one is the private, unified "what have I built" view a
learner reaches from their own nav, always their own data."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from auth import get_current_user
from models import User
from services.ecosystem_builder import (
    EcosystemBuilderSurface,
    compute_ecosystem_builder_surface,
)

router = APIRouter(prefix="/ecosystem-builder", tags=["ecosystem-builder"])


@router.get("/me", response_model=EcosystemBuilderSurface)
async def my_ecosystem_builder_surface(current: User = Depends(get_current_user)):
    return await compute_ecosystem_builder_surface(current)
