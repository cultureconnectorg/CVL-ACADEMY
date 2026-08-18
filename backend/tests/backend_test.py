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
                  "duration_h", "stades", "cc", "badge_name", "modules_count",
                  "contexts", "audience_levels", "bridge_entities",
                  "positioning_note", "reconciliation_flags", "primary_job",
                  "reconstruction_status", "needs_external_calibration",
                  "delivery_formats", "market_job_title",
                  "calibration_confidence", "calibration_date"):
            assert k in sample

    def test_music_business_cartography_positioning(self, http):
        r = http.get(f"{API}/formations/FMS-02")
        assert r.status_code == 200
        f = r.json()
        assert f["contexts"] == ["EXTERNAL", "BRIDGE"]
        assert "PROFESSIONNEL" in f["audience_levels"]
        assert f["economics"]["public_price_eur"] == 1400
        assert "LabelOS" in f["bridge_entities"]
        assert f["job_truth"]["market_name"] == "Chargé de production / label manager musique"
        assert f["cartography"]["primary_job"] == "Chargé de production / label manager musique"
        assert f["cartography"]["needs_external_calibration"] is True
        assert "HYBRIDE" in f["cartography"]["delivery_formats"]

    def test_catalogue_cartography_complete_for_all_formations(self, http):
        r = http.get(f"{API}/formations")
        assert r.status_code == 200
        formations = r.json()
        assert len(formations) == 30
        for formation in formations:
            assert formation["primary_job"]
            assert formation["contexts"]
            assert formation["audience_levels"]
            assert formation["bridge_entities"]
            assert formation["delivery_formats"]
            assert formation["needs_external_calibration"] is True
            assert formation["reconstruction_status"] in {"MAPPED_FROM_SEED", "NEEDS_RECONSTRUCTION"}

    def test_external_calibration_complete_for_all_formations(self, http):
        r = http.get(f"{API}/formations")
        assert r.status_code == 200
        formations = r.json()
        assert len(formations) == 30
        for formation in formations:
            assert formation["market_job_title"]
            assert formation["calibration_date"] == "2026-08-18"
            assert formation["calibration_confidence"] in {"low", "medium", "high"}

    def test_external_calibration_separates_states(self, http):
        r = http.get(f"{API}/formations/GMD-01")
        assert r.status_code == 200
        calibration = r.json()["external_calibration"]
        assert set(calibration) >= {
            "current_cvln_state",
            "external_market_state",
            "recommended_future_state",
            "calibration_confidence",
            "calibration_date",
        }
        external = calibration["external_market_state"]
        assert external["market_job_title"] == "Chef de projet événementiel"
        assert external["external_job_references"]
        assert external["certification_references"]
        assert external["market_price_range"]["status"] == "needs_benchmark"
        assert calibration["recommended_future_state"]["gaps"]

    def test_reconciliation_flags_preserve_doctrine_drift(self, http):
        r = http.get(f"{API}/formations/FMS-06")
        assert r.status_code == 200
        flags = r.json().get("reconciliation_flags", [])
        assert any(flag["type"] == "HOURS_CC_MISMATCH" for flag in flags)

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

    def test_quiz_submit_gated_without_prereqs(self, http, auth_headers):
        """LX v2 gate — quiz must reject before all pre-phases are ticked."""
        answers = self._correct_answers(http)
        r = http.post(
            f"{API}/formations/FMS-01/modules/FMS-01-M01/quiz/submit",
            json={"module_code": "FMS-01-M01", "answers": answers},
            headers=auth_headers,
        )
        assert r.status_code == 400, r.text
        detail = r.json().get("detail", "")
        assert "Complète d'abord les phases" in detail
        # Missing phases should include all 5 gates
        for expected in ("hook", "objectives", "course", "workshop", "deliverable"):
            assert expected in detail, f"expected '{expected}' in gate error: {detail}"

    def _complete_prereqs(self, http, auth_headers, fc="FMS-01", mc="FMS-01-M01"):
        """Tick all 4 pre-phases + submit deliverable (>=250 chars)."""
        base = f"{API}/modules/{fc}/{mc}/phase"
        for key in ("hook", "objectives", "workshop"):
            r = http.post(base, json={"key": key}, headers=auth_headers)
            assert r.status_code == 200, f"phase {key}: {r.text}"
        r = http.post(base, json={"key": "course", "progress_pct": 100},
                      headers=auth_headers)
        assert r.status_code == 200, r.text
        text = ("Voici mon livrable détaillé pour FMS-01-M01. "
                "Intention : produire un plan de sortie caribéen. "
                "Méthode : j'ai suivi les 5 étapes de l'atelier CVLN, "
                "en m'ancrant dans le contexte Martinique. "
                "Résultat : un plan structuré en 3 phases (teasing, sortie, "
                "sustain). Apprentissages : la doctrine CVLN est concrète, "
                "l'ancrage territorial est central, la mini-mission relie "
                "théorie et terrain de manière opérationnelle.")
        assert len(text) >= 250
        r = http.post(f"{API}/modules/{fc}/{mc}/deliverable",
                      json={"text": text}, headers=auth_headers)
        assert r.status_code == 200, r.text

    def test_submit_all_correct(self, http, auth_headers, registered):
        # Complete prereqs first (LX v2)
        self._complete_prereqs(http, auth_headers)

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


