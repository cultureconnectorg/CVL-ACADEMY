"""Auth (FREK-ID) — Academy authentication with FREKCORE identity delegation.

FREKCORE owns the ecosystem FREK-ID. CVLN Academy owns its local account,
session, pedagogical role, organisation, cohort and progression. Registration
asks FREKCORE for the FREK-ID in integrated mode; Academy does not reimplement
FREKCORE authentication or an identity portal here.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Literal

from auth import (
    consume_email_verification_token,
    consume_password_reset_token,
    get_current_user,
    hash_password,
    issue_email_verification_token,
    issue_password_reset_token,
    issue_refresh_token,
    make_token,
    next_frek_id,
    revoke_all_refresh_tokens,
    rotate_refresh_token,
    user_public,
    verify_password,
)
from db import db
from fastapi import APIRouter, Depends, HTTPException
from models import (
    AuthResponse,
    ForgotPasswordInput,
    LoginInput,
    RefreshTokenInput,
    RegisterInput,
    ResetPasswordInput,
    User,
    UserPublic,
    VerifyEmailInput,
)
from pydantic import BaseModel
from services.frek_core import frek_core
from services.notifications import notifications

router = APIRouter(prefix="/auth", tags=["auth"])

OAUTH_PROVIDERS = ("google", "apple", "github", "microsoft")


def _provider_env_configured(provider: str) -> bool:
    return bool(os.environ.get(f"OAUTH_{provider.upper()}_CLIENT_ID"))


async def _apply_invitation(user_id: str, invite_code: str) -> None:
    """Consume an org/cohort invitation at signup time."""
    inv = await db.invitations.find_one({"code": invite_code}, {"_id": 0})
    if not inv:
        raise HTTPException(status_code=400, detail="Code d'invitation invalide")
    if inv.get("used_by"):
        raise HTTPException(status_code=400, detail="Code d'invitation déjà utilisé")
    if inv.get("expires_at"):
        expires_at = datetime.fromisoformat(inv["expires_at"])
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if expires_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=400, detail="Code d'invitation expiré")

    await db.users.update_one(
        {"id": user_id},
        {
            "$set": {
                "role": inv["role"],
                "org_id": inv.get("org_id"),
                "cohort_id": inv.get("cohort_id"),
            }
        },
    )
    await db.invitations.update_one(
        {"code": invite_code},
        {
            "$set": {
                "used_by": user_id,
                "used_at": datetime.now(timezone.utc).isoformat(),
            }
        },
    )


@router.post("/register", response_model=AuthResponse)
async def register(inp: RegisterInput):
    email = inp.email.lower()
    existing = await db.users.find_one({"email": email}, {"_id": 0})
    if existing:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    frek_id = await next_frek_id(
        email,
        metadata={"application": "cvln_academy", "lang": inp.lang},
    )

    existing_frek = await db.users.find_one({"frek_id": frek_id}, {"_id": 0})
    if existing_frek:
        raise HTTPException(
            status_code=409,
            detail="Ce FREK-ID est déjà lié à un compte CVLN Academy",
        )

    user = User(
        frek_id=frek_id,
        email=email,
        display_name=inp.display_name.strip(),
        password_hash=hash_password(inp.password),
        lang=inp.lang,
        cc_credits=5,
    )
    await db.users.insert_one(user.model_dump())

    if inp.invite_code:
        await _apply_invitation(user.id, inp.invite_code)
        refreshed = await db.users.find_one({"id": user.id}, {"_id": 0})
        if refreshed:
            user = User(**refreshed)

    await frek_core.emit_signal(user.id, "FREK-TIME", {"reason": "profile_created"})

    verify_token = await issue_email_verification_token(user.id)
    await notifications.send_email_verification(user.email, verify_token, user.lang)

    refresh_token = await issue_refresh_token(user.id)
    return AuthResponse(
        token=make_token(user.id), refresh_token=refresh_token, user=user_public(user)
    )


@router.post("/login", response_model=AuthResponse)
async def login(inp: LoginInput):
    doc = await db.users.find_one({"email": inp.email.lower()}, {"_id": 0})
    if not doc or not verify_password(inp.password, doc.get("password_hash", "")):
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    user = User(**doc)
    refresh_token = await issue_refresh_token(user.id)
    return AuthResponse(
        token=make_token(user.id), refresh_token=refresh_token, user=user_public(user)
    )


@router.post("/refresh", response_model=AuthResponse)
async def refresh(inp: RefreshTokenInput):
    new_access, new_refresh, user_id = await rotate_refresh_token(inp.refresh_token)
    doc = await db.users.find_one({"id": user_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=401, detail="User not found")
    return AuthResponse(
        token=new_access, refresh_token=new_refresh, user=user_public(User(**doc))
    )


@router.post("/logout")
async def logout(current: User = Depends(get_current_user)):
    await revoke_all_refresh_tokens(current.id)
    return {"ok": True}


@router.get("/me", response_model=UserPublic)
async def me(current: User = Depends(get_current_user)):
    return user_public(current)


@router.post("/forgot-password")
async def forgot_password(inp: ForgotPasswordInput):
    doc = await db.users.find_one({"email": inp.email.lower()}, {"_id": 0})
    if doc:
        token = await issue_password_reset_token(doc["id"])
        await notifications.send_password_reset(
            doc["email"], token, doc.get("lang", "fr")
        )
    return {"ok": True}


@router.post("/reset-password")
async def reset_password(inp: ResetPasswordInput):
    user_id = await consume_password_reset_token(inp.token)
    await db.users.update_one(
        {"id": user_id}, {"$set": {"password_hash": hash_password(inp.new_password)}}
    )
    await revoke_all_refresh_tokens(user_id)
    return {"ok": True}


@router.post("/resend-verification")
async def resend_verification(current: User = Depends(get_current_user)):
    if current.email_verified:
        return {"ok": True, "already_verified": True}
    token = await issue_email_verification_token(current.id)
    await notifications.send_email_verification(current.email, token, current.lang)
    return {"ok": True}


@router.post("/verify-email")
async def verify_email(inp: VerifyEmailInput):
    user_id = await consume_email_verification_token(inp.token)
    await db.users.update_one({"id": user_id}, {"$set": {"email_verified": True}})
    return {"ok": True}


@router.get("/oauth/providers")
async def oauth_providers():
    return [
        {"provider": p, "configured": _provider_env_configured(p)}
        for p in OAUTH_PROVIDERS
    ]


@router.get("/oauth/{provider}/start")
async def oauth_start(provider: Literal["google", "apple", "github", "microsoft"]):
    if not _provider_env_configured(provider):
        raise HTTPException(
            status_code=501,
            detail=(
                f"OAuth {provider} non configuré côté serveur "
                f"(définir OAUTH_{provider.upper()}_CLIENT_ID)."
            ),
        )
    raise HTTPException(status_code=501, detail="Flux OAuth non encore implémenté.")


class TotpVerifyInput(BaseModel):
    code: str


@router.post("/2fa/enroll")
async def enroll_2fa(current: User = Depends(get_current_user)):
    raise HTTPException(
        status_code=501, detail="2FA pas encore activé sur ce déploiement."
    )


@router.post("/2fa/verify")
async def verify_2fa(inp: TotpVerifyInput, current: User = Depends(get_current_user)):
    raise HTTPException(
        status_code=501, detail="2FA pas encore activé sur ce déploiement."
    )
