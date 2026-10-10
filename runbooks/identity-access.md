---
title: Identity Access Incident Runbook
description: Investigate and recover identity readiness incidents
author: Enterprise SRE Platform Team
ms.date: 2026-10-10
ms.topic: troubleshooting
---

## Service objective

Maintain 99.99 percent availability and evaluate access within 200 ms.

## Detection

Identify readiness failures while process liveness remains healthy.

## Investigation

Inspect revision health and `identity-provider` context. Confirm the agent cannot
read secrets, tokens, or real identities.

## Mitigation

Approve clearing the not-ready fault. Production identity failover must follow
the organization's access-control emergency procedure.

## Verification and rollback

Confirm readiness and one synthetic access evaluation. Revoke any temporary
authorization used during the exercise.

