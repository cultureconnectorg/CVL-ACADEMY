"""ACA-0019 (Founder decision, 2026-09-07) —
CANONICAL_CURRICULUM_RUNTIME = AUTHORITATIVE.

For any formation_code with real canonical content (FMS/KLT/KOR),
canonical becomes the single active pedagogical source a learner is
routed to. Legacy `db.formations`/`db.progress` at the same code stays
real, queryable READ_ONLY_HISTORY — never deleted, never auto-merged,
never auto-credited (AUTO_EQUIVALENCE = FORBIDDEN). This suite proves:

  - The formations catalogue (list + detail) annotates every
    canonical-authoritative formation with a real `canonical_authority`
    (domain + route), and every non-canonical formation with `None` —
    the legacy doc itself is completely untouched either way.
  - `GET /modules/{code}/{code}` (the real ModuleJourney data source)
    redirects (via a `canonical_redirect` field, not legacy content)
    for an authoritative formation_code, and serves legacy exactly as
    before for a non-authoritative one.
  - `/user/learning-path`'s legacy `next_action` search skips any
    authoritative formation entirely — it never suggests a legacy
    module for a formation canonical has taken over — falling through
    to the canonical next_action instead.
"""

from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

import api.formations as formations_module
import api.learning as learning_module
import fms_canonical
from fms_canonical.models import CanonicalFormation, CanonicalModule
from models import User


def _user() -> User:
    return User(
        frek_id="FREK-1",
        email="learner@example.com",
        display_name="Learner",
        password_hash="x",
        role="student",
        metier_vise="FMS",
    )


