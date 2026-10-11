---
title: Enterprise SRE Agent Business Specification
description: Business case, outcomes, stakeholders, operating model, and adoption requirements
author: Enterprise SRE Platform Team
ms.date: 2026-10-11
ms.topic: concept
keywords:
  - business specification
  - azure sre agent
  - enterprise adoption
estimated_reading_time: 25
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

| Business case | Application details | Expected outcome | How Azure SRE Agent helps |
|---------------|---------------------|------------------|---------------------------|
| Retail Checkout | Processes synthetic purchases and depends on payment authorization. Its 99.95 percent availability and 450 ms latency objectives protect the point where customer intent becomes revenue. | Identify payment dependency loss without confusing it with process failure. Recover checkout, complete three synthetic purchases below 450 ms, and avoid unauthorized payment-provider changes. | Correlates HTTP 503 responses, request telemetry, revision state, business impact, source, and the checkout runbook. It presents an evidence-backed cause, asks for approval, and verifies the complete checkout journey after recovery. |
| Inventory Service | Reserves stock for checkout and fulfillment through the simulated `inventory-database` dependency. Incorrect or unavailable reservations can reject valid orders or allow overselling. | Distinguish a healthy application from database dependency failure. Restore a synthetic reservation below 500 ms and confirm checkout and fulfillment no longer report correlated failures. | Connects dependency-unavailable logs, failed business metrics, health probes, and adjacent-service impact. It recommends a reversible response without changing quantities or accessing customer orders. |
| Order Fulfillment | Dispatches paid orders to warehouses through the `fulfillment-queue` context. Application errors delay already-paid orders and threaten warehouse commitments. | Identify whether dispatch errors originate in application code, a revision, or the queue boundary. Restore dispatch below 800 ms without replaying production orders. | Correlates HTTP 500 errors with revision and deployment evidence, checks queue context, and proposes fault clearing or rollback only when supported by evidence. It verifies repeated synthetic dispatches after approval. |

### Financial services

Payments API, Banking Ledger, and Claims Processing represent latency-sensitive,
high-availability, and regulated workflows. These scenarios emphasize cautious
permissions, audit evidence, and data boundaries.

| Business case | Application details | Expected outcome | How Azure SRE Agent helps |
|---------------|---------------------|------------------|---------------------------|
| Payments API | Authorizes synthetic payments against a latency-sensitive card-processor context. The service targets 99.99 percent availability and authorization below 300 ms. | Detect a latency SLO breach even when requests return HTTP 200. Restore three synthetic authorizations below 300 ms with no error regression or payment-data exposure. | Compares request duration, fault state, revision history, probes, and platform utilization. It excludes unsupported processor claims, protects cardholder boundaries, proposes the bounded recovery, and produces an auditable verification report. |
| Banking Ledger | Posts synthetic ledger entries with strict readiness and audit expectations. An unhealthy revision can interrupt balance updates and regulated transaction processing. | Separate liveness from readiness, identify the affected revision, and restore a synthetic ledger operation below 250 ms without accessing ledger records. | Uses probe history, replica and revision events, deployment context, and business telemetry to recommend fault clearing or approved traffic removal. It never requests balance, transaction, credential, or database-write access. |
| Claims Processing | Accepts synthetic insurance claims and depends on a document service. Dependency loss stops claim intake and increases policyholder resolution time. | Diagnose document-service unavailability, restore a synthetic claim below 1,000 ms, and prove that no documents or personal data entered the investigation. | Correlates HTTP 503 responses, dependency logs, healthy probes, and the claims runbook. It preserves regulated-data boundaries and avoids unsafe replay or document retrieval. |

### Customer experience

Patient Scheduling, Airline Reservation, and Media Streaming represent direct
customer journeys where latency or errors quickly affect demand, trust, and
support volume.

