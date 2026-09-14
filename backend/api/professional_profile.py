"""ACA-0028 — Professional FREK profile as identity surface API.

`GET /professional/profile/mine` and `POST /professional/profile/
visibility` require real authenticated identity, same as every other
domain router. `GET /professional/public/{frek_id}` is deliberately
the one unauthenticated route in this file — see `services/
professional_profile.py`'s own docstring for the privacy contract it
enforces (off by default, opt-in, and non-distinguishing 404 between
"doesn't exist" and "exists but private")."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from auth import get_current_user
from models import User
from services.professional_profile import (
    ProfessionalProfile,
    compute_professional_profile,
    get_public_professional_profile,
    set_profile_visibility,
)

router = APIRouter(prefix="/professional", tags=["professional-profile"])


@router.get("/profile/mine", response_model=ProfessionalProfile)
async def my_professional_profile(current: User = Depends(get_current_user)):
    return await compute_professional_profile(current)


class VisibilityInput(BaseModel):
    is_public: bool


@router.post("/profile/visibility")
async def update_profile_visibility(
    body: VisibilityInput, current: User = Depends(get_current_user)
):
    await set_profile_visibility(current.id, body.is_public)
    return {"is_public": body.is_public}


@router.get("/public/{frek_id}", response_model=ProfessionalProfile)
async def public_professional_profile(frek_id: str):
    profile = await get_public_professional_profile(frek_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profil professionnel introuvable.")
    return profile
