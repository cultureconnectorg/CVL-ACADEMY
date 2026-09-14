"""CVLN Wallet group-level financial integration.

CVLN Academy never talks directly to a PSP. It delegates group money movement,
wallet balances and entity charges to CVLN Wallet, whose Financial Core remains
the accounting authority. Commercial payment attempts use the same client with
an Academy-owned idempotency key; ambiguous network outcomes are never retried
automatically by Academy.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

import httpx

from .base import IntegrationNotConfigured


class CVLNWalletNotConfigured(RuntimeError):
    pass


class CVLNWalletAmbiguousResult(RuntimeError):
    """Remote outcome cannot safely be retried automatically."""


class CVLNWalletIntegration:
    # RECONCILE-2 Groupe 5: "(djsayd, external)" disambiguates this from
    # `wallet/` — Academy's own internal CC/JCC ledger — the same
    # distinction r35l31's parallel `EcosystemIntegration("CVLN Wallet
    # (djsayd, external)", ...)` drew (see registry.py's module
    # docstring); docs/INTEGRATIONS_REPORT.md's own row already uses
    # this exact name.
    name = "CVLN Wallet (djsayd, external)"
    env_prefix = "CVLN_WALLET"

    def __init__(self) -> None:
        self.base_url = os.environ.get("CVLN_WALLET_URL")
        self.api_key = os.environ.get("CVLN_WALLET_API_KEY")
        self.timeout_seconds = float(
            os.environ.get("CVLN_WALLET_TIMEOUT_SECONDS", "10")
        )

    def is_remote_enabled(self) -> bool:
        return bool(self.base_url and self.api_key)

    def describe(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "configured": self.is_remote_enabled(),
            "env_vars": ["CVLN_WALLET_URL", "CVLN_WALLET_API_KEY"],
            "role": "group_financial_core",
            "contract": "entity-api-v1",
        }

    def _headers(self, idempotency_key: Optional[str] = None) -> Dict[str, str]:
        api_key = self.api_key
        if not self.base_url or not api_key:
            raise CVLNWalletNotConfigured(
                "CVLN Wallet non configuré (CVLN_WALLET_URL / CVLN_WALLET_API_KEY)"
            )
        headers = {"X-API-Key": api_key}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        return headers

    async def _request(
        self,
        method: str,
        path: str,
        payload: Optional[Dict[str, Any]] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        base_url = self.base_url
        if not base_url:
            raise CVLNWalletNotConfigured("CVLN Wallet non configuré")

        try:
            async with httpx.AsyncClient(
                base_url=base_url,
                timeout=self.timeout_seconds,
                headers=self._headers(idempotency_key),
            ) as client:
                response = await client.request(method, path, json=payload)
                response.raise_for_status()
                data = response.json()
        except (httpx.TimeoutException, httpx.NetworkError) as exc:
            raise CVLNWalletAmbiguousResult(
                f"CVLN Wallet {method} {path} outcome ambiguous"
            ) from exc

        if not isinstance(data, dict):
            raise CVLNWalletAmbiguousResult("Réponse CVLN Wallet invalide")
        return data

    async def entity(self) -> Dict[str, Any]:
        return await self._request("GET", "/api/v1/entity/me")

    async def entity_info(self) -> Dict[str, Any]:
        """Compatibility name used by Academy commercial order creation."""
        return await self.entity()

    async def balance(self) -> Dict[str, Any]:
        return await self._request("GET", "/api/v1/entity/balance")

    async def transactions(self) -> Dict[str, Any]:
        return await self._request("GET", "/api/v1/entity/transactions")

    async def charge(
        self,
        frek_id: str,
        amount_cc: float,
        note: str = "",
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        data = await self._request(
            "POST",
            "/api/v1/entity/charge",
            {"frek_id": frek_id, "amount": amount_cc, "note": note},
            idempotency_key=idempotency_key,
        )
        if idempotency_key and data.get("ok") is not True:
            raise CVLNWalletAmbiguousResult("CVLN Wallet returned non-confirmed charge")
        return data

    async def transfer(
        self,
        to: str,
        amount_cc: float,
        note: str = "",
    ) -> Dict[str, Any]:
        return await self._request(
            "POST",
            "/api/v1/entity/transfer",
            {"to": to, "amount": amount_cc, "note": note},
        )

    async def request(
        self, path: str, payload: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """RECONCILE-2 Groupe 5: generic-integration compatibility shim.

        `services/integrations/subscribers.py` (r35l31, ACA-0029) treats
        every ecosystem handoff uniformly through
        `EcosystemIntegration.request(path, payload)`, catching the shared
        `IntegrationNotConfigured` to skip the side-effect when unset. This
        client predates that pattern and exposes typed methods instead
        (`charge`/`transfer`/`balance`/...); this shim makes it satisfy the
        same generic contract for that one caller, without touching any of
        the typed methods real commerce/billing code already depends on.
        Raises the shared `IntegrationNotConfigured` (not
        `CVLNWalletNotConfigured`) so the generic caller's except clause
        matches.
        """
        if not self.is_remote_enabled():
            raise IntegrationNotConfigured(self.name, self.env_prefix)
        return await self._request("POST", path, payload or {})


cvln_wallet = CVLNWalletIntegration()
