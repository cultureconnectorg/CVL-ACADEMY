"""FrekCore integration layer.

CVLN Academy is a CLIENT of the CVLN ecosystem. This module is the sole boundary
through which the app talks to FrekCore (identity, badges, progression, proofs of skill).

For the current stage, we ship a LOCAL implementation that mimics the FrekCore contract
so the rest of the app can develop against a stable interface. When the real FrekCore
endpoints are provided, only this file changes.

Contract (public methods):
    mint_frek_id()                     -> str            (unique cultural identifier)
    emit_signal(user_id, signal, meta) -> None           (FREK-TIME, WORK, SCORE, ...)
    issue_proof(user_id, kind, meta)   -> str            (badge / cert / mission)
    resolve_stade(cc_credits)          -> str            (graine..foret)
    is_remote_enabled()                -> bool
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

import httpx

from db import db, utc_now_iso

FREK_CORE_BASE_URL = os.environ.get(
    "FREK_CORE_BASE_URL"
)  # optional; when set, remote calls are attempted
FREK_CORE_API_KEY = os.environ.get("FREK_CORE_API_KEY")

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


class FrekCoreClient:
    """Public client used everywhere. Swap remote impl by wiring FREK_CORE_BASE_URL."""

    def is_remote_enabled(self) -> bool:
        return bool(FREK_CORE_BASE_URL)

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
            async with httpx.AsyncClient(timeout=8.0) as c:
                r = await c.post(
                    f"{FREK_CORE_BASE_URL}{path}", json=payload, headers=headers
                )
                if r.status_code < 400:
                    return r.json()
        except Exception:
            pass
        return None

    async def mint_frek_id(self) -> str:
        """Reserve a stable, sequential FREK-ID like FREK-042."""
        # Try remote first
        remote = await self._remote_post("/mint", {})
        if remote and "frek_id" in remote:
            return remote["frek_id"]
        # Local fallback: counter document
        res: Optional[Dict[str, Any]] = await db.counters.find_one_and_update(
            {"_id": "frek_id"},
            {"$inc": {"seq": 1}},
            upsert=True,
            return_document=True,
        )
        # motor returns the updated doc; seq starts at 1
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
        # best-effort remote mirror
        await self._remote_post(
            "/signal", {"user_id": user_id, "signal": signal, "meta": meta or {}}
        )

    async def issue_proof(
        self, user_id: str, kind: str, meta: Optional[Dict[str, Any]] = None
    ) -> str:
        """Issue a portable proof (badge/cert). Returns a proof reference id."""
        remote = await self._remote_post(
            "/proof",
            {
                "user_id": user_id,
                "kind": kind,
                "meta": meta or {},
            },
        )
        if remote and "proof_id" in remote:
            return remote["proof_id"]
        # Local proof id
        import uuid

        return f"PROOF-{uuid.uuid4().hex[:10].upper()}"

    def resolve_stade(self, cc_credits: int) -> str:
        for name, thr in STADE_THRESHOLDS:
            if cc_credits >= thr:
                return name
        return "graine"


frek_core = FrekCoreClient()
