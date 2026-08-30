"""CVLN Academy API — one router per domain, aggregated here.

Each sub-router owns one bounded concern (auth, onboarding, formations,
learning journey, quiz, badges, missions, progression, mentor). This module
just mounts them all under the single `/api` prefix used by the app.
"""

from __future__ import annotations

from fastapi import APIRouter

from . import (
    auth,
    badges,
    fms,
    formations,
    health,
    learning,
    mentor,
    missions,
    onboarding,
    orgs,
    progression,
    quizzes,
)

router = APIRouter(prefix="/api")

for module in (
    health,
    auth,
    onboarding,
    orgs,
    formations,
    learning,
    quizzes,
    badges,
    missions,
    progression,
    mentor,
    fms,
):
    router.include_router(module.router)
