"""FrekID auth — JWT access tokens + rotating refresh tokens + bcrypt.

The ``frek_id`` field is a stable, unique cultural identifier assigned at
registration. Academy delegates identity issuance to the FrekCore integration
boundary; in sovereign mode, FrekCore is the only authority allowed to issue
that identifier.

Token scheme:
- Access token: short-lived JWT (JWT_EXPIRE_MINUTES), sent as a Bearer
  header on every request, verified statelessly.
- Refresh token: opaque random string, stored server-side hashed
  (db.refresh_tokens) so it can be revoked; rotates on every use.
"""

from __future__ import annotations

import hashlib
import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Coroutine, Optional, Sequence

import bcrypt
import jwt
from db import db, utc_now_iso
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models import Role, User, UserPublic
from services.frek_core import (
    FrekCoreConfigurationError,
    FrekCoreUnavailableError,
    frek_core,
)

JWT_SECRET = os.environ["JWT_SECRET"]
JWT_ALGO = "HS256"
JWT_EXPIRE_MINUTES = int(os.environ.get("JWT_EXPIRE_MINUTES", "120"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS", "30"))
RESET_TOKEN_EXPIRE_MINUTES = 60
VERIFY_TOKEN_EXPIRE_HOURS = 48

bearer = HTTPBearer(auto_error=False)


def hash_password(pw: str) -> str:
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()


def verify_password(pw: str, ph: str) -> bool:
    try:
        return bcrypt.checkpw(pw.encode(), ph.encode())
    except ValueError:
        return False


def _hash_opaque_token(raw: str) -> str:
    """Opaque (non-JWT) tokens are stored hashed — never plaintext at rest."""
    return hashlib.sha256(raw.encode()).hexdigest()


def make_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)


def decode_token(token: str) -> Optional[str]:
    try:
        p = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
    except jwt.PyJWTError:
        return None
    if p.get("type") != "access":
        return None
    return p.get("sub")


async def issue_refresh_token(user_id: str) -> str:
    raw = secrets.token_urlsafe(48)
    await db.refresh_tokens.insert_one(
        {
            "token_hash": _hash_opaque_token(raw),
            "user_id": user_id,
            "created_at": utc_now_iso(),
            "expires_at": (
                datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
            ).isoformat(),
            "revoked": False,
        }
    )
    return raw


async def rotate_refresh_token(raw_token: str) -> tuple[str, str, str]:
    """Validate + revoke the given refresh token and issue a fresh pair."""
    token_hash = _hash_opaque_token(raw_token)
    doc = await db.refresh_tokens.find_one({"token_hash": token_hash})
    if not doc or doc.get("revoked"):
        raise HTTPException(status_code=401, detail="Refresh token invalide ou révoqué")
    expires_at = datetime.fromisoformat(doc["expires_at"])
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Refresh token expiré")

    user_id = doc["user_id"]
    await db.refresh_tokens.update_one(
        {"token_hash": token_hash}, {"$set": {"revoked": True}}
    )
    new_access = make_token(user_id)
    new_refresh = await issue_refresh_token(user_id)
    return new_access, new_refresh, user_id


async def revoke_all_refresh_tokens(user_id: str) -> None:
    await db.refresh_tokens.update_many(
        {"user_id": user_id}, {"$set": {"revoked": True}}
    )


async def issue_password_reset_token(user_id: str) -> str:
    raw = secrets.token_urlsafe(32)
    await db.password_resets.insert_one(
        {
            "token_hash": _hash_opaque_token(raw),
            "user_id": user_id,
            "expires_at": (
                datetime.now(timezone.utc)
                + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
            ).isoformat(),
            "used": False,
            "created_at": utc_now_iso(),
        }
    )
    return raw


async def consume_password_reset_token(raw_token: str) -> str:
    token_hash = _hash_opaque_token(raw_token)
    doc = await db.password_resets.find_one({"token_hash": token_hash})
    if not doc or doc.get("used"):
        raise HTTPException(status_code=400, detail="Lien de réinitialisation invalide")
    expires_at = datetime.fromisoformat(doc["expires_at"])
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Lien de réinitialisation expiré")
    await db.password_resets.update_one(
        {"token_hash": token_hash}, {"$set": {"used": True}}
    )
    return doc["user_id"]


async def issue_email_verification_token(user_id: str) -> str:
    raw = secrets.token_urlsafe(32)
    await db.email_verifications.insert_one(
        {
            "token_hash": _hash_opaque_token(raw),
            "user_id": user_id,
            "expires_at": (
                datetime.now(timezone.utc) + timedelta(hours=VERIFY_TOKEN_EXPIRE_HOURS)
            ).isoformat(),
            "used": False,
            "created_at": utc_now_iso(),
        }
    )
    return raw


async def consume_email_verification_token(raw_token: str) -> str:
    token_hash = _hash_opaque_token(raw_token)
    doc = await db.email_verifications.find_one({"token_hash": token_hash})
    if not doc or doc.get("used"):
        raise HTTPException(status_code=400, detail="Lien de vérification invalide")
    expires_at = datetime.fromisoformat(doc["expires_at"])
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Lien de vérification expiré")
    await db.email_verifications.update_one(
        {"token_hash": token_hash}, {"$set": {"used": True}}
    )
    return doc["user_id"]


async def next_frek_id(
    email: Optional[str] = None,
    *,
    metadata: Optional[dict[str, Any]] = None,
) -> str:
    """Resolve/issue the ecosystem identity through the configured FREKCORE boundary."""
    try:
        return await frek_core.mint_frek_id(email=email, metadata=metadata)
    except FrekCoreConfigurationError as exc:
        raise HTTPException(
            status_code=503,
            detail="Service d'identité FREKCORE mal configuré",
        ) from exc
    except FrekCoreUnavailableError as exc:
        raise HTTPException(
            status_code=503,
            detail="Service d'identité FREKCORE temporairement indisponible",
        ) from exc


async def get_current_user(
    creds: Optional[HTTPAuthorizationCredentials] = Depends(bearer),
) -> User:
    if not creds:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user_id = decode_token(creds.credentials)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    doc = await db.users.find_one({"id": user_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=401, detail="User not found")
    return User(**doc)


async def get_current_user_optional(
    creds: Optional[HTTPAuthorizationCredentials] = Depends(bearer),
) -> Optional[User]:
    if not creds:
        return None
    user_id = decode_token(creds.credentials)
    if not user_id:
        return None
    doc = await db.users.find_one({"id": user_id}, {"_id": 0})
    return User(**doc) if doc else None


def require_role(*roles: Role) -> Callable[[User], Coroutine[Any, Any, User]]:
    allowed: Sequence[Role] = roles

    async def _dep(current: User = Depends(get_current_user)) -> User:
        if current.role not in allowed:
            raise HTTPException(
                status_code=403, detail="Rôle insuffisant pour cette action"
            )
        return current

    return _dep


def user_public(u: User) -> UserPublic:
    return UserPublic(
        id=u.id,
        frek_id=u.frek_id,
        email=u.email,
        display_name=u.display_name,
        role=u.role,
        org_id=u.org_id,
        cohort_id=u.cohort_id,
        lang=u.lang,
        stade=u.stade,
        cc_credits=u.cc_credits,
        signals=u.signals,
        created_at=u.created_at,
        onboarding_completed=u.onboarding_completed,
        metier_vise=u.metier_vise,
        territoire=u.territoire,
        objectif_perso=u.objectif_perso,
        email_verified=u.email_verified,
        totp_enabled=u.totp_enabled,
    )
