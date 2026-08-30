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
    formations,
    health,
    learning,
    mentor,
    missions,
    onboarding,
    progression,
    quizzes,
)

router = APIRouter(prefix="/api")

for module in (
    health,
    auth,
    onboarding,
    formations,
    learning,
    quizzes,
    badges,
    missions,
    progression,
    mentor,
):
    router.include_router(module.router)
