"""Pydantic models for CVLN Academy OS."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field, ConfigDict, EmailStr


def _uid() -> str:
    return str(uuid.uuid4())


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------- USERS (FREK-ID) ----------------
class User(BaseModel):
    """A CVLN Academy learner identified by their FREK-ID."""
    model_config = ConfigDict(extra="ignore")

    id: str = Field(default_factory=_uid)
    frek_id: str  # e.g. FREK-001, unique cultural identifier
    email: EmailStr
    display_name: str
    password_hash: str
    lang: str = "fr"  # fr | en | kr
    stade: str = "graine"  # graine | pousse | racine | branches | arbre | foret
    cc_credits: int = 0
    signals: Dict[str, int] = Field(default_factory=lambda: {
        "FREK-TIME": 0, "FREK-WORK": 0, "FREK-SCORE": 0,
        "FREK-LINK": 0, "FREK-CERT": 0, "FREK-CONTRIB": 0
    })
    created_at: str = Field(default_factory=_now)


class UserPublic(BaseModel):
    id: str
    frek_id: str
    email: EmailStr
    display_name: str
    lang: str
    stade: str
    cc_credits: int
    signals: Dict[str, int]
    created_at: str


class RegisterInput(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    display_name: str = Field(min_length=1, max_length=80)
    lang: str = "fr"


class LoginInput(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    token: str
    user: UserPublic


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
