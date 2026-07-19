"""CLI-surface contract: group help must not advertise commands that do not ship.

The risk/system/tests groups previously listed subcommands (risk add/edit/score,
system edit, tests list) that were never implemented, so `--help` was wrong at
runtime. This locks each group's help description to its registered command set:
any command name listed after the colon in the help must actually be registered.
"""

from __future__ import annotations

import re

from riskforge.cli.commands import risk, system, tests_cmd


def _groups():
    return {"risk": risk.app, "system": system.app, "tests": tests_cmd.app}


def test_group_help_lists_only_registered_commands() -> None:
    for name, app in _groups().items():
        registered = {c.name for c in app.registered_commands}
        help_text = app.info.help or ""
        if ":" not in help_text:
            continue
        listed = re.findall(r"[a-z][a-z_]+", help_text.rsplit(":", 1)[1])
        phantom = [token for token in listed if token not in registered]
        assert not phantom, (
            f"'{name}' group help advertises command(s) that do not ship: {phantom}; "
            f"registered = {sorted(registered)}"
        )


def test_each_group_registers_at_least_one_command() -> None:
    for name, app in _groups().items():
        assert app.registered_commands, f"'{name}' group has no registered commands"
