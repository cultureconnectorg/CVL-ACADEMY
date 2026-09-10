"""Canonical Trust & Signature API (TRU-01..TRU-14)."""

from __future__ import annotations

from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import get_current_user, require_role
from models import User
from services import trust_signature

router = APIRouter(prefix="/trust/signatures", tags=["trust"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class SignerSpec(BaseModel):
    signer_user_id: str
    signer_frek_id: str
    signer_role: str


class SignatureRequestCreate(BaseModel):
    subject_type: str
    subject_id: str
    document_version_id: str
    document_hash: str = Field(min_length=64, max_length=64)
    required_signers: List[SignerSpec] = Field(min_length=1)
    evidence_refs: List[str] = Field(min_length=1)


class DelegateCreate(BaseModel):
    delegate_user_id: str
    delegate_frek_id: str
    delegate_role: str
    evidence_refs: List[str] = Field(min_length=1)


class RevokeCreate(BaseModel):
    evidence_refs: List[str] = Field(min_length=1)


class SignIntentCreate(BaseModel):
    actor_frek_id: str
    document_hash: str = Field(min_length=64, max_length=64)
    intent: str
    evidence_refs: List[str] = Field(default_factory=list)


class InvalidateCreate(BaseModel):
    replacement_version_id: Optional[str] = None
    replacement_hash: Optional[str] = Field(default=None, min_length=64, max_length=64)
    evidence_refs: List[str] = Field(min_length=1)


class EvidencePackCreate(BaseModel):
    evidence_node_ids: List[str] = Field(min_length=1)
    evidence_refs: List[str] = Field(min_length=1)


def _translate(exc: Exception):
    if isinstance(exc, LookupError):
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if isinstance(exc, PermissionError):
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("")
async def create_signature_request(
    payload: SignatureRequestCreate, current: User = Admin
):
    try:
        data = payload.model_dump()
        data["required_signers"] = [item.model_dump() for item in payload.required_signers]
        return await trust_signature.create_signature_request(actor_id=current.id, **data)
    except (LookupError, PermissionError, ValueError) as exc:
        _translate(exc)


@router.post("/{signature_request_id}/delegate/{authorization_id}")
async def delegate_signer(
    signature_request_id: str,
    authorization_id: str,
    payload: DelegateCreate,
    current: User = Admin,
):
    del signature_request_id
    try:
        return await trust_signature.delegate_signer_authority(
            actor_id=current.id, authorization_id=authorization_id, **payload.model_dump()
        )
    except (LookupError, PermissionError, ValueError) as exc:
        _translate(exc)


@router.post("/authorizations/{authorization_id}/revoke")
async def revoke_signer(
    authorization_id: str, payload: RevokeCreate, current: User = Admin
):
    try:
        return await trust_signature.revoke_signer_authority(
            actor_id=current.id,
            authorization_id=authorization_id,
            evidence_refs=payload.evidence_refs,
        )
    except (LookupError, PermissionError, ValueError) as exc:
        _translate(exc)


@router.post("/{signature_request_id}/sign")
async def sign(
    signature_request_id: str,
    payload: SignIntentCreate,
    current: User = Depends(get_current_user),
):
    try:
        return await trust_signature.sign_intent(
            actor_id=current.id,
            signature_request_id=signature_request_id,
            **payload.model_dump(),
        )
    except (LookupError, PermissionError, ValueError) as exc:
        _translate(exc)


@router.post("/evidence/{signature_id}/verify")
async def verify(signature_id: str, current: User = Admin):
    try:
        return await trust_signature.verify_signature(actor_id=current.id, signature_id=signature_id)
    except (LookupError, PermissionError, ValueError) as exc:
        _translate(exc)


@router.get("/{signature_request_id}/multisig-gate")
async def multisig_gate(signature_request_id: str, current: User = Admin):
    try:
        return await trust_signature.evaluate_multisignature(signature_request_id)
    except LookupError as exc:
        _translate(exc)


@router.post("/{signature_request_id}/invalidate")
async def invalidate(
    signature_request_id: str,
    payload: InvalidateCreate,
    current: User = Admin,
):
    try:
        return await trust_signature.invalidate_document_version(
            actor_id=current.id,
            signature_request_id=signature_request_id,
            **payload.model_dump(),
        )
    except (LookupError, PermissionError, ValueError) as exc:
        _translate(exc)


@router.post("/{signature_request_id}/evidence-pack")
async def evidence_pack(
    signature_request_id: str,
    payload: EvidencePackCreate,
    current: User = Admin,
):
    try:
        return await trust_signature.create_signature_evidence_pack(
            actor_id=current.id,
            signature_request_id=signature_request_id,
            **payload.model_dump(),
        )
    except (LookupError, PermissionError, ValueError) as exc:
        _translate(exc)
