"""Exporter abstract base class."""
from __future__ import annotations

from abc import ABC, abstractmethod

from riskforge.models.rmf import RiskManagementFile


class Exporter(ABC):
    """Base class for all RiskForge exporters.

    Each exporter receives a fully-populated and schema-validated
    RiskManagementFile and returns bytes for writing to disk.
    """

    @abstractmethod
    def render(self, rmf: RiskManagementFile) -> bytes:
        """Render the RMF to bytes in the target format."""
        ...
