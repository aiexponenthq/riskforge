"""Property tests for risk-score band boundaries (low/medium/high/critical).

Bands: low 1-4, medium 5-9, high 10-16, critical 17-25. Only scores achievable as
likelihood*severity (both 1-5) are testable, which still pins every band boundary.
"""

from __future__ import annotations

import pytest
from riskforge.models.risk import Likelihood, RiskDimension, RiskItem, Severity


def _item(lh: int, sv: int) -> RiskItem:
    return RiskItem(
        dimension=RiskDimension.privacy,
        title="t",
        description="d",
        source="manual",
        likelihood=Likelihood(lh),
        severity=Severity(sv),
        residual_likelihood=Likelihood(lh),
        residual_severity=Severity(sv),
    )


@pytest.mark.parametrize(
    ("lh", "sv", "score", "band"),
    [
        (1, 4, 4, "low"),  # top of low
        (2, 2, 4, "low"),
        (1, 5, 5, "medium"),  # bottom of medium
        (3, 3, 9, "medium"),  # top of medium
        (2, 5, 10, "high"),  # bottom of high
        (4, 4, 16, "high"),  # top of high
        (4, 5, 20, "critical"),  # into critical
        (5, 5, 25, "critical"),  # top of critical
    ],
)
def test_risk_band_boundaries(lh: int, sv: int, score: int, band: str) -> None:
    item = _item(lh, sv)
    assert item.risk_score == score
    assert item.risk_band == band
    # residual uses the same inputs here, so its band matches too
    assert item.residual_risk_band == band
