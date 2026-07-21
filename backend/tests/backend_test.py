"""CVLN Academy OS — backend E2E test suite.

Covers:
- Health (/api/)
- Auth flows (register, duplicate, login, /me)
- Formations (list + detail)
- Quiz (get, submit all-correct, CC + stade + threshold badges)
- Missions (list, accept, submit)
- Badges (list, mine)
- Progression summary + FREK profile
- Mentor (agents, chat, session persistence)
"""
from __future__ import annotations

import os
import time
import uuid

import pytest
import requests


BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "").rstrip("/")
if not BASE_URL:
    # fallback: read frontend/.env
    try:
        with open("/app/frontend/.env") as f:
            for line in f:
                if line.startswith("REACT_APP_BACKEND_URL="):
                    BASE_URL = line.split("=", 1)[1].strip().rstrip("/")
                    break
    except Exception:  # noqa: BLE001
        pass
API = f"{BASE_URL}/api"


# ---------------- fixtures ----------------
@pytest.fixture(scope="session")
def http():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


@pytest.fixture(scope="session")
def qa_credentials():
    return {
        "email": "qa+cvln@test.com",
        "password": "Cvln!2026",
        "display_name": "QA Learner",
        "lang": "fr",
    }


@pytest.fixture(scope="session")
def unique_credentials():
    # Fresh account each pytest session — avoids collisions with existing data
    uid = uuid.uuid4().hex[:8]
    return {
        "email": f"qa+cvln-{uid}@test.com",
        "password": "Cvln!2026",
        "display_name": f"QA {uid}",
        "lang": "fr",
    }


@pytest.fixture(scope="session")
def registered(http, unique_credentials):
    """Register a brand-new user for the whole session."""
    r = http.post(f"{API}/auth/register", json=unique_credentials)
    assert r.status_code == 200, f"register failed: {r.status_code} {r.text}"
    data = r.json()
    return {"token": data["token"], "user": data["user"], "creds": unique_credentials}


@pytest.fixture(scope="session")
def auth_headers(registered):
    return {"Authorization": f"Bearer {registered['token']}"}


# ---------------- HEALTH ----------------
class TestHealth:
    def test_root_metadata(self, http):
        r = http.get(f"{API}/")
        assert r.status_code == 200
        j = r.json()
        assert j["app"] == "CVLN Academy OS"
        assert "version" in j
        assert j["frek_core_remote"] is False
        assert j["agent_factory_remote"] is False


# ---------------- AUTH ----------------
class TestAuth:
    def test_register_new_user(self, registered):
        u = registered["user"]
        assert u["email"] == registered["creds"]["email"]
        assert u["display_name"] == registered["creds"]["display_name"]
        assert u["frek_id"].startswith("FREK-"), f"got {u['frek_id']}"
        assert u["cc_credits"] == 5
        assert u["stade"] == "graine"
        assert isinstance(u["signals"], dict)
        assert registered["token"] and isinstance(registered["token"], str)
        # New: onboarding must be false on fresh register
        assert u["onboarding_completed"] is False

    def test_register_duplicate_email(self, http, registered):
        r = http.post(f"{API}/auth/register", json=registered["creds"])
        assert r.status_code == 400
        assert "détail" in r.text.lower() or "detail" in r.json()

    def test_login_ok(self, http, registered):
        r = http.post(f"{API}/auth/login", json={
            "email": registered["creds"]["email"],
            "password": registered["creds"]["password"],
        })
        assert r.status_code == 200
        j = r.json()
        assert j["user"]["email"] == registered["creds"]["email"]
        assert j["token"]

    def test_login_wrong_password(self, http, registered):
        r = http.post(f"{API}/auth/login", json={
            "email": registered["creds"]["email"],
            "password": "wrongpass!!",
        })
        assert r.status_code == 401

    def test_me_returns_public_user(self, http, auth_headers, registered):
        r = http.get(f"{API}/auth/me", headers=auth_headers)
        assert r.status_code == 200
        j = r.json()
        assert j["frek_id"] == registered["user"]["frek_id"]
        assert j["email"] == registered["creds"]["email"]
        assert "cc_credits" in j and "stade" in j and "signals" in j
        assert j["onboarding_completed"] is False

    def test_me_requires_auth(self, http):
        r = http.get(f"{API}/auth/me")
        assert r.status_code == 401


