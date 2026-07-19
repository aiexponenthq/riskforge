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

    EXPERIMENTAL. The server is optional, not security-hardened, and not part of the
    flagship test suite. The CLI never imports it at startup, which preserves the
    zero-server-dependency guarantee.
    """
    console.print(
        "[yellow]⚠ EXPERIMENTAL:[/yellow] the RiskForge API server is not security-hardened "
        "(minimal auth, no rate limiting) and is not covered by the flagship tests. "
        "Do not expose it to untrusted networks."
    )

    is_external = host not in ("127.0.0.1", "localhost", "::1")
    if is_external and not allow_external:
        console.print(
            f"[red]✗[/red] Refusing to bind to non-localhost host '{host}' without "
            "--allow-external. Pass --allow-external only on a trusted network."
        )
        raise typer.Exit(1)
    if is_external:
        console.print(
            "[yellow]WARNING:[/yellow] binding to a non-localhost host exposes the API. "
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
    console.print(f"Docs: [link]http://{host}:{port}/docs[/link]")

    uvicorn.run(
        "riskforge.server.app:app",
        host=host,
        port=port,
        reload=False,
    )
