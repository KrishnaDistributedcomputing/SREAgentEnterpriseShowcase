---
title: Identity Access Incident Runbook
description: Application context and governed investigation of identity readiness incidents
author: Enterprise SRE Platform Team
ms.date: 2026-10-11
ms.topic: troubleshooting
estimated_reading_time: 8
---

## Application overview

Identity Access evaluates synthetic access requests and represents a shared
security service with a broad enterprise blast radius. Readiness loss prevents
employees and customers from reaching protected systems.

| Attribute | Value |
|-----------|-------|
| Portfolio | Digital platforms |
| Business domain | Enterprise security |
| Business operation | `evaluate-access` |
| Critical dependency | `identity-provider` |
| Availability objective | 99.99 percent |
| Latency objective | Under 200 ms |
| Demonstrated fault | Revision not ready |
| Business impact | Users cannot access protected enterprise systems |

The not-ready fault fails readiness while process liveness remains successful.
The showcase evaluates synthetic identities and does not issue real tokens.

## Where Azure SRE Agent plays a role

Azure SRE Agent correlates probe history, revision health, deployment events, and
identity-provider context without accessing identity data.

1. Detect readiness failure while confirming liveness.
2. Identify the affected revision and traffic impact.
3. Correlate failure with rollout and platform events.
4. Explain broad access-continuity impact.
5. Recommend fault clearing or removal of an unhealthy revision for approval.
6. Verify readiness and a synthetic access evaluation.

The agent must not read tokens, secrets, identities, group membership, or access
policies. It must not grant roles or change authentication configuration.

## Detection and triage

Investigate failed readiness with successful liveness. Treat loss across multiple
replicas as high priority because the service has a broad dependent population.

Collect probe history, revision, replica events, deployment time, and failed
synthetic evaluation evidence.

## Investigation procedure

1. Confirm service identity and the 200 ms objective.
2. Compare readiness and liveness histories.
3. Identify unhealthy and healthy revisions.
4. Review deployment and Container Apps events at fault onset.
5. Confirm the agent's data and tool restrictions remain enforced.
6. Present probable cause, confidence, blast radius, and proposed action.

## Mitigation

Approve clearing the bounded not-ready fault. If readiness does not recover,
remove the correlated revision from traffic through an approved action.
Production failover must follow the organization's access-control emergency plan.

## Recovery verification

1. Confirm both health probes return HTTP 200.
2. Submit one synthetic access evaluation.
3. Confirm success below 200 ms.
4. Verify the recovered revision remains stable.
5. Revoke any temporary authorization and record all actions.

Escalate immediately if recovery would require broader identity privileges.
