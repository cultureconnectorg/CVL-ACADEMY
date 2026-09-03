"""Pure unit tests for lifecycle.py's `is_returning_session` — no DB
required. Complements backend_test.py (live-server E2E, exercises the
real `/frek/profile` `returning` field end-to-end) with fast, isolated
coverage of the derivation logic itself.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from lifecycle import RETURNING_THRESHOLD, is_returning_session


def _iso(dt: datetime) -> str:
    return dt.isoformat()


def test_no_created_at_is_never_returning():
    assert is_returning_session(None, [_iso(datetime.now(timezone.utc))]) is False


def test_no_refresh_tokens_is_never_returning():
    # fails safe: a user with a created_at but literally zero recorded
    # authentications should never be reported as "returning" — this
    # shouldn't happen in practice (register itself issues one), but the
    # function must not crash or guess.
    assert is_returning_session(_iso(datetime.now(timezone.utc)), []) is False


def test_signup_moment_alone_is_not_returning():
    now = datetime.now(timezone.utc)
    created = _iso(now)
    # register() issues a refresh token in the same request as account
    # creation — the two timestamps should be effectively simultaneous.
    assert is_returning_session(created, [created]) is False


def test_login_well_after_signup_is_returning():
    created = datetime.now(timezone.utc) - timedelta(days=10)
    recent_login = datetime.now(timezone.utc)
    assert (
        is_returning_session(_iso(created), [_iso(created), _iso(recent_login)]) is True
    )


def test_login_just_under_threshold_is_not_returning():
    now = datetime.now(timezone.utc)
    created = now - RETURNING_THRESHOLD + timedelta(minutes=5)
    assert is_returning_session(_iso(created), [_iso(created), _iso(now)]) is False


def test_login_just_over_threshold_is_returning():
    now = datetime.now(timezone.utc)
    created = now - RETURNING_THRESHOLD - timedelta(minutes=5)
    assert is_returning_session(_iso(created), [_iso(created), _iso(now)]) is True


def test_malformed_timestamps_are_ignored_not_crashed_on():
    now = datetime.now(timezone.utc)
    created = _iso(now - timedelta(days=5))
    assert (
        is_returning_session(created, ["not-a-real-timestamp", None, _iso(now)]) is True
    )


def test_naive_timestamp_treated_as_utc_not_crashed_on():
    # historical rows written before a hypothetical tz-naive bug, or any
    # other producer that omits tzinfo — must not raise.
    created_naive = (
        (datetime.now(timezone.utc) - timedelta(days=5))
        .replace(tzinfo=None)
        .isoformat()
    )
    recent_naive = datetime.now(timezone.utc).replace(tzinfo=None).isoformat()
    assert is_returning_session(created_naive, [created_naive, recent_naive]) is True
