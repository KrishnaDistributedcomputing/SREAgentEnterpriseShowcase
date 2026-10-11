---
title: Retail Checkout Incident Runbook
description: Application context and governed investigation of checkout dependency incidents
author: Enterprise SRE Platform Team
ms.date: 2026-10-11
ms.topic: troubleshooting
estimated_reading_time: 8
---

## Application overview

Retail Checkout converts a customer's purchase intent into a completed order. It
submits a synthetic checkout request and depends on payment authorization before
reporting success. A sustained outage directly affects conversion and revenue.

| Attribute | Value |
|-----------|-------|
| Portfolio | Commerce and retail |
| Business domain | Retail |
| Business operation | `submit-checkout` |
| Critical dependency | `payment-authorization` |
| Availability objective | 99.95 percent |
| Latency objective | Under 450 ms |
| Demonstrated fault | Dependency unavailable |
| Business impact | Customers cannot complete purchases and revenue is lost |

The dependency fault produces HTTP 503 responses while process health can remain
normal. This demonstrates why service health alone is insufficient evidence of
a functioning customer journey.

## Where Azure SRE Agent plays a role

Azure SRE Agent assembles the alert, request traces, business-operation metric,
revision context, service metadata, and runbook into one investigation.

1. Detect checkout error growth and connect it to the availability objective.
2. Correlate failed `submit-checkout` traces with `payment-authorization`.
3. Exclude readiness, replica saturation, and recent revision changes.
4. Describe customer and revenue impact using the application metadata.
5. Recommend a reversible, pre-authorized response for operator approval.
6. Verify the full checkout operation after the approved action.

The agent must not process a real payment, retrieve payment data or secrets,
change payment-provider configuration, broaden access, or delete resources.

## Detection and triage

Investigate elevated HTTP 503 responses or failed checkout operations while
liveness and readiness remain healthy. Escalate priority when failures are
sustained or other commerce services report correlated impact.

Capture the alert time, failure rate, active revision, failed dependency span,
and the last known successful checkout.

## Investigation procedure

1. Confirm service identity, SLO, dependency, and impact through `/api/metadata`.
2. Compare `/health/live` and `/health/ready` with failed business requests.
3. Inspect traces for the `payment-authorization` dependency marker.
4. Review deployment and configuration changes around the first error.
5. Check Payments API and Inventory Service for correlated symptoms.
6. Present probable cause, confidence, evidence, blast radius, and proposed
   action before requesting approval.

## Mitigation

In Review mode, approve clearing the bounded dependency fault. A production
analogue must use the payment team's approved failover, circuit-breaker, or
traffic-control procedure. Never improvise a provider change during an incident.

If recovery is unavailable, pause synthetic traffic and escalate to the payment
service owner.

## Recovery verification

1. Confirm `/health/ready` returns HTTP 200.
2. Submit three synthetic checkout operations and confirm HTTP 200.
3. Confirm latency remains under 450 ms and dependency errors stop.
4. Verify the alert recovers and no new fault appears in adjacent services.
5. Record approval, action, recovery time, and follow-up.

If verification fails, reverse the last approved change and preserve the agent
investigation for escalation.
