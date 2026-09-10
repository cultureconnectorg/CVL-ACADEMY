"""P0 auth token atomicity regression tests.

Proves refresh-token rotation, password-reset consumption and email-verification
consumption cannot succeed twice for the same opaque token.
"""

from __future__ import annotations

import asyncio

import pytest
from fastapi import HTTPException
from mongomock_motor import AsyncMongoMockClient

import auth as auth_module
from auth import (
    consume_email_verification_token,
    consume_password_reset_token,
    issue_email_verification_token,
    issue_password_reset_token,
    issue_refresh_token,
    rotate_refresh_token,
)


@pytest.fixture
async def auth_db(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_academy_auth_atomicity_test"]
    monkeypatch.setattr(auth_module, "db", mock_db)
    return mock_db


@pytest.mark.asyncio
async def test_refresh_rotation_is_single_winner_under_concurrent_reuse(auth_db):
    raw = await issue_refresh_token("u1")

    results = await asyncio.gather(
        rotate_refresh_token(raw),
        rotate_refresh_token(raw),
        return_exceptions=True,
    )

    successes = [r for r in results if not isinstance(r, Exception)]
    failures = [r for r in results if isinstance(r, HTTPException)]

    assert len(successes) == 1
    assert len(failures) == 1
    assert failures[0].status_code == 401
    stored = await auth_db.refresh_tokens.find_one({"user_id": "u1", "revoked": True})
    assert stored is not None


@pytest.mark.asyncio
async def test_password_reset_token_can_only_be_consumed_once(auth_db):
    raw = await issue_password_reset_token("u1")

    assert await consume_password_reset_token(raw) == "u1"
    with pytest.raises(HTTPException) as exc:
        await consume_password_reset_token(raw)
    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_email_verification_token_can_only_be_consumed_once(auth_db):
    raw = await issue_email_verification_token("u1")

    assert await consume_email_verification_token(raw) == "u1"
    with pytest.raises(HTTPException) as exc:
        await consume_email_verification_token(raw)
    assert exc.value.status_code == 400
