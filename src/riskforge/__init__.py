"""RiskForge: EU AI Act Article 9 Risk Management System CLI."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("riskforge")
except PackageNotFoundError:  # pragma: no cover - only when not installed
    __version__ = "0.0.0+unknown"