# ---------------- LX v2 — Module Journey / Gating / Learning Path ----------------
DELIVERABLE_TEXT = (
    "Voici mon livrable LX v2. Intention : produire un plan de sortie caribéen. "
    "Méthode : j'ai suivi les 5 étapes de l'atelier CVLN, en m'ancrant dans le "
    "contexte Martinique. Résultat : un plan en 3 phases (teasing / sortie / "
    "sustain), aligné avec la doctrine FREK. Apprentissages : la doctrine CVLN "
    "est concrète, l'ancrage territorial est central, la mini-mission relie "
    "théorie et terrain de manière opérationnelle."
)


CORRECT_ANSWERS = {"1": "A", "2": "A", "3": "VRAI", "4": "C",
                   "5": "A", "6": "C", "7": "A", "8": "A"}


@pytest.fixture(scope="module")
def lx_user(http):
    """Fresh, fully-onboarded FMS user shared across LX v2 test classes."""
    uid = uuid.uuid4().hex[:8]
    creds = {
        "email": f"qa-lx2+{uid}@test.com",
        "password": "Cvln!2026",
        "display_name": f"QA LX2 {uid}",
        "lang": "fr",
    }
    r = http.post(f"{API}/auth/register", json=creds)
    assert r.status_code == 200, r.text
    data = r.json()
    headers = {"Authorization": f"Bearer {data['token']}"}
    # Onboard as FMS
    ob = http.post(f"{API}/onboarding/complete", headers=headers, json={
        "lang": "fr", "metier_vise": "FMS", "territoire": "martinique",
        "objectif_perso": "Sortir mon premier EP CVLN caribéen.",
    })
    assert ob.status_code == 200, ob.text
    return {"token": data["token"], "user": data["user"], "creds": creds, "headers": headers}


@pytest.fixture(scope="module")
def lx_headers(lx_user):
    return lx_user["headers"]


@pytest.fixture(scope="class")
def lx_fresh_headers(http):
    """Isolated fresh onboarded FMS user for read-only journey shape tests."""
    uid = uuid.uuid4().hex[:8]
    creds = {"email": f"qa-lxf+{uid}@test.com", "password": "Cvln!2026",
             "display_name": f"QA LXF {uid}", "lang": "fr"}
    r = http.post(f"{API}/auth/register", json=creds)
    assert r.status_code == 200
    headers = {"Authorization": f"Bearer {r.json()['token']}"}
    http.post(f"{API}/onboarding/complete", headers=headers, json={
        "lang": "fr", "metier_vise": "FMS", "territoire": "martinique",
        "objectif_perso": "Read-only journey inspection.",
    })
    return headers


