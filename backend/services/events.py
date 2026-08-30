"""In-process event bus — the "architecture orientée événements" rule 9
asks for. Academy publishes domain events (a certification passed, a
badge earned, ...); any number of handlers subscribe without the
publisher knowing or caring who's listening. This keeps ecosystem
integrations decoupled at the *call site* too — a route handler emits
`academy.certification.passed`, it never calls CVLN Brain directly.

In-process only (no external broker) — swapping the internals for a real
queue (SQS, Redis Streams, ...) later doesn't change `publish()`'s
signature, so no caller needs to change.
"""

from __future__ import annotations

import logging
from collections import defaultdict
from typing import Any, Awaitable, Callable, DefaultDict, Dict, List

from db import db, utc_now_iso

logger = logging.getLogger("cvln.events")

EventHandler = Callable[[Dict[str, Any]], Awaitable[None]]


class EventBus:
    def __init__(self) -> None:
        self._subscribers: DefaultDict[str, List[EventHandler]] = defaultdict(list)

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        self._subscribers[event_type].append(handler)

    async def publish(self, event_type: str, payload: Dict[str, Any]) -> None:
        await db.event_log.insert_one(
            {
                "event_type": event_type,
                "payload": payload,
                "published_at": utc_now_iso(),
            }
        )
        for handler in self._subscribers.get(event_type, []):
            try:
                await handler(payload)
            except (
                Exception
            ):  # noqa: BLE001 — one bad handler must not break the others
                logger.exception("Event handler failed for %s", event_type)


events = EventBus()
