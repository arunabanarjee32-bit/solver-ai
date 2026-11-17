# [SAI-B109] Measure bounded capacity and overload behavior using original fixtures

<!-- solver-ai-backlog:SAI-B109 -->
Order: 52 / Priority: P1 / Phase: operated-pilot
Area: operations-capacity / Suggested role: Performance engineer and operator

## Problem

Queue limits need an empirical operating envelope before opening a pilot.

## Prerequisites

- SAI-B105 (publish/complete prerequisite first)
- SAI-B107 (publish/complete prerequisite first)
- SAI-B124 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- scripts/verification
- services/api/tests/submissions
- services/judge/tests/control
- docs/onboarding/DEVELOPMENT.md

## Scope

- Add a proposed opt-in load rehearsal with explicit concurrency/job/time ceilings and only original harmless programs.
- Measure queue latency, rejection behavior, cancellations and recovery under the configured local/dedicated test environment.

## Acceptance criteria

- The run refuses to start without an explicit finite budget.
- Over-capacity requests receive the documented bounded response and the queue drains after load stops.
- A reproducible report records environment/revision and distinguishes measured limits from production guarantees.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/operations/test_load_budget.py
- uv run --project services/api --frozen pytest services/api/tests/submissions/test_submissions.py -k queue

## Out of scope

- Unbounded stress loops
- Paid load infrastructure or testing third-party endpoints

## Risk and review

A careless load test can exhaust the shared development machine.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
