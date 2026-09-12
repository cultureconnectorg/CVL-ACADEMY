"""CVLN Academy API — one router per domain, aggregated here.

Each sub-router owns one bounded concern (auth, onboarding, formations,
learning journey, quiz, badges, missions, progression, mentor, FMS import,
FMS lineage, skills, certification, templates, assistants, wallet,
integrations, stakeholders, economy, institutional bridge). This module just
mounts them all under the single `/api` prefix used by the app.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from . import (
    assistants,
    auth,
    badges,
    certification,
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
)
from .legal import require_legal_acceptance

router = APIRouter(prefix="/api")

for module in (health, auth, legal):
    router.include_router(module.router)

for module in (
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
    institutional,
):
    router.include_router(module.router)

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
