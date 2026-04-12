"""RiskItem, Mitigation, Likelihood, Severity, RiskDimension models."""
from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum, IntEnum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, computed_field, field_validator

VAGUE_PHRASES = frozenset({
    "we'll monitor it", "will monitor", "to be determined", "tbd", "n/a",
    "will address later", "monitor", "ongoing", "review", "future work",
    "to be confirmed", "tbc", "see comments",
})


class Likelihood(IntEnum):
    rare = 1
    unlikely = 2
    possible = 3
    likely = 4
    almost_certain = 5


class Severity(IntEnum):
    negligible = 1
    minor = 2
    moderate = 3
    major = 4
    critical = 5


class RiskDimension(str, Enum):
    health_safety = "health_safety"
    fundamental_rights = "fundamental_rights"
    discrimination = "discrimination"
    privacy = "privacy"
    transparency = "transparency"
    human_oversight = "human_oversight"
    robustness = "robustness"
    data_governance = "data_governance"
    # Additional EU AI Act / NIST AI RMF dimensions
    accuracy = "accuracy"
    bias_fairness = "bias_fairness"
    security = "security"
    accountability = "accountability"
    safety = "safety"


class Mitigation(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    description: str
    control_type: Literal["preventive", "detective", "corrective"]
    owner: str
    status: Literal["planned", "implemented", "verified"]
    evidence_refs: list[str] = Field(default_factory=list)
    is_vague: bool = False  # auto-flagged if description is generic
    article_ref: str = ""
    nist_rmf_ref: str = ""

    @field_validator("description")
    @classmethod
    def flag_vague_description(cls, v: str) -> str:
        """Warn consumers when the description matches a known placeholder phrase."""
        # Validation passes; is_vague is set separately as a computed flag.
        return v

    @property
    def description_is_vague(self) -> bool:
        """True if the description is a known vague placeholder."""
        lowered = self.description.strip().lower()
        if lowered in VAGUE_PHRASES:
            return True
        for phrase in VAGUE_PHRASES:
            if phrase in lowered and len(lowered) < len(phrase) + 20:
                return True
        return False


class RiskItem(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    dimension: RiskDimension
    title: str
    description: str
    source: Literal["manual", "question_bank", "pattern", "traceforge", "rag_benchmarking"] = "manual"
    likelihood: Likelihood
    severity: Severity
    mitigations: list[Mitigation] = Field(default_factory=list)
    residual_likelihood: Likelihood
    residual_severity: Severity
    accepted: bool = False
    acceptance_rationale: str = ""
    identified_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    article_refs: list[str] = Field(default_factory=list)  # e.g. ["Art.9(2)(a)", "Art.14"]
    nist_rmf_refs: list[str] = Field(default_factory=list)  # e.g. ["MANAGE 1.3"]
    iso42001_refs: list[str] = Field(default_factory=list)  # e.g. ["Clause 8.4"]
    nist_rmf_ref: str = ""  # legacy single-ref field; prefer nist_rmf_refs
    iso42001_ref: str = ""  # legacy single-ref field; prefer iso42001_refs
    regulatory_status: Literal["settled", "pending_implementing_act"] = "settled"
    knowledge_gap: bool = False  # true when source answer was "unknown"
    knowledge_gap_reason: str = ""
    source_ref: str = ""  # e.g. "rag:pipeline_001", "traceforge:lineage_042"
    tags: list[str] = Field(default_factory=list)
    notes: str = ""

    @computed_field
    @property
    def risk_score(self) -> int:
        return int(self.likelihood) * int(self.severity)

    @computed_field
    @property
    def residual_risk_score(self) -> int:
        return int(self.residual_likelihood) * int(self.residual_severity)

    @computed_field
    @property
    def risk_band(self) -> Literal["low", "medium", "high", "critical"]:
        s = self.risk_score
        if s <= 4:
            return "low"
        if s <= 9:
            return "medium"
        if s <= 16:
            return "high"
        return "critical"

    @computed_field
    @property
    def residual_risk_band(self) -> Literal["low", "medium", "high", "critical"]:
        s = self.residual_risk_score
        if s <= 4:
            return "low"
        if s <= 9:
            return "medium"
        if s <= 16:
            return "high"
        return "critical"
