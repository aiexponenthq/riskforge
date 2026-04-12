"""Plugin loader — convenience wrapper for loading question banks from data files."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from riskforge.models.risk import RiskDimension


def load_question_bank(
    dimension: RiskDimension, data_dir: Path | None = None
) -> list[dict[str, Any]]:
    """Load the YAML question bank for a given dimension.

    Uses importlib.resources to locate bundled data when data_dir is None.
    """
    if data_dir is not None:
        path = data_dir / "question_bank" / f"{dimension.value}.yaml"
        raw = path.read_text()
    else:
        from importlib.resources import files

        raw = files("riskforge._data.question_bank").joinpath(f"{dimension.value}.yaml").read_text()
    data = yaml.safe_load(raw)
    return data.get("questions", [])


def load_patterns(data_dir: Path | None = None) -> list[dict[str, Any]]:
    """Load the risk pattern library."""
    if data_dir is not None:
        path = data_dir / "patterns" / "patterns.yaml"
        raw = path.read_text()
    else:
        from importlib.resources import files

        raw = files("riskforge._data.patterns").joinpath("patterns.yaml").read_text()
    data = yaml.safe_load(raw)
    return data.get("patterns", [])
