"""Mentor IA — CVLN Agent Factory client (local fallback: Anthropic SDK)."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from auth import get_current_user
from db import db, utc_now_iso
from models import MentorChatInput, User
from services.agent_factory import agent_factory

router = APIRouter(prefix="/mentor", tags=["mentor"])


@router.get("/agents")
async def list_agents():
    return await agent_factory.list_available_agents()


@router.get("/session/{session_id}")
async def get_session(session_id: str, current: User = Depends(get_current_user)):
    doc = await db.mentor_conversations.find_one(
        {"user_id": current.id, "session_id": session_id}, {"_id": 0}
    )
    return doc or {"session_id": session_id, "messages": []}


@router.post("/chat")
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
        {
            "$set": {
                "user_id": current.id,
                "session_id": session_id,
                "messages": new_messages,
                "updated_at": utc_now_iso(),
            }
        },
        upsert=True,
    )
    return {"session_id": session_id, "reply": reply}
