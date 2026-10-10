---
title: Enterprise Azure SRE Agent Showcase Implementation Plan
description: Technical plan for the sample fleet, observability, Azure platform, and demonstrations
author: Enterprise SRE Platform Team
ms.date: 2026-10-10
ms.topic: concept
estimated_reading_time: 14
---

## Technical context

| Concern | Decision |
|---------|----------|
| Runtime | Python 3.12 and FastAPI |
| Packaging | One installable shared package with 15 thin application wrappers |
| Configuration | JSON scenario files validated into typed dataclasses |
| Telemetry | OpenTelemetry traces and metrics over optional OTLP/gRPC |
| Local execution | uv, Uvicorn, and Docker Compose |
| Azure compute | Azure Container Apps with scale-to-zero settings |
| Observability | Log Analytics and workspace-based Application Insights |
| Identity | User-assigned managed identity for Azure-hosted workloads |
| SRE workflow | Source, logs, Azure resources, alerts, runbooks, and Review mode |
| Infrastructure | Bicep for showcase workloads; official Azure SRE Agent templates for the agent |
| CI | GitHub Actions for lint, tests, and container build |

## Architecture

```text
GitHub repository
  | source, scenarios, runbooks
  v
Azure SRE Agent <------ Azure Monitor response plan
  |        |                    ^
  |        +------ approval ----+
  | diagnostics and governed action
  v
Azure subscription / non-production resource group
  |
  +-- Azure Container Apps environment
  |     +-- 15 FastAPI sample applications
  |     +-- managed identity and secret references
  |
  +-- Application Insights
  +-- Log Analytics workspace
  +-- Azure Monitor alerts
```

## Runtime design

The shared factory loads one scenario, creates a consistent API, configures
OpenTelemetry, and holds fault state in memory. Application directories contain
only a scenario definition and entry point. This keeps incident behavior
consistent while preserving industry-specific operational context.

The fault controller uses an in-process lock, UTC expiry, and a hard 900-second
limit. Restarts clear state. No fault mutates infrastructure or external data.

## Azure SRE Agent design

The agent receives context from:

* GitHub source connection for runtime code, scenario metadata, and runbooks
* Application Insights or Log Analytics for requests, errors, dependencies, and traces
* Azure resource access at the showcase resource-group scope
* Azure Monitor as the incident platform
* Response plans filtered to showcase alert names and severities

Initial operation uses Reader permissions and Review mode. The facilitator can
approve a reversible action such as clearing a fault or restarting a revision
only after the investigation explains expected impact and validation.

## Governance design

Global tool policies deny resource deletion and ask before write operations.
Agent hooks can enforce evidence requirements and log tool usage. A production
adoption should integrate these controls with organizational policy, privileged
identity management, change management, and central audit retention.

## Deployment sequence

1. Validate source, tests, and container build locally.
2. Create or select a non-production Azure subscription and resource group.
3. Build and publish one image with scenario-specific tags or one shared digest.
4. Run the Bicep what-if operation and review role assignments.
5. Deploy the observability plane and 15 Container Apps.
6. Deploy Azure SRE Agent through the official `microsoft/sre-agent` templates.
7. Connect GitHub, Application Insights, Azure resources, and Azure Monitor.
8. Apply tool policies and configure a Review-mode response plan.
9. Run a smoke scenario, verify recovery, and save the investigation summary.

## Validation strategy

* Catalog test for exactly 15 complete and unique scenarios
* Parameterized API contract test for every application
* Fault enablement, authentication, activation, and recovery tests
* Ruff static analysis
* Container build and health check
* Bicep build and deployment what-if before Azure changes
* Manual end-to-end alert and agent investigation acceptance test

## Productionization gaps

The showcase intentionally omits durable state, private networking by default,
regional redundancy, production traffic, data-classification controls, enterprise
certificate management, and service-specific remediation. Adoption teams must
address these gaps before reusing patterns in production.

