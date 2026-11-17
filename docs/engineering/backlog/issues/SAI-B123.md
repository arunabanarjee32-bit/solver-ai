# [SAI-B123] Enforce an atomic active-lease allowance per worker principal

<!-- solver-ai-backlog:SAI-B123 -->
Order: 44 / Priority: P0 / Phase: 1-safe-pilot
Area: judge-admission / Suggested role: Backend queue engineer

## Problem

The current worker implementation runs serially, but the API lease transaction has no check for an existing RUNNING lease belonging to the worker. Repeated or concurrent authenticated lease requests can reserve many jobs, so the client convention is not an enforceable execution allowance.

## Prerequisites

- SAI-B122 (publish/complete prerequisite first)
- SAI-B013 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/features/submissions/store.py
- services/api/solver_api/main.py
- services/api/tests/submissions/test_submissions.py
- services/judge/solver_judge/control/worker.py
- services/judge/tests/control/test_worker.py

## Scope

- Inside the existing atomic lease transaction, enforce a configured active-lease allowance for the authenticated worker principal; begin with the current one-job-per-worker contract.
- Return a documented busy/no-new-lease outcome without claiming another job, and release allowance only after the authoritative completion or expiry transition.
- Keep idempotent retry and cross-worker ownership semantics explicit; integrate with registered identities from B122 so inventing another worker_id cannot evade the allowance.

## Acceptance criteria

- Two concurrent lease calls for the same principal cannot create more RUNNING jobs than its configured allowance.
- A busy worker does not consume another queued job; a second independently authorized worker can lease its own job.
- Completion and lease expiry each release exactly the intended allowance, while stale completion and forged identity do not release or consume another worker slot.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/submissions/test_submissions.py
- uv run --project services/api --frozen pytest services/judge/tests/control/test_worker.py

## Out of scope

- Distributed host-capacity scheduling
- Changing learner submission quotas or provider budgets
- Assuming a lease count measures actual CPU or aggregate memory

## Risk and review

A nontransactional count-and-lease check can race; a stranded lease must expire without allowing cross-worker or double completion.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
