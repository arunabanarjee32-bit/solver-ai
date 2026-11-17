# [SAI-B112] Run a bounded incident exercise for worker outage and recovery

<!-- solver-ai-backlog:SAI-B112 -->
Order: 55 / Priority: P2 / Phase: operated-pilot
Area: operations-recovery / Suggested role: Site reliability engineer and service owner

## Problem

Operators need evidence that readiness, job reconciliation and user messaging work during failures.

## Prerequisites

- SAI-B107 (publish/complete prerequisite first)
- SAI-B108 (publish/complete prerequisite first)
- SAI-B110 (publish/complete prerequisite first)
- SAI-B111 (publish/complete prerequisite first)
- SAI-B126 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- docs/security/JUDGE_SECURITY.md
- docs/onboarding/DEVELOPMENT.md
- scripts/verification
- services/judge/tests/control
- services/api/tests

## Scope

- Add a proposed isolated exercise covering lost worker heartbeat, interrupted control service and restored service.
- Record detection, containment, queued-job reconciliation and owner communication steps without sending external messages automatically.

## Acceptance criteria

- The exercise demonstrates unavailable execution while probes fail and safe recovery after reconciliation.
- No attempt is attributed to another account or completed twice.
- A post-exercise report names observed times, unresolved gaps and a responsible owner; live databases remain untouched.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/operations/test_incident_rehearsal.py
- uv run --project services/api --frozen pytest services/judge/tests/control/test_worker.py

## Out of scope

- Simulated credential theft against real accounts
- Automatic incident messaging or account-admin changes

## Risk and review

An exercise that touches live state can create the incident it is meant to test.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
