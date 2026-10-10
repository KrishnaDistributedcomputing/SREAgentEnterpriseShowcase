---
title: Sample Application Portfolio
description: Logical organization and operational purpose of the 15 enterprise test applications
author: Enterprise SRE Platform Team
ms.date: 2026-10-10
ms.topic: reference
estimated_reading_time: 6
---

## Portfolio structure

The 15 applications are grouped into five business portfolios. Each portfolio
contains three independent applications while sharing the same runtime, API
contract, telemetry, container image, and deployment model.

```text
apps/
  commerce-retail/
    retail-checkout/
    inventory-service/
    order-fulfillment/
  financial-services/
    payments-api/
    banking-ledger/
    claims-processing/
  customer-experience/
    patient-scheduling/
    airline-reservation/
    media-streaming/
  industrial-data/
    logistics-tracking/
    iot-ingestion/
    data-pipeline/
  digital-platforms/
    identity-access/
    collaboration-api/
    ai-inference-gateway/
```

## Portfolio rationale

| Portfolio | Business theme | Applications | Reliability focus |
|-----------|----------------|--------------|-------------------|
| Commerce and retail | Revenue and physical fulfillment | Retail Checkout, Inventory Service, Order Fulfillment | Dependency chains, order continuity, customer conversion |
| Financial services | Regulated transaction and case processing | Payments API, Banking Ledger, Claims Processing | Low latency, high availability, audit boundaries |
| Customer experience | Direct digital customer journeys | Patient Scheduling, Airline Reservation, Media Streaming | Availability, responsiveness, demand-facing impact |
| Industrial and data | Events, telemetry, and analytical flows | Logistics Tracking, IoT Ingestion, Data Pipeline | Stream dependencies, ingestion, data freshness |
| Digital platforms | Shared enterprise capabilities | Identity Access, Collaboration API, AI Inference Gateway | Platform blast radius, provider dependencies, access continuity |

## Application contents

Each application directory contains:

* `scenario.json` for machine-readable SLO, dependency, fault, and business context
* `main.py` for an independently importable FastAPI entry point

Runbooks remain in the top-level `runbooks/` directory so Azure SRE Agent can
retrieve operational procedures without traversing executable application code.

## Running one application

Application slugs do not include the portfolio name:

```powershell
$env:APP_SLUG = "banking-ledger"
uv run uvicorn sre_showcase.app:create_app_from_environment --factory --port 8080
```

