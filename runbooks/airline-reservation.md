---
title: Airline Reservation Incident Runbook
description: Investigate and recover reservation errors
author: Enterprise SRE Platform Team
ms.date: 2026-10-10
ms.topic: troubleshooting
---

## Service objective

Maintain 99.95 percent availability and reserve seats within 700 ms.

## Detection

Look for HTTP 500 responses from `reserve-seat`.

## Investigation

Correlate failures with the active revision and inspect `seat-inventory` context.
Confirm no external booking system is connected.

## Mitigation

Approve clearing the error fault. Production reservation replay requires
idempotency and inventory reconciliation controls not represented here.

## Verification and rollback

Reserve one synthetic seat and confirm success. Roll back only a correlated
revision change.

