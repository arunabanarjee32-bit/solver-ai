# [SAI-B050] Reserve and reconcile durable per-account hint budgets atomically

<!-- solver-ai-backlog:SAI-B050 -->
Order: 65 / Priority: P1 / Phase: AI-1 controlled model hints
Area: AI token and request quotas / Suggested role: Backend persistence engineer

## Problem

Submission quotas exist for execution jobs, but no durable reservation mechanism currently limits model tokens or model request count.

## Prerequisites

- SAI-B044 (publish/complete prerequisite first)
- SAI-B049 (publish/complete prerequisite first)
- SAI-B013 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/features/hints/service.py
- services/api/solver_api/features/submissions/store.py
- services/api/tests/hints/test_hints.py
- docs/onboarding/DEVELOPMENT.md

## Scope

- Add a separate model-usage ledger with atomic request/token reservation and idempotent reconciliation.
- Reserve the configured upper bound before transport; conservatively handle unknown usage and interrupted runs.
- Document additive local schema migration and keep submission quota responsibility separate.

## Acceptance criteria

- Concurrent requests cannot reserve beyond an account limit.
- Restart/repeated settlement cannot erase consumption or charge one reservation twice.
- Exhausted budget returns a stable 429 without a provider request.

## Validation

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints services/api/tests/submissions -q

## Out of scope

- Payment collection
- Treating missing usage as free

## Risk and review

Ledger races and ambiguous completion can bypass caps or unfairly consume allowance.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
