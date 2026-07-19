"""riskforge risk — risk item management subcommands."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Optional  # noqa: UP007 — Typer 0.12.3 compat

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Manage risk items: list, accept, mitigate.")
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
    from riskforge.engine.risk import AmbiguousRiskIdError, RiskEngine, RiskNotFoundError
    from riskforge.models.audit import AuditActor
    from riskforge.storage.filesystem import FileStore

    store = FileStore(project_dir)
    actor = AuditActor(type="human", identity="cli")
    audit = AuditEngine(store, actor)
    engine = RiskEngine(store, audit)

    try:
        item = asyncio.run(engine.accept_risk(system_id, risk_id, rationale, "cli"))
    except RiskNotFoundError:
        console.print(
            f"[red]✗[/red] No risk item matches id [bold]{risk_id}[/bold] in this register. "
            "Run [bold]riskforge risk list[/bold] to see the ids."
        )
        raise typer.Exit(1)
    except AmbiguousRiskIdError as exc:
        console.print(f"[red]✗[/red] {exc}")
        raise typer.Exit(1)
    except ValueError as exc:
        console.print(f"[red]✗[/red] {exc}")
        raise typer.Exit(1)

    console.print(f"[green]✓[/green] Risk [bold]{str(item.id)[:8]}[/bold] accepted and audited.")


@app.command("mitigate")
def mitigate_risk(
    system_id: str = typer.Argument(..., help="System ID"),
    risk_id: str = typer.Argument(..., help="Risk item ID (or first 8 chars)"),
    description: str = typer.Option(..., "--description", "-m", help="What the control does"),
    control_type: str = typer.Option(
        ..., "--control-type", "-c", help="preventive | detective | corrective"
    ),
    owner: str = typer.Option(..., "--owner", help="Team or person accountable for the control"),
    status: str = typer.Option("planned", "--status", help="planned | implemented | verified"),
    residual_likelihood: Optional[int] = typer.Option(
        None, "--residual-likelihood", help="Post-mitigation likelihood (1-5)"
    ),
    residual_severity: Optional[int] = typer.Option(
        None, "--residual-severity", help="Post-mitigation severity (1-5)"
    ),
    project_dir: Path = typer.Option(Path("."), "--project-dir"),
) -> None:
    """Add a mitigation to a risk item, optionally re-scoring residual risk."""
    from riskforge.engine.audit import AuditEngine
    from riskforge.engine.risk import AmbiguousRiskIdError, RiskEngine, RiskNotFoundError
    from riskforge.models.audit import AuditActor
    from riskforge.models.risk import Mitigation
    from riskforge.storage.filesystem import FileStore

    if control_type not in ("preventive", "detective", "corrective"):
        console.print("[red]✗[/red] --control-type must be preventive, detective, or corrective.")
        raise typer.Exit(1)
    if status not in ("planned", "implemented", "verified"):
        console.print("[red]✗[/red] --status must be planned, implemented, or verified.")
        raise typer.Exit(1)

    store = FileStore(project_dir)
    actor = AuditActor(type="human", identity="cli")
    audit = AuditEngine(store, actor)
    engine = RiskEngine(store, audit)
    mitigation = Mitigation(
        description=description, control_type=control_type, owner=owner, status=status
    )

    try:
        item = asyncio.run(
            engine.add_mitigation(
                system_id, risk_id, mitigation, residual_likelihood, residual_severity
            )
        )
    except RiskNotFoundError:
        console.print(
            f"[red]✗[/red] No risk item matches id [bold]{risk_id}[/bold] in this register. "
            "Run [bold]riskforge risk list[/bold] to see the ids."
        )
        raise typer.Exit(1)
    except AmbiguousRiskIdError as exc:
        console.print(f"[red]✗[/red] {exc}")
        raise typer.Exit(1)

    vague = " [yellow](flagged vague — replace with a specific control)[/yellow]"
    note = vague if item.mitigations[-1].is_vague else ""
    console.print(
        f"[green]✓[/green] Mitigation added to risk [bold]{str(item.id)[:8]}[/bold].{note} "
        f"Residual: {item.residual_risk_score} ({item.residual_risk_band})."
    )
