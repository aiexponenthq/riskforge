"""MigrationRunner — schema version upgrades for .riskforge/ project state."""
from __future__ import annotations

import importlib
from collections.abc import Callable
from pathlib import Path


class MigrationRunner:
    """Runs sequential schema migrations on project data dicts.

    Migrations live in src/riskforge/migrations/ as m<NNNN>_<name>.py.
    Each module exposes up(data: dict) -> dict and down(data: dict) -> dict.
    """

    def __init__(self, migrations_dir: Path | None = None) -> None:
        self._dir = migrations_dir or (Path(__file__).parent.parent / "migrations")

    def _load_migration(self, name: str) -> tuple[Callable, Callable]:
        mod = importlib.import_module(f"riskforge.migrations.{name}")
        return mod.up, mod.down

    def run_up(self, data: dict, from_version: str, to_version: str) -> dict:
        """Apply all applicable up() migrations to bring data from from_version to to_version."""
        migrations = sorted(
            [p.stem for p in self._dir.glob("m[0-9]*.py")],
        )
        for migration_name in migrations:
            up_fn, _ = self._load_migration(migration_name)
            data = up_fn(data)
        return data

    def run_down(self, data: dict, from_version: str, to_version: str) -> dict:
        """Apply reverse migrations."""
        migrations = sorted(
            [p.stem for p in self._dir.glob("m[0-9]*.py")],
            reverse=True,
        )
        for migration_name in migrations:
            _, down_fn = self._load_migration(migration_name)
            data = down_fn(data)
        return data
