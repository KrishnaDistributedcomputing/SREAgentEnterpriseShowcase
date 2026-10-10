---
title: Enterprise SRE Agent Business Specification
description: Business case, outcomes, stakeholders, operating model, and adoption requirements
author: Enterprise SRE Platform Team
ms.date: 2026-10-10
ms.topic: concept
keywords:
  - business specification
  - azure sre agent
  - enterprise adoption
estimated_reading_time: 18
---

## Business vision

Create a credible enterprise evaluation environment where leaders, reliability
teams, platform engineers, security architects, and application owners can
assess Azure SRE Agent against the same observable incidents and governance
controls.

The showcase supports a decision to adopt, extend, defer, or reject the product
based on measured evidence. It does not assume that automation is valuable in
every incident or that autonomous remediation is the desired end state.

## Business problem

Enterprise incident response is slowed by fragmented evidence, inconsistent
runbooks, manual correlation, repeated diagnosis, and approval handoffs. Product
demonstrations often hide the controls that determine whether an AI operations
tool can be adopted safely.

This initiative addresses four decision gaps:

1. Can the agent identify a probable cause from telemetry and source context?
2. Can teams preserve human accountability and least privilege?
3. Can the same operating pattern serve materially different business domains?
4. Can benefits and costs be measured before production commitment?

## Target outcomes

| Outcome | Business value | Evidence |
|---------|----------------|----------|
| Faster investigation | Reduce customer-impact duration | Alert-to-investigation time |
| Consistent diagnosis | Reduce dependency on individual expertise | Correct fault and dependency identification |
| Governed action | Preserve accountability and compliance | Approval and audit records |
| Reusable knowledge | Improve onboarding and repeat incidents | Source-linked runbooks and investigation history |
| Portfolio consistency | Lower platform operating cost | One contract across 15 applications |
| Transparent economics | Support an informed investment decision | Central US cost model and usage metrics |

## Stakeholders

| Stakeholder | Accountability | Decision interest |
|-------------|----------------|-------------------|
| Executive sponsor | Funds evaluation and owns adoption outcome | Value, risk, and total cost |
| SRE leadership | Defines reliability outcomes and operating model | MTTA, MTTR, toil, escalation |
| Platform engineering | Owns shared deployment and telemetry | Standardization and maintainability |
| Security and compliance | Approves identity, data, and automation controls | Least privilege, audit, policy |
| Application owners | Validate diagnosis and runbooks | Correctness and service impact |
| FinOps | Validates assumptions and monitors spend | Unit economics and budgets |
| Workshop facilitator | Runs safe and repeatable scenarios | Usability and recovery |

## Business capabilities

### Incident understanding

The evaluation must demonstrate signal correlation across alerts, telemetry,
Azure resources, source, and runbooks. A response based only on a single error
message does not satisfy this capability.

### Decision support

The agent must produce an evidence-backed probable cause, business impact, and
proposed action. The operator remains accountable for approval in the evaluation.

### Governed remediation

The platform must separate read access from write access, preserve action logs,
and block prohibited operations. Autonomous mode is a later adoption decision.

### Knowledge reuse

Runbooks, application context, and prior investigation outcomes must reduce
repeated discovery work for future incidents and new on-call engineers.

### Portfolio operations

The same runtime and governance model must cover commerce, financial services,
customer experience, industrial data, and digital platform workloads.

## Business requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| BR-001 | Demonstrate 15 applications across five enterprise portfolios | Must |
| BR-002 | Relate every technical incident to an explicit business impact | Must |
| BR-003 | Define an availability and latency objective for every application | Must |
| BR-004 | Require human approval for showcase remediation | Must |
| BR-005 | Prevent resource deletion and secret retrieval by agent policy | Must |
| BR-006 | Use synthetic data and a non-production Azure boundary | Must |
| BR-007 | Capture investigation and recovery timing | Must |
| BR-008 | Provide a Central US USD cost model with variable assumptions | Must |
| BR-009 | Support repeatable local and Azure deployment | Must |
| BR-010 | Produce an adoption recommendation after the pilot | Should |
| BR-011 | Compare model choices by quality and AAU consumption | Should |
| BR-012 | Export evidence for architecture and risk review | Should |

## Portfolio scenarios

### Commerce and retail

