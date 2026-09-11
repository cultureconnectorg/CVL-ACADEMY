"""FREKCORE OpenID Connect client for CVLN Academy.

FREKCORE is the canonical CVLN identity provider. Academy is a relying party:
it never mints a sovereign FREK-ID in this flow and only creates/updates its
local Academy projection after FREKCORE has authenticated the identity.
"""

from __future__ import annotations

import base64
import hashlib
import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Dict
from urllib.parse import urlencode

import httpx
from fastapi import HTTPException

from db import db, utc_now_iso

FREK_CORE_ISSUER_URL = os.environ.get("FREK_CORE_ISSUER_URL", "").rstrip("/")
FREK_CORE_CLIENT_ID = os.environ.get("FREK_CORE_CLIENT_ID", "")
FREK_CORE_CLIENT_SECRET = os.environ.get("FREK_CORE_CLIENT_SECRET", "")
FREK_CORE_REDIRECT_URI = os.environ.get("FREK_CORE_REDIRECT_URI", "")
FREK_CORE_SCOPES = os.environ.get(
    "FREK_CORE_SCOPES", "openid profile email frek_identity"
)
STATE_TTL_MINUTES = 10


def _b64url(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


def _pkce_pair() -> tuple[str, str]:
    verifier = _b64url(secrets.token_bytes(48))
    challenge = _b64url(hashlib.sha256(verifier.encode()).digest())
    return verifier, challenge


class FrekOIDCClient:
    def is_configured(self) -> bool:
        return bool(
            FREK_CORE_ISSUER_URL
            and FREK_CORE_CLIENT_ID
            and FREK_CORE_REDIRECT_URI
        )

    async def discovery(self) -> Dict[str, Any]:
        if not self.is_configured():
            raise HTTPException(status_code=503, detail="FREKCORE SSO non configuré")
        url = f"{FREK_CORE_ISSUER_URL}/.well-known/openid-configuration"
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise HTTPException(status_code=503, detail="FREKCORE SSO indisponible") from exc

        required = ("authorization_endpoint", "token_endpoint", "userinfo_endpoint")
        if not all(data.get(key) for key in required):
            raise HTTPException(status_code=503, detail="Contrat OIDC FREKCORE incomplet")
        return data

    async def begin(self, return_to: str = "/") -> Dict[str, str]:
        config = await self.discovery()
        state = secrets.token_urlsafe(32)
        verifier, challenge = _pkce_pair()
        now = datetime.now(timezone.utc)
        await db.frek_sso_states.insert_one(
            {
                "state_hash": hashlib.sha256(state.encode()).hexdigest(),
                "code_verifier": verifier,
                "return_to": return_to if return_to.startswith("/") else "/",
                "created_at": utc_now_iso(),
                "expires_at": (now + timedelta(minutes=STATE_TTL_MINUTES)).isoformat(),
                "used": False,
            }
        )
        query = urlencode(
            {
                "response_type": "code",
                "client_id": FREK_CORE_CLIENT_ID,
                "redirect_uri": FREK_CORE_REDIRECT_URI,
                "scope": FREK_CORE_SCOPES,
                "state": state,
                "code_challenge": challenge,
                "code_challenge_method": "S256",
            }
        )
        return {
            "authorization_url": f"{config['authorization_endpoint']}?{query}",
            "state": state,
        }

    async def exchange(self, code: str, state: str) -> Dict[str, Any]:
        state_hash = hashlib.sha256(state.encode()).hexdigest()
        doc = await db.frek_sso_states.find_one({"state_hash": state_hash})
        if not doc or doc.get("used"):
            raise HTTPException(status_code=400, detail="État SSO FREK invalide")

        expires_at = datetime.fromisoformat(doc["expires_at"])
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if expires_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=400, detail="État SSO FREK expiré")

        claimed = await db.frek_sso_states.update_one(
            {"state_hash": state_hash, "used": False},
            {"$set": {"used": True, "used_at": utc_now_iso()}},
        )
        if claimed.modified_count != 1:
            raise HTTPException(status_code=400, detail="État SSO FREK déjà consommé")

        config = await self.discovery()
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": FREK_CORE_REDIRECT_URI,
            "client_id": FREK_CORE_CLIENT_ID,
            "code_verifier": doc["code_verifier"],
        }
        if FREK_CORE_CLIENT_SECRET:
            payload["client_secret"] = FREK_CORE_CLIENT_SECRET

        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                token_response = await client.post(config["token_endpoint"], data=payload)
                token_response.raise_for_status()
                token_data = token_response.json()
                access_token = token_data.get("access_token")
                if not access_token:
                    raise HTTPException(status_code=502, detail="Token FREKCORE absent")
                user_response = await client.get(
                    config["userinfo_endpoint"],
                    headers={"Authorization": f"Bearer {access_token}"},
                )
                user_response.raise_for_status()
                claims = user_response.json()
        except HTTPException:
            raise
        except (httpx.HTTPError, ValueError) as exc:
            raise HTTPException(status_code=503, detail="Échange SSO FREKCORE impossible") from exc

        frek_id = claims.get("frek_id") or claims.get("sub")
        if not isinstance(frek_id, str) or not frek_id.startswith("FREK-"):
            raise HTTPException(status_code=502, detail="Identité FREKCORE invalide")

        return {
            "frek_id": frek_id,
            "subject": claims.get("sub", frek_id),
            "email": claims.get("email"),
            "email_verified": bool(claims.get("email_verified")),
            "display_name": claims.get("name") or claims.get("preferred_username") or frek_id,
            "return_to": doc.get("return_to") or "/",
            "claims": claims,
        }


frek_oidc = FrekOIDCClient()
