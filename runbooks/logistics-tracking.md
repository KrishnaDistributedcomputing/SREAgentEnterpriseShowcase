---
title: Logistics Tracking Incident Runbook
description: Investigate and recover tracking event-stream incidents
author: Enterprise SRE Platform Team
ms.date: 2026-10-10
ms.topic: troubleshooting
---

## Service objective

Maintain 99.9 percent availability and record locations within 900 ms.

## Detection

Identify HTTP 503 responses referencing `tracking-event-stream`.

## Investigation

Confirm application health, review dependency traces, and assess whether
synthetic location updates have stopped.

## Mitigation

Approve clearing the dependency fault. Do not purge or replay external streams
during the showcase.

## Verification and rollback

Record a synthetic location and confirm success. Stop producers if recovery does
not occur.

