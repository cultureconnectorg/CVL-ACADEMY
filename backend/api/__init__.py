"""CVLN Academy API — one router per domain, aggregated here.

Each sub-router owns one bounded concern (auth, onboarding, formations,
learning journey, quiz, badges, missions, progression, mentor, FMS import,
FMS lineage, canonical FMS runtime, canonical Kiltikonet runtime, skills,
certification, templates, assistants, wallet, integrations). This module
just mounts them all under the single `/api` prefix used by the app.
"""

from __future__ import annotations

from fastapi import APIRouter

from . import (assistants, auth, badges, canonical, certification, fms,
               fms_lineage, formations, health, integrations, klt_canonical,
               learning, mentor, missions, onboarding, orgs, progression,
               quizzes, skills, templates, wallet)

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
    skills,
    certification,
    templates,
    assistants,
    wallet,
    integrations,
):
    router.include_router(module.router)
