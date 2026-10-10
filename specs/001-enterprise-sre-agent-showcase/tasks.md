---
title: Enterprise SRE Showcase Delivery Tasks
description: Ordered implementation and acceptance checklist for the showcase
author: Enterprise SRE Platform Team
ms.date: 2026-10-10
ms.topic: reference
---

## Foundation

* [x] Define the constitution and product specification
* [x] Verify Azure SRE Agent capabilities against official sources
* [x] Define the common scenario data model and API contract
* [x] Create the Python 3.12 project and shared runtime

## Sample fleet

* [x] Add 15 complete application scenarios
* [x] Add business metadata, SLOs, dependencies, and fault defaults
* [x] Add consistent entry points and API behavior
* [x] Add authenticated, bounded, self-expiring fault injection
* [x] Add OpenTelemetry instrumentation

## Platform

* [x] Add the parameterized container image
* [x] Add Docker Compose for the local fleet
* [x] Add Bicep for Azure Container Apps and observability
* [x] Add Azure SRE Agent onboarding and governance guidance
* [x] Add GitHub Actions validation

## Documentation

* [x] Add one runbook per application
* [x] Add an enterprise demonstration guide
* [x] Add security, cost, cleanup, and productionization guidance
* [x] Add official source citations

## Verification

* [x] Test the application contract across all 15 scenarios
* [x] Test fault enablement and recovery
* [x] Run static analysis
* [x] Build the container image
* [ ] Run Azure Bicep what-if with customer subscription parameters
* [ ] Complete an end-to-end Azure SRE Agent alert investigation

