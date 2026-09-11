"""FREKCORE integration boundary for CVLN Academy.

Academy does not own the ecosystem identity. In integrated deployments it asks
FREKCORE for the canonical FREK-ID and stores that identifier as a foreign,
stable identity key. Academy-local roles, organisations, cohorts, progression
and permissions stay in Academy.

Identity authority modes:
- ``local_dev``: development/test only; local sequential FREK-ID allowed.
- ``frekcore``: FREKCORE v1 identity API is authoritative; no local fallback.

The remote contract below matches the existing FREKCORE August 2026 API:
1. POST /api/v1/auth/token (client_credentials)
2. POST /api/v1/identity/emit (Bearer client token)
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

import httpx

from db import db, utc_now_iso

FREK_CORE_BASE_URL = os.environ.get("FREK_CORE_BASE_URL", "").rstrip("/")
FREK_CORE_CLIENT_ID = os.environ.get("FREK_CORE_CLIENT_ID", "").strip()
FREK_CORE_CLIENT_SECRET = os.environ.get("FREK_CORE_CLIENT_SECRET", "").strip()
# Retained for existing best-effort signal/proof mirrors until those contracts
# are reconciled separately. It is NOT used for FREK-ID issuance.
FREK_CORE_API_KEY = os.environ.get("FREK_CORE_API_KEY")
FREK_CORE_IDENTITY_AUTHORITY = (
    os.environ.get("FREK_CORE_IDENTITY_AUTHORITY", "local_dev").strip().lower()
)

VALID_IDENTITY_AUTHORITIES = {"local_dev", "frekcore"}

STADE_THRESHOLDS = [
    ("foret", 300),
    ("arbre", 150),
    ("branches", 100),
    ("racine", 50),
    ("pousse", 10),
    ("graine", 0),
]

VALID_SIGNALS = {
    "FREK-TIME",
    "FREK-WORK",
    "FREK-SCORE",
    "FREK-LINK",
    "FREK-CERT",
    "FREK-CONTRIB",
    "FREK-SHARE",
    "FREK-MISSION",
}


class FrekCoreUnavailableError(RuntimeError):
    """Raised when FREKCORE is authoritative but cannot fulfil identity work."""


class FrekCoreConfigurationError(RuntimeError):
    """Raised when FREKCORE identity configuration is invalid or incomplete."""


class FrekCoreClient:
    """Single Academy boundary to FREKCORE."""

    def identity_authority(self) -> str:
        if FREK_CORE_IDENTITY_AUTHORITY not in VALID_IDENTITY_AUTHORITIES:
            raise FrekCoreConfigurationError(
                "FREK_CORE_IDENTITY_AUTHORITY must be 'local_dev' or 'frekcore'"
            )
        return FREK_CORE_IDENTITY_AUTHORITY

    def is_remote_enabled(self) -> bool:
        return bool(FREK_CORE_BASE_URL)

    def is_sovereign_identity_enabled(self) -> bool:
        return self.identity_authority() == "frekcore" and bool(
            FREK_CORE_BASE_URL and FREK_CORE_CLIENT_ID and FREK_CORE_CLIENT_SECRET
        )

    def _require_identity_client_config(self) -> None:
        missing = []
        if not FREK_CORE_BASE_URL:
            missing.append("FREK_CORE_BASE_URL")
        if not FREK_CORE_CLIENT_ID:
            missing.append("FREK_CORE_CLIENT_ID")
        if not FREK_CORE_CLIENT_SECRET:
            missing.append("FREK_CORE_CLIENT_SECRET")
        if missing:
            raise FrekCoreConfigurationError(
                "Missing FREKCORE identity configuration: " + ", ".join(missing)
            )

    async def _identity_client_token(self) -> str:
        self._require_identity_client_config()
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                response = await client.post(
                    f"{FREK_CORE_BASE_URL}/api/v1/auth/token",
                    json={
                        "client_id": FREK_CORE_CLIENT_ID,
                        "client_secret": FREK_CORE_CLIENT_SECRET,
                        "grant_type": "client_credentials",
                    },
                )
                response.raise_for_status()
                body = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise FrekCoreUnavailableError(
                "FREKCORE client authentication failed"
            ) from exc

        token = body.get("access_token") if isinstance(body, dict) else None
        if not isinstance(token, str) or not token.strip():
            raise FrekCoreUnavailableError(
                "FREKCORE did not return a client access_token"
            )
        return token.strip()

    async def mint_frek_id(
        self,
        email: Optional[str] = None,
        *,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Return the FREK-ID for an Academy registration.

        In ``frekcore`` mode this calls FREKCORE's existing idempotent identity
        emission endpoint. The email is sent only to FREKCORE over the server-to-
        server channel; FREKCORE hashes it before identity persistence.
        """
        authority = self.identity_authority()

        if authority == "frekcore":
            if not email:
                raise FrekCoreConfigurationError(
                    "An email is required to emit a FREK-ID through FREKCORE v1"
                )
            token = await self._identity_client_token()
            payload: Dict[str, Any] = {
                "email": email.lower().strip(),
                "source": "cvln_academy",
                "metadata": metadata or {},
            }
            try:
                async with httpx.AsyncClient(timeout=8.0) as client:
                    response = await client.post(
                        f"{FREK_CORE_BASE_URL}/api/v1/identity/emit",
                        json=payload,
                        headers={"Authorization": f"Bearer {token}"},
                    )
                    response.raise_for_status()
                    body = response.json()
            except (httpx.HTTPError, ValueError) as exc:
                raise FrekCoreUnavailableError(
                    "FREKCORE identity emission failed; local minting is forbidden"
                ) from exc

            frek_id = body.get("frek_id") if isinstance(body, dict) else None
            if not isinstance(frek_id, str) or not frek_id.strip():
                raise FrekCoreUnavailableError(
                    "FREKCORE did not return a valid frek_id; local minting is forbidden"
                )
            return frek_id.strip()

        # Explicit local development/test authority only.
        res: Optional[Dict[str, Any]] = await db.counters.find_one_and_update(
            {"_id": "frek_id"},
            {"$inc": {"seq": 1}},
            upsert=True,
            return_document=True,
        )
        seq = (res or {}).get("seq") or 1
        return f"FREK-{seq:03d}"

    async def _remote_post(
        self, path: str, payload: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Legacy best-effort mirror used by non-identity integrations only."""
        if not self.is_remote_enabled():
            return None
        try:
            headers = (
                {"Authorization": f"Bearer {FREK_CORE_API_KEY}"}
                if FREK_CORE_API_KEY
                else {}
            )
            async with httpx.AsyncClient(timeout=8.0) as client:
                response = await client.post(
                    f"{FREK_CORE_BASE_URL}{path}", json=payload, headers=headers
                )
                if response.status_code < 400:
                    body = response.json()
                    return body if isinstance(body, dict) else None
        except (httpx.HTTPError, ValueError):
            return None
        return None

    async def emit_signal(
        self, user_id: str, signal: str, meta: Optional[Dict[str, Any]] = None
    ) -> None:
        if signal not in VALID_SIGNALS:
            return
        await db.frek_signals.insert_one(
            {
                "user_id": user_id,
                "signal": signal,
                "meta": meta or {},
                "ts": utc_now_iso(),
            }
        )
        await db.users.update_one({"id": user_id}, {"$inc": {f"signals.{signal}": 1}})
        await self._remote_post(
            "/signal", {"user_id": user_id, "signal": signal, "meta": meta or {}}
        )

    async def issue_proof(
        self, user_id: str, kind: str, meta: Optional[Dict[str, Any]] = None
    ) -> str:
        remote = await self._remote_post(
            "/proof",
            {"user_id": user_id, "kind": kind, "meta": meta or {}},
        )
        if remote and "proof_id" in remote:
            return str(remote["proof_id"])

        import uuid

        return f"PROOF-{uuid.uuid4().hex[:10].upper()}"

    def resolve_stade(self, cc_credits: int) -> str:
        for name, threshold in STADE_THRESHOLDS:
            if cc_credits >= threshold:
                return name
        return "graine"


frek_core = FrekCoreClient()