| Business case | Application details | Expected outcome | How Azure SRE Agent helps |
|---------------|---------------------|------------------|---------------------------|
| Patient Scheduling | Books synthetic appointments against provider-calendar availability. Slow booking reduces access to care and shifts demand to the contact center. | Detect sustained latency before full outage, restore three bookings below 600 ms, and keep all patient and clinical data outside telemetry. | Correlates request percentiles, calendar context, revision state, and resource utilization. It explains patient-access impact, proposes a governed recovery, and validates bookings without retrieving protected health information. |
| Airline Reservation | Creates synthetic seat reservations against seat-inventory context. Errors prevent purchase completion and can create inconsistent capacity views. | Isolate application or revision failure, restore three reservations below 700 ms, and avoid booking replay or inventory mutation. | Connects HTTP 500 errors with operation traces, active revision, deployment history, and inventory context. It proposes only reversible recovery and explicitly excludes passenger data, fare changes, and replay. |
| Media Streaming | Starts synthetic playback sessions through content-delivery context. Startup delay drives viewer abandonment even when the request eventually succeeds. | Detect p95 startup latency above 350 ms, restore three sessions below the objective, and avoid increasing playback errors. | Compares request duration, revision behavior, compute saturation, and CDN context. It explains experience impact and confirms sustained latency recovery without accessing viewing history or content keys. |

### Industrial and data

Logistics Tracking, IoT Ingestion, and Data Pipeline represent event streams,
telemetry ingestion, and data freshness. These scenarios test dependency
correlation without operating real queues or warehouses.

| Business case | Application details | Expected outcome | How Azure SRE Agent helps |
|---------------|---------------------|------------------|---------------------------|
| Logistics Tracking | Records synthetic shipment locations through tracking-event-stream context. Failed updates create stale visibility and hide delivery exceptions. | Identify stream dependency loss, restore three location updates below 900 ms, and confirm freshness resumes without replaying external events. | Correlates HTTP 503 responses, stream context, revision health, and freshness impact. It recommends bounded recovery while excluding real shipment locations, stream purge, and replay. |
| IoT Ingestion | Accepts synthetic device telemetry and represents the entry point for manufacturing and predictive-maintenance signals. Ingestion errors create data gaps. | Identify application or revision error, restore three telemetry operations below 400 ms, and keep production device data outside the exercise. | Correlates ingestion errors with revision and event-hub context, explains maintenance impact, and proposes safe recovery without changing partitions or accessing factory payloads. |
| Data Pipeline | Starts synthetic analytical jobs against warehouse context. Dependency failure makes reports and machine-learning features stale. | Diagnose warehouse unavailability, restore a synthetic job start below 1,500 ms, and avoid modifying or retrying real jobs. | Combines HTTP 503 evidence, warehouse context, health probes, revision events, and freshness impact. It proposes a reversible action and verifies recovery without querying warehouse data. |

### Digital platforms

Identity Access, Collaboration API, and AI Inference Gateway represent shared
services with broad blast radius. These scenarios emphasize platform dependency,
provider availability, and access continuity.

| Business case | Application details | Expected outcome | How Azure SRE Agent helps |
|---------------|---------------------|------------------|---------------------------|
| Identity Access | Evaluates synthetic access requests through identity-provider context. Readiness loss can block every dependent protected application. | Distinguish readiness failure from process failure, restore an access evaluation below 200 ms, and preserve identity and token confidentiality. | Uses liveness, readiness, revision, replica, and deployment evidence to propose fault clearing or approved traffic removal. It never requests tokens, identities, group membership, or directory roles. |
| Collaboration API | Publishes synthetic messages through message-broker context. Latency delays time-sensitive collaboration and notifications while requests may still succeed. | Detect publish latency above 300 ms, restore three messages below the objective, and avoid message-content or queue access. | Correlates request duration, broker context, revision state, and platform capacity. It proposes governed recovery and validates performance without reading messages or purging queues. |
| AI Inference Gateway | Routes synthetic inference requests to model-endpoint context while enforcing provider, policy, and cost boundaries. Endpoint loss stalls AI-assisted workflows. | Identify endpoint dependency failure, restore three inference operations below 1,200 ms, and preserve prompt, output, safety, and credential boundaries. | Correlates HTTP 503 responses, gateway health, revision evidence, and model-endpoint context. It recommends bounded recovery without switching providers, deploying models, or accessing prompts and outputs. |

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
