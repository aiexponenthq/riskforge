"""Export router."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from riskforge.server.auth import verify_token

router = APIRouter(tags=["exports"])


@router.post("/registers/{system_id}/export", dependencies=[Depends(verify_token)])
async def trigger_export(system_id: str, body: dict) -> dict:
    """Trigger an export for a system. Returns the export artefact metadata."""
    return {"message": "Not yet implemented — scaffold only"}
