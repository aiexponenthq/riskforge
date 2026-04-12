"""AISystem and AnnexIIICategory models."""
from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class AnnexIIICategory(str, Enum):
    biometric = "biometric"
    critical_infrastructure = "critical_infrastructure"
    education = "education"
    employment = "employment"
    essential_services = "essential_services"
    law_enforcement = "law_enforcement"
    migration = "migration"
    justice = "justice"

    def display_name(self) -> str:
        return {
            "biometric": "Biometric Identification (Annex III §1)",
            "critical_infrastructure": "Critical Infrastructure (Annex III §2)",
            "education": "Education & Vocational Training (Annex III §3)",
            "employment": "Employment & Worker Management (Annex III §4)",
            "essential_services": "Access to Essential Services (Annex III §5)",
            "law_enforcement": "Law Enforcement (Annex III §6)",
            "migration": "Migration, Asylum & Border Control (Annex III §7)",
            "justice": "Administration of Justice (Annex III §8)",
        }[self.value]


class AISystem(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    version: str
    purpose: str  # one sentence; used in PDF executive summary
    intended_users: list[str] = Field(default_factory=list)
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    deployment_context: str = ""
    annex_iii_category: AnnexIIICategory | None = None
    annex_iii_self_classification_documented: bool = False  # AC: Art. 6(2) gate
    provider_name: str
    provider_contact: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    schema_version: str = "1.0.0"
