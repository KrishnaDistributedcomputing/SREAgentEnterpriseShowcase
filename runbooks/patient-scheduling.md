---
title: Patient Scheduling Incident Runbook
description: Investigate and recover scheduling latency
author: Enterprise SRE Platform Team
ms.date: 2026-10-10
ms.topic: troubleshooting
---

## Service objective

Maintain 99.95 percent availability and book appointments within 600 ms.

## Detection

Look for sustained latency above the objective with successful health probes.

## Investigation

Inspect traces around `provider-calendar`, revision timing, and request duration.
Confirm all records are synthetic.

## Mitigation

Approve clearing the latency fault. Do not connect the exercise to a clinical
system or patient dataset.

## Verification and rollback

Book three synthetic appointments and confirm latency recovery. Revert any
demonstration configuration that creates continued delay.

