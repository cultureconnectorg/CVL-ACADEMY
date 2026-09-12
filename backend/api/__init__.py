"""CVLN Academy API — one router per domain, aggregated here.

Each sub-router owns one bounded concern (auth, onboarding, formations,
learning journey, quiz, badges, missions, progression, mentor, FMS import,
FMS lineage, skills, certification, templates, assistants, wallet,
integrations, stakeholders, economy, workbook runtime, institutional bridge,
careops, commercial, billing and accelerated compute). This module mounts them
under the single `/api` prefix used by the app.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from . import (
    accelerators,
    assistants,
    auth,
    badges,
    billing,
    billing_views,
    careops,
    certification,
    commercial,
    economy,
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
    stakeholders,
    templates,
    wallet,
    workbook_runtime,
)
from .commercial_access import require_commercial_learning_access
from .legal import require_legal_acceptance

router = APIRouter(prefix="/api")

for module in (health, auth, legal):
    router.include_router(module.router)

for module in (
    accelerators,
    orgs,
    stakeholders,
    formations,
    badges,
    fms,
    fms_lineage,
    skills,
    templates,
    assistants,
    integrations,
    economy,
    workbook_runtime,
    institutional,
    careops,
):
    router.include_router(module.router)

router.include_router(
    learning.router,
    dependencies=[
        Depends(require_legal_acceptance),
        Depends(require_commercial_learning_access),
    ],
)

for module in (commercial, billing, billing_views):
    router.include_router(
        module.router,
        dependencies=[Depends(require_legal_acceptance)],
    )

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
