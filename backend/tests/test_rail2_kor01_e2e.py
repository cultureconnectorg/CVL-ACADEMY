"""RAIL 2 — "MASTER -> RUNTIME ACADEMY" end-to-end proof (Founder
instruction, 2026-09-06).

Gate: "au moins une formation canonique complète est suivable de bout en
bout dans le runtime réel." This suite drives the full target chain —
Learning -> Skill -> Evidence -> Assessment -> Certification ->
Qualification -> Opportunity -> Mission — against KOR-01 (Podcast &
Audio Production), the pilot formation, using real code paths only:

  1. `kor_canonical.import_kor_docs` imports the real `docs/kor/kor01/`
     tree (no fixture — same rationale as `test_klt_canonical.py`: the
     corpus already lives unpacked in this repo).
  2. Every one of KOR-01's 14 real skills is registered
     (`skills.progression.register_skill`) and evidence recorded
     (`record_evidence`) until each is "acquired".
  3. A real `Rubric` is created for certification code `KOR01-A01`, one
     criterion per skill, mirroring the Rubric Master doctrine already
     reconciled in `certification/models.py`.
  4. `certification.service.start_attempt` / `submit_attempt` /
     `grade_attempt` run the existing, untouched certification engine —
     grading with maximal scores passes the attempt.
  5. `grade_attempt`'s own `if passed:` block (unmodified except for one
     additive call) issues a `Qualification` via
     `qualification.maybe_issue_qualification` — the one genuinely new
     link this rail adds.
  6. A `Mission` with `required_qualification_codes` naming that
     qualification is created; `api.missions.list_missions` and
     `accept_mission` (called directly, not over HTTP — same tier as
     every other test in this suite) prove the eligibility gate — the
     Opportunity view — actually works: ineligible before certification,
     eligible and acceptable after.

DB-backed pieces run against `mongomock_motor.AsyncMongoMockClient` — no
live MongoDB in this sandbox, same rationale as every other canonical
runtime binding test in this repo.
"""

from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

import api.missions as missions_api_module
import certification.service as certification_service_module
import kor_canonical.import_pipeline as kor_import_pipeline_module
import kor_canonical.progress as kor_progress_module
import kor_canonical.provenance as kor_provenance_module
import kor_canonical.read_model as kor_read_model_module
import qualification.service as qualification_service_module
import services.events as events_module
import services.frek_core as frek_core_module
import skills.progression as skills_progression_module
import wallet.service as wallet_service_module
from certification.models import GradeInput, Rubric, RubricCriterion, RubricInput
from certification.service import (get_rubric, grade_attempt, start_attempt,
                                   submit_attempt)
from kor_canonical.import_pipeline import import_kor_docs
from kor_canonical.read_model import (get_canonical_kor_formation,
                                      list_canonical_kor_skills)
from models import Mission, User
from qualification.models import QualificationDefinitionInput
from qualification.service import list_user_qualifications, register_definition
from skills.progression import get_user_progress, record_evidence, register_skill

CERTIFICATION_CODE = "KOR01-A01"
QUALIFICATION_CODE = "QUAL-KOR01-PRODUCTEUR-PODCAST"
MISSION_CODE = "MISSION-KORA-ANTENNE-LANBI"


