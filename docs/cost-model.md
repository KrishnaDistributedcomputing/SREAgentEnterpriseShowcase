---
title: Azure SRE Agent Showcase MVP Cost Model
description: Lean cost estimate and operating controls for an on-demand MVP evaluation
author: Enterprise SRE Platform Team
ms.date: 2026-10-11
ms.topic: reference
keywords:
  - azure cost
  - mvp
  - finops
  - azure agent units
estimated_reading_time: 12
---

## MVP cost objective

Validate Azure SRE Agent investigation quality, governance, and recovery with the
smallest practical Azure footprint. The MVP is an evaluation environment, not a
continuously available production service.

The recommended cost ceilings are:

| MVP period | Cost ceiling | Operating model |
|------------|--------------|-----------------|
| One-day validation | $15 | Eight scheduled cloud hours |
| Five-day sprint | $45 | Forty scheduled cloud hours |
| One-month MVP | $85 | Eighty scheduled cloud hours |

These ceilings include a $5 monthly allowance for a dedicated Basic container
registry. Reusing an existing registry lowers each estimate by about $5.

> [!IMPORTANT]
> Delete Azure SRE Agent and the disposable Container Apps environment outside
> scheduled sessions. Stopping traffic or scaling applications to zero does not
> stop the agent's always-on charge.

## MVP scope

The repository retains all 15 application definitions. The cloud MVP actively
investigates four representative scenarios that cover every fault class:

| Application | Fault class | Reliability lesson |
|-------------|-------------|--------------------|
| Retail Checkout | Dependency | Downstream outage with a healthy process |
| Order Fulfillment | Error | Business-operation failure |
| Payments API | Latency | SLO breach with successful status codes |
| Banking Ledger | Not ready | Revision and traffic readiness |

The remaining 11 applications stay at zero replicas and can be activated for a
customer-specific session. This preserves portfolio breadth without generating
continuous compute, telemetry, web-test, or investigation cost.

## Pricing basis

This estimate uses the public Central US retail rates captured on 2026-10-10.
It is not a quote. Enterprise agreements, taxes, grants, model selection, data
volume, network egress, and evaluation offers can change the result.

Validate rates in the Azure Pricing Calculator and actual spend in Azure Cost
Management before and during the MVP.

## Unit rates used

### Azure SRE Agent

| Meter | MVP assumption |
|-------|----------------|
| Azure Agent Unit | $0.10 per AAU |
| Always-on flow | 4 AAUs per provisioned agent-hour |
| Representative investigation | 4.9 AAUs, or $0.49 |

One continuously provisioned agent would cost approximately $292 per 730-hour
month before active investigations. The MVP avoids that cost by creating the
agent only for scheduled evaluation windows and deleting it afterward.

### Azure Container Apps

| Meter | Rate |
|-------|------|
| Active vCPU | $0.000024 per vCPU-second |
| Idle vCPU | $0.000003 per vCPU-second |
| Active or idle memory | $0.000003 per GiB-second |
| Requests | $0.40 per million |
| Environment management | $0.10 per hour |

The public pricing page lists monthly grants of 180,000 vCPU-seconds, 360,000
GiB-seconds, and 2 million requests. The MVP assumes request and active compute
remain within those grants.

All applications use zero minimum replicas outside live demonstrations. Keeping
all 15 applications warm for an eight-hour event is an optional $0.97 allowance
before free grants. Disable warm replicas immediately after the event.

### Azure Monitor

| Meter | Rate |
|-------|------|
| Analytics Logs ingestion | $2.76 per GB |
| Standard web test | $0.00056 per execution |
| Billable metric alert time series | $0.10 per month |

The MVP retains 30 days of telemetry, enables alerts and web tests only for the
four representative scenarios, and excludes request or business payloads.

## Recommended MVP estimates

### One-day validation

Assumptions:

* Azure SRE Agent and Container Apps environment exist for eight hours
* Four investigations, one for each fault class
* All 15 applications may remain warm during the eight-hour session
* 0.5 GB of Analytics Logs
* Four alert time series
* Four web tests every five minutes
* Requests and active compute remain within monthly grants

| Component | Calculation | Estimate |
|-----------|-------------|----------|
| SRE Agent always-on | 8 hours x 4 AAUs x $0.10 | $3.20 |
| SRE Agent active flow | 4 investigations x $0.49 | $1.96 |
| Container Apps environment | 8 hours x $0.10 | $0.80 |
| Optional warm replicas | Eight-hour allowance | $0.97 |
| Container compute and requests | Within assumed grants | $0.00 |
| Analytics Logs | 0.5 GB x $2.76 | $1.38 |
| Alerts | 4 series x $0.10 | $0.40 |
| Web tests | 384 executions x $0.00056 | $0.22 |
| Existing-registry total |  | **$8.93** |
| Dedicated Basic registry allowance | Monthly allowance | $5.00 |
| Recommended one-day budget |  | **$13.93** |

### Five-day MVP sprint

Assumptions:

