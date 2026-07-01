"""Liveness/readiness endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas import HealthStatus

router = APIRouter(tags=["health"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.get("/health", response_model=HealthStatus)
async def health(session: SessionDep) -> HealthStatus:
    """Report service health, including database connectivity."""
    try:
        await session.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False
    return HealthStatus(status="ok" if db_ok else "degraded", database=db_ok)
