---
title: Enterprise SRE Showcase Constitution
description: Governing principles for the Azure SRE Agent enterprise showcase
author: Enterprise SRE Platform Team
ms.date: 2026-10-10
ms.topic: concept
---

## Purpose

The showcase must prove how Azure SRE Agent investigates, explains, and safely
responds to operational failures across representative enterprise domains.

## Governing principles

### Observable by default

Every workload must emit enough health, request, dependency, error, trace, and
business-operation context for an investigation. A scenario that produces only
an HTTP error without correlated telemetry is incomplete.

### Safe failure is a product feature

Faults must be explicitly enabled, authenticated, bounded in duration, reversible,
and isolated to non-production resources. No scenario may mutate external systems,
delete data, or consume unbounded capacity.

### Governed autonomy before convenience

Demonstrations begin with Reader permissions and Review-mode incident response.
Write permissions must be resource-scoped, auditable, and introduced only after
the review workflow succeeds.

### One contract, many industries

All 15 workloads share the same operational API and deployment model. Industry
variation belongs in service metadata, SLOs, business impact, dependencies, and
runbooks, not in unnecessary framework divergence.

### Evidence over theater

Each demonstration must have measurable success criteria, repeatable fault
activation, expected telemetry, an investigation path, and a recovery check.
Claims about Azure SRE Agent must cite official Microsoft documentation.

### Enterprise controls are explicit

Identity, RBAC, network boundaries, secrets, audit trails, approval modes, cost,
data handling, and rollback must appear in the architecture and operator guide.

## Quality gates

The repository is releasable only when:

* Exactly 15 scenarios pass the common contract tests
* Static analysis and automated tests pass
* Fault injection is disabled without explicit configuration
* Every scenario names an SLO, business impact, dependency, and runbook
* Infrastructure can be reviewed with an Azure deployment what-if operation
* Documentation distinguishes showcase controls from production requirements

## Change governance

Changes that weaken authentication, fault expiry, least privilege, or auditability
require a written architecture decision and security review. Changes to the common
API require synchronized updates to tests, the OpenAPI contract, runbooks, and
operator documentation.

