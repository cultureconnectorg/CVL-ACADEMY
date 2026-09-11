"""CVLN Academy API — one router per domain, aggregated here.

Each sub-router owns one bounded concern (auth, onboarding, formations,
learning journey, quiz, badges, missions, progression, mentor, FMS import,
FMS lineage, skills, certification, templates, assistants, wallet,
integrations). This module just mounts them all under the single `/api`
prefix used by the app.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from . import (
    assistants,
    auth,
    badges,
    certification,
    fms,
    fms_lineage,
    formations,
    health,
    integrations,
    learning,
    legal,
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
from .legal import require_legal_acceptance

router = APIRouter(prefix="/api")

# Public/auth/bootstrap surfaces: no Academy legal gate.
for module in (health, auth, legal):
    router.include_router(module.router)

# The learner cannot even bootstrap onboarding options or submit onboarding
# until the current legal bundle has been signed server-side.
router.include_router(
    onboarding.router,
    dependencies=[Depends(require_legal_acceptance)],
)

# Existing domain routers keep their own authentication/authorization rules.
# The frontend Protected gate also prevents learner navigation until acceptance;
# backend expansion of the dependency to additional mutating routes can happen
# incrementally without breaking service-to-service integrations.
for module in (
    orgs,
    formations,
    learning,
    quizzes,
    badges,
    missions,
    progression,
    mentor,
    fms,
    fms_lineage,
    skills,
    certification,
    templates,
    assistants,
    wallet,
    integrations,
):
    router.include_router(module.router)
