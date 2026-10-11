"""FastAPI application factory shared by all showcase workloads."""

from __future__ import annotations

import asyncio
import logging
import os
from datetime import datetime
from typing import Annotated

from fastapi import FastAPI, Header, HTTPException, Query, Request, status
from fastapi.responses import HTMLResponse
from opentelemetry import metrics
from pydantic import BaseModel, Field

from .catalog import FaultMode, list_scenarios, load_scenario
from .faults import MAX_FAULT_SECONDS, FaultController, FaultSnapshot
from .landing import render_application_page, render_landing_page
from .telemetry import configure_telemetry

logger = logging.getLogger(__name__)


class WorkResponse(BaseModel):
    """Successful synthetic business operation."""

    application: str
    operation: str
    outcome: str
    units: int
    dependency: str


class FaultRequest(BaseModel):
    """Request to enable one bounded demonstration fault."""

    mode: FaultMode
    duration_seconds: int = Field(default=300, ge=1, le=MAX_FAULT_SECONDS)


class FaultResponse(BaseModel):
    """Serializable fault state."""

    mode: FaultMode
    expires_at: datetime | None


def _fault_response(snapshot: FaultSnapshot) -> FaultResponse:
    return FaultResponse(mode=snapshot.mode, expires_at=snapshot.expires_at)


def create_app(slug: str) -> FastAPI:
    """Create one configured showcase application."""
    scenario = load_scenario(slug)
    controller = FaultController()
    app = FastAPI(
        title=scenario.name,
        description=scenario.description,
        version="1.0.0",
        contact={"name": "Enterprise SRE Platform Team"},
    )
    configure_telemetry(app, scenario.slug)
    meter = metrics.get_meter("sre_showcase")
    operations = meter.create_counter(
        "showcase.business.operations",
        description="Synthetic business operations by outcome",
    )

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    async def landing(request: Request) -> HTMLResponse:
        return HTMLResponse(render_landing_page(request, scenario, list_scenarios()))

    @app.get("/app", response_class=HTMLResponse, include_in_schema=False)
    async def application_page(request: Request) -> HTMLResponse:
        return HTMLResponse(render_application_page(request, scenario))

    @app.get("/api/metadata", tags=["metadata"])
    async def metadata() -> dict[str, object]:
        return {
            "slug": scenario.slug,
            "name": scenario.name,
            "domain": scenario.domain,
            "description": scenario.description,
            "slo": {
                "availability": scenario.slo_availability,
                "latency_ms": scenario.slo_latency_ms,
            },
            "business_impact": scenario.business_impact,
            "runbook": scenario.runbook,
        }

    @app.get("/health/live", tags=["health"])
    async def liveness() -> dict[str, str]:
        return {"status": "alive"}

    @app.get("/health/ready", tags=["health"])
    async def readiness() -> dict[str, str]:
        if controller.current().mode == "not-ready":
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Application is intentionally not ready",
            )
        return {"status": "ready"}

    @app.post("/work", response_model=WorkResponse, tags=["business"])
    async def perform_work(
        units: Annotated[int, Query(ge=1, le=100)] = 1,
    ) -> WorkResponse:
        fault = controller.current().mode
        attributes = {"application": scenario.slug, "fault.mode": fault}
        if fault == "latency":
            await asyncio.sleep(max(1.0, scenario.slo_latency_ms / 500))
        if fault == "error":
            operations.add(1, {**attributes, "outcome": "error"})
            logger.error("synthetic_error application=%s operation=%s", slug, scenario.operation)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Intentional demonstration error",
            )
        if fault == "dependency":
            operations.add(1, {**attributes, "outcome": "dependency_error"})
            logger.error(
                "dependency_unavailable application=%s dependency=%s",
                slug,
                scenario.dependency,
            )
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Intentional dependency failure: {scenario.dependency}",
            )

        operations.add(units, {**attributes, "outcome": "success"})
        logger.info(
            "operation_completed application=%s operation=%s units=%s",
            slug,
            scenario.operation,
            units,
        )
        return WorkResponse(
            application=scenario.slug,
            operation=scenario.operation,
            outcome="success",
            units=units,
            dependency=scenario.dependency,
        )

    @app.get("/faults", response_model=FaultResponse, tags=["demonstration"])
    async def get_fault() -> FaultResponse:
        return _fault_response(controller.current())

    @app.post("/faults", response_model=FaultResponse, tags=["demonstration"])
    async def set_fault(
        request: FaultRequest,
        demo_key: Annotated[str | None, Header(alias="X-Demo-Key")] = None,
    ) -> FaultResponse:
        if os.getenv("ENABLE_FAULT_INJECTION", "false").lower() != "true":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        expected_key = os.getenv("DEMO_API_KEY")
        if not expected_key or demo_key != expected_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="A valid X-Demo-Key is required",
            )
        return _fault_response(controller.activate(request.mode, request.duration_seconds))

    @app.delete("/faults", response_model=FaultResponse, tags=["demonstration"])
    async def clear_fault(
        demo_key: Annotated[str | None, Header(alias="X-Demo-Key")] = None,
    ) -> FaultResponse:
        expected_key = os.getenv("DEMO_API_KEY")
        if not expected_key or demo_key != expected_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="A valid X-Demo-Key is required",
            )
        return _fault_response(controller.clear())

    return app


def create_app_from_environment() -> FastAPI:
    """Create an application from the APP_SLUG environment variable."""
    slug = os.getenv("APP_SLUG")
    if not slug:
        raise RuntimeError("APP_SLUG must identify an application in apps/")
    return create_app(slug)
