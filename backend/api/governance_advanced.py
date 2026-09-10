"""Advanced Professional Governance APIs (GOV-003/009/011)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import expert_cost_ledger, governance_notifications, professional_workspace

router = APIRouter(prefix="/governance-advanced", tags=["governance"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class CostEntryCreate(BaseModel):
    case_id: str
    expert_id: str
    intervention_type: str = Field(min_length=2, max_length=120)
    hours: float = Field(ge=0)
    amount_cents: int = Field(ge=0)
    currency: str = Field(min_length=3, max_length=3)
    evidence_refs: List[str] = Field(min_length=1)
    baseline_without_core_hours: Optional[float] = Field(default=None, ge=0)
    baseline_hourly_rate_cents: Optional[int] = Field(default=None, ge=0)
    note: Optional[str] = Field(default=None, max_length=4000)


class ChannelPreference(BaseModel):
    channels: List[str] = Field(min_length=1)


class NotificationCreate(BaseModel):
    subject_id: str = Field(min_length=1, max_length=240)
    kind: str = Field(min_length=2, max_length=120)
    payload: Dict[str, Any] = Field(default_factory=dict)
    criticality: str
    email: Optional[str] = None
    phone: Optional[str] = None
    channels: Optional[List[str]] = None


def _expert_key(x_cvln_expert_key: str | None = Header(default=None)) -> str:
    if not x_cvln_expert_key:
        raise HTTPException(status_code=401, detail="Expert credential required")
    return x_cvln_expert_key


@router.get("/expert-workspace/{case_id}")
async def expert_workspace(case_id: str, raw_key: str = Depends(_expert_key)):
    try:
        return await professional_workspace.get_workspace(raw_key=raw_key, case_id=case_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


@router.post("/expert-costs")
async def record_expert_cost(payload: CostEntryCreate, current: User = Admin):
    try:
        return await expert_cost_ledger.record_cost(actor_id=current.id, **payload.model_dump())
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/cases/{case_id}/cost-summary")
async def case_cost_summary(case_id: str, current: User = Admin):
    try:
        return await expert_cost_ledger.case_cost_summary(case_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/cost-reduction")
async def global_cost_reduction(current: User = Admin):
    return await expert_cost_ledger.global_cost_reduction_summary()


@router.put("/notification-preferences/{subject_id}")
async def set_notification_preferences(
    subject_id: str, payload: ChannelPreference, current: User = Admin
):
    try:
        return await governance_notifications.set_channel_preference(
            actor_id=current.id, subject_id=subject_id, channels=payload.channels
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/notifications/dispatch")
async def dispatch_notification(payload: NotificationCreate, current: User = Admin):
    try:
        return await governance_notifications.route_notification(
            actor_id=current.id, **payload.model_dump()
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
