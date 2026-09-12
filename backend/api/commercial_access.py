"""FastAPI dependency for commercial learning access."""

from __future__ import annotations

from fastapi import Depends, HTTPException, Request

from auth import get_current_user
from commercial import has_commercial_access
from models import User


async def require_commercial_learning_access(
    request: Request,
    current: User = Depends(get_current_user),
) -> None:
    formation_code = request.path_params.get("formation_code")
    if not formation_code:
        return
    if not await has_commercial_access(current.id, formation_code):
        raise HTTPException(status_code=402, detail="COMMERCIAL_ENTITLEMENT_REQUIRED")