* Five eight-hour evaluation windows
* Agent and disposable environment are deleted after each window
* 12 investigations across four representative applications
* 2 GB of Analytics Logs
* Four alerts and four five-minute web tests
* Warm replicas are enabled only during the 40 scheduled hours

| Component | Estimate |
|-----------|----------|
| SRE Agent always-on | $16.00 |
| SRE Agent active flow | $5.88 |
| Container Apps environment | $4.00 |
| Warm replica allowance | $4.86 |
| Container compute and requests | $0.00 after assumed grants |
| Analytics Logs | $5.52 |
| Alerts | $0.40 |
| Web tests | $1.08 |
| Dedicated Basic registry allowance | $5.00 |
| Recommended five-day budget | **$42.74** |

### One-month controlled MVP

This is a scheduled evaluation, not a 24-hour service. It uses 80 cloud hours
across the month, such as ten eight-hour workshop days.

Assumptions:

* Agent and disposable environment exist for 80 scheduled hours
* 20 investigations
* 5 GB of Analytics Logs
* Four alerts and four five-minute web tests during scheduled windows
* Warm replicas are enabled only during scheduled windows
* One Basic registry remains for the month

| Component | Estimate |
|-----------|----------|
| SRE Agent always-on | $32.00 |
| SRE Agent active flow | $9.80 |
| Container Apps environment | $8.00 |
| Warm replica allowance | $9.72 |
| Container compute and requests | $0.00 after assumed grants |
| Analytics Logs | $13.80 |
| Alerts | $0.40 |
| Web tests | $2.15 |
| Dedicated Basic registry allowance | $5.00 |
| Recommended monthly MVP budget | **$80.87** |

## What is not part of the MVP

The following choices move the solution beyond MVP scope:

* Continuously provisioned Azure SRE Agent
* A continuously retained Container Apps environment
* Fifteen always-warm applications
* Alerts and web tests for every application
* High-volume load generation
* More than 5 GB of monthly Analytics Logs
* Premium registry, private networking, Firewall, or NAT Gateway
* Microsoft Sentinel, Defender for Cloud, ServiceNow, PagerDuty, or other
  enterprise integrations
* Multi-region deployment, disaster recovery, backup, or production support

Leaving the agent and environment provisioned for 730 hours adds approximately
$365 per month before investigations, logs, registry, or warm replicas. That
configuration violates the MVP cost objective.

## MVP deployment lifecycle

1. Keep source, Bicep, runbooks, and scenario definitions in GitHub.
2. Reuse an existing registry when governance allows it.
3. Deploy the agent and showcase environment shortly before a scheduled session.
4. Keep `minimumReplicas=0` during preparation and idle periods.
5. Set `minimumReplicas=1` only when live navigation speed is required.
6. Enable alerts and web tests only for the four representative applications.
7. Run the approved investigation set with an AAU allocation limit.
8. Export the investigation evidence needed for the MVP decision.
9. Clear every fault and return replicas to zero.
10. Delete Azure SRE Agent and the disposable environment after the session.
11. Confirm deletion and actual cost in Azure Cost Management.

Recreating the environment can change application hostnames. Use deployment
outputs or automation to refresh links rather than retaining billable resources
only to preserve URLs.

## Cost controls

1. Set an MVP resource-group budget of $15 for one day, $45 for five days, or
   $85 for one month.
2. Configure alerts at 50, 75, 90, and 100 percent of the selected ceiling.
3. Assign an owner and expiry date to every resource.
4. Delete the agent outside scheduled sessions.
5. Use one agent for all four representative scenarios.
6. Cap active-flow AAUs and use Review mode.
7. Apply response-plan filters and a reinvestigation cooldown.
8. Keep applications at zero replicas except during live demonstrations.
9. Limit Analytics Logs to 0.5 GB per day and 5 GB per MVP month.
10. Exclude payloads, high-cardinality fields, health-check success traces, and
    unnecessary debug logs.
11. Review actual cost after every session before scheduling the next one.

## Cost formulas

```text
agent_always_on =
  scheduled_agent_hours x 4 AAUs/hour x AAU_price

agent_active =
  investigations x AAUs_per_investigation x AAU_price

environment =
  scheduled_environment_hours x environment_hourly_rate

logs =
  analytics_GB x analytics_ingestion_rate

web_tests =
  applications x executions_per_hour x scheduled_hours x execution_rate
```

## Source references

* [Azure SRE Agent pricing and billing](https://learn.microsoft.com/en-us/azure/sre-agent/pricing-billing)
* [Azure SRE Agent pricing](https://azure.microsoft.com/en-us/pricing/details/sre-agent/)
* [Azure Container Apps pricing](https://azure.microsoft.com/en-us/pricing/details/container-apps/)
* [Azure Container Apps billing](https://learn.microsoft.com/en-us/azure/container-apps/billing)
* [Azure Monitor pricing](https://azure.microsoft.com/en-us/pricing/details/monitor/)
* [Azure Retail Prices API](https://prices.azure.com/)
* [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/)
