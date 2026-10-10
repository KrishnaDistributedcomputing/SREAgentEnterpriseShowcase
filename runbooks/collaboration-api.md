---
title: Collaboration API Incident Runbook
description: Investigate and recover collaboration messaging latency
author: Enterprise SRE Platform Team
ms.date: 2026-10-10
ms.topic: troubleshooting
---

## Service objective

Maintain 99.95 percent availability and publish messages within 300 ms.

## Detection

Look for latency above the objective with successful status and health probes.

## Investigation

Inspect traces around `message-broker`, compare revisions, and verify no customer
message content is captured.

## Mitigation

Approve clearing the latency fault. Production queue scaling requires separate
capacity and cost approval.

## Verification and rollback

Publish three synthetic messages and confirm latency recovery.

