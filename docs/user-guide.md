---
title: Enterprise SRE Agent Showcase User Guide
description: Setup, operation, incident simulation, recovery, and troubleshooting guide
author: Enterprise SRE Platform Team
ms.date: 2026-10-11
ms.topic: how-to
keywords:
  - user guide
  - operations
  - azure sre agent
estimated_reading_time: 20
---

## Choose your user path

| Role | Start here |
|------|------------|
| Local evaluator | Run one application with uv |
| Workshop facilitator | Deploy fleet, configure the agent, run a scenario |
| On-call operator | Review evidence, approve action, verify recovery |
| Platform administrator | Configure Azure, identity, telemetry, and policies |
| FinOps reviewer | Apply the cost model and monitor actual usage |

## Local setup

### Prerequisites

Install Python 3.12, uv, Git, and optionally Docker Desktop.

### Install dependencies

```powershell
uv sync --frozen
uv run ruff check .
uv run pytest
```

### Browse the application portfolios

Read `apps/README.md`, then choose a slug from one of the five portfolios.
Portfolio names organize files but are not part of the slug.

### Start an application

```powershell
$env:APP_SLUG = "payments-api"
$env:ENABLE_FAULT_INJECTION = "true"
$env:DEMO_API_KEY = "replace-with-a-local-secret"
uv run uvicorn sre_showcase.app:create_app_from_environment --factory --port 8080
```

Open:

* `http://localhost:8080/` for the fleet landing page and application table
* `http://localhost:8080/api/metadata` for current application and SLO context
* `http://localhost:8080/docs` for interactive API documentation
* `http://localhost:8080/health/ready` for readiness

## Run the local fleet

Start Docker Desktop, then run:

```powershell
$env:DEMO_API_KEY = "replace-with-a-local-secret"
docker compose up --build
```

Applications use ports `8101` through `8115` in the order shown in the root
README catalog. Stop the fleet with `docker compose down`.

## Deploy to Azure

### Choose the deployment path

Use `infra/mvp/foundation.bicep` and `infra/mvp/workload.bicep` for a new
evaluation. The complete MVP deployment creates the resource group, budget,
registry, workload identity, observability resources, Container Apps environment,
15 applications, representative alerts, and availability tests.

Use `infra/main.bicep` only when the registry and workload identity already exist.

### Deploy the complete MVP

1. Copy `infra/mvp/foundation.bicepparam` to an environment-specific file.
2. Replace owner, email, cost center, budget date, and expiry placeholders.
3. Run a subscription-scope what-if for `foundation.bicep`.
4. Deploy the foundation and capture its outputs.
5. Build the shared image in the output registry with `az acr build`.
6. Run a resource-group what-if for `workload.bicep`.
7. Supply the demonstration key through `DEMO_API_KEY`.
8. Deploy the workload using the foundation output names.
9. Verify application URLs, telemetry, availability tests, and alerts.

The complete commands and output mappings are in
`infra/mvp/README.md`.

### Deploy with existing resources

```powershell
az deployment group what-if `
  --resource-group "rg-sre-showcase-demo" `
  --template-file "infra/main.bicep" `
  --parameters "infra/main.bicepparam" `
  --parameters demoApiKey="$env:DEMO_API_KEY"

az deployment group create `
  --resource-group "rg-sre-showcase-demo" `
  --template-file "infra/main.bicep" `
  --parameters "infra/main.bicepparam" `
  --parameters demoApiKey="$env:DEMO_API_KEY"
```

Do not deploy until the what-if output matches the expected 15 applications and
shared observability resources.

## Configure Azure SRE Agent

1. Deploy one agent using the official `microsoft/sre-agent` Bicep template.
2. Connect this GitHub repository.
3. Map the MVP foundation Application Insights application ID and resource ID.
4. Grant the agent Reader access to the showcase resource group.
5. Map the MVP foundation Log Analytics resource ID.
6. Connect Azure Monitor as the incident platform.
7. Add a response plan filtered to `SRE-SHOWCASE` alerts.
8. Select Review mode.
9. Add global tool policy that denies deletion and secret retrieval.
10. Set an active-flow AAU allocation limit.

## Run an incident scenario

### Prevent cold starts during a live event

Set `minimumReplicas=1` during a scheduled demonstration so browser navigation
does not time out while Azure starts a scaled-to-zero replica. Restore the value
to `0` after the event.

### Select the scenario

Choose one application based on audience priorities. Read its `scenario.json`
and runbook before activating a fault.

### Verify baseline

```powershell
$baseUrl = "https://REPLACE_WITH_APP_FQDN"
Invoke-RestMethod "$baseUrl/health/live"
Invoke-RestMethod "$baseUrl/health/ready"
Invoke-RestMethod -Method Post "$baseUrl/work"
```

All three calls must succeed before the exercise.

### Activate the default fault

```powershell
$headers = @{ "X-Demo-Key" = $env:DEMO_API_KEY }
$body = @{
  mode = "dependency"
  duration_seconds = 300
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "$baseUrl/faults" `
  -Headers $headers -ContentType "application/json" -Body $body
```

Use the fault defined in the selected `scenario.json`. Keep duration at five
minutes or less for live demonstrations.

### Generate the signal

Send a small number of requests that is sufficient to meet the configured alert
threshold. Avoid continuous traffic.

```powershell
1..10 | ForEach-Object {
  try {
    Invoke-WebRequest -Method Post -Uri "$baseUrl/work" -ErrorAction Stop
  }
  catch {
    Write-Host "Expected demonstration response: $($_.Exception.Message)"
  }
}
```

### Review the investigation

Confirm that Azure SRE Agent identifies:

* Correct application and alert
* Customer or business impact
* Fault class and named dependency
* Supporting telemetry
* Relevant source and runbook
* Reversible proposed action
* Required approval

Reject the action if any item is missing or incorrect.

### Recover

```powershell
Invoke-RestMethod -Method Delete -Uri "$baseUrl/faults" -Headers $headers
Invoke-RestMethod "$baseUrl/health/ready"
Invoke-RestMethod -Method Post "$baseUrl/work"
```

Record investigation start and recovery time.

## Operator guardrails

Never:

* Connect production data to this showcase
* Expand Azure scope during an active incident
* Approve deletion or role-assignment changes
* Display the demonstration key
* Treat a generated conclusion as verified without telemetry
* Leave the resource group running without an owner and budget

## Troubleshooting

### Application does not start

Check `APP_SLUG`, confirm it matches a scenario directory, and run
`uv run pytest tests/test_catalog.py`.

### Fault endpoint returns 404

Set `ENABLE_FAULT_INJECTION=true`. A 404 is expected when fault injection is
disabled.

### Fault endpoint returns 401

Confirm `DEMO_API_KEY` is set and the `X-Demo-Key` header matches. Do not log the
value.

### Telemetry does not appear

Confirm the Application Insights connection string is present in the Container
App revision, then inspect revision logs for telemetry configuration. Allow for
ingestion delay before changing configuration.

### Alert does not reach the agent

Check alert state, Azure Monitor connector health, response-plan severity and
title filters, cooldown, and agent state. Do not broaden the filter to unrelated
production alerts.

### Docker build fails to connect

Start Docker Desktop and confirm the Linux container engine is running. Compose
configuration can be checked without a running engine:

```powershell
docker compose config --quiet
```

## End the workshop

1. Clear every fault.
2. Confirm all applications are healthy.
3. Export approved evidence and cost data.
4. Remove temporary connector authorization.
5. Delete the dedicated resource group when retention is not required.
6. Delete the agent to stop always-on billing when the evaluation is complete.
