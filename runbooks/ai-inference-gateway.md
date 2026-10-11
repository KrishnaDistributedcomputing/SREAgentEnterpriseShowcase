---
title: AI Inference Gateway Incident Runbook
description: Application context and governed investigation of model endpoint incidents
author: Enterprise SRE Platform Team
ms.date: 2026-10-11
ms.topic: troubleshooting
estimated_reading_time: 8
---

## Application overview

AI Inference Gateway routes synthetic inference requests to a model endpoint. It
represents a controlled access layer for AI-assisted workflows, provider policy,
and cost boundaries. Endpoint loss stalls dependent business processes.

| Attribute | Value |
|-----------|-------|
| Portfolio | Digital platforms |
| Business domain | Artificial intelligence |
| Business operation | `run-inference` |
| Critical dependency | `model-endpoint` |
| Availability objective | 99.9 percent |
| Latency objective | Under 1,200 ms |
| Demonstrated fault | Dependency unavailable |
| Business impact | AI-assisted workflows stall and user experience degrades |

The dependency fault returns HTTP 503 while gateway health may remain successful.
Prompts and outputs are synthetic and are not persisted.

## Where Azure SRE Agent plays a role

Azure SRE Agent correlates failed inference traces with endpoint health, gateway
revision state, provider context, and policy boundaries.

1. Detect failed `run-inference` operations and SLO impact.
2. Correlate HTTP 503 responses with `model-endpoint`.
3. Exclude gateway readiness, deployment, and capacity causes.
4. Explain dependent workflow impact and provider boundary.
5. Recommend the bounded dependency-fault clear operation for approval.
6. Verify a synthetic inference request after recovery.

The agent must not read prompts or outputs, switch providers, deploy models,
change safety policy, retrieve credentials, or approve cost changes.

## Detection and triage

Investigate HTTP 503 responses referencing the model endpoint. Escalate sustained
failure, multi-provider impact, or any policy-control anomaly.

Collect dependency spans, active revision, endpoint status, first failure, and
last successful synthetic inference.

## Investigation procedure

1. Confirm service metadata and the 1,200 ms objective.
2. Compare failed inference with liveness and readiness.
3. Inspect endpoint dependency evidence without payload content.
4. Review gateway revisions and provider changes near fault onset.
5. Confirm policy, privacy, and cost boundaries remain enforced.
6. Present probable cause, confidence, impact, and reversible action.

## Mitigation

Approve clearing the bounded dependency fault. Production provider failover
requires model quality, safety, privacy, capacity, and cost validation.

## Recovery verification

1. Confirm readiness returns HTTP 200.
2. Submit three synthetic inference operations.
3. Confirm success below 1,200 ms and dependency errors stop.
4. Verify policy controls and telemetry boundaries remain intact.
5. Record approval, action, evidence, and recovery time.

Revert any provider change that increases errors, cost, or policy risk.
