"""CVLN Wallet integration for Academy commercial transactions.

Financial value movement stays owned by djsayd/CVLN-Wallet. Academy owns
pricing/order/entitlement state and calls the Wallet entity API only after a
server-side order has been created from Economy 3D.
"""

from __future__ import annotations

import os
from typing import Any, Dict

import httpx


class CVLNWalletNotConfigured(RuntimeError):
    pass


class CVLNWalletAmbiguousResult(RuntimeError):
    """Raised when the remote outcome cannot safely be retried automatically."""


class CVLNWalletClient:
    def __init__(self) -> None:
        self.base_url = os.environ.get("CVLN_WALLET_URL", "").rstrip("/")
        self.api_key = os.environ.get("CVLN_WALLET_API_KEY", "")
        self.timeout_seconds = float(
            os.environ.get("CVLN_WALLET_TIMEOUT_SECONDS", "10")
        )

    def is_remote_enabled(self) -> bool:
        return bool(self.base_url and self.api_key)

    def describe(self) -> Dict[str, Any]:
        return {
            "name": "CVLN Wallet",
            "configured": self.is_remote_enabled(),
            "env_vars": ["CVLN_WALLET_URL", "CVLN_WALLET_API_KEY"],
            "contract": "entity-api-v1",
        }

    def _headers(self, idempotency_key: str | None = None) -> Dict[str, str]:
        if not self.is_remote_enabled():
            raise CVLNWalletNotConfigured(
                "CVLN Wallet non configuré (CVLN_WALLET_URL / CVLN_WALLET_API_KEY)"
            )
        headers = {"X-API-Key": self.api_key}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        return headers

    async def entity_info(self) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient(
                base_url=self.base_url, timeout=self.timeout_seconds
            ) as client:
                response = await client.get(
                    "/api/v1/entity/me", headers=self._headers()
                )
                response.raise_for_status()
                return response.json()
        except (httpx.TimeoutException, httpx.NetworkError) as exc:
            raise CVLNWalletAmbiguousResult(
                "CVLN Wallet entity lookup ambiguous"
            ) from exc

    async def charge(
        self,
        frek_id: str,
        amount_cc: float,
        note: str,
        idempotency_key: str,
    ) -> Dict[str, Any]:
        """Charge a Wallet user with an Academy-owned stable attempt key.

        Academy sends `Idempotency-Key` now. Until the Wallet entity endpoint
        proves server-side support for that header, Academy still refuses to
        auto-retry after a timeout/network ambiguity and moves the order to
        REQUIRES_REVIEW.
        """
        payload = {"frek_id": frek_id, "amount": amount_cc, "note": note}
        try:
            async with httpx.AsyncClient(
                base_url=self.base_url, timeout=self.timeout_seconds
            ) as client:
                response = await client.post(
                    "/api/v1/entity/charge",
                    json=payload,
                    headers=self._headers(idempotency_key),
                )
                response.raise_for_status()
                data = response.json()
                if data.get("ok") is not True:
                    raise CVLNWalletAmbiguousResult(
                        "CVLN Wallet returned non-confirmed charge"
                    )
                return data
        except (httpx.TimeoutException, httpx.NetworkError) as exc:
            raise CVLNWalletAmbiguousResult(
                "CVLN Wallet charge outcome ambiguous"
            ) from exc


cvln_wallet = CVLNWalletClient()