# ---------------- FORMATIONS ----------------
class TestFormations:
    def test_list_30_formations(self, http):
        r = http.get(f"{API}/formations")
        assert r.status_code == 200
        arr = r.json()
        assert isinstance(arr, list)
        assert len(arr) == 30, f"expected 30 formations, got {len(arr)}"
        # summary shape
        sample = arr[0]
        for k in ("code", "name", "pole", "pole_name", "pole_color",
                  "duration_h", "stades", "cc", "badge_name", "modules_count"):
            assert k in sample

    def test_fms01_detail_has_12_modules(self, http):
        r = http.get(f"{API}/formations/FMS-01")
        assert r.status_code == 200
        f = r.json()
        assert f["code"] == "FMS-01"
        modules = f.get("modules", [])
        assert len(modules) == 12, f"FMS-01 should have 12 modules, got {len(modules)}"
        # module shape
        m0 = modules[0]
        for k in ("code", "name", "duration_h", "hook", "deliverable", "frek_signal"):
            assert k in m0, f"missing {k} in module"

    def test_formation_not_found(self, http):
        r = http.get(f"{API}/formations/FMS-ZZ")
        assert r.status_code == 404


# ---------------- QUIZ ----------------
class TestQuiz:
    def test_get_quiz_no_leaked_correct_flag(self, http):
        r = http.get(f"{API}/formations/FMS-01/modules/FMS-01-M01/quiz")
        assert r.status_code == 200
        payload = r.json()
        assert "quiz" in payload and "module" in payload
        for q in payload["quiz"]:
            for c in q["choices"]:
                assert "correct" not in c, "quiz endpoint leaked correct flag!"

    def _correct_answers(self, http):
        """Fetch quiz then rebuild expected correct answers by hitting server-side quiz
        template directly? We can't; instead we know the deliverable is that correct=True
        options match specific texts. Simplest: we brute-force by submitting all A / VRAI first
        since seed_data + quiz.py always place correct=A on QCM and correct=VRAI on VRAI_FAUX.
        """
        # From quiz.py inspection: Q1=A, Q2=A, Q3=VRAI, Q4=C, Q5=A, Q6=C, Q7=A, Q8=A
        return {"1": "A", "2": "A", "3": "VRAI", "4": "C", "5": "A", "6": "C", "7": "A", "8": "A"}

    def test_submit_all_correct(self, http, auth_headers, registered):
        # snapshot user state
        r_me_before = http.get(f"{API}/auth/me", headers=auth_headers).json()
        cc_before = r_me_before["cc_credits"]

        answers = self._correct_answers(http)
        r = http.post(
            f"{API}/formations/FMS-01/modules/FMS-01-M01/quiz/submit",
            json={"module_code": "FMS-01-M01", "answers": answers},
            headers=auth_headers,
        )
        assert r.status_code == 200, r.text
        j = r.json()
        assert j["passed"] is True, f"quiz should pass with all-correct answers: {j}"
        assert j["correct"] == j["total"]
        assert j["score"] >= 0.8
        assert j["cc_earned"] > 0
        assert j["signal_emitted"]

        # user CC updated
        me_after = http.get(f"{API}/auth/me", headers=auth_headers).json()
        assert me_after["cc_credits"] == cc_before + j["cc_earned"]

    def test_submit_quiz_awards_badges(self, http, auth_headers):
        r = http.get(f"{API}/badges/mine", headers=auth_headers)
        assert r.status_code == 200
        mine = r.json()
        assert isinstance(mine, list)
        # At least the 0-threshold "découverte" badge should be awarded post-quiz-pass
        codes = [b["code"] for b in mine]
        assert len(codes) >= 1, f"expected at least 1 badge earned, got {codes}"


