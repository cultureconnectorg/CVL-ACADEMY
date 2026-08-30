"""CVLN Academy API — one router per domain, aggregated here.

Each sub-router owns one bounded concern (auth, onboarding, formations,
learning journey, quiz, badges, missions, progression, mentor, FMS import,
skills, certification, templates, assistants, wallet, integrations). This
module just mounts them all under the single `/api` prefix used by the app.
"""

from __future__ import annotations

from fastapi import APIRouter

from . import (
    assistants,
    auth,
    badges,
    certification,
    fms,
    formations,
    health,
    integrations,
    learning,
    mentor,
    missions,
    onboarding,
    orgs,
    progression,
    quizzes,
    skills,
    templates,
    wallet,
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
    skills,
    certification,
    templates,
    assistants,
    wallet,
    integrations,
):
    router.include_router(module.router)
