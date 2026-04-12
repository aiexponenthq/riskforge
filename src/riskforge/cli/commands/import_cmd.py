"""riskforge import — import upstream tool reports into the risk register."""
from __future__ import annotations

import asyncio
from pathlib import Path

import typer
from rich.console import Console

console = Console()


def cmd(
    system_id: str = typer.Argument(..., help="System ID"),
    adapter: str = typer.Option(..., "--adapter", "-a", help="Adapter name (e.g. rag-benchmarking)"),
    report: Path = typer.Option(..., "--report", "-r", help="Path to upstream report JSON"),
    project_dir: Path = typer.Option(Path("."), "--project-dir"),
) -> None:
    """Import an upstream tool report and add derived risk items to the register.

    Supported adapters: rag-benchmarking, traceforge
    """
    import json

    from riskforge.engine.audit import AuditEngine
    from riskforge.engine.risk import RiskEngine
    from riskforge.models.audit import AuditActor
    from riskforge.plugins.registry import PluginRegistry
    from riskforge.storage.filesystem import FileStore

    data = json.loads(report.read_text())
    registry = PluginRegistry()
    registry.load_all()

    upstream_adapter = registry.get_adapter(adapter)
    risk_items = upstream_adapter.transform(data)

    store = FileStore(project_dir)
    actor = AuditActor(type="human", identity="cli-import")
    audit = AuditEngine(store, actor)
    engine = RiskEngine(store, audit)

    async def _import() -> None:
        for item in risk_items:
            await engine.add_risk(system_id, item)

    asyncio.run(_import())
    console.print(
        f"[green]✓[/green] Imported {len(risk_items)} risk item(s) from "
        f"[bold]{adapter}[/bold] report."
    )