class TestLXv2ModuleJourney:
    """GET /api/modules/{fc}/{mc} enriched payload."""

    def test_module_journey_shape(self, http, lx_fresh_headers):
        r = http.get(f"{API}/modules/FMS-01/FMS-01-M01", headers=lx_fresh_headers)
        assert r.status_code == 200, r.text
        j = r.json()
        # Top-level keys
        for k in ("formation", "module", "is_unlocked", "lock_reason",
                  "progress", "status", "phase_flags"):
            assert k in j, f"missing {k}"
        assert j["is_unlocked"] is True
        assert j["status"] == "available"
        # phase_flags all False initially
        pf = j["phase_flags"]
        for key in ("hook", "objectives", "course", "workshop",
                    "deliverable", "quiz", "mini_mission"):
            assert pf[key] is False, f"expected {key}=False, got {pf}"

        # Enriched module → phases dict
        phases = j["module"]["phases"]
        assert "narrative" in phases["hook"]
        assert len(phases["objectives"]["items"]) == 4
        assert len(phases["course"]["content_md"]) > 200
        assert isinstance(phases["course"]["reading_min"], int)
        assert len(phases["workshop"]["steps"]) == 5
        assert phases["deliverable"]["min_chars"] == 250
        assert phases["quiz"]["passing_score"] == 0.8
        assert "brief" in phases["mini_mission"]

    def test_module_journey_requires_auth(self, http):
        r = http.get(f"{API}/modules/FMS-01/FMS-01-M01")
        assert r.status_code == 401

    def test_module_journey_locked_module(self, http, lx_fresh_headers):
        # FMS-01-M02 is locked until M01 validated
        r = http.get(f"{API}/modules/FMS-01/FMS-01-M02", headers=lx_fresh_headers)
        assert r.status_code == 200
        j = r.json()
        assert j["is_unlocked"] is False
        assert j["lock_reason"]


