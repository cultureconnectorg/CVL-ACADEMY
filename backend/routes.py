"""All CVLN Academy API routes, prefixed by /api at server level."""
from __future__ import annotations

import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from db import db, utc_now_iso
from models import (
    User, UserPublic, RegisterInput, LoginInput, AuthResponse,
    Formation, Badge, Mission, QuizSubmission, QuizResult,
    MentorChatInput, OnboardingInput, OnboardingResult,
)
from auth import (
    hash_password, verify_password, make_token,
    get_current_user, next_frek_id, user_public,
)
from services.frek_core import frek_core
from services.agent_factory import agent_factory
from quiz import build_quiz, evaluate


router = APIRouter(prefix="/api")


# ============ HEALTH ============
@router.get("/")
async def root():
    return {
        "app": "CVLN Academy OS",
        "version": "0.1",
        "frek_core_remote": frek_core.is_remote_enabled(),
        "agent_factory_remote": agent_factory.is_remote_enabled(),
    }


# ============ AUTH (FREK-ID) ============
@router.post("/auth/register", response_model=AuthResponse)
async def register(inp: RegisterInput):
    existing = await db.users.find_one({"email": inp.email.lower()}, {"_id": 0})
    if existing:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    frek_id = await next_frek_id()
    user = User(
        frek_id=frek_id,
        email=inp.email.lower(),
        display_name=inp.display_name.strip(),
        password_hash=hash_password(inp.password),
        lang=inp.lang,
        cc_credits=5,  # welcome CC per Master OS §3 (5 CC on profile creation)
    )
    doc = user.model_dump()
    await db.users.insert_one(doc)
    # Emit FREK-ID creation signal
    await frek_core.emit_signal(user.id, "FREK-TIME", {"reason": "profile_created"})
    return AuthResponse(token=make_token(user.id), user=user_public(user))


@router.post("/auth/login", response_model=AuthResponse)
async def login(inp: LoginInput):
    doc = await db.users.find_one({"email": inp.email.lower()}, {"_id": 0})
    if not doc or not verify_password(inp.password, doc.get("password_hash", "")):
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    user = User(**doc)
    return AuthResponse(token=make_token(user.id), user=user_public(user))


@router.get("/auth/me", response_model=UserPublic)
async def me(current: User = Depends(get_current_user)):
    return user_public(current)


# ============ ONBOARDING (FREK Origin Story) ============
TERRITOIRES = [
    {"code": "martinique", "name": "Martinique"},
    {"code": "guadeloupe", "name": "Guadeloupe"},
    {"code": "guyane", "name": "Guyane"},
    {"code": "france", "name": "France hexagonale"},
    {"code": "caraibe", "name": "Autre Caraïbe"},
    {"code": "diaspora", "name": "Diaspora monde"},
    {"code": "autre", "name": "Autre"},
]


@router.get("/onboarding/options")
async def onboarding_options():
    """Returns available options for the FREK Origin Story wizard."""
    poles = await db.poles.find({}, {"_id": 0}).to_list(50)
    return {
        "langs": [{"code": "fr", "name": "Français"},
                  {"code": "en", "name": "English"},
                  {"code": "kr", "name": "Kreyòl"}],
        "metiers": poles,  # each pole = career direction
        "territoires": TERRITOIRES,
    }


