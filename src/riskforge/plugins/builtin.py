"""Built-in question bank entry point classes.

These are thin wrappers that satisfy the entry_point registration contract.
The actual questions live in src/riskforge/_data/question_bank/*.yaml.
"""

from __future__ import annotations

from riskforge.models.risk import RiskDimension
from riskforge.plugins.loader import load_question_bank


class _QuestionBankBase:
    dimension: RiskDimension

    def questions(self) -> list[dict]:
        return load_question_bank(self.dimension)


class HealthSafetyBank(_QuestionBankBase):
    dimension = RiskDimension.health_safety


class FundamentalRightsBank(_QuestionBankBase):
    dimension = RiskDimension.fundamental_rights


class DiscriminationBank(_QuestionBankBase):
    dimension = RiskDimension.discrimination


class PrivacyBank(_QuestionBankBase):
    dimension = RiskDimension.privacy


class TransparencyBank(_QuestionBankBase):
    dimension = RiskDimension.transparency


class HumanOversightBank(_QuestionBankBase):
    dimension = RiskDimension.human_oversight


class RobustnessBank(_QuestionBankBase):
    dimension = RiskDimension.robustness


class DataGovernanceBank(_QuestionBankBase):
    dimension = RiskDimension.data_governance
