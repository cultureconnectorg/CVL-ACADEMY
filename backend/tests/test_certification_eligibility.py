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
import klt_canonical
import kor_canonical
from fms_canonical.models import CanonicalModuleProgress
from fms_canonical.models import CanonicalFormation
from fastapi import HTTPException


@pytest.fixture
async def cert_db(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_cert_eligibility_test"]
    monkeypatch.setattr(certification_service_module, "db", mock_db)

    # ACA-0019 — `check_certification_eligibility` now calls
    # `get_canonical_authority` unconditionally first, which walks all
    # three canonical domains' `list_canonical_*` functions. Every
    # module holds its own `db` reference (see test_canonical_
    # convergence.py's identical fixture note) — unstubbed, these hit a
    # real, absent MongoDB and time out. Default: no canonical content
    # anywhere, i.e. every formation_code in this file is legacy-only
    # unless a test explicitly overrides one of these three.
    async def no_formations(*_a, **_kw):
        return []

    monkeypatch.setattr(fms_canonical, "list_canonical_formations", no_formations)
    monkeypatch.setattr(klt_canonical, "list_canonical_klt_formations", no_formations)
    monkeypatch.setattr(kor_canonical, "list_canonical_kor_formations", no_formations)
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


def _fms01_formation():
    return CanonicalFormation(
        canonical_formation_code="FMS-01",
        metier_number="01",
        metier_name="Métier Un",
        module_codes_in_order=["FMS01-M01", "FMS01-M02"],
        module_count=2,
    )


def _stub_fms01_authority(monkeypatch):
    """`get_canonical_authority`'s own read (`list_canonical_formations`)
    is a *different* function from `get_canonical_formation` (the
    single-formation getter `_check_canonical_eligibility` uses) —
    both must agree FMS-01 is real canonical content, or the new
    authority-first branch in `check_certification_eligibility` won't
    even reach the eligibility check these tests are about."""

    async def formations(*_a, **_kw):
        return [_fms01_formation()]

    monkeypatch.setattr(fms_canonical, "list_canonical_formations", formations)


@pytest.mark.asyncio
async def test_canonical_eligible_once_every_module_content_viewed(cert_db, monkeypatch):
    async def formation(*_a, **_kw):
        return _fms01_formation()

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

    _stub_fms01_authority(monkeypatch)
    monkeypatch.setattr(fms_canonical, "get_canonical_formation", formation)
    monkeypatch.setattr(fms_canonical, "get_user_canonical_progress", progress)

    eligible, reason = await certification_service_module.check_certification_eligibility(
        "user-1", "FMS-01"
    )
    assert eligible is True


@pytest.mark.asyncio
async def test_canonical_ineligible_when_a_module_was_never_viewed(cert_db, monkeypatch):
    async def formation(*_a, **_kw):
        return _fms01_formation()

    async def progress(user_id, **_kw):
        return [
            CanonicalModuleProgress(
                user_id=user_id,
                canonical_formation_code="FMS-01",
                canonical_module_code="FMS01-M01",
                content_viewed_at="2026-09-01T00:00:00+00:00",
            )
        ]

    _stub_fms01_authority(monkeypatch)
    monkeypatch.setattr(fms_canonical, "get_canonical_formation", formation)
    monkeypatch.setattr(fms_canonical, "get_user_canonical_progress", progress)

    eligible, reason = await certification_service_module.check_certification_eligibility(
        "user-1", "FMS-01"
    )
    assert eligible is False
    assert "FMS01-M02" in reason


# --------------------------------------------------------------------
# ACA-0019 — a formation_code with BOTH a legacy db.formations doc
# (READ_ONLY_HISTORY) AND real canonical content (the exact FMS-01
# shape this whole convergence effort is about). Canonical must be the
# only path consulted — this is the regression the routing-authority
# change itself introduced (`get_module_journey` stops routing a
# learner to the legacy quiz/mini-mission, so requiring it here would
# make certification permanently unreachable for them).
# --------------------------------------------------------------------


@pytest.mark.asyncio
async def test_authoritative_formation_ignores_legacy_and_uses_canonical_only(
    cert_db, monkeypatch
):
    # Legacy doc exists (never deleted — READ_ONLY_HISTORY) but its
    # module was never touched: a legacy-only gate would reject this.
    await _seed_legacy_formation(cert_db, module_codes=("M01",))

    async def formation(*_a, **_kw):
        return _fms01_formation()

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

    _stub_fms01_authority(monkeypatch)
    monkeypatch.setattr(fms_canonical, "get_canonical_formation", formation)
    monkeypatch.setattr(fms_canonical, "get_user_canonical_progress", progress)

    eligible, reason = await certification_service_module.check_certification_eligibility(
        "user-1", "FMS-01"
    )
    assert eligible is True
    assert reason == ""


@pytest.mark.asyncio
async def test_authoritative_formation_never_credits_stale_legacy_progress(
    cert_db, monkeypatch
):
    """AUTO_EQUIVALENCE = FORBIDDEN, at the certification gate too: a
    learner who fully validated the legacy modules (e.g. before this
    formation became canonical-authoritative) but never touched the
    canonical content must NOT be treated as eligible — legacy
    completion is never auto-credited toward the canonical gate."""
    await _seed_legacy_formation(cert_db, module_codes=("M01",))
    await _validate_module(cert_db, "user-1", "M01")

    async def formation(*_a, **_kw):
        return _fms01_formation()

    async def progress(user_id, **_kw):
        return []  # canonical content never viewed at all

    _stub_fms01_authority(monkeypatch)
    monkeypatch.setattr(fms_canonical, "get_canonical_formation", formation)
    monkeypatch.setattr(fms_canonical, "get_user_canonical_progress", progress)

    eligible, reason = await certification_service_module.check_certification_eligibility(
        "user-1", "FMS-01"
    )
    assert eligible is False
    assert "canonique" in reason
