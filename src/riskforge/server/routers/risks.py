"""Risk item CRUD router."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from riskforge.server.auth import verify_token

router = APIRouter(tags=["risks"])


@router.get("/registers/{system_id}/risks", dependencies=[Depends(verify_token)])
async def list_risks(system_id: str) -> dict:
    """List all risk items for a system."""
    return {"system_id": system_id, "risks": [], "message": "Not yet implemented — scaffold only"}


@router.post("/registers/{system_id}/risks", dependencies=[Depends(verify_token)])
async def create_risk(system_id: str, body: dict) -> dict:
    """Create a new risk item."""
    return {"message": "Not yet implemented — scaffold only"}
