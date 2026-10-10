---
title: Azure SRE Agent Product Research
description: Official product evidence and design implications for the enterprise showcase
author: Enterprise SRE Platform Team
ms.date: 2026-10-10
ms.topic: reference
estimated_reading_time: 10
---

## Research method

Product claims were checked against Microsoft Learn and the official
`microsoft/sre-agent` repository on 2026-10-10. Feature availability, regions,
models, billing, and interfaces can change. Revalidate before a customer event.

## Verified capabilities and implications

| Official capability | Showcase implication |
|---------------------|----------------------|
| Correlates observability, incident, Azure resource, and source context | Connect GitHub, Application Insights, the showcase resource group, and Azure Monitor |
| Supports incident response plans and Review or Autonomous modes | Begin every workshop in Review mode |
| Uses a user-assigned managed identity | Grant resource-group-scoped diagnostic access without secrets |
| Provides Reader and Privileged permission levels | Default to Reader and approve temporary or scoped writes |
| Supports skills, Python tools, MCP servers, and hooks | Keep base demo native, then discuss controlled extensions |
| Supports allow, ask, and deny tool policies | Deny deletion and ask before write operations |
| Supports IaC through official templates | Use the official templates for the agent and repository Bicep for workloads |
| Supports scheduled operational work | Include proactive health-check use cases in the workshop backlog |

## Key control findings

Each agent has a user-assigned managed identity. Without assigned resource groups,
the identity has no resource permissions. Microsoft recommends explicit access
and describes Reader, Log Analytics Reader, Monitoring Reader, and Monitoring
Contributor roles for core scenarios.

Response plans filter incidents and choose autonomy. In Review mode, proposed
actions require approval. In Autonomous mode, allowed actions can execute within
configured permissions.

Tool policy precedence and hook behavior require careful design. Global policies
can deny tools, while approved hook behavior can affect policy evaluation. Only
SRE Agent administrators should create governance hooks, and every override must
be audited.

## Primary sources

* [Overview of Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/overview)
* [Create and Set Up Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/create-and-set-up)
* [Agent Permissions](https://learn.microsoft.com/en-us/azure/sre-agent/permissions)
* [Automate Incident Response](https://learn.microsoft.com/en-us/azure/sre-agent/automate-incidents)
* [Deploy with Infrastructure as Code](https://learn.microsoft.com/en-us/azure/sre-agent/deploy-iac)
* [Tool Access Policies](https://learn.microsoft.com/en-us/azure/sre-agent/tool-access-policies)
* [Agent Hooks](https://learn.microsoft.com/en-us/azure/sre-agent/agent-hooks)
* [Official Azure SRE Agent community repository](https://github.com/microsoft/sre-agent)
* [Enable OpenTelemetry in Application Insights](https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-enable)
