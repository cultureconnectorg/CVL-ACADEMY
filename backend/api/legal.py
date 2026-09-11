"""Legal gate: versioned acknowledgement + signature evidence."""

from __future__ import annotations

import hashlib
import re
import uuid
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from auth import get_current_user
from db import db, utc_now_iso
from legal_policy import (
    DOCUMENT_BY_ID,
    LEGAL_BUNDLE_VERSION,
    PUBLIC_LEGAL_DOCUMENTS,
    REQUIRED_DOCUMENT_IDS,
)
from models import User

router = APIRouter(prefix="/legal", tags=["legal"])

_SIGNATURE_RE = re.compile(r"^data:image/png;base64,[A-Za-z0-9+/=\r\n]+$")
MAX_SIGNATURE_DATA_URL = 350_000


class LegalAcceptanceInput(BaseModel):
    documents: Dict[str, str] = Field(default_factory=dict)
    signature_data_url: str = Field(min_length=100, max_length=MAX_SIGNATURE_DATA_URL)
    signer_name: str = Field(min_length=1, max_length=120)


async def _legal_state(user_id: str) -> dict:
    doc = await db.users.find_one(
        {"id": user_id},
        {"_id": 0, "legal_bundle_version": 1, "legal_accepted_at": 1, "legal_acceptance_id": 1},
    )
    doc = doc or {}
    accepted = doc.get("legal_bundle_version") == LEGAL_BUNDLE_VERSION
    return {
        "accepted": accepted,
        "accepted_at": doc.get("legal_accepted_at") if accepted else None,
        "acceptance_id": doc.get("legal_acceptance_id") if accepted else None,
    }


async def require_legal_acceptance(current: User = Depends(get_current_user)) -> User:
    """Fail closed when the learner has not signed the current legal bundle."""
    state = await _legal_state(current.id)
    if not state["accepted"]:
        raise HTTPException(
            status_code=428,
            detail={
                "code": "LEGAL_ACCEPTANCE_REQUIRED",
                "message": "Le bundle juridique Academy doit être accepté avant de continuer.",
                "bundle_version": LEGAL_BUNDLE_VERSION,
            },
        )
    return current


@router.get("/requirements")
async def legal_requirements(current: User = Depends(get_current_user)):
    state = await _legal_state(current.id)
    return {
        "bundle_version": LEGAL_BUNDLE_VERSION,
        "documents": PUBLIC_LEGAL_DOCUMENTS,
        **state,
    }


@router.post("/accept")
async def accept_legal_bundle(
    inp: LegalAcceptanceInput,
    request: Request,
    current: User = Depends(get_current_user),
):
    if not _SIGNATURE_RE.match(inp.signature_data_url):
        raise HTTPException(status_code=400, detail="Signature invalide")

    expected = {doc_id: DOCUMENT_BY_ID[doc_id]["version"] for doc_id in REQUIRED_DOCUMENT_IDS}
    if inp.documents != expected:
        raise HTTPException(
            status_code=409,
            detail="Le bundle juridique a changé. Rechargez les documents avant de signer.",
        )

    signer_name = " ".join(inp.signer_name.split()).strip()
    if not signer_name:
        raise HTTPException(status_code=400, detail="Nom du signataire requis")

    accepted_at = utc_now_iso()
    signature_sha256 = hashlib.sha256(inp.signature_data_url.encode("utf-8")).hexdigest()
    user_agent = (request.headers.get("user-agent") or "")[:500]
    client_host = request.client.host if request.client else "unknown"

    # Raw IP is intentionally not retained here. It participates in a one-way
    # evidence fingerprint together with the signed bundle and request metadata.
    evidence_fingerprint = hashlib.sha256(
        "|".join(
            [current.id, LEGAL_BUNDLE_VERSION, accepted_at, user_agent, client_host, signature_sha256]
        ).encode("utf-8")
    ).hexdigest()

    acceptance_id = str(uuid.uuid4())
    record = {
        "id": acceptance_id,
        "user_id": current.id,
        "frek_id": current.frek_id,
        "email": str(current.email),
        "signer_name": signer_name,
        "bundle_version": LEGAL_BUNDLE_VERSION,
        "documents": PUBLIC_LEGAL_DOCUMENTS,
        "accepted_versions": expected,
        "accepted_at": accepted_at,
        "signature_data_url": inp.signature_data_url,
        "signature_sha256": signature_sha256,
        "evidence_fingerprint": evidence_fingerprint,
        "user_agent": user_agent,
        "source": "academy_web_legal_gate",
        "revoked": False,
    }

    await db.legal_acceptances.insert_one(record)
    await db.users.update_one(
        {"id": current.id},
        {
            "$set": {
                "legal_bundle_version": LEGAL_BUNDLE_VERSION,
                "legal_accepted_at": accepted_at,
                "legal_acceptance_id": acceptance_id,
            }
        },
    )

    return {
        "accepted": True,
        "bundle_version": LEGAL_BUNDLE_VERSION,
        "accepted_at": accepted_at,
        "acceptance_id": acceptance_id,
        "evidence_fingerprint": evidence_fingerprint,
        "signature_sha256": signature_sha256,
    }
