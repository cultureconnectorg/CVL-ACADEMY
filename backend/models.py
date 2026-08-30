"""Pydantic models for CVLN Academy OS."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


def _uid() -> str:
    return str(uuid.uuid4())


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


AcademyContext = Literal["INTERNAL", "EXTERNAL", "BRIDGE"]
AudienceLevel = Literal[
    "DEBUTANT", "INTERMEDIAIRE", "AVANCE", "PROFESSIONNEL", "INSTITUTIONNEL"
]


class InternalJobVersion(BaseModel):
    context: Optional[str] = None
    tools: List[str] = Field(default_factory=list)
    methods: List[str] = Field(default_factory=list)
    missions: List[str] = Field(default_factory=list)


class ExternalJobVersion(BaseModel):
    transferable_skills: List[str] = Field(default_factory=list)
    market_tools: List[str] = Field(default_factory=list)
    market_practices: List[str] = Field(default_factory=list)
    outcomes: List[str] = Field(default_factory=list)


class BridgeJobVersion(BaseModel):
    cvln_entities: List[str] = Field(default_factory=list)
    missions: List[str] = Field(default_factory=list)
    opportunities: List[str] = Field(default_factory=list)
    contribution: Optional[str] = None


class JobTruth(BaseModel):
    model_config = ConfigDict(extra="ignore")

    market_name: Optional[str] = None
    cvln_name: Optional[str] = None
    rome_refs: List[str] = Field(default_factory=list)
    external_certification_refs: List[str] = Field(default_factory=list)
    level: Optional[str] = None
    sectors: List[str] = Field(default_factory=list)
    real_missions: List[str] = Field(default_factory=list)
    technical_skills: List[str] = Field(default_factory=list)
    behavioral_skills: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    deliverables: List[str] = Field(default_factory=list)
    evidence: List[str] = Field(default_factory=list)
    prerequisites: List[str] = Field(default_factory=list)
    outcomes: List[str] = Field(default_factory=list)
    market_salary_or_economics: Optional[str] = None
    market_need: Optional[str] = None
    job_evolution: Optional[str] = None
    internal_version: InternalJobVersion = Field(default_factory=InternalJobVersion)
    external_version: ExternalJobVersion = Field(default_factory=ExternalJobVersion)
    bridge: BridgeJobVersion = Field(default_factory=BridgeJobVersion)


class FormationEconomics(BaseModel):
    model_config = ConfigDict(extra="ignore")

    public_price_eur: Optional[float] = None
    company_price_eur: Optional[float] = None
    funding_options: List[str] = Field(default_factory=list)
    pedagogical_cost_eur: Optional[float] = None
    instructors_cost_eur: Optional[float] = None
    production_cost_eur: Optional[float] = None
    studio_or_venue_cost_eur: Optional[float] = None
    tech_cost_eur: Optional[float] = None
    acquisition_cost_eur: Optional[float] = None
    administration_cost_eur: Optional[float] = None
    reinvestment_rate: Optional[float] = None
    margin_target: Optional[float] = None


class ReconciliationFlag(BaseModel):
    type: str
    message: str


class FormationCartography(BaseModel):
    model_config = ConfigDict(extra="ignore")

    primary_job: str
    secondary_jobs: List[str] = Field(default_factory=list)
    contexts: List[AcademyContext] = Field(default_factory=list)
    audience: List[AudienceLevel] = Field(default_factory=list)
    level: str
    competencies: List[str] = Field(default_factory=list)
    professional_activities: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    deliverables: List[str] = Field(default_factory=list)
    evidence: List[str] = Field(default_factory=list)
    outcomes: List[str] = Field(default_factory=list)
    meta_entities: List[str] = Field(default_factory=list)
    bridges: List[str] = Field(default_factory=list)
    delivery_formats: List[str] = Field(default_factory=list)
    duration_h: int
    cc: int
    current_price_eur: Optional[float] = None
    provisional_economics: Dict[str, Any] = Field(default_factory=dict)
    calibration_sources: List[str] = Field(default_factory=list)
    needs_external_calibration: bool = True
    inconsistencies: List[ReconciliationFlag] = Field(default_factory=list)
    reconstruction_status: str
    source: str


# ---------------- USERS (FREK-ID) ----------------
Role = Literal[
    "student", "trainer", "corrector", "jury", "admin", "super_admin", "founder"
]

# Roles with elevated / staff-level access — used by permission checks that
# should accept "any staff role" rather than one specific role.
STAFF_ROLES: tuple = ("trainer", "corrector", "jury", "admin", "super_admin", "founder")
ADMIN_ROLES: tuple = ("admin", "super_admin", "founder")


class OAuthAccount(BaseModel):
    """One linked external identity (Google / Apple / GitHub / Microsoft)."""

    provider: Literal["google", "apple", "github", "microsoft"]
    provider_user_id: str
    linked_at: str = Field(default_factory=_now)


class User(BaseModel):
    """A CVLN Academy learner identified by their FREK-ID."""

    model_config = ConfigDict(extra="ignore")

    id: str = Field(default_factory=_uid)
    frek_id: str  # e.g. FREK-001, unique cultural identifier
    email: EmailStr
    display_name: str
    password_hash: str
    role: Role = "student"
    org_id: Optional[str] = None
    cohort_id: Optional[str] = None
    lang: str = "fr"  # fr | en | kr
    stade: str = "graine"  # graine | pousse | racine | branches | arbre | foret
    cc_credits: int = 0
    # Onboarding — FREK Origin Story
    onboarding_completed: bool = False
    metier_vise: Optional[str] = None  # pole code (FMS / KOR / KLT / FRK / ...)
    territoire: Optional[str] = (
        None  # martinique | guadeloupe | guyane | france | caraibe | diaspora | autre
    )
    objectif_perso: Optional[str] = None  # free text (≤ 240 chars)
    signals: Dict[str, int] = Field(
        default_factory=lambda: {
            "FREK-TIME": 0,
            "FREK-WORK": 0,
            "FREK-SCORE": 0,
            "FREK-LINK": 0,
            "FREK-CERT": 0,
            "FREK-CONTRIB": 0,
        }
    )
    # Auth hardening
    email_verified: bool = False
    oauth_accounts: List[OAuthAccount] = Field(default_factory=list)
    totp_secret: Optional[str] = None  # set once 2FA is enrolled; None = 2FA off
    totp_enabled: bool = False
    created_at: str = Field(default_factory=_now)


class UserPublic(BaseModel):
    id: str
    frek_id: str
    email: EmailStr
    display_name: str
    role: Role = "student"
    org_id: Optional[str] = None
    cohort_id: Optional[str] = None
    lang: str
    stade: str
    cc_credits: int
    signals: Dict[str, int]
    created_at: str
    onboarding_completed: bool = False
    metier_vise: Optional[str] = None
    territoire: Optional[str] = None
    objectif_perso: Optional[str] = None
    email_verified: bool = False
    totp_enabled: bool = False


class RegisterInput(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    display_name: str = Field(min_length=1, max_length=80)
    lang: str = "fr"
    invite_code: Optional[str] = None  # accepts an org/cohort invitation at signup


class LoginInput(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    token: str
    refresh_token: str
    user: UserPublic


class RefreshTokenInput(BaseModel):
    refresh_token: str


class ForgotPasswordInput(BaseModel):
    email: EmailStr


class ResetPasswordInput(BaseModel):
    token: str
    new_password: str = Field(min_length=6)


class VerifyEmailInput(BaseModel):
    token: str


# ---------------- ORGANISATIONS / COHORTS / INVITATIONS ----------------
class Organisation(BaseModel):
    id: str = Field(default_factory=_uid)
    name: str
    slug: str
    created_at: str = Field(default_factory=_now)


class OrganisationInput(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    slug: str = Field(min_length=1, max_length=60)


class Cohort(BaseModel):
    id: str = Field(default_factory=_uid)
    org_id: str
    name: str
    pole: Optional[str] = None  # optional metier/pole focus for this cohort
    starts_at: Optional[str] = None
    ends_at: Optional[str] = None
    created_at: str = Field(default_factory=_now)


class CohortInput(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    pole: Optional[str] = None
    starts_at: Optional[str] = None
    ends_at: Optional[str] = None


class Invitation(BaseModel):
    id: str = Field(default_factory=_uid)
    code: str  # opaque, shareable invite code
    email: Optional[str] = None  # optional — set to restrict to one address
    role: Role = "student"
    org_id: Optional[str] = None
    cohort_id: Optional[str] = None
    invited_by: str  # user id
    used_by: Optional[str] = None
    used_at: Optional[str] = None
    expires_at: Optional[str] = None
    created_at: str = Field(default_factory=_now)


class InvitationInput(BaseModel):
    email: Optional[EmailStr] = None
    role: Role = "student"
    org_id: Optional[str] = None
    cohort_id: Optional[str] = None
    expires_in_days: int = 14


# ---------------- FORMATIONS ----------------
class Module(BaseModel):
    code: str
    name: str
    duration_h: float
    stade: str  # graine | pousse | racine | branches | arbre | foret
    hook: str
    deliverable: str
    frek_signal: str


class Formation(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=_uid)
    code: str  # e.g. FMS-01
    name: str
    pole: str  # pole code
    pole_name: str
    pole_color: str
    duration_h: int
    stades: List[str]
    cc: int
    badge_name: str
    prerequisites: str
    debouches: str
    description: str
    objective_strategic: str
    modules: List[Module]
    contexts: List[AcademyContext] = Field(default_factory=list)
    audience_levels: List[AudienceLevel] = Field(default_factory=list)
    positioning_note: Optional[str] = None
    bridge_entities: List[str] = Field(default_factory=list)
    job_truth: JobTruth = Field(default_factory=JobTruth)
    economics: FormationEconomics = Field(default_factory=FormationEconomics)
    calibration_sources: List[str] = Field(default_factory=list)
    reconciliation_flags: List[ReconciliationFlag] = Field(default_factory=list)
    needs_external_calibration: bool = True
    reconstruction_status: str = "NEEDS_RECONSTRUCTION"
    cartography: Optional[FormationCartography] = None
    external_calibration: Optional[Dict[str, Any]] = None
    market_job_title: Optional[str] = None
    calibration_confidence: Optional[str] = None
    calibration_date: Optional[str] = None


# ---------------- BADGES ----------------
class Badge(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=_uid)
    code: str
    name: str
    tier: str  # decouverte | pole | senior | executive | foret
    color: str
    description: str
    cc_threshold: int  # cc credits required
    pole: Optional[str] = None
    icon: str = "medal"


class UserBadge(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=_uid)
    user_id: str
    badge_code: str
    earned_at: str = Field(default_factory=_now)


# ---------------- MISSIONS ----------------
class Mission(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=_uid)
    code: str
    title: str
    description: str
    pole: str
    cc_reward: int
    stade_required: str
    entity: str  # CVLN entity that gets outputs
    status_type: str = "open"  # open | featured | urgent


class UserMission(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=_uid)
    user_id: str
    mission_code: str
    status: str = "accepted"  # accepted | submitted | validated
    submitted_at: Optional[str] = None
    proof: Optional[str] = None


# ---------------- QUIZ ----------------
class QuizChoice(BaseModel):
    id: str
    text: str
    correct: bool


class QuizQuestion(BaseModel):
    n: int
    type: str
    question: str
    choices: List[QuizChoice]


class QuizSubmission(BaseModel):
    module_code: str
    answers: Dict[str, str]  # question_n -> choice_id


class QuizResult(BaseModel):
    score: float
    passed: bool  # score >= 0.8
    correct: int
    total: int
    cc_earned: int
    signal_emitted: str


# ---------------- PROGRESSION ----------------
class ModuleProgress(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=_uid)
    user_id: str
    formation_code: str
    module_code: str
    completed: bool = False
    score: float = 0.0
    completed_at: Optional[str] = None
    signal_emitted: Optional[str] = None


# ---------------- MENTOR (AI) ----------------
class MentorMessage(BaseModel):
    role: str  # user | assistant
    content: str
    ts: str = Field(default_factory=_now)


class MentorConversation(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=_uid)
    user_id: str
    session_id: str
    messages: List[MentorMessage] = Field(default_factory=list)
    created_at: str = Field(default_factory=_now)
    updated_at: str = Field(default_factory=_now)


class MentorChatInput(BaseModel):
    message: str
    session_id: Optional[str] = None


# ---------------- ONBOARDING (FREK Origin Story) ----------------
class OnboardingInput(BaseModel):
    lang: str  # fr | en | kr
    metier_vise: str  # pole code
    territoire: (
        str  # martinique | guadeloupe | guyane | france | caraibe | diaspora | autre
    )
    objectif_perso: str = Field(min_length=3, max_length=240)


class OnboardingResult(BaseModel):
    user: UserPublic
    recommended_formation: Optional[Dict[str, Any]] = None
    recommended_mission: Optional[Dict[str, Any]] = None
    badge_earned: Optional[Dict[str, Any]] = None
    signals_emitted: List[str] = Field(default_factory=list)
