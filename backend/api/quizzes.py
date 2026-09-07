"""Module quiz — get (answers hidden) + submit (scored, gated by LX v2 phases)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from auth import get_current_user
from badges_engine import award_threshold_badges
from db import db, utc_now_iso
from lx import prereqs_before_quiz_ready
from models import QuizResult, QuizSubmission, User
from quiz import build_quiz, evaluate
from services.frek_core import frek_core

router = APIRouter(
    prefix="/formations/{formation_code}/modules/{module_code}", tags=["quiz"]
)


@router.get("/quiz")
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
                "n": q["n"],
                "type": q["type"],
                "question": q["question"],
                "choices": [{"id": c["id"], "text": c["text"]} for c in q["choices"]],
            }
            for q in quiz
        ],
    }


@router.post("/quiz/submit", response_model=QuizResult)
async def submit_module_quiz(
    formation_code: str,
    module_code: str,
    submission: QuizSubmission,
    current: User = Depends(get_current_user),
):
    doc = await db.formations.find_one({"code": formation_code}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Formation introuvable")
    mod = next((m for m in doc.get("modules", []) if m["code"] == module_code), None)
    if not mod:
        raise HTTPException(status_code=404, detail="Module introuvable")

    # LX v2 gate — quiz is a validation step, not a shortcut. All learning
    # phases must be done first.
    p = await db.progress.find_one(
        {"user_id": current.id, "module_code": module_code},
        {"_id": 0},
    )
    ready, missing = prereqs_before_quiz_ready(p or {})
    if not ready:
        raise HTTPException(
            status_code=400,
            detail=f"Complète d'abord les phases : {', '.join(missing)}.",
        )

    quiz = build_quiz(mod)
    result = evaluate(quiz, submission.answers)

    signal = mod.get("frek_signal", "FREK-WORK").split(" ")[0]
    cc_earned = 0
    first_pass = False

    # Attempt count + latest score are recorded on every submission,
    # pass or fail — a real pedagogical re-attempt is always allowed
    # and always tracked.
    await db.progress.update_one(
        {"user_id": current.id, "module_code": module_code},
        {
            "$inc": {"quiz_attempts": 1},
            "$set": {
                "user_id": current.id,
                "formation_code": formation_code,
                "module_code": module_code,
                "quiz_score": result["score"],
            },
        },
        upsert=True,
    )

    if result["passed"]:
        # ECON-02 (Audit Chirurgical 2026-09-07) — the first pass credits
        # CC exactly once; a further passing re-attempt on an
        # already-passed quiz updates the recorded score above but must
        # never re-credit. The transition itself
        # (quiz_passed != True -> True) is the concurrency guard, same
        # compare-and-swap pattern as ECON-01's mission fix: `$ne: True`
        # matches both a missing field (first-ever attempt) and an
        # explicit `False`, so under real concurrency at most one
        # caller's filter can still match by the time it executes.
        cas = await db.progress.update_one(
            {
                "user_id": current.id,
                "module_code": module_code,
                "quiz_passed": {"$ne": True},
            },
            {"$set": {"quiz_passed": True, "quiz_passed_at": utc_now_iso()}},
        )
        first_pass = cas.modified_count == 1

        if first_pass:
            cc_earned = int(mod.get("duration_h", 4))
            await frek_core.emit_signal(
                current.id,
                signal,
                {
                    "formation": formation_code,
                    "module": module_code,
                    "score": result["score"],
                },
            )
            await frek_core.emit_signal(
                current.id,
                "FREK-SCORE",
                {
                    "score": result["score"],
                    "module": module_code,
                },
            )
            new_cc, _new_stade = await frek_core.credit_cc(current.id, cc_earned)
            await award_threshold_badges(current.id, new_cc)

    return QuizResult(
        score=result["score"],
        passed=result["passed"],
        correct=result["correct"],
        total=result["total"],
        cc_earned=cc_earned,
        signal_emitted=signal if first_pass else "",
    )
