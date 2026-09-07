"""P0-H (Audit Chirurgical 2026-09-07) — CERT-01: certification
eligibility is a real, server-enforced gate, not just a rubric lookup.

ROOT_CAUSE this closes: `certification.service.start_attempt` checked
only that a `Rubric` existed for `certification_code` — nothing stopped
a candidate who had never opened a single module of the underlying
formation from starting (and, once graded, passing) a real
certification attempt. `submit_attempt`/`grade_attempt` never re-derive
eligibility either — they trust that an existing attempt was already
gated at creation, which is now true.

Legacy domain covered against `mongomock_motor`; the three canonical
domains (FMS/KLT/KOR) are exercised through
`certification.service.check_certification_eligibility` directly, with
each domain's own already-tested read model stubbed (same pattern as
`test_canonical_convergence.py`) — this suite is about the eligibility
gate's own logic, not re-proving each domain's read model.
"""

from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

import certification.service as certification_service_module
import fms_canonical
from fms_canonical.models import CanonicalModuleProgress
from fms_canonical.models import CanonicalFormation
from fastapi import HTTPException


@pytest.fixture
async def cert_db(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_cert_eligibility_test"]
    monkeypatch.setattr(certification_service_module, "db", mock_db)
    return mock_db


async def _seed_legacy_formation(db, code="FMS-01", module_codes=("M01", "M02")):
    await db.formations.insert_one(
        {
            "code": code,
            "name": "Formation Test",
            "pole": "FMS",
            "modules": [{"code": m, "name": m} for m in module_codes],
        }
    )


async def _validate_module(db, user_id, module_code):
    await db.progress.update_one(
        {"user_id": user_id, "module_code": module_code},
        {
            "$set": {
                "user_id": user_id,
                "module_code": module_code,
                "quiz_passed": True,
                "mini_mission_committed_at": "2026-09-01T00:00:00+00:00",
            }
        },
        upsert=True,
    )


# --------------------------------------------------------------------
# Legacy domain
# --------------------------------------------------------------------


@pytest.mark.asyncio
async def test_legacy_eligible_when_every_module_validated(cert_db):
    await _seed_legacy_formation(cert_db, module_codes=("M01", "M02"))
    await _validate_module(cert_db, "user-1", "M01")
    await _validate_module(cert_db, "user-1", "M02")

    eligible, reason = await certification_service_module.check_certification_eligibility(
        "user-1", "FMS-01"
    )
    assert eligible is True
    assert reason == ""


@pytest.mark.asyncio
async def test_legacy_ineligible_when_a_module_is_not_validated(cert_db):
    await _seed_legacy_formation(cert_db, module_codes=("M01", "M02"))
    await _validate_module(cert_db, "user-1", "M01")
    # M02 never touched at all.

    eligible, reason = await certification_service_module.check_certification_eligibility(
        "user-1", "FMS-01"
    )
    assert eligible is False
    assert "M02" in reason


@pytest.mark.asyncio
async def test_legacy_ineligible_when_formation_has_no_modules(cert_db):
    await _seed_legacy_formation(cert_db, module_codes=())

    eligible, reason = await certification_service_module.check_certification_eligibility(
        "user-1", "FMS-01"
    )
    assert eligible is False


@pytest.mark.asyncio
async def test_start_attempt_403s_a_candidate_who_never_opened_a_module(cert_db):
    await _seed_legacy_formation(cert_db, module_codes=("M01",))
    await cert_db.certification_rubrics.insert_one(
        {
            "certification_code": "FMS01-N1",
            "level": "N1",
            "formation_code": "FMS-01",
            "version": "1.0",
            "pass_threshold_pct": 80.0,
            "criteria": [],
            "cap_rules": [],
            "mention_thresholds": [],
            "created_at": "2026-09-01T00:00:00+00:00",
        }
    )

    with pytest.raises(HTTPException) as exc:
        await certification_service_module.start_attempt("user-1", "FMS01-N1")
    assert exc.value.status_code == 403

    # And no attempt was ever written — the gate runs before insertion.
    count = await cert_db.certification_attempts.count_documents({})
    assert count == 0


@pytest.mark.asyncio
async def test_start_attempt_succeeds_once_the_candidate_is_eligible(cert_db):
    await _seed_legacy_formation(cert_db, module_codes=("M01",))
    await _validate_module(cert_db, "user-1", "M01")
    await cert_db.certification_rubrics.insert_one(
        {
            "certification_code": "FMS01-N1",
            "level": "N1",
            "formation_code": "FMS-01",
            "version": "1.0",
            "pass_threshold_pct": 80.0,
            "criteria": [],
            "cap_rules": [],
            "mention_thresholds": [],
            "created_at": "2026-09-01T00:00:00+00:00",
        }
    )

    attempt = await certification_service_module.start_attempt("user-1", "FMS01-N1")
    assert attempt.status == "in_progress"


@pytest.mark.asyncio
async def test_unrecognized_formation_code_is_rejected_not_silently_allowed(
    cert_db, monkeypatch
):
    """A rubric's formation_code that matches neither a legacy nor a
    canonical formation must never be treated as automatically
    eligible — that would defeat the whole gate for any admin data
    error or typo."""

    async def none_fms(*_a, **_kw):
        return None

    async def none_progress(*_a, **_kw):
        return []

    monkeypatch.setattr(fms_canonical, "get_canonical_formation", none_fms)
    monkeypatch.setattr(fms_canonical, "get_user_canonical_progress", none_progress)

    eligible, reason = await certification_service_module.check_certification_eligibility(
        "user-1", "NO-SUCH-FORMATION"
    )
    assert eligible is False
    assert "introuvable" in reason


# --------------------------------------------------------------------
# Canonical domain (FMS side stubbed — same rationale as
# test_canonical_convergence.py: the read models are already tested)
# --------------------------------------------------------------------


@pytest.mark.asyncio
async def test_canonical_eligible_once_every_module_content_viewed(cert_db, monkeypatch):
    async def formation(*_a, **_kw):
        return CanonicalFormation(
            canonical_formation_code="FMS-01",
            metier_number="01",
            metier_name="Métier Un",
            module_codes_in_order=["FMS01-M01", "FMS01-M02"],
            module_count=2,
        )

    async def progress(user_id, **_kw):
        return [
            CanonicalModuleProgress(
                user_id=user_id,
                canonical_formation_code="FMS-01",
                canonical_module_code="FMS01-M01",
                content_viewed_at="2026-09-01T00:00:00+00:00",
            ),
            CanonicalModuleProgress(
                user_id=user_id,
                canonical_formation_code="FMS-01",
                canonical_module_code="FMS01-M02",
                content_viewed_at="2026-09-01T00:00:00+00:00",
            ),
        ]

    monkeypatch.setattr(fms_canonical, "get_canonical_formation", formation)
    monkeypatch.setattr(fms_canonical, "get_user_canonical_progress", progress)

    eligible, reason = await certification_service_module.check_certification_eligibility(
        "user-1", "FMS-01"
    )
    assert eligible is True


@pytest.mark.asyncio
async def test_canonical_ineligible_when_a_module_was_never_viewed(cert_db, monkeypatch):
    async def formation(*_a, **_kw):
        return CanonicalFormation(
            canonical_formation_code="FMS-01",
            metier_number="01",
            metier_name="Métier Un",
            module_codes_in_order=["FMS01-M01", "FMS01-M02"],
            module_count=2,
        )

    async def progress(user_id, **_kw):
        return [
            CanonicalModuleProgress(
                user_id=user_id,
                canonical_formation_code="FMS-01",
                canonical_module_code="FMS01-M01",
                content_viewed_at="2026-09-01T00:00:00+00:00",
            )
        ]

    monkeypatch.setattr(fms_canonical, "get_canonical_formation", formation)
    monkeypatch.setattr(fms_canonical, "get_user_canonical_progress", progress)

    eligible, reason = await certification_service_module.check_certification_eligibility(
        "user-1", "FMS-01"
    )
    assert eligible is False
    assert "FMS01-M02" in reason
