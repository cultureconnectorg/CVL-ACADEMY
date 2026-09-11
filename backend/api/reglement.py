"""CVLN Academy regulation acceptance and signature evidence."""

from __future__ import annotations

import hashlib
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import get_current_user
from db import db, utc_now_iso
from models import User

router = APIRouter(prefix="/reglement", tags=["reglement"])

REGLEMENT_VERSION = "2.0-2026-09"
REGLEMENT_CONTENT_HASH = "cvln-academy-reglement-v2-2026-09"


class SignatureInput(BaseModel):
    accepted: bool
    signer_name: str = Field(min_length=1, max_length=120)
    signature_png: str = Field(min_length=100, max_length=350000)
    version: str
    content_hash: str


def _record_id(user_id: str) -> str:
    """Deterministic id: one immutable acceptance per user and regulation version."""
    return f"{user_id}:{REGLEMENT_VERSION}"


@router.get("/status")
async def status(current: User = Depends(get_current_user)):
    record = await db.reglement_signatures.find_one(
        {"_id": _record_id(current.id)},
        {"signature_png": 0},
    )
    return {
        "signed": bool(record),
        "version": REGLEMENT_VERSION,
        "content_hash": REGLEMENT_CONTENT_HASH,
        "signed_at": record.get("signed_at") if record else None,
    }


@router.post("/sign")
async def sign(inp: SignatureInput, current: User = Depends(get_current_user)):
    if not inp.accepted:
        raise HTTPException(status_code=400, detail="Vous devez accepter le règlement")
    if inp.version != REGLEMENT_VERSION or inp.content_hash != REGLEMENT_CONTENT_HASH:
        raise HTTPException(status_code=409, detail="Le règlement a changé. Rechargez la page.")
    if not inp.signature_png.startswith("data:image/png;base64,"):
        raise HTTPException(status_code=400, detail="Signature invalide")
    if inp.signer_name.strip().casefold() != current.display_name.strip().casefold():
        raise HTTPException(status_code=400, detail="Le nom doit correspondre au compte connecté")

    record_id = _record_id(current.id)
    existing = await db.reglement_signatures.find_one(
        {"_id": record_id}, {"signature_png": 0}
    )
    if existing:
        return {
            "signed": True,
            "version": REGLEMENT_VERSION,
            "signed_at": existing["signed_at"],
        }

    signature_hash = hashlib.sha256(inp.signature_png.encode("utf-8")).hexdigest()
    signed_at = utc_now_iso()
    record = {
        "_id": record_id,
        "user_id": current.id,
        "frek_id": current.frek_id,
        "signer_name": current.display_name,
        "version": REGLEMENT_VERSION,
        "content_hash": REGLEMENT_CONTENT_HASH,
        "signature_png": inp.signature_png,
        "signature_hash": signature_hash,
        "signed_at": signed_at,
        "capture_method": "web_signature_pad",
    }
    await db.reglement_signatures.update_one(
        {"_id": record_id},
        {"$setOnInsert": record},
        upsert=True,
    )

    persisted = await db.reglement_signatures.find_one(
        {"_id": record_id}, {"signature_png": 0}
    )
    return {
        "signed": True,
        "version": REGLEMENT_VERSION,
        "signed_at": persisted["signed_at"] if persisted else signed_at,
    }
