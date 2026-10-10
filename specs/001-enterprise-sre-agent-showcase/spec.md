---
title: Enterprise Azure SRE Agent Showcase Specification
description: Functional and nonfunctional requirements for 15 observable incident scenarios
author: Enterprise SRE Platform Team
ms.date: 2026-10-10
ms.topic: concept
keywords:
  - specification
  - azure sre agent
  - incident response
estimated_reading_time: 18
---

## Executive outcome

Enterprise stakeholders can observe Azure SRE Agent receive an alert, combine
telemetry with repository and runbook context, form a probable root cause,
recommend a bounded mitigation, request approval, and verify recovery. The same
platform demonstrates this flow across 15 recognizable business domains.

## Problem statement

Generic reliability demonstrations rarely answer enterprise adoption questions.
They often omit identity boundaries, approval controls, source correlation,
repeatability, business impact, measurable recovery, and deployment automation.
This showcase closes those gaps while remaining small enough to deploy for a
workshop.

## Personas

| Persona | Primary need |
|---------|--------------|
| Executive sponsor | Understand operational and business value |
| SRE or on-call engineer | Evaluate investigation quality and time saved |
| Platform engineer | Assess deployment, telemetry, and fleet consistency |
| Security architect | Verify identity, permission, policy, and audit controls |
| Application owner | Connect technical symptoms to service impact and runbooks |
| Workshop facilitator | Trigger, explain, recover, and reset scenarios repeatedly |

## Scope

### Included

* 15 independently runnable FastAPI applications
* A shared operational API and OpenTelemetry runtime
* Bounded error, latency, dependency, and readiness faults
* Local and Azure Container Apps execution
* Application Insights and Log Analytics integration
* Azure SRE Agent onboarding, incident response, governance, and demo guidance
* Source-controlled runbooks and scenario metadata
* Automated contract, lint, and build validation

### Excluded

* Production data stores or external payment, clinical, or identity systems
* Real customer, employee, patient, or regulated data
* Autonomous destructive remediation
* Performance or scale benchmarking
* Multi-region production continuity
* A guarantee of Azure SRE Agent service availability or feature parity by region

## User stories and acceptance scenarios

### Story 1: Deploy a repeatable showcase

As a platform engineer, I can deploy the fleet from source control so every
workshop starts from a known configuration.

Acceptance scenarios:

1. Given valid Azure parameters, when the infrastructure deployment runs, then
   one shared observability plane and 15 container applications are declared.
2. Given a local workstation, when Docker Compose starts, then each application
   responds on its assigned port.
3. Given any application slug, when its container starts, then metadata and
   health endpoints represent that scenario.

### Story 2: Investigate an incident with correlated context

As an on-call engineer, I can see Azure SRE Agent correlate alerts, telemetry,
source code, scenario metadata, and a runbook.

Acceptance scenarios:

1. Given a connected repository and telemetry source, when a fault causes an
   alert, then the investigation can identify the application and active symptom.
2. Given a dependency fault, when the agent inspects logs and code, then the
   investigation distinguishes dependency failure from application readiness.
3. Given the scenario runbook, when mitigation is proposed, then the operator
   receives recovery and verification steps.

### Story 3: Demonstrate governed remediation

As a security architect, I can verify that diagnostic and remediation access is
bounded and reviewable.

Acceptance scenarios:

1. Given a Reader-level agent, when a write action is needed, then the action
   requires authorization rather than silently expanding privileges.
2. Given a response plan in Review mode, when the agent proposes a mitigation,
   then an authorized operator must approve it.
3. Given a global tool policy, when a prohibited destructive command is
   requested, then policy blocks the command and records the outcome.

### Story 4: Explain enterprise value

As an executive sponsor, I can connect a technical signal to customer impact and
measured recovery.

Acceptance scenarios:

1. Given a selected scenario, when the facilitator opens metadata, then the
   audience sees the SLO and business impact.
2. Given a completed investigation, when the summary is presented, then it
   includes symptom, probable cause, proposed action, approval state, and result.
3. Given a recovery action, when normal traffic resumes, then readiness and
   business operations return to success.

### Story 5: Reset safely

As a facilitator, I can stop a fault and reuse the environment.

Acceptance scenarios:

