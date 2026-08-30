"""CVLN Wallet API — balance/history + Apple/Google Wallet pass payloads."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends

from auth import get_current_user
from models import User
from wallet import (
    WalletSummary,
    WalletTransaction,
    build_apple_pass_payload,
    build_google_pass_payload,
    get_summary,
    list_transactions,
)

router = APIRouter(prefix="/wallet", tags=["wallet"])


@router.get("/me", response_model=WalletSummary)
async def my_wallet(current: User = Depends(get_current_user)):
    return await get_summary(current.id)


@router.get("/transactions", response_model=List[WalletTransaction])
async def my_transactions(current: User = Depends(get_current_user)):
    return await list_transactions(current.id)


@router.get("/pass/apple")
async def apple_pass(current: User = Depends(get_current_user)):
    summary = await get_summary(current.id)
    return {
        "status": "unsigned",
        "note": "Pass data only — a real .pkpass needs an Apple Developer WWDR certificate + Pass Type ID.",
        "payload": build_apple_pass_payload(
            current.frek_id, current.display_name, summary.account
        ),
    }


@router.get("/pass/google")
async def google_pass(current: User = Depends(get_current_user)):
    summary = await get_summary(current.id)
    return {
        "status": "unsigned",
        "note": "Pass data only — a real save link needs a Google Wallet Issuer account to sign the JWT.",
        "payload": build_google_pass_payload(
            current.frek_id, current.display_name, summary.account
        ),
    }