# ---------------- MISSIONS ----------------
class TestMissions:
    def test_list_missions_min_6(self, http):
        r = http.get(f"{API}/missions")
        assert r.status_code == 200
        arr = r.json()
        assert len(arr) >= 6, f"expected >=6 missions, got {len(arr)}"

    def test_accept_then_submit_mission(self, http, auth_headers, registered):
        # pick MIS-KLT-01 if exists, else first mission
        all_m = http.get(f"{API}/missions").json()
        codes = [m["code"] for m in all_m]
        code = "MIS-KLT-01" if "MIS-KLT-01" in codes else codes[0]
        mission = next(m for m in all_m if m["code"] == code)
        reward = int(mission["cc_reward"])

        cc_before = http.get(f"{API}/auth/me", headers=auth_headers).json()["cc_credits"]

        r_a = http.post(f"{API}/missions/{code}/accept", headers=auth_headers)
        assert r_a.status_code == 200

        r_s = http.post(f"{API}/missions/{code}/submit", headers=auth_headers)
        assert r_s.status_code == 200
        js = r_s.json()
        assert js["cc_earned"] == reward
        assert "new_stade" in js

        cc_after = http.get(f"{API}/auth/me", headers=auth_headers).json()["cc_credits"]
        assert cc_after == cc_before + reward


# ---------------- BADGES ----------------
class TestBadges:
    def test_list_badges_has_8(self, http):
        r = http.get(f"{API}/badges")
        assert r.status_code == 200
        arr = r.json()
        assert len(arr) == 8, f"expected 8 badges, got {len(arr)}"
        for b in arr:
            for k in ("code", "name", "tier", "cc_threshold"):
                assert k in b


# ---------------- PROGRESSION + FREK PROFILE ----------------
class TestProgression:
    def test_progression_summary(self, http, auth_headers):
        r = http.get(f"{API}/progression/summary", headers=auth_headers)
        assert r.status_code == 200
        j = r.json()
        for k in ("completed_modules", "total_modules", "global_pct", "stade", "cc_credits"):
            assert k in j
        assert j["total_modules"] > 0
        assert 0 <= j["global_pct"] <= 100

    def test_frek_profile(self, http, auth_headers, registered):
        r = http.get(f"{API}/frek/profile", headers=auth_headers)
        assert r.status_code == 200
        j = r.json()
        assert j["user"]["frek_id"] == registered["user"]["frek_id"]
        assert "stade_progress_pct" in j
        assert "modules_completed" in j
        assert "badges_count" in j
        assert "signals" in j and isinstance(j["signals"], dict)
        assert "recent_signals" in j


# ---------------- MENTOR ----------------
class TestMentor:
    def test_list_agents(self, http):
        r = http.get(f"{API}/mentor/agents")
        assert r.status_code == 200
        arr = r.json()
        assert any(a["code"] == "mentor-cvln" for a in arr)

    def test_mentor_chat_returns_non_empty(self, http, auth_headers):
        session_id = f"pytest-{uuid.uuid4().hex[:8]}"
        r = http.post(
            f"{API}/mentor/chat",
            json={"message": "Bonjou! Qui es-tu en une phrase?", "session_id": session_id},
            headers=auth_headers,
            timeout=60,  # LLM can be slow
        )
        assert r.status_code == 200, r.text
        j = r.json()
        assert j["session_id"] == session_id
        assert isinstance(j["reply"], str) and len(j["reply"].strip()) > 0

        # session should be persisted
        r2 = http.get(f"{API}/mentor/session/{session_id}", headers=auth_headers, timeout=30)
        assert r2.status_code == 200
        conv = r2.json()
        msgs = conv.get("messages", [])
        assert len(msgs) >= 2
        assert msgs[0]["role"] == "user"
        assert msgs[1]["role"] == "assistant"



# ---------------- ONBOARDING (FREK Origin Story) ----------------
@pytest.fixture(scope="class")
def onboarding_user(http):
    """Fresh user just for onboarding tests (never onboarded)."""
    uid = uuid.uuid4().hex[:8]
    creds = {
        "email": f"qa-ob+{uid}@test.com",
        "password": "Cvln!2026",
        "display_name": f"QA OB {uid}",
        "lang": "fr",
    }
    r = http.post(f"{API}/auth/register", json=creds)
    assert r.status_code == 200, r.text
    data = r.json()
    return {"token": data["token"], "user": data["user"], "creds": creds}


@pytest.fixture(scope="class")
def ob_headers(onboarding_user):
    return {"Authorization": f"Bearer {onboarding_user['token']}"}


