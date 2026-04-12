"""Risk register CRUD router."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from riskforge.server.auth import verify_token

router = APIRouter(tags=["registers"])


@router.get("/registers", dependencies=[Depends(verify_token)])
async def list_registers() -> dict:
    """List all risk registers in the project."""
    return {"registers": [], "message": "Not yet implemented — scaffold only"}


@router.get("/registers/{system_id}", dependencies=[Depends(verify_token)])
async def get_register(system_id: str) -> dict:
    """Get a specific risk register by system ID."""
    return {"system_id": system_id, "message": "Not yet implemented — scaffold only"}
