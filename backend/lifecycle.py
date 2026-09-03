"""Academy lifecycle — derived, non-exclusive maturity signals.

Per docs/ACADEMY_LIFECYCLE_STATE_MODEL.md: these are DERIVED read-time
signals, never a stored account-status field, never a replacement for
any real domain field. This module intentionally starts with exactly
one derivation — `is_returning_session` — because W-FUNNEL-1's own
mission scope is the foundation, not the full lifecycle surface.

`RETURNING` (W-FUNNEL-0's own gap-matrix finding) was originally
expected to need a new `User.last_login_at` field. It doesn't: every
successful authentication (register AND login, `backend/api/auth.py`)
already calls `issue_refresh_token`, which inserts a real
`db.refresh_tokens` document stamped with `created_at`
(`backend/auth.py::issue_refresh_token`). The most recent of those
timestamps for a user *is* "last successful authentication" — an
already-existing, trustworthy signal, so no schema change, no
migration, and no new field was needed. This is exactly the
"if existing repository data already provides an equivalent
trustworthy signal, reuse it instead" case the mission itself asked to
be checked for.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import List, Optional

# A user is "returning" once a session boundary of at least this long
# has passed since the account was created and they authenticated again
# — deliberately conservative (not "any second login counts") so a
# multi-tab/refresh-token-rotation burst right after signup never reads
# as a return visit.
RETURNING_THRESHOLD = timedelta(days=1)


def _parse(ts: Optional[str]) -> Optional[datetime]:
    """Best-effort ISO-8601 parse, tolerant of a naive (no-tz) string —
    every timestamp this module reads is written by `utc_now_iso()`
    (`db.py`), which is always tz-aware, but defensive parsing costs
    nothing and avoids a crash on any historical/malformed row."""
    if not ts:
        return None
    try:
        dt = datetime.fromisoformat(ts)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def is_returning_session(
    user_created_at: Optional[str],
    refresh_token_created_ats: List[Optional[str]],
    *,
    now: Optional[datetime] = None,
    threshold: timedelta = RETURNING_THRESHOLD,
) -> bool:
    """True once the user's most recent authentication happened at
    least `threshold` after their account was created — i.e. they came
    back, not just refreshed a token moments after signing up.

    Pure function — no DB access, no I/O — so it is fully unit-testable
    without MongoDB, same pattern as `quiz.py`/`certification/scoring.
    py`'s own "no DB required" test suites.
    """
    created = _parse(user_created_at)
    if created is None:
        return False  # no created_at at all -> cannot derive anything real
    stamps = [
        d for d in (_parse(t) for t in refresh_token_created_ats) if d is not None
    ]
    if not stamps:
        return False  # never authenticated at all (shouldn't happen, fails safe)
    most_recent = max(stamps)
    return (most_recent - created) >= threshold
