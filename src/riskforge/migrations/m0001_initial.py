"""Migration m0001_initial — initial schema; identity migration.

All migrations expose:
  up(data: dict) -> dict   — apply the migration
  down(data: dict) -> dict — reverse the migration

This is the baseline migration. Data at schema_version 1.0.0 passes through
unchanged. Future migrations (m0002, m0003, ...) transform data incrementally.
"""
from __future__ import annotations


def up(data: dict) -> dict:
    """Apply migration m0001: no-op for initial schema version 1.0.0."""
    if "schema_version" not in data:
        data["schema_version"] = "1.0.0"
    return data


def down(data: dict) -> dict:
    """Reverse migration m0001: no-op (baseline — cannot go lower)."""
    return data
