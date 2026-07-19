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


class SigningError(RuntimeError):
    """Raised when detached signing of the exported file fails."""


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
        sign_with: str | None = None,
    ) -> Path:
        # 1. Inject mandatory disclosure
        from importlib.metadata import version as pkg_version

        rmf.disclosure = self.DISCLOSURE_TEMPLATE.format(
            version=pkg_version("riskforge"),
            qb_version=rmf.register.question_bank_version,
        )

        # 2. Self-verifying SHA-256 over the document CONTENT. The integrity and
        # provenance fields are blanked first: sha256_hash cannot cover itself;
        # audit_entry_hash is derived from this hash (its audit entry carries the
        # sha256, so it would be circular); signed_by is provenance carried by the
        # detached signature. `verify --file` blanks the same three before recomputing.
        # by_alias=True ensures risk_register serialises as "register" per the schema.
        rmf.sha256_hash = ""
        rmf.audit_entry_hash = ""
        rmf.signed_by = ""
        canonical = json.dumps(
            rmf.model_dump(mode="json", by_alias=True), sort_keys=True, separators=(",", ":")
        )
        rmf.sha256_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

        # 3. Validate against rmf.schema.json before recording anything.
        self._validate_schema(rmf)

        # 4. Link the export to the append-only audit chain, then carry the entry
        # hash back on the RMF so the written artefact references its audit record.
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
        rmf.signed_by = sign_with or ""

        # 5. Render + write the fully-populated document (chmod 600)
        exporter = self._registry.get_exporter(fmt)
        output_path.write_bytes(exporter.render(rmf))
        output_path.chmod(0o600)

        # 6. Optional PGP detached signature over the written file
        if sign_with:
            self._sign(output_path, sign_with)

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

    def _sign(self, path: Path, signer: str) -> None:
        """Create a detached, armored GPG signature with the caller-supplied key.

        `signer` is a GPG key identifier (email, key id, or fingerprint) passed via
        `--local-user`, so the signature carries the provenance the caller intended
        rather than GPG's default key. Failures raise SigningError with a clean message.
        """
        import shutil
        import subprocess

        if shutil.which("gpg") is None:
            raise SigningError("gpg is not installed; cannot sign. Install GnuPG or omit --sign.")
        try:
            subprocess.run(
                ["gpg", "--detach-sign", "--armor", "--local-user", signer, str(path)],
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as exc:
            detail = (exc.stderr or "").strip() or str(exc)
            raise SigningError(f"gpg signing with key '{signer}' failed: {detail}") from exc
