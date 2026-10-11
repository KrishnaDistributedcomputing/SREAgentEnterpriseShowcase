---
title: Azure Deployment Guide
description: Choose and deploy the complete MVP or existing-resource Azure Container Apps topology
author: Enterprise SRE Platform Team
ms.date: 2026-10-11
ms.topic: how-to
estimated_reading_time: 8
---

## Deployment options

| Option | Entry point | Use when |
|--------|-------------|----------|
| Complete MVP | [`mvp/foundation.bicep`](mvp/foundation.bicep) and [`mvp/workload.bicep`](mvp/workload.bicep) | Azure resources do not exist yet |
| Existing resources | [`main.bicep`](main.bicep) | Registry and workload identity already exist |

The complete MVP is the recommended path for a new evaluation. It adds cost
governance, identity, registry, shared observability, application monitoring, and
availability tests. Read the [complete MVP deployment guide](mvp/README.md).

## Complete MVP resource model

The two-stage deployment creates:

* One dedicated resource group
* One resource-group-filtered monthly budget
* One Basic Azure Container Registry
* One user-assigned workload identity with registry-scoped `AcrPull`
* One Log Analytics workspace with 30-day retention
* One workspace-based Application Insights resource
* One Azure Container Apps environment
* One optional Azure Monitor action group
* Fifteen independently addressable Container Apps
* Readiness availability tests for the four representative MVP applications
* Latency, error-rate, and availability alerts for those applications

The applications scale to zero by default. The monitored MVP applications are
Retail Checkout, Order Fulfillment, Payments API, and Banking Ledger.

## Why deployment has two stages

Bicep deploys Azure resources but does not build a container image. The
foundation stage creates Azure Container Registry and returns its name. Build the
image with `az acr build`, then deploy the workload stage that references it.

This sequence prevents Container Apps from starting with a missing image.

## Existing-resource deployment

The legacy template creates Log Analytics, Application Insights, a Container
Apps environment, and all 15 applications. It expects an existing registry and
user-assigned identity.

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

## Azure SRE Agent

Azure SRE Agent is deployed separately with Microsoft's maintained
[official Bicep templates](https://github.com/microsoft/sre-agent/tree/main/sreagent-templates/bicep).
The MVP foundation outputs the Application Insights application ID, Application
Insights resource ID, Log Analytics resource ID, and target resource-group name
required by that template.

Keeping the vendor-managed template separate avoids copying preview resource
schemas into this repository and allows Microsoft upgrades to be adopted
deliberately.

## Teardown

Delete the agent with the official template's cleanup workflow. Delete the
showcase resource group after exporting required evidence:

```powershell
az group delete --name "rg-sre-showcase-mvp"
```

Resource deletion remains a facilitator action outside Azure SRE Agent incident
response.
