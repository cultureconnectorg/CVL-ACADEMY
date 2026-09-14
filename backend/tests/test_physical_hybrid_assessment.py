"""PHYSICAL/HYBRID assessment architecture (Founder decision, 2026-09-07).

Do not invent a second certification or grading engine — reuse the
existing certification/competency/rubric infrastructure, but do not
confuse delivery evidence with certification:

  ATTENDANCE != ASSESSMENT
  ATTENDANCE != SKILL_VALIDATION
  ATTENDANCE != CERTIFICATION
  PHYSICAL_ASSESSMENT_REQUIRED_WHERE_SOURCE_REQUIRES_IT = TRUE
  PHYSICAL_EVIDENCE_MUST_BE_SERVER_RECORDED = TRUE
  HYBRID_DOUBLE_CREDIT = FORBIDDEN
  AUTO_SKILL_AWARD = FORBIDDEN
  AUTO_CERTIFICATION = FORBIDDEN
  EXISTING_RUBRIC_ENGINE = REUSE_WHERE_SEMANTICALLY_COMPATIBLE
  NEW_PARALLEL_RUBRIC_SYSTEM = FORBIDDEN

This suite proves the full learner journey (formation -> delivery mode
-> real session -> enrollment -> attendance -> practical assessment
when required -> evidence -> competency result -> certification
eligibility), the composed HYBRID no-double-credit state machine in
`certification.service.check_full_eligibility`, and the explicit,
differentiated RBAC on the trainer/staff side (`api/physical_sessions.py`,
`api/certification.py`) — a jury/corrector/admin/trainer do NOT all
receive identical permissions.
"""

from __future__ import annotations

import pytest
from fastapi import HTTPException
from mongomock_motor import AsyncMongoMockClient

import api.certification as certification_api_module
import api.physical_sessions as physical_sessions_api_module
import certification.service as certification_service_module
import fms_canonical
import klt_canonical
import kor_canonical
import physical_delivery
import qualification.service as qualification_service_module
import services.events as events_module
import services.frek_core as frek_core_module
import skills.progression as skills_progression_module
import wallet.service as wallet_service_module
from certification.models import (
    GradeInput,
    PhysicalAssessmentRequirementInput,
    RubricInput,
    RubricCriterion,
)
from models import User
from physical_delivery import Location, TrainingSession, create_location, create_session
from skills.progression import get_user_progress, register_skill


