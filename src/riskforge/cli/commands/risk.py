"""riskforge risk — risk item management subcommands."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Optional  # noqa: UP007 — Typer 0.12.3 compat

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Manage risk items: list, add, edit, accept, score.")
console = Console()


@app.command("list")
def list_risks(
    system_id: str = typer.Argument(..., help="System ID"),
    project_dir: Path = typer.Option(Path("."), "--project-dir"),
    dimension: Optional[str] = typer.Option(None, "--dimension", "-d"),
) -> None:
    """List all risk items for a system."""
    from riskforge.models.risk import RiskDimension
    from riskforge.storage.filesystem import FileStore

    store = FileStore(project_dir)
    register = asyncio.run(store.read_register(system_id))

    dim_filter = RiskDimension(dimension) if dimension else None
    items = [i for i in register.items if dim_filter is None or i.dimension == dim_filter]

    table = Table(title=f"Risk Items — {system_id}")
    table.add_column("ID", style="dim", max_width=8)
    table.add_column("Dimension")
    table.add_column("Title", max_width=40)
    table.add_column("Score")
    table.add_column("Band")
    table.add_column("Accepted")

    for item in items:
        band_colour = {"low": "green", "medium": "yellow", "high": "orange1", "critical": "red"}
        table.add_row(
            str(item.id)[:8],
            item.dimension.value,
            item.title[:40],
            str(item.risk_score),
            f"[{band_colour.get(item.risk_band, 'white')}]{item.risk_band}[/]",
            "Yes" if item.accepted else "No",
        )

    console.print(table)


@app.command("accept")
def accept_risk(
    system_id: str = typer.Argument(..., help="System ID"),
    risk_id: str = typer.Argument(..., help="Risk item ID (or first 8 chars)"),
    rationale: str = typer.Option(..., "--rationale", "-r", help="Acceptance rationale"),
    project_dir: Path = typer.Option(Path("."), "--project-dir"),
) -> None:
    """Accept a risk item with a documented rationale."""
    from riskforge.engine.audit import AuditEngine
    from riskforge.engine.risk import RiskEngine
    from riskforge.models.audit import AuditActor
    from riskforge.storage.filesystem import FileStore

    store = FileStore(project_dir)
    actor = AuditActor(type="human", identity="cli")
    audit = AuditEngine(store, actor)
    engine = RiskEngine(store, audit)

    item = asyncio.run(engine.accept_risk(system_id, risk_id, rationale, "cli"))
    console.print(f"[green]✓[/green] Risk [bold]{str(item.id)[:8]}[/bold] accepted and audited.")
