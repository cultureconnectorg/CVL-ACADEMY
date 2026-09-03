"""Wires ecosystem integrations to domain events — call register() once at
startup. This is the concrete example the event-driven pattern (rule 9)
follows: a handler best-effort-forwards to whichever integrations are
configured, and silently skips the ones that aren't (IntegrationNotConfigured
is expected, not an error) — Academy's own logic never blocks on it.
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from services.events import events

from .base import IntegrationNotConfigured
from .registry import brain, command_center

logger = logging.getLogger("cvln.integrations")


async def _on_certification_passed(payload: Dict[str, Any]) -> None:
    for integration in (brain, command_center):
        try:
            await integration.request("/academy/certification-passed", payload)
        except IntegrationNotConfigured:
            continue  # expected until the real system is wired — not an error
        except Exception:  # noqa: BLE001
            logger.exception(
                "%s failed to receive certification-passed event", integration.name
            )


def register() -> None:
    events.subscribe("academy.certification.passed", _on_certification_passed)
