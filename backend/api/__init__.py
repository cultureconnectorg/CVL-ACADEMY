"""CVLN Academy API — one router per domain, aggregated here.

Each sub-router owns one bounded concern (auth, onboarding, formations,
learning journey, quiz, badges, missions, progression, mentor, FMS import,
FMS lineage, skills, certification, templates, assistants, wallet,
integrations, CareOps). This module just mounts them all under the single `/api`
prefix used by the app.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from . import (
    assistants,
    auth,
    badges,
    careops,
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

# Informational/admin/integration/support surfaces stay reachable under their existing
# auth rules. CareOps must remain reachable even when a learner cannot enter the journey:
# a blocked user still needs to be able to ask for help or file a complaint.
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
    careops,
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
