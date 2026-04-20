"""Contract tests — every export path must validate against rmf.schema.json."""

from __future__ import annotations

import datetime
import json
from pathlib import Path

import jsonschema
import pytest
from riskforge.models.register import RiskRegister
from riskforge.models.risk import Likelihood, RiskDimension, RiskItem, Severity
from riskforge.models.rmf import RiskManagementFile
from riskforge.models.system import AISystem, AnnexIIICategory


@pytest.fixture
def schema() -> dict:
    schema_path = (
        Path(__file__).parent.parent.parent / "src/riskforge/_data/schemas/rmf.schema.json"
    )
    return json.loads(schema_path.read_text())


def minimal_rmf() -> RiskManagementFile:
    system = AISystem(
        name="Fraud Detector",
        version="1.2",
        purpose="Detect fraudulent transactions in real time.",
        provider_name="AI Exponent LLC",
        annex_iii_category=AnnexIIICategory.essential_services,
        annex_iii_self_classification_documented=True,
    )
    item = RiskItem(
        dimension=RiskDimension.robustness,
        title="Model accuracy below threshold",
        description="Accuracy on minority class falls below 85% in production.",
        source="manual",
        likelihood=Likelihood.possible,
        severity=Severity.major,
        residual_likelihood=Likelihood.unlikely,
        residual_severity=Severity.moderate,
    )
    register = RiskRegister(
        system=system,
        items=[item],
        assessor_name="Alice Wong",
        assessor_role="AI Governance Lead",
        assessment_date=datetime.datetime.now(datetime.UTC),
        review_date=datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=365),
        question_bank_version="1.0.0",
    )
    return RiskManagementFile(register=register)


def test_minimal_rmf_passes_schema(schema: dict) -> None:
    rmf = minimal_rmf()
    data = rmf.model_dump(mode="json", by_alias=True)
    # Should not raise
    jsonschema.validate(data, schema)


def test_schema_has_correct_id(schema: dict) -> None:
    assert schema["$id"] == "https://schemas.aiexponent.com/riskforge/rmf/v1.0.0"


def test_schema_requires_sha256_hash(schema: dict) -> None:
    assert "sha256_hash" in schema["required"]


def test_rmf_without_register_fails_schema(schema: dict) -> None:
    data = minimal_rmf().model_dump(mode="json", by_alias=True)
    del data["register"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(data, schema)


def test_risk_item_invalid_dimension_fails_schema(schema: dict) -> None:
    data = minimal_rmf().model_dump(mode="json", by_alias=True)
    data["register"]["items"][0]["dimension"] = "invalid_dimension"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(data, schema)
