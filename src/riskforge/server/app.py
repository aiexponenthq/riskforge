"""FastAPI server application factory."""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from riskforge.server.metrics import setup_metrics
from riskforge.server.middleware import CorrelationMiddleware
from riskforge.server.routers import exports, health, registers, risks, webhooks


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: validate config, connect storage
    from riskforge.server.config import ServerConfig

    config = ServerConfig()
    if not config.secret_key:
        raise RuntimeError(
            "RISKFORGE_SECRET_KEY is required. "
            "Generate with: python -c \"import secrets; print(secrets.token_hex(32))\""
        )
    yield
    # Shutdown: flush any pending writes


def create_app() -> FastAPI:
    app = FastAPI(
        title="RiskForge API",
        version="1.0.0",
        description="EU AI Act Article 9 Risk Management System",
        docs_url="/docs",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    app.add_middleware(CorrelationMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[],  # must be explicitly configured; no wildcard
        allow_methods=["GET", "POST", "PATCH", "DELETE"],
        allow_headers=["Authorization", "Content-Type", "X-Correlation-ID"],
    )

    app.include_router(health.router, prefix="")
    app.include_router(registers.router, prefix="/api/v1")
    app.include_router(risks.router, prefix="/api/v1")
    app.include_router(exports.router, prefix="/api/v1")
    app.include_router(webhooks.router, prefix="/api/v1")

    setup_metrics(app)
    return app


app = create_app()
