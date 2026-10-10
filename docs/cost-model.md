---
title: Azure SRE Agent Showcase Cost Model
description: Central US retail estimate for workshops, pilots, and sustained evaluation
author: Enterprise SRE Platform Team
ms.date: 2026-10-10
ms.topic: reference
keywords:
  - azure cost
  - central us
  - finops
  - azure agent units
estimated_reading_time: 15
---

## Pricing basis

This model uses public Azure retail rates for Central US in USD, retrieved on
2026-10-10. It is an estimate, not a quote. Enterprise agreements, taxes, free
grants, model changes, data volume, network egress, and preview or evaluation
offers can change the result.

Validate all figures in the Azure Pricing Calculator and Azure Cost Management
before deployment.

## Unit rates

### Azure SRE Agent

Microsoft bills Azure SRE Agent in Azure Agent Units (AAUs):

* One AAU is modeled at $0.10.
* Always-on flow consumes 4 AAUs per agent-hour.
* Active flow depends on model-specific input, output, cache-read, and cache-write tokens.
* Always-on billing continues until the agent is deleted.
* New-customer evaluation can waive always-on cost when eligible.

One continuously provisioned agent has an estimated fixed monthly cost:

```text
4 AAUs/hour x 730 hours x $0.10/AAU = $292.00/month
```

### Azure Container Apps

Central US retail meters:

| Meter | Rate |
|-------|------|
| Active vCPU | $0.000024 per vCPU-second |
| Idle vCPU | $0.000003 per vCPU-second |
| Active or idle memory | $0.000003 per GiB-second |
| Requests | $0.40 per million |
| Environment management | $0.10 per hour |

The public pricing page lists monthly grants of 180,000 vCPU-seconds, 360,000
GiB-seconds, and 2 million requests. Scale-to-zero applications have no replica
compute charge while stopped. The environment meter can still apply.

### Azure Monitor and Log Analytics

Central US retail meters used by this model:

| Meter | Rate |
|-------|------|
| Analytics Logs ingestion | $2.76 per GB |
| Basic Logs ingestion | $0.615 per GB |
| Auxiliary Logs ingestion | $0.06 per GB |
| Extra Analytics Logs retention | $0.12 per GB-month |
| Standard web test | $0.00056 per execution |
| Billable metric alert time series | $0.10 per month |

Application Insights uses the connected Log Analytics workspace for data. Table
plan, retention, alert frequency, and notification channels affect the bill.

## Active-flow assumption

The estimate uses GPT 5.3 Codex and one representative investigation:

| Token type | Tokens | AAUs per million | AAUs |
|------------|--------|------------------|------|
| Input | 50,000 | 35 | 1.75 |
| Output | 10,000 | 280 | 2.80 |
| Cache read | 100,000 | 3.5 | 0.35 |
| Cache write | 0 | 0 | 0.00 |
| Total |  |  | 4.90 |

At $0.10 per AAU, the representative investigation costs $0.49. The same token
assumption with Claude Opus 4.6 is approximately 11 AAUs or $1.10. Real
investigations can be materially higher or lower.

## Cost scenarios

### Short enterprise workshop

Assumptions:

* One agent exists for 8 hours
* 15 investigations, one per application
* 7.5 aggregate active application-hours
* 50,000 requests, within the monthly free grant
* 2 GB Analytics Logs
* 15 conservatively billable alert time series
* Existing registry, or add about $5 for a Basic registry month

| Component | Estimate |
|-----------|----------|
| SRE Agent always-on | $3.20 |
| SRE Agent active flow | $7.35 |
| Container Apps environment | $0.80 |
| Container compute and requests | $0.00 after assumed free grant |
| Analytics Logs | $5.52 |
| Alerts | $1.50 |
| Estimated workshop total | $18.37 |
| Total with a dedicated Basic registry month | About $23.37 |

### One-month pilot

Assumptions:

* One agent exists for 730 hours
* 100 investigations
* 100 aggregate active application-hours
* 1 million requests
* 20 GB Analytics Logs
* 15 alert time series
* One Basic registry

| Component | Estimate |
|-----------|----------|
| SRE Agent always-on | $292.00 |
| SRE Agent active flow | $49.00 |
| Container Apps environment | $73.00 |
| Container compute and requests | $0.00 after assumed free grant |
| Analytics Logs | $55.20 |
| Alerts | $1.50 |
| Container registry allowance | $5.00 |
| Estimated monthly pilot total | $475.70 |

### Sustained enterprise evaluation

Assumptions:

* One agent exists for 730 hours
* 1,000 investigations
* 1,000 aggregate active application-hours
* 10 million requests
* 100 GB Analytics Logs
* 15 alert time series
* One Basic registry

| Component | Estimate |
|-----------|----------|
| SRE Agent always-on | $292.00 |
| SRE Agent active flow | $490.00 |
| Container Apps environment | $73.00 |
| Container compute after free grant | $21.60 |
| Requests after free grant | $3.20 |
| Analytics Logs | $276.00 |
| Alerts | $1.50 |
| Container registry allowance | $5.00 |
| Estimated monthly total | $1,162.30 |

## Cost formulas

```text
agent_always_on =
  agent_hours x 4 AAUs/hour x AAU_price

agent_active =
  investigations x AAUs_per_investigation x AAU_price

container_cpu =
  max(0, active_vCPU_seconds - monthly_vCPU_grant) x vCPU_rate

container_memory =
  max(0, active_GiB_seconds - monthly_memory_grant) x memory_rate

logs =
  analytics_GB x analytics_ingestion_rate
```

## Costs not included

* Taxes and enterprise agreement discounts
* Network egress, private endpoints, NAT Gateway, Firewall, or private DNS
* Defender for Cloud, Sentinel, ServiceNow, PagerDuty, or third-party connectors
* GitHub licensing and hosted runner overages
* Premium Azure Container Registry capabilities
* Log retention beyond included periods
* SMS, voice, or other paid action-group notifications
* Engineering labor, support plans, training, and compliance assessment
* Production resilience, backup, disaster recovery, or multi-region deployment

## Cost controls

1. Use one agent across the showcase resource scope.
2. Delete the agent after temporary workshops to stop always-on flow.
3. Set an active-flow AAU allocation limit.
4. Use Review mode to prevent repeated unintended actions.
5. Filter response plans and enable reinvestigation cooldown.
6. Scale sample applications to zero.
7. Sample telemetry and exclude unnecessary payload fields.
8. Set Log Analytics daily caps and retention appropriate to the evaluation.
9. Create resource-group budgets at 50, 75, 90, and 100 percent.
10. Tag every resource with owner, environment, cost center, and expiry date.

## Source references

* [Azure SRE Agent pricing and billing](https://learn.microsoft.com/en-us/azure/sre-agent/pricing-billing)
* [Azure SRE Agent pricing](https://azure.microsoft.com/en-us/pricing/details/sre-agent/)
* [Azure Container Apps pricing](https://azure.microsoft.com/en-us/pricing/details/container-apps/)
* [Azure Container Apps billing](https://learn.microsoft.com/en-us/azure/container-apps/billing)
* [Azure Monitor pricing](https://azure.microsoft.com/en-us/pricing/details/monitor/)
* [Azure Retail Prices API](https://prices.azure.com/)
* [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/)

