---
title: Claims Processing Incident Runbook
description: Application context and governed investigation of claims document incidents
author: Enterprise SRE Platform Team
ms.date: 2026-10-11
ms.topic: troubleshooting
estimated_reading_time: 8
---

## Application overview

Claims Processing accepts synthetic insurance claims and coordinates supporting
documents. It represents a regulated intake workflow where dependency failure
stops new claims and increases the time policyholders wait for resolution.

| Attribute | Value |
|-----------|-------|
| Portfolio | Financial services |
| Business domain | Insurance |
| Business operation | `submit-claim` |
| Critical dependency | `document-service` |
| Availability objective | 99.9 percent |
| Latency objective | Under 1,000 ms |
| Demonstrated fault | Dependency unavailable |
| Business impact | Claim intake stops and policyholder resolution time increases |

The dependency fault returns HTTP 503 while application health can remain normal.
Only synthetic claims are permitted in the showcase.

## Where Azure SRE Agent plays a role

Azure SRE Agent correlates claim-submission failures with dependency traces,
revision state, resource health, and business metadata without reading claim
documents or policyholder data.

1. Detect failed `submit-claim` operations and SLO impact.
2. Correlate HTTP 503 responses with `document-service`.
3. Exclude readiness, deployment, and platform health causes.
4. Describe intake interruption and policyholder impact.
5. Recommend the bounded dependency-fault clear operation for approval.
6. Verify a new synthetic claim after recovery.

The agent must not retrieve documents, inspect personal data, replay claims,
change claim state, access secrets, or broaden permissions.

## Detection and triage

Investigate HTTP 503 responses referencing `document-service`. Escalate sustained
failure or any indication that a real document system is connected.

Collect the first failure, active revision, dependency span, health status, and
last successful synthetic claim.

## Investigation procedure

1. Confirm the SLO, operation, and dependency through `/api/metadata`.
2. Compare claim failures with liveness and readiness.
3. Inspect dependency spans without opening payloads.
4. Review revisions and Azure resource health near fault onset.
5. Confirm all data and connected systems are synthetic.
6. State probable cause, confidence, impact, and proposed reversible action.

## Mitigation

Approve clearing the bounded dependency fault. Production document replay
requires a separate data-handling, retention, and idempotency procedure.

Stop the exercise immediately if regulated data or a production connector is
detected.

## Recovery verification

1. Confirm readiness returns HTTP 200.
2. Submit one synthetic claim and confirm HTTP 200.
3. Verify latency remains under 1,000 ms and dependency errors stop.
4. Confirm no unauthorized data was accessed during the investigation.
5. Record approval, action, recovery time, and follow-up.

Escalate unresolved dependency failure to the document-service owner.