@pytest.fixture
async def phys_db(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_phys_hybrid_test"]
    for module in (
        certification_service_module,
        physical_delivery,
        skills_progression_module,
        wallet_service_module,
        frek_core_module,
        events_module,
        qualification_service_module,
    ):
        monkeypatch.setattr(module, "db", mock_db)

    # `check_full_eligibility`'s digital-content-existence check walks
    # all three canonical domains — default: no canonical content
    # anywhere in this suite (every module holds its own `db`
    # reference; these three functions are stubbed directly rather than
    # patching each package's real `db`, matching the established
    # pattern in test_certification_eligibility.py).
    async def none_formation(*_a, **_kw):
        return None

    async def empty_list(*_a, **_kw):
        return []

    monkeypatch.setattr(fms_canonical, "get_canonical_formation", none_formation)
    monkeypatch.setattr(klt_canonical, "get_canonical_klt_formation", none_formation)
    monkeypatch.setattr(kor_canonical, "get_canonical_kor_formation", none_formation)
    monkeypatch.setattr(fms_canonical, "list_canonical_formations", empty_list)
    monkeypatch.setattr(klt_canonical, "list_canonical_klt_formations", empty_list)
    monkeypatch.setattr(kor_canonical, "list_canonical_kor_formations", empty_list)
    return mock_db


def _user(uid: str, role: str = "student") -> User:
    return User(
        id=uid,
        frek_id=f"FREK-{uid}",
        email=f"{uid}@example.com",
        display_name=uid,
        password_hash="x",
        role=role,
    )


async def _seed_location_and_session(
    db, formation_code: str, trainer_user_id: str = "trainer-1"
) -> TrainingSession:
    loc = await create_location(
        Location(
            name="Centre Test",
            address="1 rue Test",
            city="Fort-de-France",
            territoire="martinique",
            capacity=20,
        )
    )
    return await create_session(
        TrainingSession(
            formation_code=formation_code,
            location_id=loc.id,
            starts_at="2020-01-01T09:00:00+00:00",  # past — irrelevant here
            ends_at="2020-01-01T17:00:00+00:00",
            capacity=10,
            trainer_user_id=trainer_user_id,
            created_by="admin-1",
        )
    )


async def _create_rubric(kind: str, code: str, formation_code: str, skill_id: str):
    inp = RubricInput(
        level="N1",
        formation_code=formation_code,
        pass_threshold_pct=80.0,
        criteria=[
            RubricCriterion(
                id="C1", label="Critère unique", bloc="B1", skill_id=skill_id,
                weight=1.0, max_score=10.0,
            )
        ],
        assessment_kind=kind,
    )
    from certification.models import Rubric

    rubric = Rubric(certification_code=code, **inp.model_dump())
    # The patched mock db (see `phys_db` fixture) — never the real,
    # unpatched `db` module singleton every module re-imports its own
    # reference of.
    await certification_service_module.db.certification_rubrics.insert_one(
        rubric.model_dump()
    )
    return rubric


# --------------------------------------------------------------------
# Physical enrollment + capacity race — already covered end-to-end by
# tests/test_physical_sessions.py (test_enroll_fills_capacity_then_
# waitlists, test_enrolled_count_never_exceeds_capacity_under_repeated_
# claims); not re-proven here to avoid duplicating that suite.
# --------------------------------------------------------------------


# --------------------------------------------------------------------
# Attendance authorization (RBAC — api/physical_sessions.py)
# --------------------------------------------------------------------


@pytest.mark.asyncio
async def test_admin_tier_may_mark_attendance_on_any_session(phys_db):
    session = await _seed_location_and_session(phys_db, "PHYS-01", trainer_user_id="trainer-1")
    await physical_sessions_api_module._assert_session_staff(session, _user("admin-1", "admin"))
    # No exception raised == authorized.


@pytest.mark.asyncio
async def test_assigned_trainer_may_mark_attendance(phys_db):
    session = await _seed_location_and_session(phys_db, "PHYS-01", trainer_user_id="trainer-1")
    await physical_sessions_api_module._assert_session_staff(
        session, _user("trainer-1", "trainer")
    )


@pytest.mark.asyncio
async def test_unassigned_trainer_cannot_mark_attendance(phys_db):
    session = await _seed_location_and_session(phys_db, "PHYS-01", trainer_user_id="trainer-1")
    with pytest.raises(HTTPException) as exc:
        await physical_sessions_api_module._assert_session_staff(
            session, _user("trainer-2", "trainer")
        )
    assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_jury_and_corrector_cannot_mark_attendance(phys_db):
    """RBAC must be explicit: jury/corrector do not automatically
    inherit trainer/admin's attendance-marking authority."""
    session = await _seed_location_and_session(phys_db, "PHYS-01", trainer_user_id="trainer-1")
    for role in ("jury", "corrector"):
        with pytest.raises(HTTPException) as exc:
            await physical_sessions_api_module._assert_session_staff(
                session, _user(f"{role}-1", role)
            )
        assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_student_cannot_mark_attendance(phys_db):
    session = await _seed_location_and_session(phys_db, "PHYS-01", trainer_user_id="trainer-1")
    with pytest.raises(HTTPException):
        await physical_sessions_api_module._assert_session_staff(
            session, _user("student-1", "student")
        )


# --------------------------------------------------------------------
# Absent learner cannot satisfy attendance prerequisite; attendance
# alone cannot validate competency; practical assessment required
# where configured.
# --------------------------------------------------------------------


@pytest.mark.asyncio
async def test_absent_learner_cannot_start_practical_attempt(phys_db):
    session = await _seed_location_and_session(phys_db, "PHYS-01")
    await register_skill("PHYS01-A1", "PHYS", "N1", "B1", "Compétence Un")
    await _create_rubric("practical", "PHYS01-PRACTICAL", "PHYS-01", "PHYS01-A1")

    with pytest.raises(HTTPException) as exc:
        await certification_service_module.start_practical_attempt(
            "student-1", "PHYS01-PRACTICAL", session.id
        )
    assert exc.value.status_code == 403
    assert "résence" in exc.value.detail  # "Présence non constatée..."


@pytest.mark.asyncio
async def test_attendance_alone_never_creates_skill_evidence(phys_db):
    """ATTENDANCE != SKILL_VALIDATION: marking present, with no
    practical assessment ever graded, must leave the skill untouched."""
    session = await _seed_location_and_session(phys_db, "PHYS-01")
    await register_skill("PHYS01-A1", "PHYS", "N1", "B1", "Compétence Un")
    await physical_delivery.enroll(session.id, "student-1")
    await physical_delivery.mark_attendance(session.id, "student-1", True, "trainer-1")

    progress = await get_user_progress("student-1", metier="PHYS")
    assert progress[0].state == "not_started"
    assert progress[0].evidence_count == 0


@pytest.mark.asyncio
async def test_practical_attempt_requires_real_rubric_of_practical_kind(phys_db):
    """start_practical_attempt refuses a "certification"-kind rubric —
    a candidate cannot bypass the standard eligibility gate by simply
    calling the practical endpoint on the wrong code."""
    session = await _seed_location_and_session(phys_db, "PHYS-01")
    await register_skill("PHYS01-A1", "PHYS", "N1", "B1", "Compétence Un")
    await _create_rubric("certification", "PHYS01-FINAL", "PHYS-01", "PHYS01-A1")
    await physical_delivery.enroll(session.id, "student-1")
    await physical_delivery.mark_attendance(session.id, "student-1", True, "trainer-1")

    with pytest.raises(HTTPException) as exc:
        await certification_service_module.start_practical_attempt(
            "student-1", "PHYS01-FINAL", session.id
        )
    assert exc.value.status_code == 400


# --------------------------------------------------------------------
# Full physical-only journey: session -> enrollment -> attendance ->
# practical assessment -> evidence -> competency result ->
# certification eligibility.
# --------------------------------------------------------------------


@pytest.mark.asyncio
async def test_full_physical_only_journey_to_certification_eligibility(phys_db):
    session = await _seed_location_and_session(phys_db, "PHYS-01")
    await register_skill("PHYS01-A1", "PHYS", "N1", "B1", "Compétence Un")
    await _create_rubric("practical", "PHYS01-PRACTICAL", "PHYS-01", "PHYS01-A1")
    await _create_rubric("certification", "PHYS01-FINAL", "PHYS-01", "PHYS01-A1")
    await certification_service_module.set_physical_assessment_requirement(
        "PHYS01-FINAL",
        PhysicalAssessmentRequirementInput(
            formation_code="PHYS-01", practical_certification_code="PHYS01-PRACTICAL"
        ),
        created_by="admin-1",
    )

    # No digital content at all for PHYS-01 -> the final certification
    # is unreachable through the standard eligibility gate alone.
    eligible, _ = await certification_service_module.check_full_eligibility(
        "student-1", "PHYS01-FINAL"
    )
    assert eligible is False

    # 1. enrollment + attendance (real, server-recorded).
    await physical_delivery.enroll(session.id, "student-1")
    await physical_delivery.mark_attendance(session.id, "student-1", True, "trainer-1")

    # 2. practical assessment (reuses the exact certification engine).
    attempt = await certification_service_module.start_practical_attempt(
        "student-1", "PHYS01-PRACTICAL", session.id
    )
    assert attempt.assessment_kind == "practical"
    assert attempt.session_id == session.id
    await certification_service_module.submit_attempt(attempt.id, "student-1")
    graded = await certification_service_module.grade_attempt(
        attempt.id, "trainer-1", GradeInput(scores={"C1": 10.0})
    )
    assert graded.passed is True

    # 3. evidence — real, ownership-correct, and NOT the "certification"
    # type (do not confuse delivery evidence with certification).
    evidence = await phys_db.skill_evidence.find({"user_id": "student-1"}, {"_id": 0}).to_list(10)
    assert len(evidence) == 1
    assert evidence[0]["skill_id"] == "PHYS01-A1"
    assert evidence[0]["evidence_type"] == "physical_assessment"
    assert evidence[0]["ref"] == attempt.id

    # 4. AUTO_SKILL_AWARD = FORBIDDEN — one practical pass alone does
    # not jump the skill straight to "acquired" the way a real
    # "certification"-kind pass does.
    progress = await get_user_progress("student-1", metier="PHYS")
    assert progress[0].state == "in_progress"

    # 5. AUTO_CERTIFICATION = FORBIDDEN — a passed practical attempt
    # never itself emits FREK-CERT, credits the JCC reward, or issues a
    # qualification.
    signals = await phys_db.frek_signals.find({"user_id": "student-1"}).to_list(10)
    assert signals == []
    wallet_tx = await phys_db.wallet_transactions.find({"user_id": "student-1"}).to_list(10)
    assert wallet_tx == []

    # 6. competency result -> certification eligibility: NOW eligible.
    eligible, reason = await certification_service_module.check_full_eligibility(
        "student-1", "PHYS01-FINAL"
    )
    assert eligible is True
    assert reason == ""

    final_attempt = await certification_service_module.start_attempt(
        "student-1", "PHYS01-FINAL"
    )
    assert final_attempt.assessment_kind == "certification"


@pytest.mark.asyncio
async def test_attended_but_ungraded_practical_attempt_is_not_eligible(phys_db):
    """ATTENDANCE != ASSESSMENT != CERTIFICATION: attendance plus a
    merely-started (never graded/passed) practical attempt still must
    not satisfy the final certification's eligibility gate."""
    session = await _seed_location_and_session(phys_db, "PHYS-01")
    await register_skill("PHYS01-A1", "PHYS", "N1", "B1", "Compétence Un")
    await _create_rubric("practical", "PHYS01-PRACTICAL", "PHYS-01", "PHYS01-A1")
    await _create_rubric("certification", "PHYS01-FINAL", "PHYS-01", "PHYS01-A1")
    await certification_service_module.set_physical_assessment_requirement(
        "PHYS01-FINAL",
        PhysicalAssessmentRequirementInput(
            formation_code="PHYS-01", practical_certification_code="PHYS01-PRACTICAL"
        ),
        created_by="admin-1",
    )
    await physical_delivery.enroll(session.id, "student-1")
    await physical_delivery.mark_attendance(session.id, "student-1", True, "trainer-1")
    await certification_service_module.start_practical_attempt(
        "student-1", "PHYS01-PRACTICAL", session.id
    )
    # Never submitted/graded.

    eligible, reason = await certification_service_module.check_full_eligibility(
        "student-1", "PHYS01-FINAL"
    )
    assert eligible is False
    assert "pratique" in reason


# --------------------------------------------------------------------
# HYBRID no-double-credit — a formation with BOTH real digital content
# and a configured physical requirement.
# --------------------------------------------------------------------


@pytest.mark.asyncio
async def test_hybrid_digital_pass_alone_is_not_enough(phys_db):
    await phys_db.formations.insert_one(
        {"code": "HYB-01", "name": "Hybrid Formation", "pole": "PHYS",
         "modules": [{"code": "M01", "name": "M01"}]}
    )
    await phys_db.progress.update_one(
        {"user_id": "student-1", "module_code": "M01"},
        {
            "$set": {
                "user_id": "student-1",
                "module_code": "M01",
                "quiz_passed": True,
                "mini_mission_committed_at": "2026-09-01T00:00:00+00:00",
            }
        },
        upsert=True,
    )
    await register_skill("HYB01-A1", "PHYS", "N1", "B1", "Compétence Un")
    await _create_rubric("practical", "HYB01-PRACTICAL", "HYB-01", "HYB01-A1")
    await _create_rubric("certification", "HYB01-FINAL", "HYB-01", "HYB01-A1")
    await certification_service_module.set_physical_assessment_requirement(
        "HYB01-FINAL",
        PhysicalAssessmentRequirementInput(
            formation_code="HYB-01", practical_certification_code="HYB01-PRACTICAL"
        ),
        created_by="admin-1",
    )

    # Digital leg alone (legacy module fully validated) is real but the
    # physical leg was never even attempted — HYBRID_DOUBLE_CREDIT =
    # FORBIDDEN means this must still be ineligible.
    eligible, reason = await certification_service_module.check_full_eligibility(
        "student-1", "HYB01-FINAL"
    )
    assert eligible is False
    assert "pratique" in reason


@pytest.mark.asyncio
async def test_hybrid_physical_pass_alone_does_not_skip_real_digital_content(phys_db):
    session = await _seed_location_and_session(phys_db, "HYB-01")
    await phys_db.formations.insert_one(
        {"code": "HYB-01", "name": "Hybrid Formation", "pole": "PHYS",
         "modules": [{"code": "M01", "name": "M01"}]}
    )
    # Module M01 never validated.
    await register_skill("HYB01-A1", "PHYS", "N1", "B1", "Compétence Un")
    await _create_rubric("practical", "HYB01-PRACTICAL", "HYB-01", "HYB01-A1")
    await _create_rubric("certification", "HYB01-FINAL", "HYB-01", "HYB01-A1")
    await certification_service_module.set_physical_assessment_requirement(
        "HYB01-FINAL",
        PhysicalAssessmentRequirementInput(
            formation_code="HYB-01", practical_certification_code="HYB01-PRACTICAL"
        ),
        created_by="admin-1",
    )
    await physical_delivery.enroll(session.id, "student-1")
    await physical_delivery.mark_attendance(session.id, "student-1", True, "trainer-1")
    attempt = await certification_service_module.start_practical_attempt(
        "student-1", "HYB01-PRACTICAL", session.id
    )
    await certification_service_module.submit_attempt(attempt.id, "student-1")
    await certification_service_module.grade_attempt(
        attempt.id, "trainer-1", GradeInput(scores={"C1": 10.0})
    )

    # Real digital content exists (the formation has a real, unfinished
    # module) — the practical pass must never cover for it.
    eligible, reason = await certification_service_module.check_full_eligibility(
        "student-1", "HYB01-FINAL"
    )
    assert eligible is False
    assert "M01" in reason


@pytest.mark.asyncio
async def test_hybrid_both_legs_passed_is_eligible(phys_db):
    session = await _seed_location_and_session(phys_db, "HYB-01")
    await phys_db.formations.insert_one(
        {"code": "HYB-01", "name": "Hybrid Formation", "pole": "PHYS",
         "modules": [{"code": "M01", "name": "M01"}]}
    )
    await phys_db.progress.update_one(
        {"user_id": "student-1", "module_code": "M01"},
        {
            "$set": {
                "user_id": "student-1",
                "module_code": "M01",
                "quiz_passed": True,
                "mini_mission_committed_at": "2026-09-01T00:00:00+00:00",
            }
        },
        upsert=True,
    )
    await register_skill("HYB01-A1", "PHYS", "N1", "B1", "Compétence Un")
    await _create_rubric("practical", "HYB01-PRACTICAL", "HYB-01", "HYB01-A1")
    await _create_rubric("certification", "HYB01-FINAL", "HYB-01", "HYB01-A1")
    await certification_service_module.set_physical_assessment_requirement(
        "HYB01-FINAL",
        PhysicalAssessmentRequirementInput(
            formation_code="HYB-01", practical_certification_code="HYB01-PRACTICAL"
        ),
        created_by="admin-1",
    )
    await physical_delivery.enroll(session.id, "student-1")
    await physical_delivery.mark_attendance(session.id, "student-1", True, "trainer-1")
    attempt = await certification_service_module.start_practical_attempt(
        "student-1", "HYB01-PRACTICAL", session.id
    )
    await certification_service_module.submit_attempt(attempt.id, "student-1")
    await certification_service_module.grade_attempt(
        attempt.id, "trainer-1", GradeInput(scores={"C1": 10.0})
    )

    eligible, reason = await certification_service_module.check_full_eligibility(
        "student-1", "HYB01-FINAL"
    )
    assert eligible is True
    assert reason == ""


# --------------------------------------------------------------------
# Grading RBAC (api/certification.py) — explicit, differentiated.
# --------------------------------------------------------------------


@pytest.mark.asyncio
async def test_jury_may_grade_any_practical_attempt(phys_db):
    from certification.models import CertificationAttempt

    attempt = CertificationAttempt(
        user_id="student-1", certification_code="X-PRACTICAL",
        formation_code="PHYS-01", level="N1", rubric_version="1.0",
        assessment_kind="practical", session_id="session-x",
    )
    assert await certification_api_module._can_grade(attempt, _user("jury-1", "jury")) is True


@pytest.mark.asyncio
async def test_assigned_trainer_may_grade_own_practical_attempt(phys_db):
    from certification.models import CertificationAttempt

    session = await _seed_location_and_session(phys_db, "PHYS-01", trainer_user_id="trainer-1")
    attempt = CertificationAttempt(
        user_id="student-1", certification_code="X-PRACTICAL",
        formation_code="PHYS-01", level="N1", rubric_version="1.0",
        assessment_kind="practical", session_id=session.id,
    )
    assert (
        await certification_api_module._can_grade(attempt, _user("trainer-1", "trainer"))
        is True
    )


@pytest.mark.asyncio
async def test_unassigned_trainer_may_not_grade_practical_attempt(phys_db):
    from certification.models import CertificationAttempt

    session = await _seed_location_and_session(phys_db, "PHYS-01", trainer_user_id="trainer-1")
    attempt = CertificationAttempt(
        user_id="student-1", certification_code="X-PRACTICAL",
        formation_code="PHYS-01", level="N1", rubric_version="1.0",
        assessment_kind="practical", session_id=session.id,
    )
    assert (
        await certification_api_module._can_grade(attempt, _user("trainer-2", "trainer"))
        is False
    )


@pytest.mark.asyncio
async def test_trainer_may_not_grade_a_certification_kind_attempt(phys_db):
    """A trainer's authority is scoped to "practical" attempts at their
    own assigned session — never a final "certification"-kind attempt,
    which stays JURY_ROLES-only exactly as before this architecture."""
    from certification.models import CertificationAttempt

    attempt = CertificationAttempt(
        user_id="student-1", certification_code="X-FINAL",
        formation_code="PHYS-01", level="N1", rubric_version="1.0",
        assessment_kind="certification",
    )
    assert (
        await certification_api_module._can_grade(attempt, _user("trainer-1", "trainer"))
        is False
    )


# --------------------------------------------------------------------
# PHYSICAL_EVIDENCE_MUST_BE_SERVER_RECORDED = TRUE / no fabricated data
# --------------------------------------------------------------------


@pytest.mark.asyncio
async def test_set_physical_assessment_requirement_rejects_non_practical_rubric(phys_db):
    """Never lets a requirement point at a rubric that isn't actually
    assessment_kind == "practical" — the gate would otherwise silently
    accept a "certification"-kind rubric as if it were a real practical
    pass, fabricating the composition."""
    await register_skill("PHYS01-A1", "PHYS", "N1", "B1", "Compétence Un")
    await _create_rubric("certification", "PHYS01-FINAL", "PHYS-01", "PHYS01-A1")
    await _create_rubric("certification", "PHYS01-NOT-PRACTICAL", "PHYS-01", "PHYS01-A1")

    with pytest.raises(HTTPException) as exc:
        await certification_service_module.set_physical_assessment_requirement(
            "PHYS01-FINAL",
            PhysicalAssessmentRequirementInput(
                formation_code="PHYS-01",
                practical_certification_code="PHYS01-NOT-PRACTICAL",
            ),
            created_by="admin-1",
        )
    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_no_requirement_configured_is_byte_identical_to_standard_gate(phys_db):
    """No PhysicalAssessmentRequirement at all -> `check_full_
    eligibility` degrades to the exact standard `check_certification_
    eligibility` result — every rubric that predates this architecture
    is completely unaffected."""
    await phys_db.formations.insert_one(
        {"code": "LEGACY-01", "name": "Legacy", "pole": "FMS", "modules": []}
    )
    await register_skill("LEG01-A1", "FMS", "N1", "B1", "Compétence Un")
    await _create_rubric("certification", "LEG01-FINAL", "LEGACY-01", "LEG01-A1")

    standard = await certification_service_module.check_certification_eligibility(
        "student-1", "LEGACY-01"
    )
    full = await certification_service_module.check_full_eligibility(
        "student-1", "LEG01-FINAL"
    )
    assert standard == full
