---
title: Order Fulfillment Incident Runbook
description: Investigate and recover fulfillment dispatch errors
author: Enterprise SRE Platform Team
ms.date: 2026-10-10
ms.topic: troubleshooting
---

## Service objective

Maintain 99.9 percent availability and dispatch orders within 800 ms.

## Detection

Look for HTTP 500 responses from `dispatch-order`.

## Investigation

Inspect error traces, affected revision, and `fulfillment-queue` context. Confirm
the symptom is an application error rather than readiness loss.

## Mitigation

Approve clearing the error fault. Production replay or queue intervention is
outside showcase scope.

## Verification and rollback

Submit a synthetic order and confirm success. Roll back a revision only when the
investigation correlates the incident with that revision.