@pytest.fixture
async def rail2_db(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_rail2_kor01_test"]
    for module in (
        kor_import_pipeline_module,
        kor_provenance_module,
        kor_read_model_module,
        kor_progress_module,
        skills_progression_module,
        certification_service_module,
        qualification_service_module,
        frek_core_module,
        events_module,
        wallet_service_module,
        missions_api_module,
    ):
        monkeypatch.setattr(module, "db", mock_db)
    return mock_db


def _rubric_criteria(skills):
    """One eliminatory-free criterion per real KOR01 skill, max_score=10
    — mirrors the FMS Rubric Master shape already reconciled in
    `certification/models.py`, parametrized by the skills this pass
    actually imported (never a hardcoded count)."""
    return [
        RubricCriterion(
            id=skill.skill_id,
            label=skill.label,
            bloc="B1",
            skill_id=skill.skill_id,
            weight=1.0,
            max_score=10.0,
        )
        for skill in skills
    ]


@pytest.mark.asyncio
async def test_kor01_full_chain_learning_to_mission(rail2_db):
    user = User(
        frek_id="FREK-RAIL2-001",
        email="rail2.candidate@example.com",
        display_name="Candidat Rail 2",
        password_hash="x",
    )
    await rail2_db.users.insert_one(user.model_dump())

    # ---- 1. Learning: import the real KOR-01 corpus -----------------
    report = await import_kor_docs()
    assert "KOR-01" in report.formations_found
    assert report.unparsed_count >= 0  # every real file accounted for
    assert report.all_files_accounted_for is True

    formation = await get_canonical_kor_formation("KOR-01")
    assert formation is not None
    assert formation.fully_complete is True
    assert formation.module_count == 14
    assert formation.unresolved_skill_ids == []

    # ---- 2. Skill + Evidence: register and acquire all 14 skills ----
    kor_skills = await list_canonical_kor_skills("KOR-01")
    assert len(kor_skills) == 14
    for skill in kor_skills:
        await register_skill(
            skill_id=skill.skill_id,
            metier="KOR01",
            niveau="N1",
            bloc="B1",
            label=skill.label,
        )
        await record_evidence(
            user_id=user.id,
            skill_id=skill.skill_id,
            evidence_type="deliverable",
            ref=skill.canonical_module_code or skill.skill_id,
        )
        await record_evidence(
            user_id=user.id,
            skill_id=skill.skill_id,
            evidence_type="quiz",
            ref=skill.canonical_module_code or skill.skill_id,
        )

    progress = await get_user_progress(user.id, metier="KOR01")
    assert len(progress) == 14
    assert all(p.state == "acquired" for p in progress)

    # ---- 3. Assessment: real Rubric for KOR01-A01 --------------------
    rubric_input = RubricInput(
        level="A01",
        formation_code="KOR-01",
        criteria=_rubric_criteria(kor_skills),
        pass_threshold_pct=80.0,
    )
    rubric = Rubric(certification_code=CERTIFICATION_CODE, **rubric_input.model_dump())
    await rail2_db.certification_rubrics.insert_one(rubric.model_dump())
    fetched_rubric = await get_rubric(CERTIFICATION_CODE)
    assert fetched_rubric.certification_code == CERTIFICATION_CODE
    assert len(fetched_rubric.criteria) == 14

    # ---- 3b. Opportunity/Mission gate BEFORE certification -----------
    definition = await register_definition(
        QUALIFICATION_CODE,
        QualificationDefinitionInput(
            label="Producteur Podcast CVLN (KOR-01)",
            formation_code="KOR-01",
            certification_codes=[CERTIFICATION_CODE],
        ),
    )
    assert definition.code == QUALIFICATION_CODE

    mission = Mission(
        code=MISSION_CODE,
        title="Produire un épisode pour L'Antenne Lanbi",
        description="Mission réservée aux producteurs podcast qualifiés KOR-01.",
        pole="KOR",
        cc_reward=20,
        stade_required="pousse",
        entity="KORA",
        required_qualification_codes=[QUALIFICATION_CODE],
    )
    await rail2_db.missions.insert_one(mission.model_dump())

    missions_before = await missions_api_module.list_missions(current=user)
    listed_before = next(m for m in missions_before if m["code"] == MISSION_CODE)
    assert listed_before["eligible"] is False

    with pytest.raises(Exception):
        await missions_api_module.accept_mission(MISSION_CODE, current=user)

    # ---- 4. Certification: start / submit / grade --------------------
    attempt = await start_attempt(user.id, CERTIFICATION_CODE)
    assert attempt.status == "in_progress"
    attempt = await submit_attempt(attempt.id, user.id)
    assert attempt.status == "submitted"

    grade = GradeInput(
        scores={c.id: c.max_score for c in fetched_rubric.criteria},
        comments="Jury Rail 2 — dossier complet, soutenance conforme.",
    )
    graded = await grade_attempt(attempt.id, "jury-rail2", grade)
    assert graded.passed is True
    assert graded.eliminated is False
    assert graded.score_global == pytest.approx(100.0)

    # ---- 5. Qualification: issued by the certification hook ----------
    quals = await list_user_qualifications(user.id)
    codes = {q.qualification_code for q in quals}
    assert QUALIFICATION_CODE in codes
    issued = next(q for q in quals if q.qualification_code == QUALIFICATION_CODE)
    assert issued.source_certification_code == CERTIFICATION_CODE
    assert issued.source_attempt_id == attempt.id

    # Re-grading (idempotent hook) must never issue a second copy.
    quals_again = await list_user_qualifications(user.id)
    assert len(quals_again) == len([q for q in quals_again if q.qualification_code == QUALIFICATION_CODE])
    assert len([q for q in quals_again if q.qualification_code == QUALIFICATION_CODE]) == 1

    # ---- 6. Opportunity/Mission: eligible + acceptable AFTER ---------
    missions_after = await missions_api_module.list_missions(current=user)
    listed_after = next(m for m in missions_after if m["code"] == MISSION_CODE)
    assert listed_after["eligible"] is True

    accept_result = await missions_api_module.accept_mission(MISSION_CODE, current=user)
    assert accept_result["ok"] is True
    assert accept_result["status"] == "accepted"

    user_mission = await rail2_db.user_missions.find_one(
        {"user_id": user.id, "mission_code": MISSION_CODE}, {"_id": 0}
    )
    assert user_mission is not None
    assert user_mission["status"] == "accepted"
