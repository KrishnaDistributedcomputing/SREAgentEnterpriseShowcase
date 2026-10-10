---
title: AI Inference Gateway Incident Runbook
description: Investigate and recover model endpoint dependency incidents
author: Enterprise SRE Platform Team
ms.date: 2026-10-10
ms.topic: troubleshooting
---

## Service objective

Maintain 99.9 percent availability and complete inference within 1,200 ms.

## Detection

Identify HTTP 503 responses referencing `model-endpoint`.

## Investigation

Confirm gateway health, inspect dependency traces, and compare the incident with
model-provider or deployment changes. No prompts or model outputs are persisted.

## Mitigation

Approve clearing the dependency fault. Production provider failover requires
model, safety, privacy, and cost validation.

## Verification and rollback

Submit a synthetic inference operation and confirm success. Revert any provider
change that increases errors or violates policy.

