"""AuditEntry and AuditActor models."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, Field


class AuditActor(BaseModel):
    type: Literal["human", "ci", "api"]  # classification of the triggering entity
    identity: str  # email, CI job name, API key fingerprint, or "anonymous"


class AuditEntry(BaseModel):
    """
    A single immutable entry in the tamper-evident audit chain.

    Entries are SHA-256 chained: each entry_hash covers the entry's payload
    plus prev_hash, creating a linked list that makes undetected tampering
    infeasible.  The chain is stored as append-only JSONL in audit.jsonl.
    """

    seq: int = Field(..., ge=0)  # monotonically increasing, 0-based
    event: str  # e.g. "system.created", "register.updated", "rmf.exported"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    actor: AuditActor
    system_id: str  # str(UUID) or "" for project-level events
    payload: dict = Field(default_factory=dict)  # event-specific structured data
    prev_hash: str = ""  # entry_hash of the preceding entry; "" for seq=0
    entry_hash: str = ""  # SHA-256(canonical_json(entry, entry_hash excluded))
