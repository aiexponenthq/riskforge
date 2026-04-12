"""AssessEngine — interactive question runner and pattern matcher."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from riskforge.models.risk import Likelihood, RiskDimension, RiskItem, Severity


class AssessEngine:
    """Loads question banks, runs questions interactively, matches patterns.

    Designed to be called by the CLI assess command. All IO is via callbacks
    so the engine remains independently testable without terminal interaction.
    """

    def __init__(self, data_dir: Path) -> None:
        self._question_bank_dir = data_dir / "question_bank"
        self._patterns_path = data_dir / "patterns" / "patterns.yaml"

    def load_questions(self, dimension: RiskDimension) -> list[dict[str, Any]]:
        """Load questions for a given dimension from the YAML question bank."""
        path = self._question_bank_dir / f"{dimension.value}.yaml"
        if not path.exists():
            return []
        data = yaml.safe_load(path.read_text())
        return data.get("questions", [])

    def load_all_questions(self) -> dict[str, list[dict[str, Any]]]:
        """Load all 8 dimension question banks."""
        return {
            dim.value: self.load_questions(dim)
            for dim in RiskDimension
        }

    def load_patterns(self) -> list[dict[str, Any]]:
        """Load risk patterns from the pattern library."""
        if not self._patterns_path.exists():
            return []
        data = yaml.safe_load(self._patterns_path.read_text())
        return data.get("patterns", [])

    def match_patterns(
        self,
        annex_iii_category: str,
        purpose_keywords: list[str],
    ) -> list[dict[str, Any]]:
        """Return patterns that trigger for this system's category and purpose."""
        matched: list[dict[str, Any]] = []
        for pattern in self.load_patterns():
            triggers = pattern.get("triggers", {})
            cat_match = triggers.get("annex_iii_category") == annex_iii_category
            kw_match = any(
                kw.lower() in [k.lower() for k in triggers.get("purpose_keywords", [])]
                for kw in purpose_keywords
            )
            if cat_match and kw_match:
                matched.append(pattern)
        return matched

    def question_to_risk_item(
        self,
        question: dict[str, Any],
        dimension: RiskDimension,
        likelihood: int,
        severity: int,
        answer_unknown: bool = False,
    ) -> RiskItem:
        """Convert a question + answer into a RiskItem."""
        lh = Likelihood(min(max(likelihood, 1), 5))
        sv = Severity(min(max(severity, 1), 5))
        return RiskItem(
            dimension=dimension,
            title=question["text"][:120],
            description=question.get("guidance", question["text"]),
            source="question_bank",
            likelihood=lh,
            severity=sv,
            residual_likelihood=lh,
            residual_severity=sv,
            article_refs=question.get("article_refs", []),
            nist_rmf_ref=question.get("nist_rmf_ref", ""),
            iso42001_ref=question.get("iso42001_ref", ""),
            regulatory_status=question.get("regulatory_status", "settled"),
            knowledge_gap=answer_unknown,
            tags=[question.get("id", "")],
        )
