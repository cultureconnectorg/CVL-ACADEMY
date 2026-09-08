"""ACA-0029 — real CVLN ecosystem handoffs.

Real gap this closes: `academy_first_value_reached` and `academy_
activation_completed` were already real, already-published events
(proven by test_activation_events.py) with ZERO subscribers --
published into the void. `academy_badge_awarded` is a new real
emission point this pass adds. All three are wired to real ecosystem
integrations (services/integrations/registry.py) via the same
best-effort, never-blocking pattern the original certification-passed
handler already established -- proven here without ever touching the
shared global `events` singleton (see the isolated-bus fixture below),
so this suite can never pollute any other test file's use of it.
"""

from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

import badges_engine as badges_module
import services.events as events_module
import services.frek_core as frek_core_module
import services.integrations.subscribers as subscribers_module
import wallet.service as wallet_service_module
from services.events import EventBus
from services.integrations.registry import all_integrations
from services.integrations.subscribers import (
    _on_activation_completed,
    _on_badge_awarded,
    _on_certification_passed,
    _on_first_value_reached,
    register,
)


def test_wallet_is_registered_as_an_ecosystem_integration():
    rows = all_integrations()
    names = [r["name"] for r in rows]
    assert "CVLN Wallet (djsayd, external)" in names
    wallet_row = next(r for r in rows if r["name"] == "CVLN Wallet (djsayd, external)")
    assert wallet_row["env_vars"] == ["CVLN_WALLET_URL", "CVLN_WALLET_API_KEY"]
    assert wallet_row["configured"] is False  # no env var set in this sandbox


# ---------------- new real emission point: academy_badge_awarded ----------


