"""AuditEngine — append-only, hash-chained audit log management."""
from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime

from riskforge.models.audit import AuditActor, AuditEntry
from riskforge.storage.base import StorageBackend


class AuditChainCorruptError(RuntimeError):
    """Raised when the audit chain fails pre-write validation."""


class AuditEngine:
    """Manages the append-only, hash-chained audit log.

    Every state mutation must go through record(). The chain is validated
    before every write — any tampering is detected before a new entry is appended.
    Exit code 2 is the contract for riskforge verify failures (CI-detectable).
    """

    def __init__(self, storage: StorageBackend, actor: AuditActor) -> None:
        self._storage = storage
        self._actor = actor

    async def _last_entry_hash(self) -> str:
        last = "0000000000"
        async for entry in self._storage.read_audit():
            last = entry.entry_hash
        return last

    async def _next_seq(self) -> int:
        last = 0
        async for entry in self._storage.read_audit():
            last = entry.seq
        return last + 1

    async def record(self, event: str, system_id: str, payload: dict) -> AuditEntry:
        """Validates chain continuity BEFORE writing, then appends."""
        is_valid, violations = await self._storage.verify_chain()
        if not is_valid:
            raise AuditChainCorruptError(
                f"Audit chain corrupt before write: {violations}. "
                "Run `riskforge verify` to diagnose."
            )
        prev_hash = await self._last_entry_hash()
        seq = await self._next_seq()
        entry = AuditEntry(
            seq=seq,
            event=event,
            timestamp=datetime.now(UTC),
            actor=self._actor,
            system_id=system_id,
            payload=payload,
            prev_hash=prev_hash,
            entry_hash="",  # computed below
        )
        entry.entry_hash = self._compute_hash(prev_hash, entry)
        await self._storage.append_audit(entry)
        return entry

    @staticmethod
    def _compute_hash(prev_hash: str, entry: AuditEntry) -> str:
        data = entry.model_dump(mode="json")
        data["entry_hash"] = ""
        canonical = json.dumps(
            {"prev_hash": prev_hash, **data}, sort_keys=True, separators=(",", ":")
        )
        return hashlib.sha256(canonical.encode()).hexdigest()
