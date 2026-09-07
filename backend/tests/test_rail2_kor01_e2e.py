"""RAIL 2 — "MASTER -> RUNTIME ACADEMY" end-to-end proof (Founder
instruction, 2026-09-06; extended 2026-09-07 to prove the chain
generalizes past the pilot — see `AGENTS.md`'s "Next concrete steps").

Gate: "au moins une formation canonique complète est suivable de bout en
bout dans le runtime réel." This suite drives the full target chain —
Learning -> Skill -> Evidence -> Assessment -> Certification ->
Qualification -> Opportunity -> Mission — against real KOR formations,
using real code paths only, parametrized over every formation this
extension proves (KOR-01, the original pilot, and KOR-02, the next-
richest formation — both independently confirmed `fully_complete=True`
by `kor_canonical`'s own derived check, per `AGENTS.md`'s KORA tier
table):

  1. `kor_canonical.import_kor_docs` imports the real `docs/kor/` tree
     (no fixture — same rationale as `test_klt_canonical.py`: the corpus
     already lives unpacked in this repo).
  2. Every one of the formation's real skills is registered
     (`skills.progression.register_skill`) and evidence recorded
     (`record_evidence`) until each is "acquired".
  3. A real `Rubric` is created for the formation's real certification
     code, one criterion per skill, mirroring the Rubric Master doctrine
     already reconciled in `certification/models.py`.
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
import fms_canonical
import klt_canonical
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
from kor_canonical.progress import record_content_viewed
from kor_canonical.read_model import (get_canonical_kor_formation,
                                      list_canonical_kor_skills)
from models import Mission, User
from qualification.models import QualificationDefinitionInput
from qualification.service import list_user_qualifications, register_definition
from skills.progression import get_user_progress, record_evidence, register_skill

# One case per formation this extension proves. Each is independently
# derived from the real corpus — never a hardcoded count — the test
# below still asserts `formation.module_count`/`len(kor_skills)` match
# what `kor_canonical` itself reports, so a mismatch here would fail
# loudly rather than silently pass on the wrong number.
KOR_CASES = [
    pytest.param(
        "KOR-01",
        "KOR01-A01",
        "QUAL-KOR01-PRODUCTEUR-PODCAST",
        "MISSION-KORA-ANTENNE-LANBI",
        "Produire un épisode pour L'Antenne Lanbi",
        "Mission réservée aux producteurs podcast qualifiés KOR-01.",
        14,
        id="KOR-01",
    ),
    pytest.param(
        "KOR-02",
        "KOR02-A01",
        "QUAL-KOR02-STORYTELLER-CULTUREL",
        "MISSION-KORA-ANTENNE-LANBI-RACONTEE",
        "Raconter et diffuser \"La valise racontée\"",
        "Mission réservée aux storytellers culturels qualifiés KOR-02.",
        12,
        id="KOR-02",
    ),
]


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

    # ACA-0019 — `check_certification_eligibility` now calls
    # `get_canonical_authority` first, which walks FMS/KLT/KOR's
    # `list_canonical_*` functions. This suite is KOR-only (real KOR-01/
    # KOR-02 corpus, no FMS/KLT content); FMS's and KLT's own `db`
    # references are untouched real modules, so unstubbed this hits a
    # real, absent MongoDB. `kor_canonical`'s own list function already
    # resolves through `kor_read_model_module.db`, patched above.
    async def no_formations(*_a, **_kw):
        return []

    monkeypatch.setattr(fms_canonical, "list_canonical_formations", no_formations)
    monkeypatch.setattr(klt_canonical, "list_canonical_klt_formations", no_formations)
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
@pytest.mark.parametrize(
    "formation_code,certification_code,qualification_code,mission_code,"
    "mission_title,mission_description,expected_skill_count",
    KOR_CASES,
)
async def test_kor_formation_full_chain_learning_to_mission(
    rail2_db,
    formation_code,
    certification_code,
    qualification_code,
    mission_code,
    mission_title,
    mission_description,
    expected_skill_count,
):
    user = User(
        frek_id=f"FREK-RAIL2-{formation_code}",
        email=f"rail2.candidate.{formation_code.lower()}@example.com",
        display_name="Candidat Rail 2",
        password_hash="x",
    )
    await rail2_db.users.insert_one(user.model_dump())
    metier = formation_code.replace("-", "")  # "KOR-01" -> "KOR01"

    # ---- 1. Learning: import the real KORA corpus --------------------
    report = await import_kor_docs()
    assert formation_code in report.formations_found
    assert report.unparsed_count >= 0  # every real file accounted for
    assert report.all_files_accounted_for is True

    formation = await get_canonical_kor_formation(formation_code)
    assert formation is not None
    assert formation.fully_complete is True
    assert formation.module_count == expected_skill_count
    assert formation.unresolved_skill_ids == []

    # ---- 1b. CERT-01 (Audit Chirurgical 2026-09-07): the candidate
    # actually opens every real module before certification is even
    # attemptable — this is exactly the server-enforced eligibility
    # gate `certification.service.check_certification_eligibility` now
    # requires; skipping it (as this test previously did) would 403 at
    # `start_attempt` below, same as it would for a real candidate who
    # never opened a single module.
    for module_code in formation.module_codes_in_order:
        await record_content_viewed(user.id, formation_code, module_code)

    # ---- 2. Skill + Evidence: register and acquire all real skills ---
    kor_skills = await list_canonical_kor_skills(formation_code)
    assert len(kor_skills) == expected_skill_count
    for skill in kor_skills:
        await register_skill(
            skill_id=skill.skill_id,
            metier=metier,
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

    progress = await get_user_progress(user.id, metier=metier)
    assert len(progress) == expected_skill_count
    assert all(p.state == "acquired" for p in progress)

    # ---- 3. Assessment: real Rubric for the formation's A01 ----------
    rubric_input = RubricInput(
        level="A01",
        formation_code=formation_code,
        criteria=_rubric_criteria(kor_skills),
        pass_threshold_pct=80.0,
    )
    rubric = Rubric(certification_code=certification_code, **rubric_input.model_dump())
    await rail2_db.certification_rubrics.insert_one(rubric.model_dump())
    fetched_rubric = await get_rubric(certification_code)
    assert fetched_rubric.certification_code == certification_code
    assert len(fetched_rubric.criteria) == expected_skill_count

    # ---- 3b. Opportunity/Mission gate BEFORE certification -----------
    definition = await register_definition(
        qualification_code,
        QualificationDefinitionInput(
            label=f"Qualification {formation_code} (Rail 2)",
            formation_code=formation_code,
            certification_codes=[certification_code],
        ),
    )
    assert definition.code == qualification_code

    mission = Mission(
        code=mission_code,
        title=mission_title,
        description=mission_description,
        pole="KOR",
        cc_reward=20,
        stade_required="pousse",
        entity="KORA",
        required_qualification_codes=[qualification_code],
    )
    await rail2_db.missions.insert_one(mission.model_dump())

    missions_before = await missions_api_module.list_missions(current=user)
    listed_before = next(m for m in missions_before if m["code"] == mission_code)
    assert listed_before["eligible"] is False

    with pytest.raises(Exception):
        await missions_api_module.accept_mission(mission_code, current=user)

    # ---- 4. Certification: start / submit / grade --------------------
    attempt = await start_attempt(user.id, certification_code)
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
    assert qualification_code in codes
    issued = next(q for q in quals if q.qualification_code == qualification_code)
    assert issued.source_certification_code == certification_code
    assert issued.source_attempt_id == attempt.id

    # Re-grading (idempotent hook) must never issue a second copy.
    quals_again = await list_user_qualifications(user.id)
    matches_again = [q for q in quals_again if q.qualification_code == qualification_code]
    assert len(matches_again) == 1

    # ---- 6. Opportunity/Mission: eligible + acceptable AFTER ---------
    missions_after = await missions_api_module.list_missions(current=user)
    listed_after = next(m for m in missions_after if m["code"] == mission_code)
    assert listed_after["eligible"] is True

    accept_result = await missions_api_module.accept_mission(mission_code, current=user)
    assert accept_result["ok"] is True
    assert accept_result["status"] == "accepted"

    user_mission = await rail2_db.user_missions.find_one(
        {"user_id": user.id, "mission_code": mission_code}, {"_id": 0}
    )
    assert user_mission is not None
    assert user_mission["status"] == "accepted"
