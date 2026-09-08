"""ACA-0030 — Ecosystem Builder surface (consumer -> learner ->
professional -> builder).

`docs/ACADEMY_FUNNEL_GAP_MATRIX.md`'s own sub-capability classification
for this row is the scope contract for this module — copied here
verbatim so the boundary stays visible next to the code that respects
it:

    Portfolio of competencies  -> PARTIAL   (real data, no unified view)
    Verified proofs            -> IMPLEMENTABLE_NOW
    Missions completed         -> IMPLEMENTABLE_NOW
    Professional identity      -> PARTIAL   (ACA-0028 already built it)
    Credentials                -> IMPLEMENTABLE_NOW
    Ecosystem history          -> PARTIAL   (event_log/frek_signals real,
                                              incomplete)
    Network/opportunities      -> REQUIRES_OTHER_CVLN_SYSTEM
    Economic activity          -> REQUIRES_OTHER_CVLN_SYSTEM
    Projects                   -> MISSING (no model exists)
    Collaborations             -> MISSING (no model exists)

This module composes ONLY the `IMPLEMENTABLE_NOW`/`PARTIAL` rows —
every one of them already-real data this codebase computes elsewhere
(`services/professional_profile.py`'s ACA-0028 composition,
`skills/progression.py`'s evidence chain, `db.user_missions`,
`db.event_log`). It never fabricates Projects, Collaborations, Network,
or Economic activity — those stay absent from the response entirely
rather than being represented as empty placeholders that could later
be mistaken for "built but empty".

**The four-stage progression** (`consumer -> learner -> professional ->
builder`) is derived, not stored — recomputed from the same real
signals on every call, exactly like `services/progressive_horizon.py`
and `services/professional_profile.py` before it:

- `consumer`: no engagement signal yet (default for a freshly
  registered user who hasn't touched a module or mission).
- `learner`: at least one real skill-evidence entry or one validated
  mission — actively producing evidence, not yet holding an acquired
  skill or a passed certification.
- `professional`: has at least one acquired skill OR one passed
  certification — the same bar `professional_profile.py` already uses
  to mean "has a real professional identity".
- `builder`: professional AND has opted their professional profile
  public (`is_public=True`, ACA-0028's own opt-in flag) — the one real,
  non-fabricated signal inside Academy today for "not just practicing
  privately, but visible and circulating in the ecosystem". This reuses
  ACA-0028's existing opt-in rather than inventing a second one.
"""

from __future__ import annotations

from typing import Any, List, Literal, Optional

from pydantic import BaseModel

from db import db
from services.professional_profile import (
    ProfessionalCertification,
    ProfessionalSkill,
    compute_professional_profile,
)

BuilderStage = Literal["consumer", "learner", "professional", "builder"]

ECOSYSTEM_HISTORY_LIMIT = 20


class VerifiedProof(BaseModel):
    skill_id: str
    evidence_type: str
    ref: str
    sha256: str
    ts: str


class CompletedMission(BaseModel):
    mission_code: str
    accepted_at: Optional[str] = None
    submitted_at: Optional[str] = None


class EcosystemHistoryEntry(BaseModel):
    event_type: str
    published_at: str


class EcosystemBuilderSurface(BaseModel):
    stage: BuilderStage
    frek_id: str
    display_name: str
    is_public: bool
    portfolio: List[ProfessionalSkill]
    credentials: List[ProfessionalCertification]
    verified_proofs: List[VerifiedProof]
    missions_completed: List[CompletedMission]
    ecosystem_history: List[EcosystemHistoryEntry]


def _derive_stage(
    has_acquired_or_certified: bool,
    has_any_evidence_or_mission: bool,
    is_public: bool,
) -> BuilderStage:
    if has_acquired_or_certified and is_public:
        return "builder"
    if has_acquired_or_certified:
        return "professional"
    if has_any_evidence_or_mission:
        return "learner"
    return "consumer"


async def compute_ecosystem_builder_surface(user: Any) -> EcosystemBuilderSurface:
    """`user` follows the same duck-typed contract `professional_profile.
    compute_professional_profile` already accepts (real `id`/`frek_id`/
    `display_name`/`stade`) — this function never fetches the user
    document itself, only what's derived from it."""
    profile = await compute_professional_profile(user)

    evidence_docs = await db.skill_evidence.find(
        {"user_id": user.id}, {"_id": 0}
    ).to_list(1000)
    verified_proofs = [
        VerifiedProof(
            skill_id=e["skill_id"],
            evidence_type=e["evidence_type"],
            ref=e["ref"],
            sha256=e["sha256"],
            ts=e["ts"],
        )
        for e in evidence_docs
    ]

    mission_docs = await db.user_missions.find(
        {"user_id": user.id, "status": "validated"}, {"_id": 0}
    ).to_list(1000)
    missions_completed = [
        CompletedMission(
            mission_code=m["mission_code"],
            accepted_at=m.get("accepted_at"),
            submitted_at=m.get("submitted_at"),
        )
        for m in mission_docs
    ]

    history_docs = (
        await db.event_log.find({"payload.user_id": user.id}, {"_id": 0})
        .sort("published_at", -1)
        .to_list(ECOSYSTEM_HISTORY_LIMIT)
    )
    ecosystem_history = [
        EcosystemHistoryEntry(
            event_type=h["event_type"], published_at=h["published_at"]
        )
        for h in history_docs
    ]

    has_acquired_or_certified = bool(profile.acquired_skills) or bool(
        profile.certifications
    )
    has_any_evidence_or_mission = bool(verified_proofs) or bool(missions_completed)

    stage = _derive_stage(
        has_acquired_or_certified, has_any_evidence_or_mission, profile.is_public
    )

    return EcosystemBuilderSurface(
        stage=stage,
        frek_id=profile.frek_id,
        display_name=profile.display_name,
        is_public=profile.is_public,
        portfolio=profile.acquired_skills,
        credentials=profile.certifications,
        verified_proofs=verified_proofs,
        missions_completed=missions_completed,
        ecosystem_history=ecosystem_history,
    )
