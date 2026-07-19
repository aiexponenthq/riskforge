"""The package __version__ must stay derived from the distribution metadata.

Guards against reintroducing a hardcoded literal that drifts from pyproject
(the shipped 1.0.0 had `__version__ = "0.1.4"`).
"""

from __future__ import annotations

import importlib.metadata

import riskforge


def test_version_matches_distribution_metadata() -> None:
    assert riskforge.__version__ == importlib.metadata.version("riskforge")
