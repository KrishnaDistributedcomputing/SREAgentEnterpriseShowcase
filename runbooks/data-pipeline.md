---
title: Data Pipeline Incident Runbook
description: Investigate and recover analytics warehouse dependency incidents
author: Enterprise SRE Platform Team
ms.date: 2026-10-10
ms.topic: troubleshooting
---

## Service objective

Maintain 99.5 percent availability and start jobs within 1,500 ms.

## Detection

Identify HTTP 503 responses referencing `analytics-warehouse`.

## Investigation

Confirm application health, review dependency evidence, and check whether the
incident affects only synthetic jobs.

## Mitigation

Approve clearing the dependency fault. Do not retry, cancel, or modify real
analytics jobs.

## Verification and rollback

Start one synthetic job and confirm success. Stop the exercise if a production
warehouse connector is present.

