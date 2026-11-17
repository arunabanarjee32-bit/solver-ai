# [SAI-B023] Enforce cumulative owned-source storage budgets at submission admission

<!-- solver-ai-backlog:SAI-B023 -->
Order: 24 / Priority: P1 / Phase: 1-safe-pilot
Area: storage-abuse / Suggested role: backend storage engineer

## Problem

Per-source size and request/concurrency quotas do not bound cumulative stored source. A valid account can accumulate completed submissions until the shared disk is exhausted.

## Prerequisites

- SAI-B003 (publish/complete prerequisite first)
- SAI-B013 (publish/complete prerequisite first)
- SAI-B022 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/features/submissions/store.py
- services/api/tests/submissions/test_submissions.py
- services/api/solver_api/main.py

## Scope

- Track or compute bounded per-owner retained-source usage transactionally and apply configured byte/record ceilings when accepting new submissions.
- Keep idempotent replay of an existing request stable and exclude already purged bytes consistently.
- Return an actionable safe quota error without revealing another account usage.

## Acceptance criteria

- Concurrent writes near the limit cannot exceed the configured budget by racing.
- An idempotency-key replay returns the original record without double-charging usage; a conflicting replay retains its existing rejection.
- After eligible retention frees bytes, a new request can be accepted, and another owner budget is unaffected.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/submissions/test_submissions.py

## Out of scope

- Paid storage plans
- A global filesystem quota implementation
- Weakening existing queue limits

## Risk and review

Accounting races can bypass budgets or reject valid replay; enforce charging in the same transaction as creation.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