@router.post("/onboarding/complete", response_model=OnboardingResult)
async def onboarding_complete(
    inp: OnboardingInput, current: User = Depends(get_current_user),
):
    # 1) Validate pole
    pole = await db.poles.find_one({"code": inp.metier_vise}, {"_id": 0})
    if not pole:
        raise HTTPException(status_code=400, detail="Métier visé inconnu")
    if inp.lang not in ("fr", "en", "kr"):
        raise HTTPException(status_code=400, detail="Langue invalide")
    if not any(t["code"] == inp.territoire for t in TERRITOIRES):
        raise HTTPException(status_code=400, detail="Territoire invalide")

    # 2) Persist onboarding data
    await db.users.update_one(
        {"id": current.id},
        {"$set": {
            "lang": inp.lang,
            "metier_vise": inp.metier_vise,
            "territoire": inp.territoire,
            "objectif_perso": inp.objectif_perso.strip(),
            "onboarding_completed": True,
        }},
    )

    # 3) Emit 3 FREK-TIME signals (language / territory / objective)
    signals_emitted: List[str] = []
    for reason in ("language_selected", "territory_selected", "objective_set"):
        await frek_core.emit_signal(current.id, "FREK-TIME", {
            "onboarding_step": reason,
            "value": {
                "language_selected": inp.lang,
                "territory_selected": inp.territoire,
                "objective_set": inp.objectif_perso[:60],
            }[reason],
        })
        signals_emitted.append("FREK-TIME")

    # 4) Auto-award BADGE-DECOUVERTE (threshold=0) — user has 5 CC already from register
    await _award_threshold_badges(current.id, current.cc_credits)
    badge_earned = await db.badges.find_one({"code": "BADGE-DECOUVERTE"}, {"_id": 0})

    # 5) Recommend a first formation matching the pole (prefer one with modules,
    #    else fall back to any formation of this pole)
    formations = await db.formations.find({"pole": inp.metier_vise}, {"_id": 0}).to_list(50)
    formations.sort(key=lambda f: (0 if f.get("modules") else 1, f.get("code", "")))
    recommended_formation = formations[0] if formations else None
    if recommended_formation:
        recommended_formation = {
            "code": recommended_formation["code"],
            "name": recommended_formation["name"],
            "pole": recommended_formation["pole"],
            "pole_name": recommended_formation.get("pole_name"),
            "pole_color": recommended_formation.get("pole_color"),
            "duration_h": recommended_formation["duration_h"],
            "cc": recommended_formation["cc"],
            "description": recommended_formation.get("description", ""),
            "modules_count": len(recommended_formation.get("modules", [])),
        }

    # 6) Recommend + auto-accept a first mission matching the pole (any stade,
    #    prefer 'featured', else 'open'). Falls back to any mission if pole has none.
    missions_pool = await db.missions.find({"pole": inp.metier_vise}, {"_id": 0}).to_list(50)
    if not missions_pool:
        missions_pool = await db.missions.find({}, {"_id": 0}).to_list(50)
    missions_pool.sort(key=lambda m: (0 if m.get("status_type") == "featured" else 1, m.get("cc_reward", 0)))
    recommended_mission = missions_pool[0] if missions_pool else None
    if recommended_mission:
        existing = await db.user_missions.find_one({
            "user_id": current.id, "mission_code": recommended_mission["code"],
        })
        if not existing:
            await db.user_missions.insert_one({
                "id": str(uuid.uuid4()),
                "user_id": current.id,
                "mission_code": recommended_mission["code"],
                "status": "accepted",
                "accepted_at": utc_now_iso(),
                "source": "onboarding",
            })
            await frek_core.emit_signal(current.id, "FREK-MISSION", {
                "mission": recommended_mission["code"], "source": "onboarding",
            })

    # 7) Reload user for accurate public payload
    doc = await db.users.find_one({"id": current.id}, {"_id": 0})
    return OnboardingResult(
        user=user_public(User(**doc)),
        recommended_formation=recommended_formation,
        recommended_mission=recommended_mission,
        badge_earned=badge_earned,
        signals_emitted=signals_emitted,
    )



# ============ POLES + FORMATIONS ============
@router.get("/poles")
async def list_poles():
    poles = await db.poles.find({}, {"_id": 0}).to_list(50)
    return poles


@router.get("/formations")
async def list_formations():
    docs = await db.formations.find({}, {"_id": 0}).to_list(200)
    # Return summary shape (no modules for the list)
    return [{
        "code": d["code"], "name": d["name"], "pole": d["pole"],
        "pole_name": d.get("pole_name"), "pole_color": d.get("pole_color"),
        "duration_h": d["duration_h"], "stades": d["stades"],
        "cc": d["cc"], "badge_name": d["badge_name"],
        "description": d.get("description", ""),
        "modules_count": len(d.get("modules", [])),
    } for d in docs]


