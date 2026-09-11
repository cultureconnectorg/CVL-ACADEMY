"""FrekCore integration boundary for CVLN Academy.

Identity doctrine
-----------------
A FREK-ID is a sovereign ecosystem identity. Academy is a client of that
identity; pedagogical roles, organisation memberships and permissions remain
Academy-local projections around the same FREK-ID.

Two authority modes are intentionally explicit:

* ``local_dev``: development/test only. Academy may mint a local sequential
  FREK-ID so the application can run without the ecosystem service.
* ``frekcore``: sovereign mode. FREKCORE is the only authority allowed to mint
  a FREK-ID. If FREKCORE is unavailable, identity creation fails closed instead
  of silently creating a potentially conflicting local identity.

Set ``FREK_CORE_IDENTITY_AUTHORITY=frekcore`` together with
``FREK_CORE_BASE_URL`` (and normally ``FREK_CORE_API_KEY``) for an integrated
deployment.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

import httpx

from db import db, utc_now_iso

FREK_CORE_BASE_URL = os.environ.get("FREK_CORE_BASE_URL", "").rstrip("/")
FREK_CORE_API_KEY = os.environ.get("FREK_CORE_API_KEY")
FREK_CORE_IDENTITY_AUTHORITY = os.environ.get(
    "FREK_CORE_IDENTITY_AUTHORITY", "local_dev"
).strip().lower()

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
    """Raised when FREKCORE is the authority but cannot fulfil identity work."""


class FrekCoreConfigurationError(RuntimeError):
    """Raised when the configured identity authority is invalid or incomplete."""


class FrekCoreClient:
    """Single Academy boundary to the ecosystem identity service."""

    def identity_authority(self) -> str:
        if FREK_CORE_IDENTITY_AUTHORITY not in VALID_IDENTITY_AUTHORITIES:
            raise FrekCoreConfigurationError(
                "FREK_CORE_IDENTITY_AUTHORITY must be 'local_dev' or 'frekcore'"
            )
        return FREK_CORE_IDENTITY_AUTHORITY

    def is_remote_enabled(self) -> bool:
        return bool(FREK_CORE_BASE_URL)

    def is_sovereign_identity_enabled(self) -> bool:
        """True only when Academy is configured to delegate identity to FREKCORE."""
        return self.identity_authority() == "frekcore" and self.is_remote_enabled()

    async def _remote_post(
        self, path: str, payload: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
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

    async def mint_frek_id(self) -> str:
        """Mint a FREK-ID according to the configured identity authority.

        In ``frekcore`` mode, no local fallback is permitted. This prevents
        Academy from independently minting an identifier that could conflict
        with another CVLN platform.
        """
        authority = self.identity_authority()

        if authority == "frekcore":
            if not self.is_remote_enabled():
                raise FrekCoreConfigurationError(
                    "FREKCORE is the identity authority but FREK_CORE_BASE_URL is unset"
                )
            remote = await self._remote_post("/mint", {})
            frek_id = (remote or {}).get("frek_id")
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
        # Signals are mirrored best-effort. Identity minting itself is fail-closed
        # in sovereign mode; telemetry must not make Academy unusable.
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

        # Proof fallback remains local for now. This is deliberately distinct
        # from sovereign identity minting and can be tightened when the FREKCORE
        # proof contract is made mandatory.
        import uuid

        return f"PROOF-{uuid.uuid4().hex[:10].upper()}"

    def resolve_stade(self, cc_credits: int) -> str:
        for name, threshold in STADE_THRESHOLDS:
            if cc_credits >= threshold:
                return name
        return "graine"


frek_core = FrekCoreClient()
