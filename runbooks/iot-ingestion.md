---
title: IoT Ingestion Incident Runbook
description: Investigate and recover device telemetry ingestion errors
author: Enterprise SRE Platform Team
ms.date: 2026-10-10
ms.topic: troubleshooting
---

## Service objective

Maintain 99.9 percent availability and ingest telemetry within 400 ms.

## Detection

Look for HTTP 500 responses from `ingest-telemetry`.

## Investigation

Inspect error traces and `device-event-hub` context. Verify that only synthetic
device events are in scope.

## Mitigation

Approve clearing the error fault. Stream partition changes and event replay are
outside showcase scope.

## Verification and rollback

Submit synthetic telemetry and confirm success. Stop event generation if errors continue.

