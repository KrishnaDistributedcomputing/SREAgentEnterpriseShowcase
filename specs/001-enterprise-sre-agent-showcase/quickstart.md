---
title: Enterprise SRE Showcase Quickstart
description: Local setup and first incident simulation for the Azure SRE Agent showcase
author: Enterprise SRE Platform Team
ms.date: 2026-10-10
ms.topic: tutorial
estimated_reading_time: 7
---

## Prepare the environment

```powershell
uv sync
uv run pytest
```

## Start Retail Checkout

```powershell
$env:APP_SLUG = "retail-checkout"
$env:ENABLE_FAULT_INJECTION = "true"
$env:DEMO_API_KEY = "local-demo-only"
uv run uvicorn sre_showcase.app:create_app_from_environment --factory --port 8080
```

In another terminal, verify normal behavior:

```powershell
Invoke-RestMethod "http://localhost:8080/health/ready"
Invoke-RestMethod -Method Post "http://localhost:8080/work?units=2"
```

## Create the incident symptom

```powershell
$headers = @{ "X-Demo-Key" = "local-demo-only" }
$body = @{ mode = "dependency"; duration_seconds = 120 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://localhost:8080/faults" `
  -Headers $headers -ContentType "application/json" -Body $body
```

Business traffic now returns HTTP 503 while liveness and readiness remain healthy.
This isolates a downstream dependency symptom from a process-health symptom.

## Recover

```powershell
Invoke-RestMethod -Method Delete -Uri "http://localhost:8080/faults" -Headers $headers
Invoke-RestMethod -Method Post "http://localhost:8080/work"
```

The final request must return HTTP 200. If the fault is not cleared manually, it
expires automatically.

