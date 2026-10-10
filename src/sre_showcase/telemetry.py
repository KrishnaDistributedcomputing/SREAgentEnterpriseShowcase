"""OpenTelemetry configuration for local and Azure-hosted samples."""

from __future__ import annotations

import logging
import os

from azure.monitor.opentelemetry import configure_azure_monitor
from fastapi import FastAPI
from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

logger = logging.getLogger(__name__)


def configure_telemetry(app: FastAPI, service_name: str) -> None:
    """Instrument a FastAPI application and enable OTLP when configured."""
    resource = Resource.create(
        {
            "service.name": service_name,
            "service.namespace": "sre-agent-enterprise-showcase",
            "deployment.environment.name": os.getenv("DEPLOYMENT_ENVIRONMENT", "local"),
        }
    )
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    application_insights = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")

    if application_insights:
        configure_azure_monitor(
            connection_string=application_insights,
            resource=resource,
            instrumentation_options={"fastapi": {"enabled": False}},
        )
        FastAPIInstrumentor.instrument_app(app)
        logger.info("telemetry_configured service=%s exporter=azure-monitor", service_name)
        return

    tracer_provider = TracerProvider(resource=resource)
    if endpoint:
        tracer_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint)))
    trace.set_tracer_provider(tracer_provider)

    if endpoint:
        metric_reader = PeriodicExportingMetricReader(OTLPMetricExporter(endpoint=endpoint))
        metrics.set_meter_provider(MeterProvider(resource=resource, metric_readers=[metric_reader]))
    else:
        metrics.set_meter_provider(MeterProvider(resource=resource))

    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer_provider)
    logger.info(
        "telemetry_configured service=%s exporter=%s",
        service_name,
        "otlp" if endpoint else "in-process",
    )