class TestOnboarding:
    def test_options_shape(self, http):
        r = http.get(f"{API}/onboarding/options")
        assert r.status_code == 200
        j = r.json()
        assert len(j["langs"]) == 3
        codes = {l["code"] for l in j["langs"]}
        assert codes == {"fr", "en", "kr"}
        assert len(j["metiers"]) == 13, f"expected 13 poles, got {len(j['metiers'])}"
        assert len(j["territoires"]) == 7
        terr_codes = {t["code"] for t in j["territoires"]}
        assert "martinique" in terr_codes

    def test_complete_requires_auth(self, http):
        r = http.post(f"{API}/onboarding/complete", json={
            "lang": "fr", "metier_vise": "FMS",
            "territoire": "martinique", "objectif_perso": "test",
        })
        assert r.status_code == 401

    def test_complete_invalid_lang(self, http, ob_headers):
        r = http.post(f"{API}/onboarding/complete", headers=ob_headers, json={
            "lang": "xx", "metier_vise": "FMS",
            "territoire": "martinique", "objectif_perso": "Faire un EP",
        })
        assert r.status_code == 400

    def test_complete_invalid_metier(self, http, ob_headers):
        r = http.post(f"{API}/onboarding/complete", headers=ob_headers, json={
            "lang": "fr", "metier_vise": "ZZZ",
            "territoire": "martinique", "objectif_perso": "Faire un EP",
        })
        assert r.status_code == 400

    def test_complete_invalid_territoire(self, http, ob_headers):
        r = http.post(f"{API}/onboarding/complete", headers=ob_headers, json={
            "lang": "fr", "metier_vise": "FMS",
            "territoire": "atlantis", "objectif_perso": "Faire un EP",
        })
        assert r.status_code == 400

    def test_complete_success_full_flow(self, http, ob_headers, onboarding_user):
        # snapshot user before
        me_before = http.get(f"{API}/auth/me", headers=ob_headers).json()
        time_before = me_before["signals"].get("FREK-TIME", 0)

        payload = {
            "lang": "fr",
            "metier_vise": "FMS",
            "territoire": "martinique",
            "objectif_perso": "Sortir mon premier EP et gagner 500 auditeurs mensuels.",
        }
        r = http.post(f"{API}/onboarding/complete", headers=ob_headers, json=payload)
        assert r.status_code == 200, r.text
        j = r.json()

        # user updated
        assert j["user"]["onboarding_completed"] is True
        assert j["user"]["metier_vise"] == "FMS"
        assert j["user"]["territoire"] == "martinique"
        assert j["user"]["objectif_perso"].startswith("Sortir mon premier EP")

        # 3 FREK-TIME signals emitted
        assert j["signals_emitted"] == ["FREK-TIME", "FREK-TIME", "FREK-TIME"]
        # signals counter incremented by 3
        assert j["user"]["signals"]["FREK-TIME"] == time_before + 3

        # badge earned
        assert j["badge_earned"] is not None
        assert j["badge_earned"]["code"] == "BADGE-DECOUVERTE"

        # recommended formation matches pole
        assert j["recommended_formation"] is not None
        assert j["recommended_formation"]["pole"] == "FMS"
        # FMS-01 has modules, should be preferred
        assert j["recommended_formation"]["code"] == "FMS-01"
        assert j["recommended_formation"]["modules_count"] > 0

        # recommended mission matches pole
        assert j["recommended_mission"] is not None
        assert j["recommended_mission"]["pole"] == "FMS"

        # /auth/me confirms onboarding_completed=true
        me_after = http.get(f"{API}/auth/me", headers=ob_headers).json()
        assert me_after["onboarding_completed"] is True

        # /missions/mine shows auto-accepted mission with source=onboarding
        mine = http.get(f"{API}/missions/mine", headers=ob_headers).json()
        assert any(
            m.get("source") == "onboarding" and m.get("status") == "accepted"
            for m in mine
        ), f"expected onboarding-sourced accepted mission in {mine}"

    def test_complete_idempotent_badge(self, http, ob_headers):
        """Re-submitting shouldn't duplicate badge, but endpoint still 200."""
        payload = {
            "lang": "fr", "metier_vise": "FMS",
            "territoire": "martinique",
            "objectif_perso": "Nouvel objectif après update",
        }
        r = http.post(f"{API}/onboarding/complete", headers=ob_headers, json=payload)
        assert r.status_code == 200
        # user still has BADGE-DECOUVERTE only once
        badges = http.get(f"{API}/badges/mine", headers=ob_headers).json()
        codes = [b["code"] for b in badges]
        assert codes.count("BADGE-DECOUVERTE") == 1
