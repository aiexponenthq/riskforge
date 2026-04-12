"""riskforge init — initialise a new risk management project."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

console = Console()


def cmd(
    name: str = typer.Option(..., "--name", "-n", help="AI system name"),
    version: str = typer.Option(..., "--version", "-v", help="AI system version"),
    purpose: str = typer.Option(..., "--purpose", "-p", help="One-sentence purpose statement"),
    provider: str = typer.Option(..., "--provider", help="Provider organisation name"),
    category: Optional[str] = typer.Option(
        None, "--category", "-c", help="Annex III category"
    ),
    project_dir: Path = typer.Option(Path("."), "--project-dir", help="Project directory"),
    non_interactive: bool = typer.Option(
        False, "--non-interactive", help="Skip interactive prompts"
    ),
) -> None:
    """Initialise a new RiskForge risk management project.

    Creates .riskforge/ directory, riskforge.yaml manifest, and an initial
    system record. Run this once per AI system you are documenting.
    """
    import asyncio
    import uuid

    from riskforge.models.audit import AuditActor
    from riskforge.models.system import AISystem, AnnexIIICategory
    from riskforge.storage.filesystem import FileStore

    store = FileStore(project_dir)
    project_id = str(uuid.uuid4())

    system = AISystem(
        name=name,
        version=version,
        purpose=purpose,
        provider_name=provider,
        annex_iii_category=AnnexIIICategory(category) if category else None,
    )

    async def _init() -> None:
        await store.init_project(
            project_id,
            {"system_name": name, "created_by": "riskforge init"},
        )
        await store.write_system(str(system.id), system)

    asyncio.run(_init())

    console.print(f"[green]✓[/green] Initialised RiskForge project: [bold]{name} v{version}[/bold]")
    console.print(f"  System ID: [dim]{system.id}[/dim]")
    console.print(f"  Project dir: [dim]{project_dir.resolve()}[/dim]")
    console.print("")
    console.print("Next: [bold]riskforge assess[/bold]")
