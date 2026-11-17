# [SAI-B010] Support bounded worker bearer rotation without an outage

<!-- solver-ai-backlog:SAI-B010 -->
Order: 11 / Priority: P1 / Phase: 1-safe-pilot
Area: worker-auth / Suggested role: backend engineer and deployment operator

## Problem

The controller trust domain relies on one configured bearer, with no tested handover protocol. Replacing it can abruptly stop heartbeat/lease/completion requests during active work.

## Prerequisites

- SAI-B009 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/main.py
- services/judge/solver_judge/control/worker.py
- services/api/tests/submissions/test_submissions.py
- docs/onboarding/DEVELOPMENT.md

## Scope

- Design a narrow current/previous credential handover with an explicit short overlap deadline and constant-time comparisons.
- Document update order and rollback for API and existing workers; prohibit permanent previous-token acceptance.
- Cover active completion during rotation and expiry without extending arbitrary job authorization.

## Acceptance criteria

- During the bounded overlap both approved credentials work; after expiry the previous credential receives the existing unauthorized response.
- An active worker can complete only its valid lease and cannot cross worker/job ownership during rotation.
- Unknown credentials and expired overlap fail closed, and token material never enters logs or public capability responses.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/submissions/test_submissions.py
- uv run --project services/api --frozen pytest services/judge/tests/control/test_worker.py

## Out of scope

- Rotating real deployment credentials in this issue without operator authorization
- Building a PKI
- Unbounded multi-token allowlists

## Risk and review

A permissive grace window can preserve a compromised key; require operator-controlled expiry and revoke procedure.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
