"""ACA-0013 — Activation / first-value event instrumentation.

Real gap this closes: `docs/ACADEMY_FUNNEL_EVENT_TAXONOMY.md` classified
`academy_activation_completed` and `academy_first_value_reached` both
`READY_TO_EMIT` (the underlying actions already have real code paths),
but neither was ever actually wired to `services/events.py`'s
already-in-production `EventBus`. This suite proves both are now
genuinely emitted, from the real call sites the taxonomy names — not
merely that a function was called, but that a real `db.event_log`
document with the right `event_type`/payload results.

DB-backed pieces run against `mongomock_motor.AsyncMongoMockClient` —
same convention as every other suite in this repo (see
test_continuation_engine.py, test_quiz_reward_idempotency.py).
"""

from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

import api.learning as learning_module
import api.onboarding as onboarding_module
import badges_engine as badges_module
import services.activation as activation_module
import services.events as events_module
import services.frek_core as frek_core_module
import wallet.service as wallet_service_module
from api.learning import PhaseTickInput, tick_phase
from api.onboarding import onboarding_complete
from models import OnboardingInput, User


def _user(**overrides) -> User:
    defaults = dict(
        frek_id="FREK-ACA0013",
        email="learner@example.com",
        display_name="Learner",
        password_hash="x",
        role="student",
        metier_vise=None,
        cc_credits=5,
    )
    defaults.update(overrides)
    return User(**defaults)


async def _events_of_type(mock_db, event_type):
    return await mock_db.event_log.find({"event_type": event_type}, {"_id": 0}).to_list(
        50
    )


# ---------------- academy_first_value_reached ----------------


@pytest.fixture
async def learning_db(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_aca0013_first_value_test"]
    for module in (
        learning_module,
        activation_module,
        events_module,
        frek_core_module,
    ):
        monkeypatch.setattr(module, "db", mock_db)
    return mock_db


@pytest.mark.asyncio
async def test_first_ever_phase_tick_emits_first_value(learning_db):
    user = _user()
    await learning_db.formations.insert_one(
        {
            "code": "FMS-01",
            "name": "Formation Test",
            "pole": "test",
            "modules": [{"code": "FMS-01-M01", "name": "Module 1"}],
        }
    )

    result = await tick_phase(
        "FMS-01", "FMS-01-M01", PhaseTickInput(key="hook"), current=user
    )
    assert result["ok"] is True

    emitted = await _events_of_type(learning_db, "academy_first_value_reached")
    assert len(emitted) == 1
    payload = emitted[0]["payload"]
    assert payload["user_id"] == user.id
    assert payload["formation_code"] == "FMS-01"
    assert payload["module_code"] == "FMS-01-M01"
    assert payload["phase"] == "hook"


@pytest.mark.asyncio
async def test_second_phase_tick_never_reemits_first_value(learning_db):
    user = _user()
    await learning_db.formations.insert_one(
        {
            "code": "FMS-01",
            "name": "Formation Test",
            "pole": "test",
            "modules": [
                {"code": "FMS-01-M01", "name": "Module 1"},
                {"code": "FMS-01-M02", "name": "Module 2"},
            ],
        }
    )

    # First touch (hook on M01) -> creates the user's first db.progress doc.
    await tick_phase("FMS-01", "FMS-01-M01", PhaseTickInput(key="hook"), current=user)
    # A later phase on the SAME module (upsert matches the same doc).
    await tick_phase(
        "FMS-01", "FMS-01-M01", PhaseTickInput(key="objectives"), current=user
    )
    # A touch on a DIFFERENT module — a second db.progress doc, but the
    # user already has one, so this must never re-fire the event either.
    await tick_phase("FMS-01", "FMS-01-M02", PhaseTickInput(key="hook"), current=user)

    emitted = await _events_of_type(learning_db, "academy_first_value_reached")
    assert len(emitted) == 1  # exactly the very first write, never again


@pytest.mark.asyncio
async def test_different_users_each_get_their_own_first_value(learning_db):
    await learning_db.formations.insert_one(
        {
            "code": "FMS-01",
            "name": "Formation Test",
            "pole": "test",
            "modules": [{"code": "FMS-01-M01", "name": "Module 1"}],
        }
    )
    user_a = _user(frek_id="FREK-A", email="a@example.com")
    user_b = _user(frek_id="FREK-B", email="b@example.com")

    await tick_phase("FMS-01", "FMS-01-M01", PhaseTickInput(key="hook"), current=user_a)
    await tick_phase("FMS-01", "FMS-01-M01", PhaseTickInput(key="hook"), current=user_b)

    emitted = await _events_of_type(learning_db, "academy_first_value_reached")
    assert {e["payload"]["user_id"] for e in emitted} == {user_a.id, user_b.id}
    assert len(emitted) == 2


# ---------------- academy_activation_completed ----------------


@pytest.fixture
async def onboarding_db(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_aca0013_activation_test"]
    for module in (
        onboarding_module,
        frek_core_module,
        badges_module,
        events_module,
        wallet_service_module,
    ):
        monkeypatch.setattr(module, "db", mock_db)
    return mock_db


@pytest.mark.asyncio
async def test_onboarding_complete_emits_activation_event(onboarding_db):
    await onboarding_db.poles.insert_one(
        {"code": "audiovisuel", "name": "Audiovisuel", "color": "#E05A33"}
    )
    await onboarding_db.formations.insert_one(
        {
            "code": "FMS-01",
            "name": "Formation Test",
            "pole": "audiovisuel",
            "duration_h": 10,
            "cc": 5,
            "modules": [{"code": "FMS-01-M01", "name": "Module 1"}],
        }
    )
    await onboarding_db.badges.insert_one(
        {"code": "BADGE-DECOUVERTE", "name": "Découverte", "cc_threshold": 0}
    )

    user = _user()
    inp = OnboardingInput(
        lang="fr",
        metier_vise="audiovisuel",
        territoire="martinique",
        objectif_perso="Devenir monteur vidéo",
    )

    await onboarding_complete(inp, current=user)

    emitted = await _events_of_type(onboarding_db, "academy_activation_completed")
    assert len(emitted) == 1
    payload = emitted[0]["payload"]
    assert payload["user_id"] == user.id
    assert payload["metier_vise"] == "audiovisuel"
    assert payload["territoire"] == "martinique"
    assert payload["recommended_formation_code"] == "FMS-01"
    assert payload["badge_earned_code"] == "BADGE-DECOUVERTE"
    assert "FREK-TIME" in payload["signals_emitted"]
