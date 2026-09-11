"""CVLN Wallet group-level financial integration.

CVLN Academy never talks directly to a PSP. It delegates group money movement,
wallet balances and entity charges to CVLN Wallet, whose Financial Core remains
the accounting authority.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

import httpx


class CVLNWalletIntegration:
    name = "CVLN Wallet"
    env_prefix = "CVLN_WALLET"

    def __init__(self) -> None:
        self.base_url = os.environ.get("CVLN_WALLET_URL")
        self.api_key = os.environ.get("CVLN_WALLET_API_KEY")

    def is_remote_enabled(self) -> bool:
        return bool(self.base_url and self.api_key)

    def describe(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "configured": self.is_remote_enabled(),
            "env_vars": ["CVLN_WALLET_URL", "CVLN_WALLET_API_KEY"],
            "role": "group_financial_core",
        }

    async def _request(self, method: str, path: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if not self.is_remote_enabled():
            raise RuntimeError("CVLN Wallet non configuré")
        headers = {"X-API-Key": self.api_key}
        async with httpx.AsyncClient(base_url=self.base_url, timeout=10.0, headers=headers) as client:
            response = await client.request(method, path, json=payload)
            response.raise_for_status()
            return response.json()

    async def entity(self) -> Dict[str, Any]:
        return await self._request("GET", "/api/v1/entity/me")

    async def balance(self) -> Dict[str, Any]:
        return await self._request("GET", "/api/v1/entity/balance")

    async def transactions(self) -> Dict[str, Any]:
        return await self._request("GET", "/api/v1/entity/transactions")

    async def charge(self, frek_id: str, amount_cc: float, note: str = "") -> Dict[str, Any]:
        return await self._request(
            "POST",
            "/api/v1/entity/charge",
            {"frek_id": frek_id, "amount": amount_cc, "note": note},
        )

    async def transfer(self, to: str, amount_cc: float, note: str = "") -> Dict[str, Any]:
        return await self._request(
            "POST",
            "/api/v1/entity/transfer",
            {"to": to, "amount": amount_cc, "note": note},
        )


cvln_wallet = CVLNWalletIntegration()
