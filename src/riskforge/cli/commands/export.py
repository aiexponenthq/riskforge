"""riskforge export — export the risk management file."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Optional  # noqa: UP007 — Typer 0.12.3 compat

import typer
from rich.console import Console

console = Console()


def cmd(
    system_id: str = typer.Argument(..., help="System ID to export"),
    fmt: str = typer.Option("json", "--format", "-f", help="Export format: json, pdf, markdown"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file path"),
    project_dir: Path = typer.Option(Path("."), "--project-dir"),
    sign: Optional[Path] = typer.Option(None, "--sign", help="PGP key path for signing"),
    force: bool = typer.Option(False, "--force", help="Skip validation gates"),
) -> None:
    """Export the Risk Management File to JSON, PDF, or Markdown.

    The export is SHA-256 signed, schema-validated, and linked to the
    audit trail. The output file is written with chmod 600.
    """

    from riskforge.engine.audit import AuditEngine
    from riskforge.engine.export import ExportEngine
    from riskforge.engine.validate import ValidateEngine
    from riskforge.models.audit import AuditActor
    from riskforge.models.rmf import RiskManagementFile
    from riskforge.plugins.registry import PluginRegistry
    from riskforge.storage.filesystem import FileStore

    store = FileStore(project_dir)
    
    # Pre-flight continuity check
    is_valid, violations = asyncio.run(store.verify_chain())
    if not is_valid:
        console.print(f"[red]✗[/red] Audit chain is corrupt: {violations}")
        raise typer.Exit(2)

    register = asyncio.run(store.read_register(system_id))

    # Run validation gates unless --force
    if not force:
        val_engine = ValidateEngine()
        results = val_engine.run(register)
        if val_engine.has_failures(results):
            console.print(
                "[red]✗[/red] Validation failed. Run `riskforge validate` for details "
                "or use --force to override."
            )
            raise typer.Exit(1)

    # Build the RMF artefact
    import datetime

    rmf = RiskManagementFile(
        register=register,
        generated_at=datetime.datetime.now(datetime.UTC),
    )

    # Determine output path
    if output is None:
        ext = {"json": "json", "pdf": "pdf", "markdown": "md"}.get(fmt, fmt)
        export_id = str(rmf.id)[:8]
        output = project_dir / f"rmf-{system_id[:8]}-{export_id}.{ext}"

    # Load registry and run export
    registry = PluginRegistry()
    registry.load_all()

    actor = AuditActor(type="human", identity="cli")
    audit = AuditEngine(store, actor)
    engine = ExportEngine(registry, audit)

    result_path = asyncio.run(engine.export(rmf, fmt, output, sign_with=sign))

    console.print(f"[green]✓[/green] Exported: [bold]{result_path}[/bold]")
    console.print(f"  SHA-256: [dim]{rmf.sha256_hash}[/dim]")
