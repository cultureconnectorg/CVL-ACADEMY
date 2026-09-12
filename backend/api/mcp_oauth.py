"""OAuth 2.1 authorization server for CVLN Academy MCP clients.

This is intentionally isolated from the existing Academy login JWTs.  MCP
clients receive audience-bound, scoped access tokens. Authorization Code +
PKCE (S256) is the only interactive grant; public clients have no client
secret. Dynamic registration is opt-in through an environment flag.
"""

from __future__ import annotations

import base64
import hashlib
import html
import json
import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any
from urllib.parse import urlencode, urlparse, urlunparse, parse_qsl

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from pydantic import BaseModel, Field

from auth import verify_password
from db import db, utc_now_iso
from mcp_auth import (
    DEFAULT_SCOPES,
    MCP_ACCESS_TOKEN_MINUTES,
    MCP_OAUTH_ISSUER,
    MCP_PRIVATE_RESOURCE,
    SCOPES,
    issue_access_token,
    issue_refresh_token,
    normalize_scopes,
    revoke_refresh_token,
    rotate_refresh_token,
)

router = APIRouter(tags=["mcp-oauth"])

AUTH_CODE_TTL_MINUTES = 10
ALLOW_DYNAMIC_REGISTRATION = os.environ.get(
    "MCP_OAUTH_ALLOW_DYNAMIC_REGISTRATION", "false"
).lower() in {"1", "true", "yes"}


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _hash(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def _b64url_sha256(value: str) -> str:
    digest = hashlib.sha256(value.encode()).digest()
    return base64.urlsafe_b64encode(digest).decode().rstrip("=")


def _redirect_with(uri: str, **params: str) -> str:
    parsed = urlparse(uri)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query.update({k: v for k, v in params.items() if v is not None})
    return urlunparse(parsed._replace(query=urlencode(query)))


def _safe_redirect_uri(uri: str) -> bool:
    parsed = urlparse(uri)
    if parsed.scheme == "https" and parsed.netloc:
        return True
    if parsed.scheme == "http" and parsed.hostname in {"127.0.0.1", "localhost"}:
        return True
    return False


def _static_clients() -> dict[str, dict[str, Any]]:
    raw = os.environ.get("MCP_OAUTH_CLIENTS_JSON", "").strip()
    if not raw:
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


async def _client(client_id: str) -> dict[str, Any] | None:
    static = _static_clients().get(client_id)
    if static:
        return {"client_id": client_id, **static}
    return await db.mcp_oauth_clients.find_one({"client_id": client_id}, {"_id": 0})


async def _validate_client_redirect(client_id: str, redirect_uri: str) -> dict[str, Any]:
    client = await _client(client_id)
    if not client or redirect_uri not in client.get("redirect_uris", []):
        raise HTTPException(status_code=400, detail="invalid_client_or_redirect_uri")
    return client


class RegistrationInput(BaseModel):
    client_name: str = Field(default="MCP client", min_length=1, max_length=120)
    redirect_uris: list[str]
    token_endpoint_auth_method: str = "none"
    grant_types: list[str] = Field(default_factory=lambda: ["authorization_code", "refresh_token"])
    response_types: list[str] = Field(default_factory=lambda: ["code"])


@router.get("/.well-known/oauth-authorization-server")
async def oauth_metadata():
    return {
        "issuer": MCP_OAUTH_ISSUER,
        "authorization_endpoint": f"{MCP_OAUTH_ISSUER}/oauth/authorize",
        "token_endpoint": f"{MCP_OAUTH_ISSUER}/oauth/token",
        "registration_endpoint": f"{MCP_OAUTH_ISSUER}/oauth/register",
        "revocation_endpoint": f"{MCP_OAUTH_ISSUER}/oauth/revoke",
        "response_types_supported": ["code"],
        "grant_types_supported": ["authorization_code", "refresh_token"],
        "code_challenge_methods_supported": ["S256"],
        "token_endpoint_auth_methods_supported": ["none"],
        "scopes_supported": list(SCOPES),
    }


@router.get("/.well-known/oauth-protected-resource/mcp/private")
async def protected_resource_metadata():
    return {
        "resource": MCP_PRIVATE_RESOURCE,
        "authorization_servers": [MCP_OAUTH_ISSUER],
        "scopes_supported": list(SCOPES),
        "bearer_methods_supported": ["header"],
    }


@router.post("/oauth/register")
async def register_client(inp: RegistrationInput):
    if not ALLOW_DYNAMIC_REGISTRATION:
        raise HTTPException(status_code=403, detail="dynamic_registration_disabled")
    if inp.token_endpoint_auth_method != "none":
        raise HTTPException(status_code=400, detail="public_clients_only")
    if not inp.redirect_uris or not all(_safe_redirect_uri(uri) for uri in inp.redirect_uris):
        raise HTTPException(status_code=400, detail="invalid_redirect_uri")
    client_id = f"mcp_{secrets.token_urlsafe(24)}"
    doc = {
        "client_id": client_id,
        "client_name": inp.client_name,
        "redirect_uris": inp.redirect_uris,
        "token_endpoint_auth_method": "none",
        "grant_types": ["authorization_code", "refresh_token"],
        "response_types": ["code"],
        "created_at": utc_now_iso(),
    }
    await db.mcp_oauth_clients.insert_one(doc)
    return {k: v for k, v in doc.items() if k != "created_at"}


@router.get("/oauth/authorize", response_class=HTMLResponse)
async def authorize_page(
    client_id: str,
    redirect_uri: str,
    response_type: str,
    code_challenge: str,
    code_challenge_method: str,
    scope: str = "academy:profile.read",
    state: str = "",
    resource: str = MCP_PRIVATE_RESOURCE,
):
    await _validate_client_redirect(client_id, redirect_uri)
    if response_type != "code" or code_challenge_method != "S256" or not code_challenge:
        raise HTTPException(status_code=400, detail="PKCE S256 authorization_code required")
    if resource.rstrip("/") != MCP_PRIVATE_RESOURCE:
        raise HTTPException(status_code=400, detail="invalid_resource")
    requested = scope.split() or list(DEFAULT_SCOPES)
    if any(item not in SCOPES for item in requested):
        raise HTTPException(status_code=400, detail="invalid_scope")
    scopes_html = "".join(f"<li>{html.escape(SCOPES[item])}</li>" for item in requested)
    hidden = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "code_challenge": code_challenge,
        "scope": " ".join(requested),
        "state": state,
        "resource": resource,
    }
    hidden_html = "".join(
        f'<input type="hidden" name="{html.escape(k)}" value="{html.escape(v, quote=True)}">'
        for k, v in hidden.items()
    )
    return HTMLResponse(
        "<!doctype html><html><head><meta charset='utf-8'><title>CVLN Academy — Connect</title>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'></head>"
        "<body><main><h1>Connecter CVLN Academy</h1>"
        "<p>Connecte-toi sur CVLN Academy pour autoriser cet assistant.</p>"
        f"<ul>{scopes_html}</ul><form method='post' action='/oauth/authorize'>"
        f"{hidden_html}<label>Email <input type='email' name='email' required></label><br>"
        "<label>Mot de passe <input type='password' name='password' required></label><br>"
        "<button type='submit'>Autoriser</button></form></main></body></html>"
    )


