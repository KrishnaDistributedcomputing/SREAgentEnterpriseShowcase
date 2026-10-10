---
title: Azure SRE Agent Configuration Guide
description: Connect, govern, and validate Azure SRE Agent for this showcase
author: Enterprise SRE Platform Team
ms.date: 2026-10-10
ms.topic: how-to
estimated_reading_time: 10
---

## Deploy the agent

Use the official
[Azure SRE Agent IaC templates](https://github.com/microsoft/sre-agent/tree/main/sreagent-templates).
The templates support Bicep, Terraform, PowerShell, and Azure Developer CLI.
Keep the agent configuration in a secured environment repository when it
contains organization-specific connector details.

## Connect context

Configure these sources in order:

1. Connect this GitHub repository for source, scenario metadata, and runbooks.
2. Connect the Application Insights resource created by `infra/main.bicep`.
3. Grant the agent Reader access to the showcase resource group.
4. Connect Azure Monitor as the incident platform.
5. Create one response plan filtered to showcase alert titles and severity.

## Permission posture

Begin with Reader permissions. Microsoft documents that the agent uses a
user-assigned managed identity and can use on-behalf-of authorization when a
Reader-level agent needs a write action. Keep permanent write roles narrow and
resource-specific.

## Response plan

Use Review mode until each scenario has completed:

* A successful investigation
* A correct proposed mitigation
* An authorized approval
* A successful recovery check
* A documented rollback path

Set a reinvestigation cooldown so one active fault does not generate repeated
investigations.

## Tool policy baseline

The example policy is conceptual because tool names depend on connected tools:

```json
{
  "allow": [
    "RunAzCliReadCommands",
    "QueryApplicationInsights"
  ],
  "ask": [
    "RestartContainerAppRevision",
    "ScaleContainerApp"
  ],
  "deny": [
    "bash(az * delete *)",
    "bash(az role assignment *)",
    "ReadSecretValue"
  ]
}
```

Validate actual tool identifiers in the portal before applying policy. Keep
deletion as a facilitator-owned cleanup action outside the incident workflow.

## Investigation prompt

Use this prompt after the alert is connected:

```text
Investigate the matching showcase incident. Identify the affected service,
customer impact, violated SLO signal, probable fault mode, and downstream
dependency. Cite telemetry, source, and runbook evidence. Propose only reversible
actions. Do not execute writes without approval. After action, verify readiness
and a successful business operation.
```

## Acceptance check

An investigation passes when it names the correct scenario, distinguishes the
fault type, references telemetry and source, proposes the documented recovery,
requests approval, and confirms a successful post-recovery operation.

