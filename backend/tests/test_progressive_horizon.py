"""ACA-0027 — Progressive Horizon composition tests.

`compute_progressive_horizon` is tested in isolation from `certification.
service.check_full_eligibility`'s own internal eligibility logic (that
function already has its own extensive test coverage — CERT-01 et al.);
here it is monkeypatched to a stub so these tests exercise only this
module's own real logic: which items appear, in what order, and when a
certification opportunity is correctly suppressed."""

from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

import services.progressive_horizon as horizon_module
from services.progressive_horizon import compute_progressive_horizon

USER_ID = "u1"


@pytest.fixture
async def horizon_db(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_aca0027_horizon_test"]
    monkeypatch.setattr(horizon_module, "db", mock_db)
    return mock_db


def _formation(code, *, progress_pct=0, is_unlocked=True, name=None, pole_color="#000"):
    return {
        "code": code,
        "name": name or code,
        "progress_pct": progress_pct,
        "is_unlocked": is_unlocked,
        "pole_color": pole_color,
    }


@pytest.mark.asyncio
async def test_resume_module_item_from_next_action(horizon_db):
    learning_path = {
        "own_pole": [_formation("FMS-01", progress_pct=40)],
        "other_poles": [],
        "next_action": {
            "formation_code": "FMS-01",
            "formation_name": "Podcast",
            "module_code": "FMS-01-M03",
            "module_name": "Module 3",
            "route": "/formations/FMS-01/modules/FMS-01-M03",
            "pole_color": "#f00",
        },
    }
    items = await compute_progressive_horizon(USER_ID, learning_path)
    assert len(items) == 1
    assert items[0].type == "RESUME_MODULE"
    assert items[0].module_code == "FMS-01-M03"
    assert items[0].route == "/formations/FMS-01/modules/FMS-01-M03"


@pytest.mark.asyncio
async def test_no_next_action_no_resume_item(horizon_db):
    learning_path = {"own_pole": [], "other_poles": [], "next_action": None}
    items = await compute_progressive_horizon(USER_ID, learning_path)
    assert items == []


@pytest.mark.asyncio
async def test_formation_expansion_only_when_own_pole_fully_exhausted(horizon_db):
    learning_path = {
        "own_pole": [_formation("FMS-01", progress_pct=100)],
        "other_poles": [
            _formation("KOR-01", progress_pct=0, is_unlocked=True, name="Podcast KOR"),
            _formation(
                "KOR-02", progress_pct=100, is_unlocked=True
            ),  # already done, skip
            _formation("KOR-03", progress_pct=0, is_unlocked=False),  # locked, skip
        ],
        "next_action": None,
    }
    items = await compute_progressive_horizon(USER_ID, learning_path)
    expansion_items = [i for i in items if i.type == "FORMATION_EXPANSION"]
    assert len(expansion_items) == 1
    assert expansion_items[0].formation_code == "KOR-01"


@pytest.mark.asyncio
async def test_no_expansion_when_own_pole_not_fully_exhausted(horizon_db):
    learning_path = {
        "own_pole": [_formation("FMS-01", progress_pct=60)],
        "other_poles": [_formation("KOR-01", progress_pct=0, is_unlocked=True)],
        "next_action": None,
    }
    items = await compute_progressive_horizon(USER_ID, learning_path)
    assert not any(i.type == "FORMATION_EXPANSION" for i in items)


@pytest.mark.asyncio
async def test_expansion_capped_at_3_candidates(horizon_db):
    learning_path = {
        "own_pole": [_formation("FMS-01", progress_pct=100)],
        "other_poles": [
            _formation(f"KOR-0{i}", progress_pct=0, is_unlocked=True)
            for i in range(1, 6)
        ],
        "next_action": None,
    }
    items = await compute_progressive_horizon(USER_ID, learning_path)
    expansion_items = [i for i in items if i.type == "FORMATION_EXPANSION"]
    assert len(expansion_items) == 3


@pytest.mark.asyncio
async def test_certification_eligible_item_appears_when_eligible(
    horizon_db, monkeypatch
):
    await horizon_db.certification_rubrics.insert_one(
        {"certification_code": "FMS01-A01", "formation_code": "FMS-01"}
    )

    async def fake_eligible(user_id, cert_code):
        return True, ""

    monkeypatch.setattr(horizon_module, "check_full_eligibility", fake_eligible)

    learning_path = {
        "own_pole": [_formation("FMS-01", progress_pct=100)],
        "other_poles": [],
        "next_action": None,
    }
    items = await compute_progressive_horizon(USER_ID, learning_path)
    cert_items = [i for i in items if i.type == "CERTIFICATION_ELIGIBLE"]
    assert len(cert_items) == 1
    assert cert_items[0].certification_code == "FMS01-A01"
    assert cert_items[0].formation_code == "FMS-01"


@pytest.mark.asyncio
async def test_no_certification_item_when_not_eligible(horizon_db, monkeypatch):
    await horizon_db.certification_rubrics.insert_one(
        {"certification_code": "FMS01-A01", "formation_code": "FMS-01"}
    )

    async def fake_not_eligible(user_id, cert_code):
        return False, "not yet"

    monkeypatch.setattr(horizon_module, "check_full_eligibility", fake_not_eligible)

    learning_path = {
        "own_pole": [_formation("FMS-01", progress_pct=100)],
        "other_poles": [],
        "next_action": None,
    }
    items = await compute_progressive_horizon(USER_ID, learning_path)
    assert not any(i.type == "CERTIFICATION_ELIGIBLE" for i in items)


@pytest.mark.asyncio
async def test_no_certification_item_when_no_rubric_exists(horizon_db, monkeypatch):
    called = False

    async def fake_eligible(user_id, cert_code):
        nonlocal called
        called = True
        return True, ""

    monkeypatch.setattr(horizon_module, "check_full_eligibility", fake_eligible)

    learning_path = {
        "own_pole": [_formation("FMS-99", progress_pct=100)],  # no rubric for this
        "other_poles": [],
        "next_action": None,
    }
    items = await compute_progressive_horizon(USER_ID, learning_path)
    assert not any(i.type == "CERTIFICATION_ELIGIBLE" for i in items)
    assert called is False  # never even attempted eligibility with no rubric


@pytest.mark.asyncio
async def test_no_certification_item_when_incomplete(horizon_db, monkeypatch):
    called = False

    async def fake_eligible(user_id, cert_code):
        nonlocal called
        called = True
        return True, ""

    monkeypatch.setattr(horizon_module, "check_full_eligibility", fake_eligible)
    await horizon_db.certification_rubrics.insert_one(
        {"certification_code": "FMS01-A01", "formation_code": "FMS-01"}
    )

    learning_path = {
        "own_pole": [_formation("FMS-01", progress_pct=80)],  # not yet 100%
        "other_poles": [],
        "next_action": None,
    }
    items = await compute_progressive_horizon(USER_ID, learning_path)
    assert not any(i.type == "CERTIFICATION_ELIGIBLE" for i in items)
    assert called is False


@pytest.mark.asyncio
async def test_no_certification_item_when_already_passed(horizon_db, monkeypatch):
    called = False

    async def fake_eligible(user_id, cert_code):
        nonlocal called
        called = True
        return True, ""

    monkeypatch.setattr(horizon_module, "check_full_eligibility", fake_eligible)
    await horizon_db.certification_rubrics.insert_one(
        {"certification_code": "FMS01-A01", "formation_code": "FMS-01"}
    )
    await horizon_db.certification_attempts.insert_one(
        {
            "user_id": USER_ID,
            "certification_code": "FMS01-A01",
            "status": "passed",
            "id": "a1",
        }
    )

    learning_path = {
        "own_pole": [_formation("FMS-01", progress_pct=100)],
        "other_poles": [],
        "next_action": None,
    }
    items = await compute_progressive_horizon(USER_ID, learning_path)
    assert not any(i.type == "CERTIFICATION_ELIGIBLE" for i in items)
    assert called is False  # already passed -- never re-checked


@pytest.mark.asyncio
async def test_certification_item_reappears_after_failed_attempt(
    horizon_db, monkeypatch
):
    async def fake_eligible(user_id, cert_code):
        return True, ""

    monkeypatch.setattr(horizon_module, "check_full_eligibility", fake_eligible)
    await horizon_db.certification_rubrics.insert_one(
        {"certification_code": "FMS01-A01", "formation_code": "FMS-01"}
    )
    await horizon_db.certification_attempts.insert_one(
        {
            "user_id": USER_ID,
            "certification_code": "FMS01-A01",
            "status": "failed",
            "id": "a1",
        }
    )

    learning_path = {
        "own_pole": [_formation("FMS-01", progress_pct=100)],
        "other_poles": [],
        "next_action": None,
    }
    items = await compute_progressive_horizon(USER_ID, learning_path)
    # A real retry opportunity -- "failed" is not a reason to hide it forever.
    assert any(i.type == "CERTIFICATION_ELIGIBLE" for i in items)


@pytest.mark.asyncio
async def test_priority_order_resume_then_expansion_then_certification(
    horizon_db, monkeypatch
):
    async def fake_eligible(user_id, cert_code):
        return True, ""

    monkeypatch.setattr(horizon_module, "check_full_eligibility", fake_eligible)
    await horizon_db.certification_rubrics.insert_one(
        {"certification_code": "FMS01-A01", "formation_code": "FMS-01"}
    )

    learning_path = {
        "own_pole": [_formation("FMS-01", progress_pct=100)],
        "other_poles": [_formation("KOR-01", progress_pct=0, is_unlocked=True)],
        "next_action": {
            "formation_code": "FMS-01",
            "module_code": "M99",
            "route": "/x",
        },
    }
    items = await compute_progressive_horizon(USER_ID, learning_path)
    assert [i.type for i in items] == [
        "RESUME_MODULE",
        "FORMATION_EXPANSION",
        "CERTIFICATION_ELIGIBLE",
    ]
