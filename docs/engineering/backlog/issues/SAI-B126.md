# [SAI-B126] Withdraw worker readiness and reconcile its current lease on retirement

<!-- solver-ai-backlog:SAI-B126 -->
Order: 47 / Priority: P1 / Phase: 1-safe-pilot
Area: judge-lifecycle / Suggested role: Backend queue engineer and judge maintainer

## Problem

Cleanup failure now stops further claims and heartbeat renewal, but the API can continue advertising the last worker heartbeat for 60 seconds. Process/transport failure also leaves lease retirement to expiry. There is no explicit generation-bound withdrawal protocol connecting shutdown, cleanup outcome and the authoritative lease state.

## Prerequisites

- SAI-B013 (publish/complete prerequisite first)
- SAI-B121 (publish/complete prerequisite first)
- SAI-B122 (publish/complete prerequisite first)
- SAI-B123 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/features/submissions/store.py
- services/api/solver_api/main.py
- services/judge/solver_judge/control/worker.py
- services/judge/tests/control/test_worker.py
- services/api/tests/submissions/test_submissions.py
- docs/onboarding/DEVELOPMENT.md

## Scope

- Add one authenticated principal-and-instance-bound retirement operation using a closed reason vocabulary. Atomically withdraw only that worker instance from availability and prevent further lease grants.
- Have graceful shutdown or revoked runtime readiness attempt this operation with a short fixed deadline while still preserving controlled in-flight completion and orphan records. A transport failure retains the existing expiry fallback.
- Specify an idempotent authoritative disposition for its current lease: retain an already committed terminal result; otherwise record only a safe SYSTEM_ERROR when retirement is authorized, and never auto-requeue code whose cleanup is unconfirmed.

## Acceptance criteria

- Successful retirement removes the affected worker from capabilities immediately while other ready workers remain available.
- A late heartbeat/retirement from a previous process generation cannot revive or retire its registered replacement, and another worker principal cannot affect the lease.
- Shutdown versus completion races yield exactly one documented terminal state with no private diagnostics, no second execution and no hung shutdown; unavailable retirement transport falls back to the documented finite heartbeat/lease expiry behavior.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/submissions/test_submissions.py
- uv run --project services/api --frozen pytest services/judge/tests/control/test_worker.py

## Out of scope

- General learner-facing cancellation UX
- Automatically rerunning uncertain jobs
- Assuming API retirement proves a container was removed

## Risk and review

Retiring a shared identity or releasing an uncertain lease incorrectly can invalidate a healthy replacement or double-execute code; principal, process generation and lease transitions must be checked transactionally.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
