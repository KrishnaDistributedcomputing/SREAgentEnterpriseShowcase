---
title: Enterprise SRE Showcase Data Model
description: Scenario, fault, operation, telemetry, incident, and recovery entities
author: Enterprise SRE Platform Team
ms.date: 2026-10-10
ms.topic: reference
---

## Scenario

| Field | Type | Constraint |
|-------|------|------------|
| `slug` | string | Unique kebab-case identifier |
| `name` | string | Human-readable service name |
| `domain` | string | Enterprise industry or capability |
| `description` | string | Operational purpose |
| `operation` | string | Synthetic business action |
| `dependency` | string | Named downstream dependency |
| `slo_availability` | number | At least 99.0 |
| `slo_latency_ms` | integer | Greater than zero |
| `default_fault` | enum | `none`, `error`, `latency`, `dependency`, or `not-ready` |
| `runbook` | string | Repository-relative Markdown path |
| `business_impact` | string | Audience-facing consequence |

## Fault state

| Field | Type | Constraint |
|-------|------|------------|
| `mode` | enum | Supported fault mode |
| `expires_at` | UTC timestamp or null | No more than 900 seconds after activation |

State transitions:

```text
none -> error | latency | dependency | not-ready
active -> none by clear, expiry, or process restart
active -> another active mode by authenticated replacement
```

## Business operation

| Field | Type | Constraint |
|-------|------|------------|
| `application` | string | Matches the scenario slug |
| `operation` | string | Matches the scenario operation |
| `outcome` | string | `success` for a completed request |
| `units` | integer | From 1 through 100 |
| `dependency` | string | Matches the scenario dependency |

## Incident evidence

An Azure SRE Agent investigation should assemble:

* Alert identity, severity, timestamp, and response-plan match
* Application, revision, deployment environment, and trace context
* HTTP status and latency trend
* Active fault symptom and downstream dependency
* Relevant source and runbook references
* Proposed mitigation, approval state, execution result, and recovery signal

## Recovery record

The facilitator records scenario slug, alert time, investigation start, probable
cause, approved action, action time, verification time, and residual follow-up.
This record supports MTTA and MTTR comparison across workshop runs.

