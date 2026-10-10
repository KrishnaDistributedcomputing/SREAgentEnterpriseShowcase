---
title: Banking Ledger Incident Runbook
description: Investigate and recover ledger readiness incidents
author: Enterprise SRE Platform Team
ms.date: 2026-10-10
ms.topic: troubleshooting
---

## Service objective

Maintain 99.99 percent availability and post entries within 250 ms.

## Detection

Look for readiness probe failures while liveness remains successful.

## Investigation

Verify the failing revision, review readiness history, and confirm no ledger data
is involved. The showcase uses synthetic operations only.

## Mitigation

Approve clearing the not-ready fault. Do not grant database or transaction-write
permissions to the agent for this scenario.

## Verification and rollback

Confirm readiness and one successful synthetic ledger operation. If readiness
does not recover, remove the revision from traffic through an approved action.

