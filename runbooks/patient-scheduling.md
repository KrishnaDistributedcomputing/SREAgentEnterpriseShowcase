---
title: Patient Scheduling Incident Runbook
description: Application context and governed investigation of appointment latency
author: Enterprise SRE Platform Team
ms.date: 2026-10-11
ms.topic: troubleshooting
estimated_reading_time: 8
---

## Application overview

Patient Scheduling books synthetic clinical appointments against provider
calendar availability. It models a patient-facing access channel where delay
prevents self-service booking and increases contact-center demand.

| Attribute | Value |
|-----------|-------|
| Portfolio | Customer experience |
| Business domain | Healthcare |
| Business operation | `book-appointment` |
| Critical dependency | `provider-calendar` |
| Availability objective | 99.95 percent |
| Latency objective | Under 600 ms |
| Demonstrated fault | Elevated latency |
| Business impact | Patients cannot book care and contact-center volume rises |

The latency fault preserves successful health probes and status codes. The
incident is visible through request duration and business telemetry.

## Where Azure SRE Agent plays a role

Azure SRE Agent correlates latency telemetry, calendar dependency spans, revision
timing, and resource health while keeping clinical and patient data out of scope.

1. Detect sustained booking latency above 600 ms.
2. Compare end-to-end duration with `provider-calendar` span duration.
3. Exclude compute saturation, readiness, and revision rollout.
4. Explain patient-access and contact-center impact.
5. Recommend the bounded latency-fault clear operation for approval.
6. Verify several synthetic bookings after recovery.

The agent must not access patient records, appointment details, clinical systems,
secrets, or real provider calendars.

## Detection and triage

Investigate sustained latency above the objective with successful probes. Increase
priority when failures or abandonment indicators accompany the delay.

Collect percentile duration, dependency spans, revision, resource utilization,
and the first SLO breach.

## Investigation procedure

1. Confirm service metadata and the 600 ms objective.
2. Compare request and `provider-calendar` duration.
3. Review latency by revision and deployment time.
4. Exclude replica scaling or platform saturation.
5. Confirm every record and dependency is synthetic.
6. Present probable cause, confidence, impact, and proposed action.

## Mitigation

Approve clearing the bounded latency fault. Do not connect the exercise to a
clinical system or patient dataset. Production calendar failover must follow the
healthcare organization's continuity and privacy procedures.

## Recovery verification

1. Book three synthetic appointments.
2. Confirm each response succeeds below 600 ms.
3. Verify health remains normal and latency returns to baseline.
4. Confirm no patient data was used or exposed.
5. Record approval, evidence, action, and recovery time.

Revert any demonstration configuration that creates continued delay.
