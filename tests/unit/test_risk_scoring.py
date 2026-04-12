"""Unit tests for risk scoring and computed fields."""
from __future__ import annotations

import pytest
from riskforge.models.risk import Likelihood, RiskDimension, RiskItem, Severity


def make_item(likelihood: int, severity: int) -> RiskItem:
    return RiskItem(
        dimension=RiskDimension.robustness,
        title="Test risk",
        description="A test risk item",
        source="manual",
        likelihood=Likelihood(likelihood),
        severity=Severity(severity),
        residual_likelihood=Likelihood(likelihood),
        residual_severity=Severity(severity),
    )


@pytest.mark.parametrize(
    "likelihood,severity,expected_score,expected_band",
    [
        (1, 1, 1, "low"),
        (2, 2, 4, "low"),
        (2, 3, 6, "medium"),
        (3, 3, 9, "medium"),
        (3, 4, 12, "high"),
        (4, 4, 16, "high"),
        (4, 5, 20, "critical"),
        (5, 5, 25, "critical"),
    ],
)
def test_risk_score_and_band(
    likelihood: int, severity: int, expected_score: int, expected_band: str
) -> None:
    item = make_item(likelihood, severity)
    assert item.risk_score == expected_score
    assert item.risk_band == expected_band


def test_risk_score_boundary_medium_low() -> None:
    """Score of 4 is low; score of 5 is medium."""
    assert make_item(2, 2).risk_band == "low"    # 2*2=4 → low
    assert make_item(1, 5).risk_band == "medium" # 1*5=5 → medium
    assert make_item(1, 4).risk_band == "low"    # 1*4=4 → low


def test_residual_risk_score() -> None:
    item = RiskItem(
        dimension=RiskDimension.privacy,
        title="Privacy risk",
        description="Test",
        source="manual",
        likelihood=Likelihood.likely,        # 4
        severity=Severity.major,             # 4
        residual_likelihood=Likelihood.unlikely,  # 2
        residual_severity=Severity.minor,         # 2
    )
    assert item.risk_score == 16
    assert item.residual_risk_score == 4


def test_knowledge_gap_default_false() -> None:
    item = make_item(3, 3)
    assert item.knowledge_gap is False


def test_accepted_default_false() -> None:
    item = make_item(2, 2)
    assert item.accepted is False
