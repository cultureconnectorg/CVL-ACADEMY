"""ACA-0013 — Activation / first-value event emission.

Per `docs/ACADEMY_FUNNEL_EVENT_TAXONOMY.md`'s own classification (both
rows marked `READY_TO_EMIT`, underscore naming convention recommended
there for W-FUNNEL-1 onward — see that doc's "Naming reconciliation"
section):

- `academy_activation_completed` — fired once, at the end of
  `POST /onboarding/complete`, from the same real convergence payload
  (`recommended_formation`/`recommended_mission`/`badge_earned`/
  `signals_emitted`) that response already builds. Not a new
  computation — an emission of data that already exists.
- `academy_first_value_reached` — fired the first time a
  `db.progress` (legacy `ModuleProgress`) document is ever created for
  a user, i.e. the first real touch of learning content. Wired at
  `POST /modules/{fc}/{mc}/phase`'s `hook` tick — in the real learner
  flow (`ModuleJourney.js`) this is the earliest write that can create
  that document: it fires on mount/first-phase-expand, before the
  quiz, deliverable, or mini-mission routes are ever reachable for that
  module. Other `db.progress`-writing routes
  (`/deliverable`, `/mini-mission/commit`, quiz submit) are not
  separately instrumented — `commit_mini_mission` already requires an
  *existing* progress doc (`quiz_passed`), so it can never be first;
  `submit_deliverable` and quiz submit are reachable in the normal flow
  only after a phase tick already ran. This is disclosed, not silently
  assumed: a client that skipped the UI and called one of those routes
  directly, first, would not trigger this event — a real limitation of
  wiring one call site rather than all four, documented rather than
  worked around, consistent with this codebase's own doctrine of never
  fabricating an event for an action that didn't happen this way.

Both use `services/events.py`'s existing, already-in-production
`EventBus` (`db.event_log` persistence + subscriber fan-out) — no new
mechanism invented.
"""

from __future__ import annotations

from typing import Any, Dict

from db import db
from services.events import events


async def emit_first_value_if_new(user_id: str, payload: Dict[str, Any]) -> bool:
    """Call BEFORE the `db.progress` upsert it guards. Returns True (and
    publishes `academy_first_value_reached`) iff the user had zero
    `db.progress` documents at call time — i.e. the write about to
    happen creates their first one. A user who already has any progress
    document never re-triggers this, by construction (count > 0 short-
    circuits before the event ever publishes)."""
    existing = await db.progress.count_documents({"user_id": user_id})
    if existing == 0:
        await events.publish("academy_first_value_reached", payload)
        return True
    return False
