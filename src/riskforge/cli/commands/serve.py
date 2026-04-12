"""riskforge serve — start the optional FastAPI server."""
from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

console = Console()


def cmd(
    host: str = typer.Option("127.0.0.1", "--host", help="Bind host"),
    port: int = typer.Option(8090, "--port", "-p", help="Bind port"),
    allow_external: bool = typer.Option(
        False, "--allow-external", help="Allow non-localhost binding (adds security warning)"
    ),
    project_dir: Path = typer.Option(Path("."), "--project-dir"),
) -> None:
    """Start the RiskForge REST API server (requires pip install riskforge[server]).

    The server is not imported by the CLI at startup — this lazy import
    preserves the CLI's zero-server-dependency guarantee.
    """
    if allow_external and host == "0.0.0.0":  # noqa: S104
        console.print(
            "[yellow]WARNING:[/yellow] Binding to 0.0.0.0 exposes the API externally. "
            "Ensure firewall rules and authentication are configured."
        )

    try:
        import uvicorn  # lazy import — only available with [server] extra
    except ImportError:
        console.print(
            "[red]✗[/red] Server dependencies not installed. "
            "Run: [bold]pip install riskforge[server][/bold]"
        )
        raise typer.Exit(1)

    console.print(f"Starting RiskForge API server on [bold]http://{host}:{port}[/bold]")
    console.print("Docs: [link]http://{host}:{port}/docs[/link]")

    uvicorn.run(
        "riskforge.server.app:app",
        host=host,
        port=port,
        reload=False,
    )
