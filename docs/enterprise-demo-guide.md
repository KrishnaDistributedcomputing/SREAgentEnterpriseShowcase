---
title: Enterprise Azure SRE Agent Demonstration Guide
description: Facilitator workflow for presenting governed incident investigation and recovery
author: Enterprise SRE Platform Team
ms.date: 2026-10-10
ms.topic: how-to
estimated_reading_time: 16
---

## Demonstration objective

Show that Azure SRE Agent can turn a business-impacting alert into a contextual,
governed, and verifiable response. The strongest narrative is not that an agent
can run commands. It is that the agent can assemble evidence, respect boundaries,
ask for approval, and confirm recovery.

## Audience map

| Audience | Emphasize |
|----------|-----------|
| Executives | Reduced incident impact, preserved human accountability, repeatability |
| SRE leaders | Investigation quality, MTTA, MTTR, toil reduction, reusable context |
| Security | Managed identity, least privilege, Review mode, policies, hooks, audit |
| Platform engineering | Shared contracts, IaC, telemetry, scale to zero, CI |
| Application teams | Source correlation, SLO, dependency evidence, runbooks |

## Preflight checklist

Complete these checks before the audience joins:

* Use a dedicated non-production Azure resource group.
* Confirm the 15 applications are healthy and traffic is idle.
* Confirm no sensitive or production data is connected.
* Confirm GitHub and Application Insights connectors are healthy.
* Confirm Azure Monitor is connected as the incident platform.
* Confirm the response plan filters only the intended showcase alerts.
* Confirm the response plan uses Review mode.
* Confirm global tool policy denies delete commands.
* Confirm the demonstration key is stored as a secret.
* Confirm a budget and teardown owner exist.

## Recommended 20-minute storyline

### Minute 0 through 3: Establish business context

Choose Retail Checkout for a broad audience or a domain-specific sample for a
customer. Open the landing page, select the application, then inspect its metadata
endpoint to identify the SLO, dependency, runbook, and stated business impact.

### Minute 3 through 6: Establish governance

Show the agent managed identity, resource-group scope, Reader posture, response
plan in Review mode, and deletion deny policy. Explain that autonomy is a bounded
configuration choice rather than an all-or-nothing feature.

### Minute 6 through 9: Trigger a synthetic incident

Activate the scenario's default fault for two to five minutes. Generate a small
number of business requests. Do not use a load generator unless alert design
requires it and the audience has approved the cost.

### Minute 9 through 14: Observe investigation

Follow the agent investigation and call out:

1. Alert and service identity
2. Request or readiness symptom
3. Log, metric, and trace evidence
4. Dependency or code context
5. Business impact and SLO
6. Proposed mitigation and confidence

### Minute 14 through 17: Approve and recover

Review the proposed action. Approve only a reversible, pre-authorized action.
Clear the fault or restart the affected revision, then generate a successful
business operation.

### Minute 17 through 20: Verify and summarize

Confirm readiness, successful business traffic, and alert recovery. Summarize
time to investigation, time to recovery, approvals, evidence, and follow-up.

## Enterprise security position

Azure SRE Agent uses a user-assigned managed identity for Azure resources. Scope
the showcase identity to its dedicated resource group. Use Reader for diagnostic
access and introduce write roles only for named, tested remediation paths.

Use tool policy to:

* Allow read-only monitoring and resource inspection
* Ask before restart, scale, deployment, or configuration changes
* Deny resource deletion, role assignment changes, and secret retrieval

Use hooks to enforce organization-specific evidence or auditing. Review hook
precedence carefully because an administrator-defined hook can affect policy
evaluation.

## Data and privacy

Use synthetic records only. Repository content, logs, traces, incidents, and
conversation history can become investigation context. Apply enterprise retention,
classification, residency, and access requirements to every connected source.

## Cost controls

* Use scale-to-zero Container Apps and no scheduled traffic by default.
* Set 30-day Log Analytics retention unless policy requires another period.
* Apply a resource-group budget and alert.
* Limit fault and traffic windows.
* Delete the resource group after temporary events.

## Failure handling

If Azure SRE Agent cannot complete an investigation:

1. Stop the demonstration fault.
2. Verify the application recovered directly.
3. Inspect connector health and response-plan filters.
4. Preserve the incident and agent transcript for follow-up.
5. Do not broaden permissions during a live customer session.

## Completion evidence

Record the scenario, alert time, investigation start, probable cause, proposed
action, approver, execution time, recovery time, and open follow-up. Compare
these values across repeated runs to measure improvement rather than relying on
anecdotal impressions.
