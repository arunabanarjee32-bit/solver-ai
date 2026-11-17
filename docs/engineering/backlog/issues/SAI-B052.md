# [SAI-B052] Deduplicate model hint retries with account-scoped idempotency

<!-- solver-ai-backlog:SAI-B052 -->
Order: 67 / Priority: P1 / Phase: AI-1 controlled model hints
Area: AI request reliability / Suggested role: Backend engineer

Implementation status: planned

## Problem

Browser retries or lost responses could trigger duplicate paid generation even when the learner intended one hint request.

## Prerequisites

- SAI-B050 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/api/solver_api/main.py
- services/api/solver_api/features/hints/service.py
- apps/web/features/hints/api.ts
- services/api/tests/hints/test_hints.py

## Scope

- Add optional account-scoped idempotency keyed by canonical request/context/backend version.
- Define replay, in-progress and same-key/different-payload outcomes.
- Reuse the same reservation/result for matching retries with bounded retention.

## Acceptance criteria

- Two matching concurrent retries result in at most one provider invocation.
- Different accounts cannot retrieve each other's cached hint.
- A reused key with changed problem/level/context receives a stable conflict.

## Validation

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q; npm run typecheck

## Out of scope

- Global shared personalized-answer cache
- Changing submission idempotency behavior

## Risk and review

An underspecified cache key can leak responses or replay stale prompt policy.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
