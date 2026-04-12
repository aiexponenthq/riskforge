"""ExportEngine — dispatches to Exporter plugins; hashes and signs the output."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from riskforge.engine.audit import AuditEngine
from riskforge.models.rmf import RiskManagementFile
from riskforge.plugins.registry import PluginRegistry


class SchemaViolationError(RuntimeError):
    """Raised when an RMF document fails schema validation at export time."""


class ExportEngine:
    """Dispatches to registered Exporter plugins; signs and hashes the output."""

    DISCLOSURE_TEMPLATE = (
        "This document was produced using RiskForge v{version}, "
        "question bank version {qb_version}. "
        "It represents the team's documented risk assessment and has not been "
        "reviewed by a qualified legal professional. "
        "It does not constitute legal advice under the EU AI Act or any other regulation."
    )

    def __init__(self, registry: PluginRegistry, audit: AuditEngine) -> None:
        self._registry = registry
        self._audit = audit

    async def export(
        self,
        rmf: RiskManagementFile,
        fmt: str,
        output_path: Path,
        sign_with: Path | None = None,
    ) -> Path:
        # 1. Inject mandatory disclosure
        from importlib.metadata import version as pkg_version

        rmf.disclosure = self.DISCLOSURE_TEMPLATE.format(
            version=pkg_version("riskforge"),
            qb_version=rmf.register.question_bank_version,
        )

        # 2. Compute SHA-256 over canonical JSON (sha256_hash field = "")
        # by_alias=True ensures risk_register serialises as "register" per the schema
        rmf.sha256_hash = ""
        canonical = json.dumps(
            rmf.model_dump(mode="json", by_alias=True), sort_keys=True, separators=(",", ":")
        )
        rmf.sha256_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

        # 3. Validate against rmf.schema.json (raises SchemaViolationError on failure)
        self._validate_schema(rmf)

        # 4. Dispatch to exporter plugin
        exporter = self._registry.get_exporter(fmt)
        payload: bytes = exporter.render(rmf)

        # 5. Write to output path (chmod 600)
        output_path.write_bytes(payload)
        output_path.chmod(0o600)

        # 6. Optional Sigstore/PGP signing
        if sign_with:
            self._sign(output_path, sign_with)

        # 7. Emit audit log entry
        entry = await self._audit.record(
            "rmf.exported",
            system_id=str(rmf.register.system.id),
            payload={
                "export_id": str(rmf.id),
                "format": fmt,
                "sha256": rmf.sha256_hash,
            },
        )
        rmf.audit_entry_hash = entry.entry_hash

        return output_path

    def _validate_schema(self, rmf: RiskManagementFile) -> None:
        from importlib.resources import files

        import jsonschema

        schema_text = files("riskforge._data.schemas").joinpath("rmf.schema.json").read_text()
        schema = json.loads(schema_text)
        try:
            jsonschema.validate(rmf.model_dump(mode="json", by_alias=True), schema)
        except jsonschema.ValidationError as e:
            raise SchemaViolationError(f"RMF schema violation: {e.message}") from e

    def _sign(self, path: Path, key_path: Path) -> None:
        import subprocess

        subprocess.run(["gpg", "--detach-sign", "--armor", str(path)], check=True)
