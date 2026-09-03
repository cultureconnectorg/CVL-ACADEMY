"""Generic ecosystem integration interface — one instance per CVLN system.

Rule 9: "prêtes mais découplées ... aucune dépendance forte ... architecture
orientée événements." Every one of these interfaces is env-var-gated, has
no compiled-in knowledge of the target system's actual API surface (that
doesn't exist publicly yet), and never silently no-ops as if it succeeded
— calling `.request()` on an unconfigured integration raises
IntegrationNotConfigured, which callers are expected to catch (typically
to just skip that side-effect, the same way frek_core/agent_factory fall
back locally when *their* remote isn't configured).
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, Optional

import httpx

logger = logging.getLogger("cvln.integrations")


class IntegrationNotConfigured(RuntimeError):
    def __init__(self, name: str, env_prefix: str) -> None:
        super().__init__(
            f"{name} non configuré (définir {env_prefix}_URL / {env_prefix}_API_KEY)"
        )
        self.name = name
        self.env_prefix = env_prefix


class EcosystemIntegration:
    """A named, env-gated HTTP client for one external CVLN system.

    `env_prefix` picks up `{PREFIX}_URL` and `{PREFIX}_API_KEY` — e.g.
    env_prefix="CVLN_BRAIN" reads CVLN_BRAIN_URL / CVLN_BRAIN_API_KEY.
    """

    def __init__(self, name: str, env_prefix: str) -> None:
        self.name = name
        self.env_prefix = env_prefix
        self.base_url = os.environ.get(f"{env_prefix}_URL")
        self.api_key = os.environ.get(f"{env_prefix}_API_KEY")

    def is_remote_enabled(self) -> bool:
        return bool(self.base_url)

    def describe(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "configured": self.is_remote_enabled(),
            "env_vars": [f"{self.env_prefix}_URL", f"{self.env_prefix}_API_KEY"],
        }

    async def request(
        self, path: str, payload: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """POST `payload` to `{base_url}{path}`. Raises IntegrationNotConfigured
        if this integration has no base URL set — callers decide whether
        that's fatal or just a skipped side-effect."""
        if not self.base_url:
            raise IntegrationNotConfigured(self.name, self.env_prefix)
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        async with httpx.AsyncClient(base_url=self.base_url, timeout=10.0) as client:
            try:
                response = await client.post(path, json=payload or {}, headers=headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                logger.error("%s request to %s failed: %s", self.name, path, e)
                raise