1. Given a valid demonstration key, when the clear endpoint is called, then the
   active fault changes to `none`.
2. Given no manual clear action, when 15 minutes elapse, then the fault expires.
3. Given fault injection is not enabled, when activation is attempted, then the
   control endpoint is unavailable.

## Functional requirements

| ID | Requirement |
|----|-------------|
| FR-001 | The repository must define exactly 15 application scenarios. |
| FR-002 | Every application must expose `/`, `/health/live`, `/health/ready`, `/work`, and `/faults`. |
| FR-003 | Every application must declare a domain, operation, dependency, SLO, business impact, default fault, and runbook. |
| FR-004 | The runtime must emit distributed traces and business-operation metrics through OpenTelemetry. |
| FR-005 | OTLP export must activate only when an exporter endpoint is configured. |
| FR-006 | Fault activation must require an explicit enable flag and API key. |
| FR-007 | Fault duration must be between 1 and 900 seconds. |
| FR-008 | The runtime must support error, latency, dependency, and not-ready faults. |
| FR-009 | Clearing a fault must immediately restore normal application behavior. |
| FR-010 | One container definition must run any scenario through `APP_SLUG`. |
| FR-011 | Docker Compose must expose all 15 applications without port collisions. |
| FR-012 | Azure infrastructure must use managed identities and secret references. |
| FR-013 | Azure deployment must provide a shared Log Analytics and Application Insights context. |
| FR-014 | Azure SRE Agent onboarding must connect this repository and application telemetry. |
| FR-015 | The initial incident response plan must use Review mode. |
| FR-016 | Runbooks must provide detection, investigation, mitigation, verification, and rollback steps. |
| FR-017 | Contract tests must execute against every scenario. |
| FR-018 | CI must run static analysis and tests for every change. |
| FR-019 | The demonstration guide must include security, cost, data, and cleanup controls. |
| FR-020 | Official product claims must cite Microsoft Learn or the official Microsoft repository. |

## Nonfunctional requirements

### Reliability

* Health endpoints must respond without relying on synthetic business dependencies.
* Liveness must remain successful during readiness and dependency scenarios.
* Fault state must be in-memory and self-expiring so restart restores safety.

### Security

* No credential may be committed to source control.
* The default deployment must not expose fault activation without a configured key.
* Azure access must begin at resource-group scope unless broader visibility has a
  documented need.
* Demonstrations must use Review mode before Autonomous mode.
* Global policy must deny destructive resource-deletion operations.

### Operability

* Application identity must be present in resource attributes, logs, and responses.
* Every scenario must have one deterministic trigger and one deterministic reset.
* A facilitator must be able to run a scenario in under 10 minutes after setup.

### Maintainability

* Application-specific code must remain a thin configuration wrapper.
* Changes to the shared contract must be tested against all scenarios.
* Scenario metadata must be machine-readable JSON.

### Cost

* Samples must use scale-to-zero capable compute.
* The guide must include teardown instructions and budget recommendations.
* No workload may generate traffic continuously by default.

## Success measures

| Measure | Target |
|---------|--------|
| Fleet contract coverage | 15 of 15 applications |
| Fault reset success | 100 percent in automated tests |
| Time from alert to investigation start | Under 2 minutes in a prepared workshop |
| Time from approved mitigation to verified recovery | Under 5 minutes |
| Unapproved write actions | Zero |
| Scenarios with business impact and SLO | 15 of 15 |
| Workshop reset without redeployment | 15 of 15 |

## Assumptions

* Azure SRE Agent is available in the selected subscription and region.
* The operator has permissions required to create the agent and assign access.
* GitHub source connectivity and Azure telemetry connectivity are approved.
* The demonstration uses synthetic data and a dedicated non-production resource group.

## Risks

| Risk | Mitigation |
|------|------------|
| Product behavior changes after publication | Pin documentation review dates and validate before each workshop |
| Excess agent privileges | Begin with Reader, scope RBAC, and use Review mode |
| Unintended fault exposure | Require enablement, key authentication, and short expiry |
| Alert noise | Route only labeled demo alerts and configure cooldown |
| Workshop cost drift | Scale to zero, set budgets, and delete the resource group |
| Audience mistakes samples for production patterns | Label limitations in README, spec, and demo guide |

