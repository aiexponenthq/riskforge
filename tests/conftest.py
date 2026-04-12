"""Shared pytest fixtures for RiskForge test suite."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def fixtures_dir() -> Path:
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_system_yaml(fixtures_dir: Path) -> Path:
    return fixtures_dir / "systems" / "sample_system.yaml"
