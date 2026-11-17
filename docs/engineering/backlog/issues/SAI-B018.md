# [SAI-B018] Implement deliberate account deletion across auth and owned submission state

<!-- solver-ai-backlog:SAI-B018 -->
Order: 19 / Priority: P1 / Phase: 1-safe-pilot
Area: privacy / Suggested role: backend/identity engineer and privacy reviewer

Implementation status: planned

## Problem

There is no end-to-end account deletion lifecycle. Removing only an auth row would strand private source/history, while deleting active work without coordination could break worker leases.

## Prerequisites

- SAI-B003 (confirm prerequisite state in the catalogue)
- SAI-B016 (confirm prerequisite state in the catalogue)
- SAI-B013 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- apps/web/features/accounts/server.ts
- apps/web/features/accounts/account-form.tsx
- services/api/solver_api/features/submissions/store.py
- services/api/solver_api/main.py
- services/api/tests/submissions/test_submissions.py
- apps/web/tests/auth.test.mjs

## Scope

- Implement an explicitly confirmed, recently authenticated account deletion flow using supported identity hooks and owner-scoped API cleanup.
- Apply the approved in-flight-job, retention and backup policy; refuse or defer unsafe active deletion rather than orphaning work.
- Make retries idempotent and explain what is removed immediately versus retained temporarily by policy.

## Acceptance criteria

- The requester cannot target a different account; forged identity, stale reauthentication and CSRF attempts fail.
- Deleting an eligible account removes or irreversibly anonymizes its approved live data classes without affecting another owner.
- Interrupted/retried deletion converges to one documented terminal state; active jobs follow the stated safe policy and credentials are invalidated as supported.

## Validation

- node --test apps/web/tests/auth.test.mjs
- uv run --project services/api --frozen pytest services/api/tests/submissions/test_submissions.py

## Out of scope

- Deleting live user data during development validation
- Promising instant erasure from historical backups without policy support
- Bypassing Better Auth mutation hooks

## Risk and review

Deletion is destructive and spans two stores; fixtures and failure recovery must prove ownership and partial-completion behavior.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
