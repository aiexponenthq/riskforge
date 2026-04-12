"""riskforge verify — verify audit chain integrity."""

from __future__ import annotations

import asyncio
from pathlib import Path

import typer
from rich.console import Console

console = Console()


def cmd(
    project_dir: Path = typer.Option(Path("."), "--project-dir"),
    file: Path = typer.Option(None, "--file", "-f", help="rmf.json to verify"),
) -> None:
    """Verify audit chain integrity. Exits 2 if tampered or corrupt.

    Exit codes:
      0 — chain valid, no tampering detected
      1 — unexpected error
      2 — chain corrupt or tampered (CI-detectable)
    """
    from riskforge.storage.filesystem import FileStore

    store = FileStore(project_dir)
    is_valid, violations = asyncio.run(store.verify_chain())

    if is_valid:
        console.print("[green]✓[/green] Audit chain verified — no tampering detected.")
        raise typer.Exit(0)
    else:
        console.print("[red]✗[/red] Audit chain CORRUPT. Tampering or corruption detected:")
        for v in violations:
            console.print(f"  [red]•[/red] {v}")
        raise typer.Exit(2)  # Exit code 2: detectable by CI pipelines
