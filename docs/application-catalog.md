---
title: Live Application Catalog
description: Live pages, API URLs, incident scenarios, and Azure SRE Agent value for all 15 applications
author: Enterprise SRE Platform Team
ms.date: 2026-10-10
ms.topic: reference
keywords:
  - application catalog
  - live urls
  - azure sre agent
  - incident scenarios
estimated_reading_time: 15
---

## Live deployment

All 15 applications are deployed to Azure Container Apps in West US 2. Each
application provides a metadata page, interactive OpenAPI page, readiness probe,
synthetic business operation, and scenario-specific runbook.

> [!NOTE]
> The applications use scale-to-zero. The first request after extended inactivity
> can take longer while Azure starts a replica.

## Commerce and retail

| Application | Live page | API page | Incident scenario | How Azure SRE Agent helps |
|-------------|-----------|----------|-------------------|---------------------------|
| Retail Checkout | [Open application](https://ca-retail-checkout-demowus2.icysky-c01fc423.westus2.azurecontainerapps.io/) | [Open API docs](https://ca-retail-checkout-demowus2.icysky-c01fc423.westus2.azurecontainerapps.io/docs) | Checkout requests fail when payment authorization is unavailable | Correlates HTTP 503 responses, traces, payment dependency errors, source, and the checkout runbook. It explains revenue impact, proposes a reversible recovery, requests approval, and verifies a successful checkout. |
| Inventory Service | [Open application](https://ca-inventory-service-demowus2.icysky-c01fc423.westus2.azurecontainerapps.io/) | [Open API docs](https://ca-inventory-service-demowus2.icysky-c01fc423.westus2.azurecontainerapps.io/docs) | Inventory reservations fail when the inventory database is unavailable | Distinguishes a healthy application process from a failed database dependency, identifies affected reservation traffic, checks correlated checkout impact, and guides recovery without changing stock quantities. |
| Order Fulfillment | [Open application](https://ca-order-fulfillment-demowus2.icysky-c01fc423.westus2.azurecontainerapps.io/) | [Open API docs](https://ca-order-fulfillment-demowus2.icysky-c01fc423.westus2.azurecontainerapps.io/docs) | Order dispatch returns application errors | Correlates HTTP 500 errors with the active revision, fulfillment queue context, and recent changes. It recommends clearing the synthetic error or rolling back only when deployment evidence supports that action. |

## Financial services

| Application | Live page | API page | Incident scenario | How Azure SRE Agent helps |
|-------------|-----------|----------|-------------------|---------------------------|
| Payments API | [Open application](https://ca-payments-api-demowus2.icysky-c01fc423.westus2.azurecontainerapps.io/) | [Open API docs](https://ca-payments-api-demowus2.icysky-c01fc423.westus2.azurecontainerapps.io/docs) | Payment authorization exceeds the 300 ms latency objective | Compares latency by revision, follows card-processor traces, and separates dependency latency from compute saturation. It proposes a governed mitigation and verifies that authorization latency returns below the objective. |
| Banking Ledger | [Open application](https://ca-banking-ledger-demowus2.icysky-c01fc423.westus2.azurecontainerapps.io/) | [Open API docs](https://ca-banking-ledger-demowus2.icysky-c01fc423.westus2.azurecontainerapps.io/docs) | The ledger revision becomes unavailable for traffic | Uses readiness and liveness evidence to identify a routing or revision-health problem without requesting ledger data access. It proposes removing an unhealthy revision from traffic and validates a synthetic ledger operation after approval. |
| Claims Processing | [Open application](https://ca-claims-processing-demowus2.icysky-c01fc423.westus2.azurecontainerapps.io/) | [Open API docs](https://ca-claims-processing-demowus2.icysky-c01fc423.westus2.azurecontainerapps.io/docs) | Claims fail because the document service is unavailable | Correlates dependency errors with healthy process signals, references the claims runbook, and preserves the synthetic-data boundary. It recommends a reversible dependency recovery without replaying or accessing real documents. |

## Customer experience

| Application | Live page | API page | Incident scenario | How Azure SRE Agent helps |
|-------------|-----------|----------|-------------------|---------------------------|
| Patient Scheduling | [Open application](https://ca-patient-scheduling-demowus2.icysky-c01fc423.westus2.azurecontainerapps.io/) | [Open API docs](https://ca-patient-scheduling-demowus2.icysky-c01fc423.westus2.azurecontainerapps.io/docs) | Appointment booking slows because the provider calendar is delayed | Detects latency degradation before full outage, traces the provider-calendar dependency, identifies patient and contact-center impact, and verifies recovery with synthetic bookings without accessing patient data. |
| Airline Reservation | [Open application](https://ca-airline-reservation-demowus2.icysky-c01fc423.westus2.azurecontainerapps.io/) | [Open API docs](https://ca-airline-reservation-demowus2.icysky-c01fc423.westus2.azurecontainerapps.io/docs) | Seat reservations return application errors | Correlates reservation errors with revision and seat-inventory context, summarizes traveler impact, and recommends a reversible recovery. It avoids unsafe replay because real inventory reconciliation is outside the scenario. |
| Media Streaming | [Open application](https://ca-media-streaming-demowus2.icysky-c01fc423.westus2.azurecontainerapps.io/) | [Open API docs](https://ca-media-streaming-demowus2.icysky-c01fc423.westus2.azurecontainerapps.io/docs) | Playback startup exceeds the 350 ms latency objective | Compares request duration, revision behavior, and content-delivery dependency traces. It explains viewer-abandonment risk and confirms that repeated playback starts return below the target after recovery. |

## Industrial and data

| Application | Live page | API page | Incident scenario | How Azure SRE Agent helps |
|-------------|-----------|----------|-------------------|---------------------------|
| Logistics Tracking | [Open application](https://ca-logistics-tracking-demowus2.icysky-c01fc423.westus2.azurecontainerapps.io/) | [Open API docs](https://ca-logistics-tracking-demowus2.icysky-c01fc423.westus2.azurecontainerapps.io/docs) | Shipment location updates fail when the tracking stream is unavailable | Combines HTTP 503 responses, event-stream dependency evidence, and stale-location business impact. It recommends recovery without purging or replaying an external stream and validates a new synthetic location update. |
| IoT Ingestion | [Open application](https://ca-iot-ingestion-demowus2.icysky-c01fc423.westus2.azurecontainerapps.io/) | [Open API docs](https://ca-iot-ingestion-demowus2.icysky-c01fc423.westus2.azurecontainerapps.io/docs) | Device telemetry ingestion returns errors | Correlates ingestion errors with device-event-hub context and active revisions, explains predictive-maintenance impact, and proposes a safe application recovery without changing stream partitions or replaying real telemetry. |
| Data Pipeline | [Open application](https://ca-data-pipeline-demowus2.icysky-c01fc423.westus2.azurecontainerapps.io/) | [Open API docs](https://ca-data-pipeline-demowus2.icysky-c01fc423.westus2.azurecontainerapps.io/docs) | Analytical jobs cannot start because the warehouse is unavailable | Identifies the downstream warehouse failure, relates it to stale reports and model features, and recommends recovery without canceling or modifying real jobs. It verifies a successful synthetic job start. |

## Digital platforms

| Application | Live page | API page | Incident scenario | How Azure SRE Agent helps |
|-------------|-----------|----------|-------------------|---------------------------|
| Identity Access | [Open application](https://ca-identity-access-demowus2.icysky-c01fc423.westus2.azurecontainerapps.io/) | [Open API docs](https://ca-identity-access-demowus2.icysky-c01fc423.westus2.azurecontainerapps.io/docs) | The identity service becomes unavailable for traffic | Uses readiness evidence and revision state to identify broad access impact while respecting secret and token boundaries. It recommends a governed routing recovery and verifies a synthetic access decision. |
| Collaboration API | [Open application](https://ca-collaboration-api-demowus2.icysky-c01fc423.westus2.azurecontainerapps.io/) | [Open API docs](https://ca-collaboration-api-demowus2.icysky-c01fc423.westus2.azurecontainerapps.io/docs) | Message publishing slows because the broker is delayed | Traces message-broker latency, compares revisions, and explains delayed employee communication. It proposes a safe recovery without reading message content and verifies latency with synthetic messages. |
| AI Inference Gateway | [Open application](https://ca-ai-inference-gateway-demowus2.icysky-c01fc423.westus2.azurecontainerapps.io/) | [Open API docs](https://ca-ai-inference-gateway-demowus2.icysky-c01fc423.westus2.azurecontainerapps.io/docs) | Inference fails because the model endpoint is unavailable | Correlates gateway health, model dependency errors, provider context, and source changes. It recommends a reversible recovery while preserving model, safety, privacy, and cost approval boundaries. |

## Common investigation flow

Azure SRE Agent applies the same governed workflow to every application:

1. Receive a matching Azure Monitor alert through a response plan.
2. Identify the application, SLO, business impact, and active revision.
3. Correlate logs, metrics, traces, Azure resources, source, and runbook context.
4. Distinguish application, dependency, latency, and readiness failures.
5. Propose a reversible action within managed-identity and tool-policy boundaries.
6. Request operator approval in Review mode.
7. Execute the approved action and verify readiness and business traffic.
8. Preserve the investigation summary for future incidents and on-call learning.

## Repository and deployment

* [GitHub repository](https://github.com/KrishnaDistributedcomputing/SREAgentEnterpriseShowcase)
* [Application portfolio structure](../apps/README.md)
* [Enterprise demonstration guide](enterprise-demo-guide.md)
* [Detailed design](detailed-design.md)
* [Cost model](cost-model.md)

