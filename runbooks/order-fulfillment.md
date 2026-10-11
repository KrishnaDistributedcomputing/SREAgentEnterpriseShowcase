---
title: Order Fulfillment Incident Runbook
description: Application context and governed investigation of fulfillment dispatch errors
author: Enterprise SRE Platform Team
ms.date: 2026-10-11
ms.topic: troubleshooting
estimated_reading_time: 8
---

## Application overview

Order Fulfillment dispatches paid orders to fulfillment centers. It represents
the handoff between digital commerce and warehouse execution. Failed dispatches
delay paid orders and can cause warehouse service-level commitments to be missed.

| Attribute | Value |
|-----------|-------|
| Portfolio | Commerce and retail |
| Business domain | Supply chain |
| Business operation | `dispatch-order` |
| Critical dependency | `fulfillment-queue` |
| Availability objective | 99.9 percent |
| Latency objective | Under 800 ms |
| Demonstrated fault | Application error |
| Business impact | Paid orders are delayed and warehouse commitments are missed |

The error fault returns HTTP 500 from the business operation. Health probes may
remain successful, which separates transaction failure from platform readiness.

## Where Azure SRE Agent plays a role

Azure SRE Agent correlates dispatch errors with request traces, active revisions,
queue context, deployment history, and the order-flow business impact.

1. Detect failed `dispatch-order` operations and quantify the affected window.
2. Determine whether the symptom is application error, readiness loss, or queue
   dependency failure.
3. Compare failures across revisions and recent deployments.
4. Explain the risk to paid orders and warehouse commitments.
5. Propose fault clearing or a correlated revision rollback for approval.
6. Verify a new synthetic dispatch and monitor error recovery.

The agent must not replay production orders, purge a queue, inspect customer
order content, modify warehouse systems, or perform an unapproved rollback.

## Detection and triage

Investigate HTTP 500 responses from `dispatch-order`. Escalate when failures are
sustained, paid-order backlog is growing, or multiple fulfillment regions are
affected.

Collect the first error time, active revision, error trace, queue dependency
context, deployment history, and last successful dispatch.

## Investigation procedure

1. Confirm the application contract and SLO through `/api/metadata`.
2. Compare business failures with liveness and readiness.
3. Inspect error traces and identify the failing operation.
4. Compare error rate by revision and correlate with deployments.
5. Check `fulfillment-queue` evidence without reading message contents.
6. Present probable cause, confidence, blast radius, and reversible response.

## Mitigation

Approve clearing the bounded error fault. Roll back a revision only when the
evidence correlates that revision with the incident. Production replay or queue
intervention requires a separate idempotency and ownership procedure.

If errors continue, stop synthetic producers and escalate to the fulfillment
application and queue owners.

## Recovery verification

1. Confirm health probes are successful.
2. Dispatch three synthetic orders and confirm HTTP 200.
3. Verify latency remains under 800 ms and error rate returns to baseline.
4. Confirm no backlog symptom remains in the demonstration evidence.
5. Record the approved action, recovery result, and required follow-up.

Reverse the approved change if it increases errors or creates readiness loss.