@pytest.fixture
async def badge_db(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_aca0029_badge_test"]
    monkeypatch.setattr(badges_module, "db", mock_db)
    monkeypatch.setattr(frek_core_module, "db", mock_db)
    monkeypatch.setattr(wallet_service_module, "db", mock_db)
    monkeypatch.setattr(events_module, "db", mock_db)
    await mock_db.badges.insert_one(
        {"code": "B10", "name": "Dix CC", "cc_threshold": 10}
    )
    # Real infra_indexes.py index -- without it mongomock allows a
    # duplicate insert, silently defeating the exact DuplicateKeyError
    # guard award_threshold_badges relies on for its award-exactly-once
    # (and therefore emit-exactly-once) guarantee.
    await mock_db.user_badges.create_index(
        [("user_id", 1), ("badge_code", 1)], unique=True
    )
    return mock_db


@pytest.mark.asyncio
async def test_badge_award_publishes_real_event(badge_db):
    await badges_module.award_threshold_badges("u1", 15)

    events = await badge_db.event_log.find(
        {"event_type": "academy_badge_awarded"}, {"_id": 0}
    ).to_list(10)
    assert len(events) == 1
    assert events[0]["payload"]["user_id"] == "u1"
    assert events[0]["payload"]["badge_code"] == "B10"
    assert events[0]["payload"]["jcc_reward"] == badges_module.BADGE_JCC_REWARD


@pytest.mark.asyncio
async def test_badge_award_is_idempotent_no_duplicate_event(badge_db):
    await badges_module.award_threshold_badges("u1", 15)
    await badges_module.award_threshold_badges("u1", 15)  # already has the badge

    events = await badge_db.event_log.find(
        {"event_type": "academy_badge_awarded"}, {"_id": 0}
    ).to_list(10)
    assert len(events) == 1  # not re-emitted on the second, no-op call


# ---------------- handler forwarding behavior ----------------


class _FakeIntegration:
    def __init__(self, name, configured=True):
        self.name = name
        self.calls = []
        self._configured = configured

    async def request(self, path, payload):
        if not self._configured:
            from services.integrations.base import IntegrationNotConfigured

            raise IntegrationNotConfigured(self.name, "FAKE")
        self.calls.append((path, payload))
        return {}


@pytest.mark.asyncio
async def test_on_badge_awarded_forwards_to_wallet_and_command_center(monkeypatch):
    fake_wallet = _FakeIntegration("wallet")
    fake_cc = _FakeIntegration("command_center")
    monkeypatch.setattr(subscribers_module, "wallet", fake_wallet)
    monkeypatch.setattr(subscribers_module, "command_center", fake_cc)

    payload = {"user_id": "u1", "badge_code": "B10", "jcc_reward": 10.0}
    await _on_badge_awarded(payload)

    assert fake_wallet.calls == [("/academy/badge-awarded", payload)]
    assert fake_cc.calls == [("/academy/badge-awarded", payload)]


@pytest.mark.asyncio
async def test_on_badge_awarded_skips_unconfigured_integration_gracefully(monkeypatch):
    fake_wallet = _FakeIntegration("wallet", configured=False)
    fake_cc = _FakeIntegration("command_center", configured=True)
    monkeypatch.setattr(subscribers_module, "wallet", fake_wallet)
    monkeypatch.setattr(subscribers_module, "command_center", fake_cc)

    payload = {"user_id": "u1", "badge_code": "B10", "jcc_reward": 10.0}
    await _on_badge_awarded(payload)  # must not raise

    assert fake_cc.calls == [("/academy/badge-awarded", payload)]


@pytest.mark.asyncio
async def test_on_activation_completed_forwards_only_to_command_center(monkeypatch):
    fake_brain = _FakeIntegration("brain")
    fake_cc = _FakeIntegration("command_center")
    monkeypatch.setattr(subscribers_module, "brain", fake_brain)
    monkeypatch.setattr(subscribers_module, "command_center", fake_cc)

    payload = {"user_id": "u1"}
    await _on_activation_completed(payload)

    assert fake_cc.calls == [("/academy/activation-completed", payload)]
    assert fake_brain.calls == []  # deliberately not included -- see subscribers.py


@pytest.mark.asyncio
async def test_on_first_value_reached_forwards_to_command_center(monkeypatch):
    fake_cc = _FakeIntegration("command_center")
    monkeypatch.setattr(subscribers_module, "command_center", fake_cc)

    payload = {"user_id": "u1"}
    await _on_first_value_reached(payload)

    assert fake_cc.calls == [("/academy/first-value-reached", payload)]


@pytest.mark.asyncio
async def test_on_certification_passed_still_forwards_to_brain_and_command_center(
    monkeypatch,
):
    fake_brain = _FakeIntegration("brain")
    fake_cc = _FakeIntegration("command_center")
    monkeypatch.setattr(subscribers_module, "brain", fake_brain)
    monkeypatch.setattr(subscribers_module, "command_center", fake_cc)

    payload = {"user_id": "u1", "certification_code": "FMS01-A01"}
    await _on_certification_passed(payload)

    assert fake_brain.calls == [("/academy/certification-passed", payload)]
    assert fake_cc.calls == [("/academy/certification-passed", payload)]


# ---------------- register() wires all 4 events, on an isolated bus ----------


@pytest.mark.asyncio
async def test_register_wires_all_four_events_on_an_isolated_bus(monkeypatch):
    """Never touches the real global `events` singleton -- a fresh
    EventBus is substituted for the duration of this one test, so this
    can never leak a subscription into any other test file's use of
    the shared bus."""
    isolated_bus = EventBus()
    monkeypatch.setattr(
        isolated_bus, "publish", isolated_bus.publish
    )  # no-op, keep real
    monkeypatch.setattr(
        __import__("services.integrations.subscribers", fromlist=["events"]),
        "events",
        isolated_bus,
    )
    # db writes inside EventBus.publish still need a mock db.
    client = AsyncMongoMockClient()
    monkeypatch.setattr(events_module, "db", client["cvln_aca0029_register_test"])

    register()

    for event_type in (
        "academy.certification.passed",
        "academy_activation_completed",
        "academy_first_value_reached",
        "academy_badge_awarded",
    ):
        assert len(isolated_bus._subscribers[event_type]) == 1

    # And a real publish on the isolated bus actually invokes the
    # handler without raising, even with every integration unconfigured.
    await isolated_bus.publish("academy_badge_awarded", {"user_id": "u1"})
