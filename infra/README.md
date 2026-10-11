---
title: Azure Deployment Guide
description: Deploy the 15 application showcase to Azure Container Apps
author: Enterprise SRE Platform Team
ms.date: 2026-10-10
ms.topic: how-to
estimated_reading_time: 7
---

## Resource model

The Bicep template creates a shared Log Analytics workspace, workspace-based
Application Insights resource, Container Apps environment, and 15 Container Apps.
It expects an existing Azure Container Registry and user-assigned managed identity.

The template does not deploy Azure SRE Agent. Use the official
[Azure SRE Agent IaC templates](https://github.com/microsoft/sre-agent/tree/main/sreagent-templates)
for the agent, then connect it to the resources created here.

## Prepare

1. Build and push the repository container image.
2. Create a user-assigned managed identity.
3. Grant that identity `AcrPull` on the registry.
4. Copy `main.bicepparam` to an environment-specific parameter file.
5. Replace every placeholder and supply the secret parameter outside source control.

## Preview

```powershell
az deployment group what-if `
  --resource-group "rg-sre-showcase-demo" `
  --parameters "infra/main.bicepparam" `
  --parameters demoApiKey="$env:DEMO_API_KEY"
```

Review resource creation, identity assignments, public ingress, and expected cost.

Set `minimumReplicas` to `1` for a scheduled live demonstration where cold-start
latency would disrupt the audience experience. Return it to `0` afterward to
restore scale-to-zero behavior.

## Deploy

```powershell
az deployment group create `
  --resource-group "rg-sre-showcase-demo" `
  --template-file "infra/main.bicep" `
  --parameters "infra/main.bicepparam" `
  --parameters demoApiKey="$env:DEMO_API_KEY"
```

## Teardown

Delete the dedicated resource group after the workshop:

```powershell
az group delete --name "rg-sre-showcase-demo"
```

Use deletion only as a facilitator cleanup action. Global Azure SRE Agent tool
policy should deny resource deletion during incident demonstrations.
