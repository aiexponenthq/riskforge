"""IntegrationAdapter protocol — base contract for upstream tool adapters."""
from __future__ import annotations

from typing import Protocol, runtime_checkable

from riskforge.models.risk import RiskItem


class AdapterSchemaError(ValueError):
    """Raised when an upstream report's schema version is incompatible."""


@runtime_checkable
class IntegrationAdapter(Protocol):
    adapter_id: str
    supported_schema_range: str  # semver range e.g. "^1.0.0"

    def validate(self, data: dict) -> None:
        """Raise AdapterSchemaError if data is incompatible."""
        ...

    def transform(self, data: dict) -> list[RiskItem]:
        """Map upstream data fields to RiskItem objects."""
        ...
