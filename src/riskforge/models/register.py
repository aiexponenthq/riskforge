"""RiskRegister model."""
from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from riskforge.models.risk import RiskDimension, RiskItem
from riskforge.models.system import AISystem


class RiskRegister(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    system: AISystem
    items: list[RiskItem] = Field(default_factory=list)
    risk_appetite_threshold: int = 9  # scores > threshold require mitigation/acceptance
    assessor_name: str
    assessor_role: str
    assessment_date: datetime = Field(default_factory=lambda: datetime.now(UTC))
    review_date: datetime | None = None
    question_bank_version: str = "1.0.0"
    schema_version: str = "1.0.0"

    def covered_dimensions(self) -> set[RiskDimension]:
        return {item.dimension for item in self.items}

    def open_items(self) -> list[RiskItem]:
        """Risk items above appetite threshold that are neither mitigated nor accepted."""
        return [
            i
            for i in self.items
            if i.residual_risk_score > self.risk_appetite_threshold and not i.accepted
        ]

    def knowledge_gaps(self) -> list[RiskItem]:
        return [i for i in self.items if i.knowledge_gap]

    def items_by_dimension(self, dim: RiskDimension) -> list[RiskItem]:
        return [i for i in self.items if i.dimension == dim]

    def items_above_appetite(self) -> list[RiskItem]:
        return [i for i in self.items if i.risk_score > self.risk_appetite_threshold]

    def summary_stats(self) -> dict[str, int]:
        return {
            "total": len(self.items),
            "open": len(self.open_items()),
            "knowledge_gaps": len(self.knowledge_gaps()),
            "above_appetite": len(self.items_above_appetite()),
            "dimensions_covered": len(self.covered_dimensions()),
        }
