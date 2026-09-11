"""CVLN Academy API — one router per domain, aggregated here.

Each sub-router owns one bounded concern (auth, onboarding, formations,
learning journey, quiz, badges, missions, progression, mentor, FMS import,
FMS lineage, skills, certification, templates, assistants, wallet,
integrations, institutional bridge). This module just mounts them all under
the single `/api` prefix used by the app.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

# isort: off
from . import (
    assistants,
    auth,
    badges,
    certification,
    fms,
    fms_lineage,
    formations,
    health,
    institutional,
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
# isort: on
from .legal import require_legal_acceptance

router = APIRouter(prefix="/api")

# Public/auth/bootstrap surfaces: no Academy legal gate.
for module in (health, auth, legal):
    router.include_router(module.router)

# Informational/admin/integration surfaces stay reachable under their existing
# auth rules so legal documents, catalogue metadata and operational integrations
# are not accidentally coupled to a learner consent state.
for module in (
    orgs,
    formations,
    badges,
    fms,
    fms_lineage,
    skills,
    templates,
    assistants,
    integrations,
    institutional,
):
    router.include_router(module.router)

# Journey surfaces are fail-closed server-side: a user cannot start onboarding,
# learning, quizzes, missions, progression, AI mentoring, certification or wallet
# activity by bypassing the React app while the current legal bundle is unsigned.
for module in (
    onboarding,
    learning,
    quizzes,
    missions,
    progression,
    mentor,
    certification,
    wallet,
):
    router.include_router(
        module.router,
        dependencies=[Depends(require_legal_acceptance)],
    )
