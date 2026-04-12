"""Webhook router — incoming events from upstream tools."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from riskforge.server.auth import verify_token

router = APIRouter(tags=["webhooks"])


@router.post("/webhooks/rag-benchmarking", dependencies=[Depends(verify_token)])
async def rag_benchmarking_webhook(body: dict) -> dict:
    """Receive a rag-benchmarking report and import risk items."""
    return {"message": "Not yet implemented — scaffold only"}


@router.post("/webhooks/traceforge", dependencies=[Depends(verify_token)])
async def traceforge_webhook(body: dict) -> dict:
    """Receive a TraceForge report and import risk items."""
    return {"message": "Not yet implemented — scaffold only"}