@router.post("/oauth/authorize")
async def authorize_submit(
    client_id: str = Form(...),
    redirect_uri: str = Form(...),
    code_challenge: str = Form(...),
    scope: str = Form(...),
    state: str = Form(""),
    resource: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):
    await _validate_client_redirect(client_id, redirect_uri)
    if resource.rstrip("/") != MCP_PRIVATE_RESOURCE:
        raise HTTPException(status_code=400, detail="invalid_resource")
    requested = normalize_scopes(scope.split())
    if not requested or len(requested) != len(scope.split()):
        return RedirectResponse(_redirect_with(redirect_uri, error="invalid_scope", state=state), status_code=302)
    user = await db.users.find_one({"email": email.lower()}, {"_id": 0})
    if not user or not verify_password(password, user.get("password_hash", "")):
        return RedirectResponse(_redirect_with(redirect_uri, error="access_denied", state=state), status_code=302)
    raw_code = secrets.token_urlsafe(48)
    await db.mcp_auth_codes.insert_one(
        {
            "code_hash": _hash(raw_code),
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "code_challenge": code_challenge,
            "user_id": user["id"],
            "scopes": requested,
            "resource": MCP_PRIVATE_RESOURCE,
            "expires_at": (_now() + timedelta(minutes=AUTH_CODE_TTL_MINUTES)).isoformat(),
            "used": False,
            "created_at": utc_now_iso(),
        }
    )
    return RedirectResponse(_redirect_with(redirect_uri, code=raw_code, state=state), status_code=302)


@router.post("/oauth/token")
async def token(
    request: Request,
    grant_type: str = Form(...),
    client_id: str = Form(...),
    code: str | None = Form(None),
    redirect_uri: str | None = Form(None),
    code_verifier: str | None = Form(None),
    refresh_token: str | None = Form(None),
    resource: str | None = Form(None),
):
    del request
    if grant_type == "authorization_code":
        if not code or not redirect_uri or not code_verifier:
            return JSONResponse({"error": "invalid_request"}, status_code=400)
        await _validate_client_redirect(client_id, redirect_uri)
        doc = await db.mcp_auth_codes.find_one({"code_hash": _hash(code)})
        if not doc or doc.get("used") or doc.get("client_id") != client_id or doc.get("redirect_uri") != redirect_uri:
            return JSONResponse({"error": "invalid_grant"}, status_code=400)
        expires = datetime.fromisoformat(doc["expires_at"])
        if expires.tzinfo is None:
            expires = expires.replace(tzinfo=timezone.utc)
        if expires <= _now() or _b64url_sha256(code_verifier) != doc.get("code_challenge"):
            return JSONResponse({"error": "invalid_grant"}, status_code=400)
        if resource and resource.rstrip("/") != MCP_PRIVATE_RESOURCE:
            return JSONResponse({"error": "invalid_target"}, status_code=400)
        await db.mcp_auth_codes.update_one({"code_hash": _hash(code)}, {"$set": {"used": True}})
        access, access_exp = issue_access_token(doc["user_id"], client_id, doc["scopes"])
        refresh = await issue_refresh_token(doc["user_id"], client_id, doc["scopes"])
        return {
            "access_token": access,
            "token_type": "Bearer",
            "expires_in": max(1, int((access_exp - _now()).total_seconds())),
            "refresh_token": refresh,
            "scope": " ".join(doc["scopes"]),
        }

    if grant_type == "refresh_token":
        if not refresh_token:
            return JSONResponse({"error": "invalid_request"}, status_code=400)
        try:
            access, new_refresh, scopes, access_exp = await rotate_refresh_token(refresh_token, client_id)
        except ValueError:
            return JSONResponse({"error": "invalid_grant"}, status_code=400)
        return {
            "access_token": access,
            "token_type": "Bearer",
            "expires_in": max(1, int((access_exp - _now()).total_seconds())),
            "refresh_token": new_refresh,
            "scope": " ".join(scopes),
        }

    return JSONResponse({"error": "unsupported_grant_type"}, status_code=400)


@router.post("/oauth/revoke")
async def revoke(token: str = Form(...), token_type_hint: str | None = Form(None)):
    del token_type_hint
    await revoke_refresh_token(token)
    return JSONResponse({}, status_code=200)
