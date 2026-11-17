# [SAI-B089] Scope contest attempts and source visibility to authorized team members

<!-- solver-ai-backlog:SAI-B089 -->
Order: 104 / Priority: P2 / Phase: contest-experience
Area: teams / Suggested role: Backend engineer with privacy reviewer

Implementation status: planned

## Problem

Existing submissions are individual-owned; team sharing must be deliberate and event-bounded.

## Prerequisites

- SAI-B086 (confirm prerequisite state in the catalogue)
- SAI-B088 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/api/solver_api/features/submissions/store.py
- services/api/solver_api/main.py
- apps/web/features/submissions
- services/api/tests

## Scope

- Add proposed team-scoring attribution and explicit source/history visibility rules for event members.
- Preserve personal practice ownership and define access after roster correction or event completion.

## Acceptance criteria

- Eligible teammates can view only the event attempts allowed by policy.
- A member of another team and a former unauthorized member cannot fetch source through detail/list endpoints.
- The event scoreboard attributes retries and idempotent attempts to exactly one team.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/contests/test_team_attempts.py services/api/tests/submissions/test_submissions.py
- npx playwright test tests/e2e/contests/team-history.spec.ts --workers=2

## Out of scope

- Shared live code editing
- Global sharing of private submissions

## Risk and review

Expanding ownership from a user to a team can leak private code.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