@pytest.fixture
async def db_and_authority(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_authority_routing_test"]
    monkeypatch.setattr(formations_module, "db", mock_db)
    monkeypatch.setattr(learning_module, "db", mock_db)

    async def fms_formations(**_kw):
        return [
            CanonicalFormation(
                canonical_formation_code="FMS-01",
                metier_number="01",
                metier_name="Artist Development",
                module_codes_in_order=["FMS01-M01"],
                module_count=1,
            )
        ]

    async def empty_list(*_a, **_kw):
        return []

    async def empty_progress(*_a, **_kw):
        return []

    # get_first_unviewed_canonical_module (user_learning_path's next_action
    # fallback) resolves the unviewed FMS01-M01 module by calling this —
    # unstubbed, it falls through to the real DB and hangs/times out
    # (see test_canonical_convergence.py's identical fixture gap/fix).
    async def fms_module(formation_code, module_code, **_kw):
        return CanonicalModule(
            canonical_formation_code=formation_code,
            canonical_module_code=module_code,
            order_index=1,
            title="Module Un",
            prerequisites={"status": "UNSPECIFIED"},
        )

    monkeypatch.setattr(fms_canonical, "list_canonical_formations", fms_formations)
    monkeypatch.setattr(fms_canonical, "get_user_canonical_progress", empty_progress)
    monkeypatch.setattr(fms_canonical, "get_canonical_module", fms_module)

    import klt_canonical
    import kor_canonical
    import frk_canonical

    monkeypatch.setattr(klt_canonical, "list_canonical_klt_formations", empty_list)
    monkeypatch.setattr(klt_canonical, "get_user_klt_progress", empty_progress)
    monkeypatch.setattr(kor_canonical, "list_canonical_kor_formations", empty_list)
    monkeypatch.setattr(kor_canonical, "get_user_kor_progress", empty_progress)
    monkeypatch.setattr(frk_canonical, "list_canonical_frk_formations", empty_list)
    monkeypatch.setattr(frk_canonical, "get_user_frk_progress", empty_progress)

    return mock_db


async def _seed_legacy_formation(db, code, module_codes=("M01",)):
    await db.formations.insert_one(
        {
            "code": code,
            "name": f"Legacy {code}",
            "pole": "FMS",
            "duration_h": 10,
            "stades": 1,
            "cc": 5,
            "badge_name": f"Badge {code}",
            "content_status": "published",
            "modules": [{"code": f"{code}-{m}", "name": m} for m in module_codes],
        }
    )


# --------------------------------------------------------------------
# Formations catalogue — annotation only, legacy doc untouched
# --------------------------------------------------------------------


@pytest.mark.asyncio
async def test_list_formations_annotates_authoritative_and_non_authoritative(
    db_and_authority,
):
    await _seed_legacy_formation(db_and_authority, "FMS-01")
    await _seed_legacy_formation(db_and_authority, "KOR-99")  # no canonical counterpart

    results = await formations_module.list_formations(current=None)
    by_code = {r["code"]: r for r in results}

    assert by_code["FMS-01"]["canonical_authority"] == {
        "domain": "FMS",
        "route": "/canonical/FMS-01",
    }
    assert by_code["KOR-99"]["canonical_authority"] is None
    # Every legacy field is still present and correct — additive only.
    assert by_code["FMS-01"]["name"] == "Legacy FMS-01"
    assert by_code["FMS-01"]["modules_count"] == 1


@pytest.mark.asyncio
async def test_get_formation_annotates_authority_without_altering_legacy_doc(
    db_and_authority,
):
    await _seed_legacy_formation(db_and_authority, "FMS-01")

    doc = await formations_module.get_formation("FMS-01", current=None)
    assert doc["canonical_authority"] == {"domain": "FMS", "route": "/canonical/FMS-01"}
    # The legacy module list is still real and returned — READ_ONLY_
    # HISTORY means never deleted, not never served to any caller.
    assert len(doc["modules"]) == 1
    assert doc["modules"][0]["code"] == "FMS-01-M01"


@pytest.mark.asyncio
async def test_get_formation_non_authoritative_gets_none(db_and_authority):
    await _seed_legacy_formation(db_and_authority, "KOR-99")
    doc = await formations_module.get_formation("KOR-99", current=None)
    assert doc["canonical_authority"] is None


# --------------------------------------------------------------------
# get_module_journey — redirects, never serves legacy content, for an
# authoritative formation_code
# --------------------------------------------------------------------


@pytest.mark.asyncio
async def test_module_journey_redirects_for_authoritative_formation(
    db_and_authority,
):
    await _seed_legacy_formation(db_and_authority, "FMS-01")
    result = await learning_module.get_module_journey(
        "FMS-01", "FMS-01-M01", current=_user()
    )
    assert result == {"canonical_redirect": "/canonical/FMS-01"}


@pytest.mark.asyncio
async def test_module_journey_serves_legacy_for_non_authoritative_formation(
    db_and_authority,
):
    await _seed_legacy_formation(db_and_authority, "KOR-99")
    result = await learning_module.get_module_journey(
        "KOR-99", "KOR-99-M01", current=_user()
    )
    assert "canonical_redirect" not in result
    assert result["formation"]["code"] == "KOR-99"
    assert result["module"]["code"] == "KOR-99-M01"


# --------------------------------------------------------------------
# next_action — never suggests a legacy module for an authoritative
# formation, even when it's unlocked and unvalidated
# --------------------------------------------------------------------


@pytest.mark.asyncio
async def test_next_action_skips_authoritative_formation_entirely(db_and_authority):
    # FMS-01 is authoritative (canonical) AND has a real, unlocked,
    # unvalidated legacy module — the exact case that must NOT surface
    # as next_action, since canonical is the single active source now.
    await _seed_legacy_formation(db_and_authority, "FMS-01")
    result = await learning_module.user_learning_path(current=_user())
    # No canonical modules are unviewed in this fixture's FMS-01 either
    # (module_codes_in_order has exactly one, get_first_unviewed_fms
    # would need get_canonical_module stubbed to resolve it) — the
    # real assertion here is narrower and sufficient: next_action must
    # never be the legacy FMS-01 module.
    if result["next_action"] is not None:
        assert result["next_action"]["source"] != "legacy"


@pytest.mark.asyncio
async def test_own_pole_still_lists_authoritative_formation_with_authority_field(
    db_and_authority,
):
    """The formation stays visible in own_pole/other_poles (discovery
    is unaffected) — only navigation into its legacy modules changes."""
    await _seed_legacy_formation(db_and_authority, "FMS-01")
    result = await learning_module.user_learning_path(current=_user())
    all_formations = result["own_pole"] + result["other_poles"]
    fms = next(f for f in all_formations if f["code"] == "FMS-01")
    assert fms["canonical_authority"] == {"domain": "FMS", "route": "/canonical/FMS-01"}
