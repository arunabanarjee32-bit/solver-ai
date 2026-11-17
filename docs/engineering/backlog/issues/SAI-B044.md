# [SAI-B044] Define an internal generation result and usage contract

<!-- solver-ai-backlog:SAI-B044 -->
Order: 59 / Priority: P1 / Phase: AI-1 controlled model hints
Area: Provider-neutral contracts / Suggested role: Backend and AI interface engineer

## Problem

HintBackend returns bounded HintContent today; real inference also needs trusted model identity, usage, finish reason and request metadata without exposing provider payloads.

## Prerequisites

- SAI-B042 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/features/hints/service.py
- services/api/tests/hints/test_hints.py
- docs/product/AI_SOLVER.md

## Scope

- Introduce an internal provider-neutral result separating display content from operational metadata.
- Represent missing usage, partial completion and unknown billing explicitly.
- Adapt authored generation to the internal interface while preserving its truthful source/provider fields.

## Acceptance criteria

- Existing HTTP v1 authored responses remain compatible.
- Operational metadata cannot serialize into the learner response accidentally.
- Invalid provenance and contradictory usage/finish data are rejected by named contract rules.

## Validation

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q

## Out of scope

- Implementing multiple providers
- Changing account JWT claims

## Risk and review

Treating absent provider usage as zero would undercount spend.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
