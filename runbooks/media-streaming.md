---
title: Media Streaming Incident Runbook
description: Investigate and recover playback startup latency
author: Enterprise SRE Platform Team
ms.date: 2026-10-10
ms.topic: troubleshooting
---

## Service objective

Maintain 99.95 percent availability and start playback within 350 ms.

## Detection

Look for elevated request duration while health probes and response status remain healthy.

## Investigation

Compare traces by revision and inspect the `content-delivery-network` dependency
before attributing the delay to application compute.

## Mitigation

Approve clearing the latency fault. CDN routing changes are outside showcase scope.

## Verification and rollback

Start three synthetic playback sessions and confirm latency returns below target.

