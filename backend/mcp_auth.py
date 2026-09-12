"""Authentication primitives for the private CVLN Academy MCP surface.

The public MCP endpoint remains anonymous/read-only.  The private endpoint is a
separate OAuth 2.1 protected resource and uses scoped bearer tokens issued by
CVLN Academy's authorization server.
"""

from __future__ import annotations

import hashlib
import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Iterable, Optional

import jwt
from mcp.server.auth.provider import AccessToken, TokenVerifier

from db import db, utc_now_iso

JWT_SECRET = os.environ["JWT_SECRET"]
JWT_ALGO = "HS256"
MCP_OAUTH_ISSUER = os.environ.get("MCP_OAUTH_ISSUER", "http://localhost:8000").rstrip("/")
MCP_PRIVATE_RESOURCE = os.environ.get(
    "MCP_PRIVATE_RESOURCE", f"{MCP_OAUTH_ISSUER}/mcp/private"
).rstrip("/")
MCP_ACCESS_TOKEN_MINUTES = int(os.environ.get("MCP_ACCESS_TOKEN_MINUTES", "60"))
MCP_REFRESH_TOKEN_DAYS = int(os.environ.get("MCP_REFRESH_TOKEN_DAYS", "30"))

SCOPES = {
    "academy:profile.read": "Read the connected user's Academy profile.",
    "academy:funding.read": "Read the user's funding cases and prepared dossiers.",
    "academy:funding.write": "Create or update the user's funding dossier drafts.",
    "academy:enrollment.read": "Read the user's enrollment requests.",
    "academy:enrollment.write": "Create an enrollment request for a published formation.",
}
DEFAULT_SCOPES = ("academy:profile.read",)


def normalize_scopes(scopes: Iterable[str]) -> list[str]:
    clean = []
    for scope in scopes:
        if scope in SCOPES and scope not in clean:
            clean.append(scope)
    return clean


def scope_string(scopes: Iterable[str]) -> str:
    return " ".join(normalize_scopes(scopes))


def _hash_secret(raw: str) -> str:
    return hashlib.sha256(raw.encode()).hexdigest()


def _now() -> datetime:
    return datetime.now(timezone.utc)


def issue_access_token(user_id: str, client_id: str, scopes: Iterable[str]) -> tuple[str, datetime]:
    granted = normalize_scopes(scopes)
    expires_at = _now() + timedelta(minutes=MCP_ACCESS_TOKEN_MINUTES)
    payload = {
        "iss": MCP_OAUTH_ISSUER,
        "aud": MCP_PRIVATE_RESOURCE,
        "sub": user_id,
        "client_id": client_id,
        "scope": scope_string(granted),
        "type": "mcp_access",
        "iat": int(_now().timestamp()),
        "exp": expires_at,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO), expires_at


async def issue_refresh_token(user_id: str, client_id: str, scopes: Iterable[str]) -> str:
    raw = secrets.token_urlsafe(48)
    await db.mcp_refresh_tokens.insert_one(
        {
            "token_hash": _hash_secret(raw),
            "user_id": user_id,
            "client_id": client_id,
            "scopes": normalize_scopes(scopes),
            "created_at": utc_now_iso(),
            "expires_at": (_now() + timedelta(days=MCP_REFRESH_TOKEN_DAYS)).isoformat(),
            "revoked": False,
        }
    )
    return raw


async def rotate_refresh_token(raw: str, client_id: str) -> tuple[str, str, list[str], datetime]:
    token_hash = _hash_secret(raw)
    doc = await db.mcp_refresh_tokens.find_one({"token_hash": token_hash})
    if not doc or doc.get("revoked") or doc.get("client_id") != client_id:
        raise ValueError("invalid_grant")
    expires_at = datetime.fromisoformat(doc["expires_at"])
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at <= _now():
        raise ValueError("invalid_grant")
    await db.mcp_refresh_tokens.update_one(
        {"token_hash": token_hash}, {"$set": {"revoked": True}}
    )
    scopes = normalize_scopes(doc.get("scopes", []))
    access, access_exp = issue_access_token(doc["user_id"], client_id, scopes)
    refresh = await issue_refresh_token(doc["user_id"], client_id, scopes)
    return access, refresh, scopes, access_exp


async def revoke_refresh_token(raw: str) -> None:
    await db.mcp_refresh_tokens.update_one(
        {"token_hash": _hash_secret(raw)}, {"$set": {"revoked": True}}
    )


class AcademyMCPTokenVerifier(TokenVerifier):
    """Validate Academy-issued OAuth access tokens for the MCP SDK."""

    async def verify_token(self, token: str) -> Optional[AccessToken]:
        try:
            payload = jwt.decode(
                token,
                JWT_SECRET,
                algorithms=[JWT_ALGO],
                audience=MCP_PRIVATE_RESOURCE,
                issuer=MCP_OAUTH_ISSUER,
            )
        except jwt.PyJWTError:
            return None
        if payload.get("type") != "mcp_access":
            return None
        user_id = payload.get("sub")
        client_id = payload.get("client_id")
        if not user_id or not client_id:
            return None
        user = await db.users.find_one({"id": user_id}, {"_id": 0, "id": 1})
        if not user:
            return None
        scopes = normalize_scopes(str(payload.get("scope", "")).split())
        return AccessToken(
            token=token,
            client_id=client_id,
            scopes=scopes,
            expires_at=payload.get("exp"),
            resource=MCP_PRIVATE_RESOURCE,
            subject=user_id,
            claims={"sub": user_id},
        )
