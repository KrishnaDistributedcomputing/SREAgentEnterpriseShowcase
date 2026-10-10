---
title: Claims Processing Incident Runbook
description: Investigate and recover claims document dependency incidents
author: Enterprise SRE Platform Team
ms.date: 2026-10-10
ms.topic: troubleshooting
---

## Service objective

Maintain 99.9 percent availability and submit claims within 1,000 ms.

## Detection

Identify HTTP 503 responses referencing `document-service`.

## Investigation

Correlate dependency errors, confirm readiness is healthy, and verify no real
policyholder documents or personal data are present.

## Mitigation

Approve clearing the dependency fault. Production document replay requires a
separate data-handling and idempotency procedure.

## Verification and rollback

Submit a synthetic claim and confirm success. Stop the exercise if any connected
source contains regulated data.

