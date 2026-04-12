# ADR-01: File-Based Storage as OSS Tier Default

**Status:** Accepted
**Date:** April 2026
**Deciders:** System Architect, Infrastructure Engineer

## Context

RiskForge needs a storage mechanism for project state (system metadata, risk register, audit log). Options considered: SQLite, PostgreSQL, YAML + JSONL files.

## Decision

Project state lives in `.riskforge/` (YAML + JSONL files). Not SQLite. Not PostgreSQL by default.

## Rationale

- **Git-diff-friendly.** A compliance team can review a PR that modifies a risk register, reading the YAML diff in GitHub. A SQLite binary blob is opaque.
- **Regulator-readable.** A competent authority can read `register.yaml` and `audit.jsonl` with a text editor and `sha256sum`. No RiskForge installation required.
- **Merge-conflict-resolvable.** Two assessors working on different sections can merge their YAML changes. Binary databases cannot be merged.
- **Zero additional dependencies.** The FileStore uses only `pyyaml` and Python stdlib.

## Trade-offs Accepted

No concurrent writes in CLI mode. Teams needing concurrent access use `riskforge serve` with SQLiteStore (Team tier) or PostgreSQLStore (Enterprise tier).

## Enforcement

The `StorageBackend` ABC defines the interface. All storage implementations must conform to the async method signature. The FileStore is the default; alternative backends are separate PyPI packages.
