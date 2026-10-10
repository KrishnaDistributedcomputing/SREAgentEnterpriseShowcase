---
title: Inventory Service Incident Runbook
description: Investigate and recover inventory database outages
author: Enterprise SRE Platform Team
ms.date: 2026-10-10
ms.topic: troubleshooting
---

## Service objective

Maintain 99.9 percent availability and reserve inventory within 500 ms.

## Detection

Identify HTTP 503 responses associated with `inventory-database`.

## Investigation

Confirm application health, trace the dependency failure, and inspect whether
Retail Checkout or Order Fulfillment reports correlated impact.

## Mitigation

Approve clearing the dependency fault. Do not simulate inventory writes or
adjust stock quantities during the showcase.

## Verification and rollback

Reserve one synthetic unit and confirm HTTP 200. Stop checkout traffic if
inventory remains unavailable.