Retail Checkout, Inventory Service, and Order Fulfillment represent the revenue
path from customer intent through stock reservation and warehouse dispatch.
These scenarios test cross-service dependency reasoning and customer conversion
impact.

### Financial services

Payments API, Banking Ledger, and Claims Processing represent latency-sensitive,
high-availability, and regulated workflows. These scenarios emphasize cautious
permissions, audit evidence, and data boundaries.

### Customer experience

Patient Scheduling, Airline Reservation, and Media Streaming represent direct
customer journeys where latency or errors quickly affect demand, trust, and
support volume.

### Industrial and data

Logistics Tracking, IoT Ingestion, and Data Pipeline represent event streams,
telemetry ingestion, and data freshness. These scenarios test dependency
correlation without operating real queues or warehouses.

### Digital platforms

Identity Access, Collaboration API, and AI Inference Gateway represent shared
services with broad blast radius. These scenarios emphasize platform dependency,
provider availability, and access continuity.

## Key performance indicators

| KPI | Definition | Pilot target |
|-----|------------|--------------|
| Mean time to acknowledge | Alert creation to investigation start | Under 2 minutes |
| Mean time to probable cause | Alert creation to evidence-backed cause | Under 5 minutes |
| Mean time to recovery | Alert creation to verified business success | Under 10 minutes |
| Diagnostic accuracy | Correct scenario fault and dependency | At least 90 percent |
| Approval compliance | Write actions with explicit approval | 100 percent |
| Unsafe action rate | Prohibited or out-of-scope actions executed | Zero |
| Recovery verification | Incidents with health and business validation | 100 percent |
| Scenario repeatability | Successful reset without redeployment | 100 percent |
| Active-flow efficiency | AAUs per completed investigation | Baseline, then improve |

## Operating model

### Evaluation stage

One platform team owns the agent, connectors, policies, and showcase resource
group. Application owners validate findings. Security approves policies. FinOps
reviews weekly consumption.

### Pilot stage

Selected application teams connect non-production telemetry. Response plans
remain in Review mode. Every proposed action maps to an approved runbook and
named owner.

### Production stage

Production use requires workload-specific risk review, data classification,
private networking, identity governance, change integration, rollback testing,
availability design, and an explicit autonomy decision.

## Adoption gates

| Gate | Pass condition |
|------|----------------|
| Product fit | Correct diagnosis in at least 90 percent of approved scenarios |
| Security | No critical findings and all write paths are scoped and audited |
| Operations | On-call engineers can understand, approve, and reverse actions |
| Reliability | Recovery checks are deterministic and false positives are manageable |
| Financial | Forecast fits approved budget and AAU limits are configured |
| Organizational | Owners, escalation, support, and training are assigned |

## Benefits hypothesis

The initiative expects value from shorter evidence-gathering time, fewer repeated
manual queries, more consistent incident records, faster onboarding, and safer
execution of known procedures. The pilot must measure these benefits against a
human-only baseline before projecting savings.

## Constraints

* Product availability and model options vary by subscription and region.
* Costs vary by agreement, telemetry volume, model, and investigation complexity.
* The samples do not represent production data, persistence, scale, or networking.
* A successful showcase does not authorize production autonomy.
* Regulated workloads require separate legal, compliance, and privacy review.

## Business risks

| Risk | Business consequence | Treatment |
|------|----------------------|-----------|
| Incorrect diagnosis | Delayed recovery or harmful action | Review mode, evidence gate, rollback |
| Excess privilege | Security or compliance incident | Managed identity, narrow RBAC, deny policy |
| Telemetry overspend | Unexpected cloud cost | Sampling, ingestion controls, budgets |
| Agent overuse | High active-flow AAUs | Allocation limit, prompt tuning, scheduled-task review |
| Skill erosion | Reduced human readiness | Exercises, manual fallback, post-incident review |
| Product dependency | Switching and continuity risk | Export runbooks, preserve standard telemetry |

## Deliverables

The business evaluation package consists of:

* Business and product specifications
* Detailed technical design and architecture
* 15 runnable sample applications in five portfolios
* User and facilitator guides
* Cost model and assumptions
* Security and governance baseline
* Automated tests, infrastructure templates, and CI
* Pilot scorecard and adoption gate definitions

