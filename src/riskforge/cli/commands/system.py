"""riskforge system — AI system management subcommands."""

from __future__ import annotations

import asyncio
from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer(help="Manage the AI system record: show, edit.")
console = Console()


@app.command("show")
def show_system(
    system_id: str = typer.Argument(..., help="System ID"),
    project_dir: Path = typer.Option(Path("."), "--project-dir"),
) -> None:
    """Show the AI system metadata."""
    import json

    from rich import print_json

    from riskforge.storage.filesystem import FileStore

    store = FileStore(project_dir)
    system = asyncio.run(store.read_system(system_id))
    print_json(json.dumps(system.model_dump(mode="json"), indent=2))
