"""RAGBenchmarkingAdapter — imports accuracy evidence from rag-benchmarking reports."""

from __future__ import annotations

from packaging.version import Version

from riskforge.adapters.base import AdapterSchemaError
from riskforge.models.risk import Likelihood, RiskDimension, RiskItem, Severity


class RAGBenchmarkingAdapter:
    """Maps rag-benchmarking benchmark_report.json fields to RiskItems.

    A metric value below its threshold generates a Robustness risk item
    with likelihood and severity proportional to the gap.
    """

    adapter_id = "rag-benchmarking"
    supported_schema_range = "^1.0.0"

    # Metric thresholds below which a risk item is generated
    THRESHOLDS = {
        "faithfulness": 0.85,
        "answer_relevance": 0.80,
        "context_recall": 0.75,
    }

    def validate(self, data: dict) -> None:
        version_str = data.get("schema_version", "0.0.0")
        v = Version(version_str)
        if v.major != 1:
            raise AdapterSchemaError(
                f"rag-benchmarking report schema v{version_str} not supported "
                f"by this adapter (supports ^1.0.0). "
                "Upgrade riskforge or pin rag-benchmarking to v1.x."
            )

    def transform(self, data: dict) -> list[RiskItem]:
        self.validate(data)
        items: list[RiskItem] = []
        metrics = data.get("metrics", {})
        pipeline_id = data.get("pipeline_id", "unknown")

        for metric_name, threshold in self.THRESHOLDS.items():
            value = metrics.get(metric_name)
            if value is not None and value < threshold:
                gap = threshold - value
                likelihood = Likelihood.likely if gap > 0.15 else Likelihood.possible
                severity = Severity.major if gap > 0.20 else Severity.moderate
                items.append(
                    RiskItem(
                        dimension=RiskDimension.robustness,
                        title=f"Accuracy below threshold: {metric_name}",
                        description=(
                            f"rag-benchmarking reports {metric_name}={value:.3f}, "
                            f"below threshold {threshold}. Pipeline: {pipeline_id}."
                        ),
                        source="rag_benchmarking",
                        source_ref=f"rag:{pipeline_id}",
                        likelihood=likelihood,
                        severity=severity,
                        residual_likelihood=likelihood,
                        residual_severity=severity,
                        article_refs=["Art.9(2)(a)", "Art.9(7)", "Art.15"],
                        nist_rmf_ref="MEASURE 2.5",
                        iso42001_ref="Clause A.9",
                    )
                )
        return items
