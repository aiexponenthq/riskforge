"""Prometheus metrics setup."""

from __future__ import annotations

from fastapi import FastAPI


def setup_metrics(app: FastAPI) -> None:
    """Register the /metrics endpoint with prometheus-client."""
    try:
        from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
        from starlette.responses import Response

        @app.get("/metrics", include_in_schema=False)
        def metrics() -> Response:
            return Response(
                content=generate_latest(),
                media_type=CONTENT_TYPE_LATEST,
            )
    except ImportError:
        pass  # prometheus-client not installed in non-server mode
