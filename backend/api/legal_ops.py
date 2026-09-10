"""Legal P0 API for matters, review policy, contract lifecycle and native attestations."""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import get_current_user, require_role
from models import User
from services import legal_ops, native_attestation_verifier, proof_bridge

router = APIRouter(prefix="/legal", tags=["legal"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class MatterCreate(BaseModel):
    title: str = Field(min_length=3, max_length=240)
    matter_type: str = Field(min_length=2, max_length=80)
    jurisdiction: Optional[str] = Field(default=None, max_length=120)
    case_id: Optional[str] = Field(default=None, max_length=240)
    owner_id: Optional[str] = Field(default=None, max_length=240)
    risk_ids: List[str] = Field(default_factory=list)
    evidence_refs: List[str] = Field(default_factory=list)


class MatterState(BaseModel):
    status: str


class ReviewDecision(BaseModel):
    external_review_required: bool
    rationale: str = Field(min_length=3, max_length=4000)
    policy_ref: str = Field(min_length=1, max_length=240)
    evidence_refs: List[str] = Field(default_factory=list)


class ContractCreate(BaseModel):
    title: str = Field(min_length=3, max_length=240)
    contract_type: str = Field(min_length=2, max_length=80)
    counterparty: str = Field(min_length=2, max_length=240)
    matter_id: Optional[str] = None
    jurisdiction: Optional[str] = Field(default=None, max_length=120)
    starts_at: Optional[str] = None
    ends_at: Optional[str] = None
    renewal_at: Optional[str] = None
    document_id: Optional[str] = None
    evidence_refs: List[str] = Field(default_factory=list)


class ContractState(BaseModel):
    status: str
    evidence_refs: List[str] = Field(default_factory=list)


class SignerAuthorizationCreate(BaseModel):
    signer_user_id: str = Field(min_length=1, max_length=240)
    signer_frek_id: str = Field(min_length=1, max_length=240)
    signer_role: str = Field(min_length=2, max_length=120)
    evidence_refs: List[str] = Field(min_length=1)


class SignerAuthorizationRevoke(BaseModel):
    evidence_refs: List[str] = Field(min_length=1)


class NativeAttestationCreate(BaseModel):
    document_hash: str = Field(min_length=64, max_length=64)
    intent: str = Field(default="SIGN", min_length=4, max_length=16)
    evidence_refs: List[str] = Field(default_factory=list)


class NativeAttestationVerify(BaseModel):
    require_btc_anchor: bool = False


class SignatureDecisionCreate(BaseModel):
    policy_ref: str = Field(min_length=1, max_length=240)
    rationale: str = Field(min_length=3, max_length=4000)
    native_attestation_ids: List[str] = Field(default_factory=list)
    external_evidence_refs: List[str] = Field(default_factory=list)
    require_btc_anchor: bool = False


def _translate(exc: Exception):
    if isinstance(exc, LookupError):
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if isinstance(exc, PermissionError):
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    if isinstance(
        exc,
        (proof_bridge.FrekNotaryUnavailable, native_attestation_verifier.FrekProofUnavailable),
    ):
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/matters")
async def create_matter(payload: MatterCreate, current: User = Admin):
    return await legal_ops.create_legal_matter(actor_id=current.id, **payload.model_dump())


@router.patch("/matters/{matter_id}/state")
async def change_matter_state(matter_id: str, payload: MatterState, current: User = Admin):
    try:
        return await legal_ops.transition_legal_matter(
            actor_id=current.id, matter_id=matter_id, status=payload.status
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/matters/{matter_id}/review-decision")
async def review_decision(matter_id: str, payload: ReviewDecision, current: User = Admin):
    try:
        return await legal_ops.record_review_policy_decision(
            actor_id=current.id, matter_id=matter_id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/contracts")
async def create_contract(payload: ContractCreate, current: User = Admin):
    try:
        return await legal_ops.create_contract(actor_id=current.id, **payload.model_dump())
    except LookupError as exc:
        _translate(exc)


@router.patch("/contracts/{contract_id}/state")
async def change_contract_state(
    contract_id: str, payload: ContractState, current: User = Admin
):
    try:
        return await legal_ops.transition_contract(
            actor_id=current.id,
            contract_id=contract_id,
            status=payload.status,
            evidence_refs=payload.evidence_refs,
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/contracts/{contract_id}/signers")
async def authorize_signer(
    contract_id: str, payload: SignerAuthorizationCreate, current: User = Admin
):
    try:
        return await legal_ops.authorize_contract_signer(
            actor_id=current.id, contract_id=contract_id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.patch("/contracts/signers/{authorization_id}/revoke")
async def revoke_signer(
    authorization_id: str,
    payload: SignerAuthorizationRevoke,
    current: User = Admin,
):
    try:
        return await legal_ops.revoke_contract_signer(
            actor_id=current.id,
            authorization_id=authorization_id,
            evidence_refs=payload.evidence_refs,
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/contracts/{contract_id}/native-attestation")
async def native_attestation(
    contract_id: str,
    payload: NativeAttestationCreate,
    current: User = Depends(get_current_user),
):
    try:
        return await proof_bridge.create_contract_native_attestation(
            actor_id=current.id,
            actor_frek_id=current.frek_id,
            contract_id=contract_id,
            **payload.model_dump(),
        )
    except (
        LookupError,
        ValueError,
        PermissionError,
        proof_bridge.FrekNotaryUnavailable,
    ) as exc:
        _translate(exc)


@router.get("/contracts/{contract_id}/native-attestations")
async def list_native_attestations(contract_id: str, current: User = Admin):
    try:
        return await native_attestation_verifier.list_contract_attestations(contract_id)
    except LookupError as exc:
        _translate(exc)


@router.post("/native-attestations/{attestation_id}/verify")
async def verify_native_attestation(
    attestation_id: str,
    payload: NativeAttestationVerify,
    current: User = Admin,
):
    try:
        return await native_attestation_verifier.verify_native_attestation(
            actor_id=current.id,
            attestation_id=attestation_id,
            require_btc_anchor=payload.require_btc_anchor,
        )
    except (LookupError, native_attestation_verifier.FrekProofUnavailable) as exc:
        _translate(exc)


@router.post("/contracts/{contract_id}/signature-decision")
async def signature_decision(
    contract_id: str,
    payload: SignatureDecisionCreate,
    current: User = Admin,
):
    """Human Authority gate before an APPROVED contract may become SIGNED."""
    try:
        return await legal_ops.record_signature_decision(
            actor_id=current.id,
            contract_id=contract_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)
