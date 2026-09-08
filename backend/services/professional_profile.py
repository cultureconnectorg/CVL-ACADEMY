"""ACA-0028 — Professional FREK profile as identity surface.

`FrekProfile.js` already exists, but as an internal engagement
dashboard (8 signal-count tiles, a raw signal log) — real data, but
never composed into anything a learner could actually use as a
professional identity: what skills they've genuinely acquired
(`skills/progression.py`'s already-real `Skill`/`UserSkill`/
`EvidenceEntry` chain), which certifications they've actually passed
(with the real jury-signed attestation proof `certification/
attestation.py` already computes), and — the one genuinely new
capability this pass adds — an explicit, off-by-default opt-in to
share that composed profile publicly by FREK-ID, so it can function as
an actual identity surface (a link a learner could point someone to),
not just a page only they themselves can see.

**Nothing here re-derives or duplicates evidence.** `acquired_skills`
reads `skills.progression.get_user_progress` (already the single real
source for skill state); `certifications` reads `certification.
service.list_user_attempts` filtered to `status == "passed"`, and each
one's proof is `certification.attestation.attestation_export_metadata`
— the exact metadata already documented as "what a FrekCore
`issue_proof` call will carry" — reused verbatim, not reshaped.

**Privacy**: `db.professional_profile_settings` is a new, additive
collection (`{user_id, is_public, updated_at}`) — a user's `is_public`
defaults to `False` (opt-in, not opt-out) and nothing here ever writes
to or reads from the core `User`/`db.users` document for this. The
public read path (`get_public_professional_profile`) returns `None`
uniformly for "no such FREK-ID" and "that FREK-ID exists but isn't
public" — never distinguishing the two, so a public caller can't use
this endpoint to enumerate which real FREK-IDs exist.
"""

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel

from certification.attestation import attestation_export_metadata
from certification.service import list_user_attempts
from db import db, utc_now_iso
from skills.progression import get_user_progress


class ProfessionalCertification(BaseModel):
    certification_code: str
    score_global: Optional[float] = None
    mention: Optional[str] = None
    jury_signature_sha256: Optional[str] = None
    graded_at: Optional[str] = None


class ProfessionalSkill(BaseModel):
    skill_id: str
    label: str
    metier: str
    niveau: str
    bloc: str
    evidence_count: int


class ProfessionalProfile(BaseModel):
    frek_id: str
    display_name: str
    stade: str
    acquired_skills: List[ProfessionalSkill]
    certifications: List[ProfessionalCertification]
    badges_count: int
    total_evidence_count: int
    is_public: bool = False


async def compute_professional_profile(user: Any) -> ProfessionalProfile:
    """`user` is a real `models.User` (or anything carrying the same
    `id`/`frek_id`/`display_name`/`stade` attributes) — this function
    itself never fetches the user document, only what's derived from
    it, so it works identically whether called for "my own profile"
    (already-authenticated `current`) or a public lookup (a `User`
    fetched by `frek_id`)."""
    skill_summaries = await get_user_progress(user.id)
    acquired = [s for s in skill_summaries if s.state == "acquired"]
    total_evidence = sum(s.evidence_count for s in skill_summaries)

    attempts = await list_user_attempts(user.id)
    passed = [a for a in attempts if a.status == "passed"]
    cert_proofs = []
    for a in passed:
        meta = attestation_export_metadata(a)
        cert_proofs.append(
            ProfessionalCertification(
                certification_code=meta["certification_code"],
                score_global=meta["score_global"],
                mention=meta["mention"],
                jury_signature_sha256=meta["jury_signature_sha256"],
                graded_at=a.graded_at,
            )
        )

    badges_count = await db.user_badges.count_documents({"user_id": user.id})

    settings = await db.professional_profile_settings.find_one(
        {"user_id": user.id}, {"_id": 0}
    )
    is_public = bool(settings and settings.get("is_public"))

    return ProfessionalProfile(
        frek_id=user.frek_id,
        display_name=user.display_name,
        stade=user.stade,
        acquired_skills=[
            ProfessionalSkill(
                skill_id=s.skill.id,
                label=s.skill.label,
                metier=s.skill.metier,
                niveau=s.skill.niveau,
                bloc=s.skill.bloc,
                evidence_count=s.evidence_count,
            )
            for s in acquired
        ],
        certifications=cert_proofs,
        badges_count=badges_count,
        total_evidence_count=total_evidence,
        is_public=is_public,
    )


async def set_profile_visibility(user_id: str, is_public: bool) -> None:
    await db.professional_profile_settings.update_one(
        {"user_id": user_id},
        {"$set": {"is_public": is_public, "updated_at": utc_now_iso()}},
        upsert=True,
    )


async def get_public_professional_profile(
    frek_id: str,
) -> Optional[ProfessionalProfile]:
    """Returns `None` for both "no such FREK-ID" and "exists but not
    public" — see module docstring for why that ambiguity is
    deliberate, not an oversight."""
    user_doc = await db.users.find_one({"frek_id": frek_id}, {"_id": 0})
    if not user_doc:
        return None
    settings = await db.professional_profile_settings.find_one(
        {"user_id": user_doc["id"]}, {"_id": 0}
    )
    if not settings or not settings.get("is_public"):
        return None

    class _UserLike:
        id = user_doc["id"]
        frek_id = user_doc["frek_id"]
        display_name = user_doc["display_name"]
        stade = user_doc.get("stade", "graine")

    return await compute_professional_profile(_UserLike())
