"""Wires ecosystem integrations to domain events — call register() once at
startup. This is the concrete example the event-driven pattern (rule 9)
follows: a handler best-effort-forwards to whichever integrations are
configured, and silently skips the ones that aren't (IntegrationNotConfigured
is expected, not an error) — Academy's own logic never blocks on it.

ACA-0029 — real handoffs, not just the one certification-passed handler
this module started with. `academy_first_value_reached` and
`academy_activation_completed` were already real, already-published
events (`services/activation.py`, `api/onboarding.py`) with ZERO
subscribers — published into the void. `academy_badge_awarded` is a new
real emission point (`badges_engine.py`) added alongside this pass. All
three are wired below, same best-effort, never-blocking pattern as the
original certification handler.
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from services.events import events

from .base import IntegrationNotConfigured
from .registry import brain, command_center, wallet

logger = logging.getLogger("cvln.integrations")


async def _forward(path: str, payload: Dict[str, Any], *integrations) -> None:
    for integration in integrations:
        try:
            await integration.request(path, payload)
        except IntegrationNotConfigured:
            continue  # expected until the real system is wired — not an error
        except Exception:  # noqa: BLE001
            logger.exception("%s failed to receive %s event", integration.name, path)


async def _on_certification_passed(payload: Dict[str, Any]) -> None:
    await _forward("/academy/certification-passed", payload, brain, command_center)


async def _on_activation_completed(payload: Dict[str, Any]) -> None:
    # Real funnel/activation milestone — Command Center's own KPI
    # surface is the natural real recipient (rule 9's own description
    # of that system); Brain is not, so it's deliberately not included
    # here, unlike the certification handler above.
    await _forward("/academy/activation-completed", payload, command_center)


async def _on_first_value_reached(payload: Dict[str, Any]) -> None:
    await _forward("/academy/first-value-reached", payload, command_center)


async def _on_badge_awarded(payload: Dict[str, Any]) -> None:
    # The one real handoff to the external Wallet app: a badge earning
    # JCC that Academy's own internal wallet ledger already,
    # separately, really credited (badges_engine.py) is exactly the
    # kind of fact the external CVLN Wallet system would want
    # reflected — Command Center too, for the same KPI reason as the
    # other funnel milestones above.
    await _forward("/academy/badge-awarded", payload, wallet, command_center)


def register() -> None:
    events.subscribe("academy.certification.passed", _on_certification_passed)
    events.subscribe("academy_activation_completed", _on_activation_completed)
    events.subscribe("academy_first_value_reached", _on_first_value_reached)
    events.subscribe("academy_badge_awarded", _on_badge_awarded)
