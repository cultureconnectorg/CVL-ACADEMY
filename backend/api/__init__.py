"""CVLN Academy API — one router per domain, aggregated here.

Each sub-router owns one bounded concern (auth, onboarding, formations,
learning journey, quiz, badges, missions, progression, mentor, FMS import,
FMS lineage, skills, certification, templates, assistants, wallet,
integrations, economy, commercial, billing). This module just mounts them all
under the single `/api` prefix used by the app.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from . import (
    assistants,
    auth,
    badges,
    billing,
    certification,
    commercial,
    economy,
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
from .commercial_access import require_commercial_learning_access
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
    economy,
):
    router.include_router(module.router)

# Learning routes have both the legal gate and, when enabled, the Economy 3D
# commercial entitlement gate. This prevents direct API bypass of paid access.
router.include_router(
    learning.router,
    dependencies=[
        Depends(require_legal_acceptance),
        Depends(require_commercial_learning_access),
    ],
)

# Commercial and billing transactions require the current legal bundle.
for module in (commercial, billing):
    router.include_router(
        module.router,
        dependencies=[Depends(require_legal_acceptance)],
    )

# Remaining journey surfaces are fail-closed server-side: a user cannot start
# onboarding, quizzes, missions, progression, AI mentoring, certification or
# the legacy Academy wallet activity by bypassing the React app while the
# current legal bundle is unsigned.
for module in (
    onboarding,
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
