---
title: Inventory Service Incident Runbook
description: Application context and governed investigation of inventory database outages
author: Enterprise SRE Platform Team
ms.date: 2026-10-11
ms.topic: troubleshooting
estimated_reading_time: 8
---

## Application overview

Inventory Service reserves stock before an order is accepted. Retail Checkout
uses the reservation result to prevent overselling, while Order Fulfillment
depends on accurate inventory state before dispatch. The showcase performs only
synthetic reservations and never changes real stock.

| Attribute | Value |
|-----------|-------|
| Portfolio | Commerce and retail |
| Business domain | Retail |
| Business operation | `reserve-inventory` |
| Critical dependency | `inventory-database` |
| Availability objective | 99.9 percent |
| Latency objective | Under 500 ms |
| Demonstrated fault | Dependency unavailable |
| Business impact | Orders oversell or fail because inventory cannot be reserved |

The process can remain live and ready while the database dependency returns an
error. This distinction helps operators avoid restarting a healthy application
when the actual failure is downstream.

## Where Azure SRE Agent plays a role

Azure SRE Agent connects the Azure Monitor alert to application telemetry,
Container Apps revision state, this runbook, and the service metadata. Its role
is to shorten investigation time while preserving operator accountability.

1. Detect HTTP 503 growth and identify Inventory Service as the affected workload.
2. Correlate failed `reserve-inventory` traces with `inventory-database`.
3. Compare liveness, readiness, revision, and resource health to exclude a process
   or deployment failure.
4. Identify correlated checkout and fulfillment impact and explain the risk of
   overselling or rejected orders.
5. Recommend the bounded fault-clear operation in Review mode.
6. After approval, verify readiness and a successful synthetic reservation.

The agent must not inspect customer orders, alter quantities, write to an
inventory database, broaden RBAC, retrieve secrets, or delete resources.

## Detection and triage

Investigate when HTTP 503 responses rise or the business-operation counter records
failed reservations. Confirm `/health/live` and `/health/ready` before assigning
severity. Treat correlated checkout failures as revenue-path impact.

Collect the alert time, affected revision, status-code trend, failed trace,
dependency name, and the first observed business failure.

## Investigation procedure

1. Read `/api/metadata` and confirm the expected SLO and dependency.
2. Compare request failures with successful liveness and readiness probes.
3. Inspect failed spans for the `inventory-database` dependency marker.
4. Check revision changes and Azure resource health near the first failure.
5. Look for correlated impact in Retail Checkout and Order Fulfillment.
6. State the probable cause, evidence, confidence, blast radius, and proposed
   reversible action before requesting approval.

## Mitigation

In the showcase, approve clearing the bounded dependency fault. Do not simulate
inventory writes or adjust quantities. In production, use the inventory team's
approved database failover, circuit-breaker, or traffic-control procedure.

If the dependency remains unavailable, stop checkout traffic that requires a
confirmed reservation and escalate to the inventory database owner.

## Recovery verification

1. Confirm `/health/ready` returns HTTP 200.
2. Submit one synthetic `reserve-inventory` operation and confirm HTTP 200.
3. Confirm dependency errors stop and request latency remains under 500 ms.
4. Verify correlated checkout and fulfillment failures recover.
5. Record the approver, action, recovery time, and remaining follow-up.

Rollback any application or routing change that introduces new errors. Do not
close the incident based only on a healthy process probe.
