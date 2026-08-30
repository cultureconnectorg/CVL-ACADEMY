"""AI assistants API — one endpoint, four personas (rule 12)."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from auth import get_current_user
from models import User
from services.ai_assistant import ASSISTANT_PERSONAS, assistant_reply, can_use_persona

router = APIRouter(prefix="/assistants", tags=["assistants"])


class AssistantChatInput(BaseModel):
    session_id: str
    message: str


@router.get("")
async def list_assistants(current: User = Depends(get_current_user)) -> List[dict]:
    return [
        {"persona": persona, "label": cfg["label"], "description": cfg["description"]}
        for persona, cfg in ASSISTANT_PERSONAS.items()
        if can_use_persona(current, persona)
    ]


@router.post("/{persona}/chat")
async def chat_with_assistant(
    persona: str, inp: AssistantChatInput, current: User = Depends(get_current_user)
):
    if persona not in ASSISTANT_PERSONAS:
        raise HTTPException(status_code=404, detail="Assistant inconnu")
    if not can_use_persona(current, persona):
        raise HTTPException(
            status_code=403, detail="Cet assistant n'est pas disponible pour votre rôle"
        )
    reply = await assistant_reply(persona, current, inp.session_id, inp.message)
    return {"persona": persona, "session_id": inp.session_id, "reply": reply}
