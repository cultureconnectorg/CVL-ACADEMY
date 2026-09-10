"""CVLN Academy API — one router per domain, aggregated here.

Each sub-router owns one bounded concern (auth, onboarding, formations,
learning journey, quiz, badges, missions, progression, mentor, FMS import,
FMS lineage, canonical FMS runtime, canonical Kiltikonet runtime, skills,
certification, templates, assistants, wallet, integrations). This module
just mounts them all under the single `/api` prefix used by the app.
"""

from __future__ import annotations

from fastapi import APIRouter

from . import (
    assistants,
    auth,
    badges,
    canonical,
    certification,
    commerce,
    ecosystem_builder,
    fms,
    fms_lineage,
    formations,
    frk_canonical,
    health,
    integrations,
    klt_canonical,
    kor_canonical,
    learning,
    mentor,
    missions,
    onboarding,
    orgs,
    payments,
    physical_sessions,
    professional_governance,
    professional_profile,
    progression,
    quizzes,
    qualification,
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
    fms_lineage,
    canonical,
    klt_canonical,
    kor_canonical,
    frk_canonical,
    skills,
    certification,
    qualification,
    physical_sessions,
    templates,
    assistants,
    wallet,
    integrations,
    commerce,
    payments,
    professional_governance,
    professional_profile,
    ecosystem_builder,
):
    router.include_router(module.router)