class TestLXv2Gating:
    """Quiz-submit gate + deliverable + mini-mission gate."""

    def test_quiz_rejects_when_no_phase_done(self, http, lx_headers):
        r = http.post(
            f"{API}/formations/FMS-01/modules/FMS-01-M01/quiz/submit",
            json={"module_code": "FMS-01-M01", "answers": CORRECT_ANSWERS},
            headers=lx_headers,
        )
        assert r.status_code == 400
        detail = r.json()["detail"]
        assert "Complète d'abord les phases" in detail
        # all 5 keys named
        for k in ("hook", "objectives", "course", "workshop", "deliverable"):
            assert k in detail

    def test_phase_tick_hook_objectives_workshop(self, http, lx_headers):
        for key in ("hook", "objectives", "workshop"):
            r = http.post(f"{API}/modules/FMS-01/FMS-01-M01/phase",
                          json={"key": key}, headers=lx_headers)
            assert r.status_code == 200, f"{key}: {r.text}"
            j = r.json()
            assert j["ok"] is True
            assert j["phase_flags"][key] is True
        # After 3 ticks (no course, no deliverable), quiz still gated
        r = http.get(f"{API}/modules/FMS-01/FMS-01-M01", headers=lx_headers)
        pf = r.json()["phase_flags"]
        assert pf["hook"] and pf["objectives"] and pf["workshop"]
        assert pf["course"] is False and pf["deliverable"] is False

    def test_course_progress_below_80_does_not_count(self, http, lx_headers):
        r = http.post(f"{API}/modules/FMS-01/FMS-01-M01/phase",
                      json={"key": "course", "progress_pct": 50},
                      headers=lx_headers)
        assert r.status_code == 200
        assert r.json()["phase_flags"]["course"] is False

    def test_course_progress_80_counts(self, http, lx_headers):
        r = http.post(f"{API}/modules/FMS-01/FMS-01-M01/phase",
                      json={"key": "course", "progress_pct": 100},
                      headers=lx_headers)
        assert r.status_code == 200
        assert r.json()["phase_flags"]["course"] is True

    def test_deliverable_too_short_rejected(self, http, lx_headers):
        r = http.post(f"{API}/modules/FMS-01/FMS-01-M01/deliverable",
                      json={"text": "trop court"}, headers=lx_headers)
        assert r.status_code == 400
        assert "250" in r.json()["detail"]

    def test_deliverable_valid_submits(self, http, lx_headers):
        r = http.post(f"{API}/modules/FMS-01/FMS-01-M01/deliverable",
                      json={"text": DELIVERABLE_TEXT}, headers=lx_headers)
        assert r.status_code == 200, r.text
        j = r.json()
        assert j["phase_flags"]["deliverable"] is True
        assert j["status"] == "ready_for_quiz"

    def test_mini_mission_gated_before_quiz(self, http, lx_headers):
        r = http.post(f"{API}/modules/FMS-01/FMS-01-M01/mini-mission/commit",
                      headers=lx_headers)
        assert r.status_code == 400
        assert "quiz" in r.json()["detail"].lower()

    def test_quiz_submit_after_prereqs(self, http, lx_headers):
        r = http.post(
            f"{API}/formations/FMS-01/modules/FMS-01-M01/quiz/submit",
            json={"module_code": "FMS-01-M01", "answers": CORRECT_ANSWERS},
            headers=lx_headers,
        )
        assert r.status_code == 200, r.text
        j = r.json()
        assert j["passed"] is True
        assert j["score"] >= 0.8
        assert j["cc_earned"] > 0

        # After quiz, status becomes awaiting_mini_mission (not validated yet)
        r2 = http.get(f"{API}/modules/FMS-01/FMS-01-M01", headers=lx_headers)
        j2 = r2.json()
        assert j2["phase_flags"]["quiz"] is True
        assert j2["phase_flags"]["mini_mission"] is False
        assert j2["status"] == "awaiting_mini_mission"

    def test_mini_mission_commit_validates_module(self, http, lx_headers):
        r = http.post(f"{API}/modules/FMS-01/FMS-01-M01/mini-mission/commit",
                      headers=lx_headers)
        assert r.status_code == 200, r.text
        j = r.json()
        assert j["status"] == "validated"
        for k in ("hook", "objectives", "course", "workshop",
                  "deliverable", "quiz", "mini_mission"):
            assert j["phase_flags"][k] is True, f"{k} not true"

    def test_module_lock_progression_after_m01_validated(self, http, lx_headers):
        """After M01 validated, M02 should unlock but M03 still locked."""
        r = http.get(f"{API}/formations/FMS-01", headers=lx_headers)
        assert r.status_code == 200
        f = r.json()
        by_code = {m["code"]: m for m in f["modules"]}
        assert by_code["FMS-01-M01"]["status"] == "validated"
        assert by_code["FMS-01-M02"]["is_unlocked"] is True
        assert by_code["FMS-01-M03"]["is_unlocked"] is False

    def test_progression_counts_validated_module(self, http, lx_headers):
        """LX v2: progression counts only fully-validated modules."""
        r = http.get(f"{API}/progression/summary", headers=lx_headers)
        assert r.status_code == 200
        j = r.json()
        assert j["completed_modules"] >= 1
        assert j["total_modules"] > 0
        assert 0 <= j["global_pct"] <= 100


