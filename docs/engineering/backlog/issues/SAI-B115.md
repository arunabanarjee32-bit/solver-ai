# [SAI-B115] Implement opt-in coach cohorts with explicit sharing permissions

<!-- solver-ai-backlog:SAI-B115 -->
Order: 77 / Priority: P2 / Phase: learning-coaching
Area: coaching / Suggested role: Backend engineer and privacy reviewer

## Problem

A coach must not gain access to a learner’s private practice simply because both have accounts.

## Prerequisites

- SAI-B113 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/features/identity
- services/api/solver_api/main.py
- apps/web/app
- services/api/tests

## Scope

- Add a proposed cohort invitation/acceptance workflow with bounded coach membership and learner-controlled sharing scopes.
- Keep ordinary private history inaccessible unless a specific cohort permission covers it.

## Acceptance criteria

- Joining requires the invited learner’s explicit action and shows exactly which data becomes visible.
- A coach outside the cohort and a removed coach cannot query cohort-only data.
- Leaving/revoking sharing changes subsequent access according to a tested policy.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/coaching/test_cohorts.py
- npx playwright test tests/e2e/coaching/invitations.spec.ts --workers=2

## Out of scope

- Automatic contact imports
- Giving coaches general account-administrator access

## Risk and review

Broad sharing scopes could expose unrelated private attempts.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
