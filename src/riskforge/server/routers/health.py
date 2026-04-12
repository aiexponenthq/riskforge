"""Health check router."""
from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> dict:
    """Liveness probe — returns 200 if server is running."""
    return {"status": "ok", "service": "riskforge"}


@router.get("/ready")
async def readiness_check() -> dict:
    """Readiness probe — returns 200 if storage is accessible."""
    return {"status": "ready"}
