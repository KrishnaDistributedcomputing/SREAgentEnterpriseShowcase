---
title: Azure SRE Agent Enterprise Showcase
description: Fifteen observable FastAPI workloads and a Spec Kit for demonstrating Azure SRE Agent
author: Enterprise SRE Platform Team
ms.date: 2026-10-10
ms.topic: overview
keywords:
  - azure sre agent
  - site reliability engineering
  - fastapi
  - opentelemetry
  - azure container apps
estimated_reading_time: 8
---

## Enterprise operations, demonstrated safely

This repository packages 15 lightweight enterprise workloads into one repeatable
Azure SRE Agent demonstration. Every workload exposes the same operational
contract: business traffic, health probes, OpenTelemetry signals, bounded fault
injection, a service-level objective (SLO), and a scenario-specific runbook.

The showcase is designed for architecture reviews, executive demonstrations,
platform engineering workshops, and incident-response exercises. It is not a
production application suite.

> [!IMPORTANT]
> Fault injection is disabled by default, requires an API key, and expires after
> at most 15 minutes. Deploy the showcase only into a non-production subscription.

## What is included

* A Spec Kit with product requirements, architecture, contracts, research,
  tasks, and acceptance criteria
* 15 Python 3.12 and FastAPI sample applications
* OpenTelemetry traces and metrics with optional OTLP export
* Consistent liveness, readiness, business, and fault-control endpoints
* A parameterized container image and local Docker Compose fleet
* Azure Container Apps, Log Analytics, and Application Insights Bicep templates
* Azure SRE Agent configuration guidance, response-plan examples, and runbooks
* Contract tests applied to every sample
* GitHub Actions validation and container-build workflows

## Application catalog

| Application | Industry | Demonstration focus | Default fault |
|-------------|----------|---------------------|---------------|
| Retail Checkout | Retail | Revenue-impacting checkout failure | Dependency |
| Payments API | Financial services | Authorization latency | Latency |
| Inventory Service | Retail | Inventory database outage | Dependency |
| Order Fulfillment | Supply chain | Dispatch processing errors | Error |
| Banking Ledger | Banking | Readiness and transaction continuity | Not ready |
| Claims Processing | Insurance | Document service outage | Dependency |
| Patient Scheduling | Healthcare | Patient-facing latency | Latency |
| Airline Reservation | Travel | Reservation errors | Error |
| Logistics Tracking | Transportation | Event-stream outage | Dependency |
| Media Streaming | Media | Playback startup latency | Latency |
| Identity Access | Enterprise security | Authentication readiness | Not ready |
| IoT Ingestion | Manufacturing | Telemetry ingestion failures | Error |
| Data Pipeline | Analytics | Warehouse outage | Dependency |
| Collaboration API | Productivity | Messaging latency | Latency |
| AI Inference Gateway | Artificial intelligence | Model endpoint outage | Dependency |

## Quick start

### Prerequisites

* Python 3.12
* [uv](https://docs.astral.sh/uv/)
* Docker Desktop (optional)
* Azure CLI and an Azure subscription (optional)

### Run one application

```powershell
uv sync
$env:APP_SLUG = "retail-checkout"
uv run uvicorn sre_showcase.app:create_app_from_environment --factory --port 8080
```

Open `http://localhost:8080/docs` for the generated OpenAPI interface.

### Trigger and clear a safe demonstration fault

```powershell
$env:ENABLE_FAULT_INJECTION = "true"
$env:DEMO_API_KEY = "local-demo-only"

$headers = @{ "X-Demo-Key" = "local-demo-only" }
$body = @{ mode = "dependency"; duration_seconds = 120 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://localhost:8080/faults" `
  -Headers $headers -ContentType "application/json" -Body $body

Invoke-RestMethod -Method Post -Uri "http://localhost:8080/work"
Invoke-RestMethod -Method Delete -Uri "http://localhost:8080/faults" -Headers $headers
```

### Run the fleet with Docker Compose

```powershell
$env:DEMO_API_KEY = "local-demo-only"
docker compose up --build
```

The applications bind to ports `8101` through `8115`.

## Spec Kit

Start with the feature [specification](specs/001-enterprise-sre-agent-showcase/spec.md),
then read the [implementation plan](specs/001-enterprise-sre-agent-showcase/plan.md)
and [enterprise demonstration guide](docs/enterprise-demo-guide.md).

## Validation

```powershell
uv run ruff check .
uv run pytest --cov=sre_showcase
docker build --build-arg APP_SLUG=retail-checkout -t sre-showcase:local .
```

## Product references

The design follows the current official Azure SRE Agent guidance:

* [Azure SRE Agent overview](https://learn.microsoft.com/azure/sre-agent/overview)
* [Create and set up Azure SRE Agent](https://learn.microsoft.com/azure/sre-agent/create-and-set-up)
* [Agent permissions](https://learn.microsoft.com/azure/sre-agent/permissions)
* [Automate incident response](https://learn.microsoft.com/azure/sre-agent/automate-incidents)
* [Deploy with infrastructure as code](https://learn.microsoft.com/azure/sre-agent/deploy-iac)
* [Tool access policies](https://learn.microsoft.com/azure/sre-agent/tool-access-policies)
* [Agent hooks](https://learn.microsoft.com/azure/sre-agent/agent-hooks)
* [Enable OpenTelemetry in Application Insights](https://learn.microsoft.com/azure/azure-monitor/app/opentelemetry-enable)

## Safety and cost

This repository creates billable Azure resources when deployed. Review Azure
pricing, use budget controls, keep response plans in Review mode until validated,
and remove the resource group after a workshop.

## License

Sample code is provided under the [MIT License](LICENSE).
