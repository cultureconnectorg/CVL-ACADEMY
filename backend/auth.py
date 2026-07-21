"""FrekID auth — JWT + bcrypt.

The `frek_id` field is a stable, unique cultural identifier assigned at registration.
This module is designed to be extended: `_generate_frek_id` and `frek_core` integration
should later delegate to the external FrekCore service.
"""
from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from db import db
from models import User, UserPublic
from services.frek_core import frek_core

JWT_SECRET = os.environ["JWT_SECRET"]
JWT_ALGO = "HS256"
JWT_EXPIRE_DAYS = 30

bearer = HTTPBearer(auto_error=False)


def hash_password(pw: str) -> str:
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()


def verify_password(pw: str, ph: str) -> bool:
    try:
        return bcrypt.checkpw(pw.encode(), ph.encode())
    except Exception:
        return False


def make_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(days=JWT_EXPIRE_DAYS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)


def decode_token(token: str) -> Optional[str]:
    try:
        p = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        return p.get("sub")
    except Exception:
        return None


async def next_frek_id() -> str:
    """Delegates to FrekCore integration layer. Falls back to local sequential."""
    return await frek_core.mint_frek_id()


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


def user_public(u: User) -> UserPublic:
    return UserPublic(
        id=u.id, frek_id=u.frek_id, email=u.email, display_name=u.display_name,
        lang=u.lang, stade=u.stade, cc_credits=u.cc_credits, signals=u.signals,
        created_at=u.created_at,
    )
