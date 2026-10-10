---
title: Retail Checkout Incident Runbook
description: Investigate and recover checkout dependency incidents
author: Enterprise SRE Platform Team
ms.date: 2026-10-10
ms.topic: troubleshooting
---

## Service objective

Maintain 99.95 percent availability and complete checkout within 450 ms.

## Detection

Look for elevated HTTP 503 responses from `retail-checkout` while liveness and
readiness remain healthy.

## Investigation

Confirm the `payment-authorization` dependency symptom, correlate the first error
with deployment changes, and verify other services are not producing the same fault.

## Mitigation

In Review mode, approve clearing the bounded dependency fault. In a production
analogue, fail over only through an approved payment-provider procedure.

## Verification and rollback

Call `/health/ready`, submit `/work`, and confirm HTTP 200. If recovery fails,
stop traffic generation and roll back the last approved change.

