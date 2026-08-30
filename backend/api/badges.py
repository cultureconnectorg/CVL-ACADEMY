"""Badges — catalogue + earned-by-me."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from auth import get_current_user
from db import db
from models import User

router = APIRouter(prefix="/badges", tags=["badges"])


@router.get("")
async def list_badges():
    return await db.badges.find({}, {"_id": 0}).to_list(200)


@router.get("/mine")
async def my_badges(current: User = Depends(get_current_user)):
    mine = await db.user_badges.find({"user_id": current.id}, {"_id": 0}).to_list(200)
    codes = [x["badge_code"] for x in mine]
    all_badges = await db.badges.find({"code": {"$in": codes}}, {"_id": 0}).to_list(200)
    by_code = {b["code"]: b for b in all_badges}
    return [
        {**by_code[m["badge_code"]], "earned_at": m["earned_at"]}
        for m in mine
        if m["badge_code"] in by_code
    ]
