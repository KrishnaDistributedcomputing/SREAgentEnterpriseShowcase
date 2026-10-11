---
title: Logistics Tracking Incident Runbook
description: Application context and governed investigation of tracking stream incidents
author: Enterprise SRE Platform Team
ms.date: 2026-10-11
ms.topic: troubleshooting
estimated_reading_time: 8
---

## Application overview

Logistics Tracking records synthetic shipment locations through an event stream.
The service supports shipment visibility and exception detection. When updates
stop, locations become stale and delayed deliveries can go unnoticed.

| Attribute | Value |
|-----------|-------|
| Portfolio | Industrial and data |
| Business domain | Transportation |
| Business operation | `record-location` |
| Critical dependency | `tracking-event-stream` |
| Availability objective | 99.9 percent |
| Latency objective | Under 900 ms |
| Demonstrated fault | Dependency unavailable |
| Business impact | Shipment locations become stale and exceptions are missed |

The dependency fault returns HTTP 503 while process health may remain normal.
Only synthetic shipment and location data is used.

## Where Azure SRE Agent plays a role

Azure SRE Agent connects request failures, dependency traces, revision state,
resource health, and location-freshness impact.

1. Detect failed `record-location` operations.
2. Correlate HTTP 503 responses with `tracking-event-stream`.
3. Exclude process, readiness, and deployment failures.
4. Explain stale visibility and missed-exception impact.
5. Recommend the bounded dependency-fault clear operation for approval.
6. Verify a new location update and telemetry recovery.

The agent must not purge or replay external streams, inspect real shipment data,
change producer configuration, or access stream credentials.

## Detection and triage

Investigate HTTP 503 responses referencing the tracking stream. Escalate when
updates are stale beyond the business threshold or multiple producers are affected.

Collect dependency spans, first failure time, revision, health status, and last
successful synthetic update.

## Investigation procedure

1. Confirm service metadata and objectives.
2. Compare failed updates with liveness and readiness.
3. Inspect `tracking-event-stream` dependency evidence.
4. Review deployment and resource health at fault onset.
5. Confirm only synthetic locations are involved.
6. Present probable cause, confidence, blast radius, and action.

## Mitigation

Approve clearing the bounded dependency fault. Do not purge, replay, or reroute
external streams during the showcase. If recovery fails, stop synthetic producers
and escalate to the stream owner.

## Recovery verification

1. Confirm readiness returns HTTP 200.
2. Record three synthetic locations and confirm HTTP 200.
3. Verify latency remains under 900 ms and errors stop.
4. Confirm location freshness resumes in demonstration telemetry.
5. Record approval, action, evidence, and recovery time.

Production replay requires ownership, ordering, and duplicate-handling controls.
