"""riskforge diff — compare two risk register snapshots."""
from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

console = Console()


def cmd(
    system_id: str = typer.Argument(..., help="System ID"),
    from_export: Path = typer.Argument(..., help="Baseline rmf.json"),
    to_export: Path = typer.Argument(..., help="Comparison rmf.json"),
) -> None:
    """Show differences between two exported Risk Management Files."""
    import json

    from_data = json.loads(from_export.read_text())
    to_data = json.loads(to_export.read_text())

    from_ids = {i["id"] for i in from_data.get("register", {}).get("items", [])}
    to_ids = {i["id"] for i in to_data.get("register", {}).get("items", [])}

    added = to_ids - from_ids
    removed = from_ids - to_ids

    console.print(f"[green]+{len(added)} added[/green]  [red]-{len(removed)} removed[/red]")

    for item in to_data.get("register", {}).get("items", []):
        if item["id"] in added:
            console.print(f"  [green]+[/green] {item['id'][:8]} {item['title'][:60]}")

    for item in from_data.get("register", {}).get("items", []):
        if item["id"] in removed:
            console.print(f"  [red]-[/red] {item['id'][:8]} {item['title'][:60]}")
