"""riskforge assess — run the interactive 8-dimension risk assessment."""
from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

console = Console()


def cmd(
    system_id: str = typer.Argument(..., help="System ID to assess"),
    project_dir: Path = typer.Option(Path("."), "--project-dir"),
    assessor_name: str = typer.Option(..., "--assessor-name"),
    assessor_role: str = typer.Option(..., "--assessor-role"),
) -> None:
    """Run the interactive 8-dimension Article 9 risk assessment.

    Walks through all question bank dimensions, prompts for likelihood
    and severity scores, and writes results to the risk register.
    """
    console.print("[bold]RiskForge Assessment[/bold] — EU AI Act Article 9")
    console.print(
        "This session will guide you through 8 risk dimensions. "
        "Type 'skip' to mark a question as not applicable, "
        "or 'unknown' to flag a knowledge gap requiring testing.\n"
    )
    console.print(
        "[yellow]Interactive assessment not yet implemented in this scaffold. "
        "Run `riskforge risk add` to add risk items manually.[/yellow]"
    )