@router.get("/formations/{code}")
async def get_formation(code: str):
    doc = await db.formations.find_one({"code": code}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Formation introuvable")
    return doc


# ============ QUIZ ============
@router.get("/formations/{formation_code}/modules/{module_code}/quiz")
async def get_module_quiz(formation_code: str, module_code: str):
    doc = await db.formations.find_one({"code": formation_code}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Formation introuvable")
    mod = next((m for m in doc.get("modules", []) if m["code"] == module_code), None)
    if not mod:
        raise HTTPException(status_code=404, detail="Module introuvable")
    quiz = build_quiz(mod)
    # Return quiz WITHOUT correct flags to avoid leaking answers
    return {
        "module": mod,
        "quiz": [
            {
                "n": q["n"], "type": q["type"], "question": q["question"],
                "choices": [{"id": c["id"], "text": c["text"]} for c in q["choices"]],
            }
            for q in quiz
        ],
    }


@router.post("/formations/{formation_code}/modules/{module_code}/quiz/submit", response_model=QuizResult)
async def submit_module_quiz(
    formation_code: str, module_code: str,
    submission: QuizSubmission, current: User = Depends(get_current_user),
):
    doc = await db.formations.find_one({"code": formation_code}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Formation introuvable")
    mod = next((m for m in doc.get("modules", []) if m["code"] == module_code), None)
    if not mod:
        raise HTTPException(status_code=404, detail="Module introuvable")

    quiz = build_quiz(mod)
    result = evaluate(quiz, submission.answers)

    signal = mod.get("frek_signal", "FREK-WORK").split(" ")[0]
    cc_earned = 0
    if result["passed"]:
        # CC awarded = duration_h of the module (heuristic aligned with Master OS)
        cc_earned = int(mod.get("duration_h", 4))
        # Emit signal + increment user CC
        await frek_core.emit_signal(current.id, signal, {
            "formation": formation_code, "module": module_code, "score": result["score"],
        })
        await frek_core.emit_signal(current.id, "FREK-SCORE", {
            "score": result["score"], "module": module_code,
        })
        # persist module progress
        await db.progress.update_one(
            {"user_id": current.id, "module_code": module_code},
            {"$set": {
                "user_id": current.id, "formation_code": formation_code,
                "module_code": module_code, "completed": True,
                "score": result["score"], "completed_at": utc_now_iso(),
                "signal_emitted": signal,
            }},
            upsert=True,
        )
        # update CC + stade
        new_cc = current.cc_credits + cc_earned
        new_stade = frek_core.resolve_stade(new_cc)
        await db.users.update_one(
            {"id": current.id},
            {"$set": {"cc_credits": new_cc, "stade": new_stade}},
        )
        # award badges automatically if thresholds crossed
        await _award_threshold_badges(current.id, new_cc)

    return QuizResult(
        score=result["score"], passed=result["passed"],
        correct=result["correct"], total=result["total"],
        cc_earned=cc_earned, signal_emitted=signal if result["passed"] else "",
    )


async def _award_threshold_badges(user_id: str, cc: int) -> None:
    badges = await db.badges.find({"cc_threshold": {"$lte": cc}}, {"_id": 0}).to_list(200)
    for b in badges:
        exists = await db.user_badges.find_one({"user_id": user_id, "badge_code": b["code"]})
        if not exists:
            await db.user_badges.insert_one({
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "badge_code": b["code"],
                "earned_at": utc_now_iso(),
            })
            await frek_core.emit_signal(user_id, "FREK-CERT", {"badge": b["code"]})


# ============ BADGES ============
@router.get("/badges")
async def list_badges():
    return await db.badges.find({}, {"_id": 0}).to_list(200)


@router.get("/badges/mine")
async def my_badges(current: User = Depends(get_current_user)):
    mine = await db.user_badges.find({"user_id": current.id}, {"_id": 0}).to_list(200)
    codes = [x["badge_code"] for x in mine]
    all_badges = await db.badges.find({"code": {"$in": codes}}, {"_id": 0}).to_list(200)
    by_code = {b["code"]: b for b in all_badges}
    return [
        {**by_code[m["badge_code"]], "earned_at": m["earned_at"]}
        for m in mine if m["badge_code"] in by_code
    ]


# ============ MISSIONS ============
@router.get("/missions")
async def list_missions():
    return await db.missions.find({}, {"_id": 0}).to_list(200)


@router.post("/missions/{mission_code}/accept")
async def accept_mission(mission_code: str, current: User = Depends(get_current_user)):
    mission = await db.missions.find_one({"code": mission_code}, {"_id": 0})
    if not mission:
        raise HTTPException(status_code=404, detail="Mission introuvable")
    existing = await db.user_missions.find_one(
        {"user_id": current.id, "mission_code": mission_code}
    )
    if existing:
        return {"ok": True, "status": existing.get("status", "accepted")}
    await db.user_missions.insert_one({
        "id": str(uuid.uuid4()),
        "user_id": current.id,
        "mission_code": mission_code,
        "status": "accepted",
        "accepted_at": utc_now_iso(),
    })
    await frek_core.emit_signal(current.id, "FREK-MISSION", {"mission": mission_code})
    return {"ok": True, "status": "accepted"}


@router.post("/missions/{mission_code}/submit")
async def submit_mission(
    mission_code: str, current: User = Depends(get_current_user),
):
    mission = await db.missions.find_one({"code": mission_code}, {"_id": 0})
    if not mission:
        raise HTTPException(status_code=404, detail="Mission introuvable")
    await db.user_missions.update_one(
        {"user_id": current.id, "mission_code": mission_code},
        {"$set": {
            "user_id": current.id, "mission_code": mission_code,
            "status": "validated", "submitted_at": utc_now_iso(),
        }},
        upsert=True,
    )
    reward = int(mission.get("cc_reward", 0))
    new_cc = current.cc_credits + reward
    new_stade = frek_core.resolve_stade(new_cc)
    await db.users.update_one(
        {"id": current.id}, {"$set": {"cc_credits": new_cc, "stade": new_stade}}
    )
    await frek_core.emit_signal(current.id, "FREK-WORK", {"mission": mission_code})
    await _award_threshold_badges(current.id, new_cc)
    return {"ok": True, "cc_earned": reward, "new_stade": new_stade}


@router.get("/missions/mine")
async def my_missions(current: User = Depends(get_current_user)):
    return await db.user_missions.find(
        {"user_id": current.id}, {"_id": 0}
    ).to_list(200)


# ============ FREK PROFILE + PROGRESSION ============
@router.get("/frek/profile")
async def frek_profile(current: User = Depends(get_current_user)):
    signals = await db.frek_signals.find(
        {"user_id": current.id}, {"_id": 0}
    ).sort("ts", -1).to_list(200)

    progress = await db.progress.find(
        {"user_id": current.id, "completed": True}, {"_id": 0}
    ).to_list(500)

    badges = await db.user_badges.find(
        {"user_id": current.id}, {"_id": 0}
    ).to_list(50)

    # stage progression: percentage inside current stade band
    stade_bands = [("graine", 0), ("pousse", 10), ("racine", 50),
                   ("branches", 100), ("arbre", 150), ("foret", 300)]
    idx = next((i for i, (n, _) in enumerate(stade_bands) if n == current.stade), 0)
    lo = stade_bands[idx][1]
    hi = stade_bands[idx + 1][1] if idx + 1 < len(stade_bands) else lo + 200
    pct = 100 if hi <= lo else max(0, min(100, int((current.cc_credits - lo) * 100 / (hi - lo))))
    return {
        "user": user_public(current).model_dump(),
        "stade_progress_pct": pct,
        "stade_next_at": hi,
        "modules_completed": len(progress),
        "badges_count": len(badges),
        "signals": current.signals,
        "recent_signals": signals[:20],
    }


@router.get("/progression/summary")
async def progression_summary(current: User = Depends(get_current_user)):
    completed = await db.progress.count_documents(
        {"user_id": current.id, "completed": True}
    )
    total_modules_doc = await db.formations.aggregate([
        {"$project": {"count": {"$size": {"$ifNull": ["$modules", []]}}}},
        {"$group": {"_id": None, "total": {"$sum": "$count"}}},
    ]).to_list(1)
    total = (total_modules_doc[0]["total"] if total_modules_doc else 0) or 0
    global_pct = int((completed / total) * 100) if total else 0
    return {
        "completed_modules": completed,
        "total_modules": total,
        "global_pct": global_pct,
        "stade": current.stade,
        "cc_credits": current.cc_credits,
    }


# ============ MENTOR (CVLN Agent Factory client) ============
@router.get("/mentor/agents")
async def list_agents():
    return await agent_factory.list_available_agents()


@router.get("/mentor/session/{session_id}")
async def get_session(session_id: str, current: User = Depends(get_current_user)):
    doc = await db.mentor_conversations.find_one(
        {"user_id": current.id, "session_id": session_id}, {"_id": 0}
    )
    return doc or {"session_id": session_id, "messages": []}


@router.post("/mentor/chat")
async def mentor_chat(inp: MentorChatInput, current: User = Depends(get_current_user)):
    session_id = inp.session_id or f"mentor-{current.id}"
    doc = await db.mentor_conversations.find_one(
        {"user_id": current.id, "session_id": session_id}, {"_id": 0}
    )
    history = (doc or {}).get("messages", [])

    reply = await agent_factory.mentor_reply(
        user_frek_id=current.frek_id,
        display_name=current.display_name,
        session_id=session_id,
        message=inp.message,
        history=history,
        lang=current.lang,
    )

    new_messages = history + [
        {"role": "user", "content": inp.message, "ts": utc_now_iso()},
        {"role": "assistant", "content": reply, "ts": utc_now_iso()},
    ]
    await db.mentor_conversations.update_one(
        {"user_id": current.id, "session_id": session_id},
        {"$set": {
            "user_id": current.id, "session_id": session_id,
            "messages": new_messages, "updated_at": utc_now_iso(),
        }},
        upsert=True,
    )
    return {"session_id": session_id, "reply": reply}
