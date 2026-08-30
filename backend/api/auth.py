"""Auth (FrekID) — register / login / me."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from auth import (
    get_current_user,
    hash_password,
    make_token,
    next_frek_id,
    user_public,
    verify_password,
)
from db import db
from models import AuthResponse, LoginInput, RegisterInput, User, UserPublic
from services.frek_core import frek_core

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse)
async def register(inp: RegisterInput):
    existing = await db.users.find_one({"email": inp.email.lower()}, {"_id": 0})
    if existing:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    frek_id = await next_frek_id()
    user = User(
        frek_id=frek_id,
        email=inp.email.lower(),
        display_name=inp.display_name.strip(),
        password_hash=hash_password(inp.password),
        lang=inp.lang,
        cc_credits=5,  # welcome CC per Master OS §3 (5 CC on profile creation)
    )
    doc = user.model_dump()
    await db.users.insert_one(doc)
    # Emit FREK-ID creation signal
    await frek_core.emit_signal(user.id, "FREK-TIME", {"reason": "profile_created"})
    return AuthResponse(token=make_token(user.id), user=user_public(user))


@router.post("/login", response_model=AuthResponse)
async def login(inp: LoginInput):
    doc = await db.users.find_one({"email": inp.email.lower()}, {"_id": 0})
    if not doc or not verify_password(inp.password, doc.get("password_hash", "")):
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    user = User(**doc)
    return AuthResponse(token=make_token(user.id), user=user_public(user))


@router.get("/me", response_model=UserPublic)
async def me(current: User = Depends(get_current_user)):
    return user_public(current)
