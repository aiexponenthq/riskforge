"""RiskForge CLI entry point."""
from __future__ import annotations

import typer
from rich import print as rprint

app = typer.Typer(
    name="riskforge",
    help="EU AI Act Article 9 Risk Management System — AiExponent LLC",
    no_args_is_help=True,
)


@app.callback(invoke_without_command=True)
def main(
    version: bool = typer.Option(False, "--version", "-V", is_eager=True),
) -> None:
    """RiskForge — EU AI Act Article 9 Risk Management System CLI."""
    if version:
        from importlib.metadata import version as pkg_version

        rprint(
            f"[bold]RiskForge[/bold] v{pkg_version('riskforge')} | "
            "Apache 2.0 | Zero telemetry | aiexponent.com"
        )
        raise typer.Exit()


# Register subcommands (lazy imports — no business logic at import time)
from riskforge.cli.commands import (  # noqa: E402
    assess,
    diff,
    export,
    import_cmd,
    init,
    risk,
    serve,
    system,
    tests_cmd,
    validate,
    verify,
)

app.add_typer(system.app, name="system")
app.add_typer(risk.app, name="risk")
app.add_typer(tests_cmd.app, name="tests")

app.command("init")(init.cmd)
app.command("assess")(assess.cmd)
app.command("validate")(validate.cmd)
app.command("export")(export.cmd)
app.command("verify")(verify.cmd)
app.command("diff")(diff.cmd)
app.command("import")(import_cmd.cmd)
app.command("serve")(serve.cmd)