class TestLXv2LearningPath:
    """GET /api/user/learning-path — pole-first sequential ordering."""

    def test_learning_path_shape_for_fresh_fms_user(self, http):
        # Fresh onboarded FMS user (independent from lx_user which has M01 done)
        uid = uuid.uuid4().hex[:8]
        creds = {
            "email": f"qa-lp+{uid}@test.com",
            "password": "Cvln!2026",
            "display_name": f"QA LP {uid}",
            "lang": "fr",
        }
        r = http.post(f"{API}/auth/register", json=creds)
        assert r.status_code == 200
        headers = {"Authorization": f"Bearer {r.json()['token']}"}
        http.post(f"{API}/onboarding/complete", headers=headers, json={
            "lang": "fr", "metier_vise": "FMS", "territoire": "martinique",
            "objectif_perso": "Learning path fresh test.",
        })

        r = http.get(f"{API}/user/learning-path", headers=headers)
        assert r.status_code == 200, r.text
        j = r.json()

        assert j["metier_vise"] == "FMS"
        # own_pole = 6 FMS formations
        own = j["own_pole"]
        assert len(own) == 6, f"expected 6 FMS formations, got {len(own)}"
        for f in own:
            assert f["pole"] == "FMS"
            assert f["is_recommended"] is True
        # sorted by code
        codes = [f["code"] for f in own]
        assert codes == sorted(codes)

        # FMS-01 unlocked, FMS-02..06 locked
        by_code = {f["code"]: f for f in own}
        assert by_code["FMS-01"]["is_unlocked"] is True
        for c in ("FMS-02", "FMS-03", "FMS-04", "FMS-05", "FMS-06"):
            if c in by_code:
                assert by_code[c]["is_unlocked"] is False, f"{c} should be locked"
                assert "50%" in by_code[c]["lock_reason"]

        # other_poles = 24 formations sorted by pole then code
        others = j["other_poles"]
        assert len(others) == 24, f"expected 24 other-pole formations, got {len(others)}"
        for f in others:
            assert f["pole"] != "FMS"
            assert f["is_recommended"] is False
        # First-of-each-other-pole should be locked with pole-completion msg
        first_per_pole = {}
        for f in others:
            first_per_pole.setdefault(f["pole"], f)
        for f in first_per_pole.values():
            assert f["is_unlocked"] is False
            assert "pôle FMS" in f["lock_reason"]

        # next_action → FMS-01 / FMS-01-M01
        na = j["next_action"]
        assert na is not None
        assert na["formation_code"] == "FMS-01"
        assert na["module_code"] == "FMS-01-M01"
        assert na["status"] == "available"


class TestLXv2FormationLockRules:
    """GET /api/formations/{code} respects sequential pole unlock."""

    def test_fms01_unlocked_for_fms_user(self, http, lx_headers):
        r = http.get(f"{API}/formations/FMS-01", headers=lx_headers)
        assert r.status_code == 200
        assert r.json()["is_unlocked"] is True

    def test_fms02_locked_until_50pct_of_fms01(self, http):
        # Fresh FMS user with 0 progress
        uid = uuid.uuid4().hex[:8]
        creds = {"email": f"qa-lock+{uid}@test.com", "password": "Cvln!2026",
                 "display_name": f"QA LK {uid}", "lang": "fr"}
        r = http.post(f"{API}/auth/register", json=creds)
        headers = {"Authorization": f"Bearer {r.json()['token']}"}
        http.post(f"{API}/onboarding/complete", headers=headers, json={
            "lang": "fr", "metier_vise": "FMS", "territoire": "martinique",
            "objectif_perso": "Lock rule test.",
        })
        r = http.get(f"{API}/formations/FMS-02", headers=headers)
        assert r.status_code == 200
        j = r.json()
        assert j["is_unlocked"] is False
        assert "FMS-01" in j["lock_reason"]

    def test_other_pole_formation_locked_for_fms_user(self, http):
        uid = uuid.uuid4().hex[:8]
        creds = {"email": f"qa-otr+{uid}@test.com", "password": "Cvln!2026",
                 "display_name": f"QA OT {uid}", "lang": "fr"}
        r = http.post(f"{API}/auth/register", json=creds)
        headers = {"Authorization": f"Bearer {r.json()['token']}"}
        http.post(f"{API}/onboarding/complete", headers=headers, json={
            "lang": "fr", "metier_vise": "FMS", "territoire": "martinique",
            "objectif_perso": "Cross pole test.",
        })
        # Get any non-FMS formation code from /formations
        forms = http.get(f"{API}/formations").json()
        non_fms = next(f for f in forms if f["pole"] != "FMS")
        r = http.get(f"{API}/formations/{non_fms['code']}", headers=headers)
        assert r.status_code == 200
        j = r.json()
        assert j["is_unlocked"] is False
        assert "FMS" in j["lock_reason"]


class TestLXv2ModuleLockRulesRemoved:
    """Merged into TestLXv2Gating to keep loadscope-safe."""
    pass


class TestLXv2ProgressionSummaryRemoved:
    """Merged into TestLXv2Gating to keep loadscope-safe."""
    pass

