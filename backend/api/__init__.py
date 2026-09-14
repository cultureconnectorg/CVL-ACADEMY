"""CVLN Academy API — one router per domain, aggregated here.

Each sub-router owns one bounded concern (auth, onboarding, formations,
learning journey, quiz, badges, missions, progression, mentor, FMS import,
FMS lineage, skills, certification, templates, assistants, wallet,
integrations, stakeholders, economy, workbook runtime, institutional bridge,
careops, commercial, billing and accelerated compute -- plus, since the
2026-09-14 main<->r35l31 reconciliation, canonical curriculum runtimes
(FRK/KOR/KLT/master registry/qualification/physical sessions) and the
legal/privacy/governance/security/quality/risk compliance layer, plus
accounting/professional/ecosystem and commerce/payments). This module
mounts them under the single `/api` prefix used by the app.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from . import (
    accelerators,
    accounting,
    accounting_advanced,
    accounting_protocols,
    assistants,
    assurance,
    auth,
    authority_policy,
    badges,
    billing,
    billing_views,
    canonical,
    careops,
    certification,
    commerce,
    commercial,
    critical_proof,
    data_classification,
    data_governance,
    ecosystem_builder,
    economy,
    evidence_graph,
    expert_portal,
    expert_validations,
    fms,
    fms_lineage,
    formations,
    frk_canonical,
    governance_advanced,
    governance_protocols,
    health,
    incident_core,
    institutional,
    integrations,
    klt_canonical,
    kor_canonical,
    learning,
    legal,
    legal_clauses,
    legal_deadlines,
    legal_documents,
    legal_evidence,
    legal_ops,
    legal_policy,
    legal_protocols,
    legal_risks,
    license_entitlement,
    master_registry,
    mentor,
    missions,
    onboarding,
    orgs,
    payments,
    physical_sessions,
    policy_registry,
    privacy_advanced,
    privacy_compliance,
    privacy_ops,
    privacy_protocols,
    production_gates,
    professional_governance,
    professional_profile,
    progression,
    qualification,
    quality,
    quality_advanced,
    quality_protocols,
    quizzes,
    regulatory_applicability,
    retention_executor,
    risk_advanced,
    risk_escalation,
    security_incident_protocol,
    security_remediation,
    security_verification,
    skills,
    stakeholders,
    templates,
    threat_model,
    trust_signature,
    wallet,
    workbook_runtime,
)
from .commercial_access import require_commercial_learning_access
from .legal import require_legal_acceptance

router = APIRouter(prefix="/api")

for module in (health, auth, legal):
    router.include_router(module.router)

# RECONCILE-2 Groupe 4 (2026-09-14): each of these modules also exports a
# `router` mounted below with the blanket require_legal_acceptance gate. This
# `public_router` is only the one or two routes each module's own docstring/
# code already documents as deliberately not requiring an Academy session —
# see professional_profile.py's and governance_advanced.py's own comments for
# each route's real, independent authorization (an opt-in public profile
# lookup; an external expert's own X-CVLN-Expert-Key header). Mounting them
# here, ungated, restores each route's originally-intended contract without
# touching the (correctly gated) rest of either module.
for module in (professional_profile, governance_advanced):
    router.include_router(module.public_router)

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

# 2026-09-14 main<->r35l31 reconciliation (RECONCILE-2): these 53 routers were
# built on claude/cvln-academy-production-r35l31 and never wired into main's
# router registry. Gated with the same require_legal_acceptance dependency as
# every other substantive business router above -- main's established default
# is "gated unless there is a specific reason not to" (health/auth/legal are
# the only ungated group, because legal-gate itself and auth cannot depend on
# having already passed the legal gate). None of these 53 are auth/health/
# legal-equivalent, so none qualify for that exemption.
#
# NOT gated with require_commercial_learning_access (unlike `learning` above):
# canonical/frk_canonical/kor_canonical/klt_canonical are formation-content
# viewers structurally similar to `learning`, so whether they should sit
# behind the same commercial paywall is a real open question -- but that is a
# monetization decision, not a technical one, and applying it wrong risks
# either paywalling content the Founder intends free or leaking paid content
# for free. Left as a flagged NEEDS_REVIEW in the RECONCILE-2 report rather
# than guessed here.
for module in (
    canonical,
    frk_canonical,
    kor_canonical,
    klt_canonical,
    master_registry,
    qualification,
    physical_sessions,
    commerce,
    payments,
    accounting,
    accounting_advanced,
    accounting_protocols,
    professional_governance,
    professional_profile,
    ecosystem_builder,
    expert_portal,
    expert_validations,
    legal_ops,
    legal_policy,
    legal_protocols,
    legal_documents,
    legal_clauses,
    legal_risks,
    legal_deadlines,
    legal_evidence,
    privacy_compliance,
    privacy_advanced,
    privacy_ops,
    privacy_protocols,
    governance_advanced,
    governance_protocols,
    quality,
    quality_advanced,
    quality_protocols,
    risk_advanced,
    risk_escalation,
    threat_model,
    security_remediation,
    security_verification,
    security_incident_protocol,
    incident_core,
    assurance,
    authority_policy,
    policy_registry,
    license_entitlement,
    data_classification,
    data_governance,
    regulatory_applicability,
    retention_executor,
    evidence_graph,
    critical_proof,
    trust_signature,
    production_gates,
):
    router.include_router(
        module.router,
        dependencies=[Depends(require_legal_acceptance)],
    )
