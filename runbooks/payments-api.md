---
title: Payments API Incident Runbook
description: Investigate and recover payment authorization latency
author: Enterprise SRE Platform Team
ms.date: 2026-10-10
ms.topic: troubleshooting
---

## Service objective

Maintain 99.99 percent availability and authorize payments within 300 ms.

## Detection

Look for request duration above the SLO without a corresponding readiness failure.

## Investigation

Compare latency by revision, inspect traces around `card-processor`, and exclude
platform CPU or replica saturation before assigning dependency cause.

## Mitigation

Approve clearing the latency fault. A production response requires processor
timeout, circuit-breaker, and fallback controls owned by the payment team.

## Verification and rollback

Submit three business operations and confirm latency returns below the threshold.
Roll back any configuration change that increases errors.

