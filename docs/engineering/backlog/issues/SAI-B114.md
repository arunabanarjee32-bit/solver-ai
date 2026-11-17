# [SAI-B114] Add editable practice plans and deterministic review reminders

<!-- solver-ai-backlog:SAI-B114 -->
Order: 76 / Priority: P2 / Phase: learning-coaching
Area: learning-plans / Suggested role: Full-stack engineer and learning designer

## Problem

Learners need a plan they can control without an opaque personalization model.

## Prerequisites

- SAI-B113 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- apps/web/app
- apps/web/features/practice
- services/api/solver_api/main.py
- services/api/tests

## Scope

- Add a proposed user-owned plan with selected topics/problems, due dates and in-app review prompts.
- Support snooze, reschedule and disabling prompts; use a documented deterministic review rule.

## Acceptance criteria

- Only the owner can read or modify a plan.
- A completed/repeated problem updates the expected next review date under fixed-clock fixtures.
- Disabled reminders stop appearing and do not trigger email or external notifications.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/learning/test_practice_plans.py
- npx playwright test tests/e2e/learning/plans.spec.ts --workers=2

## Out of scope

- Model-based adaptation
- Unrequested email/push notifications

## Risk and review

Incorrect scheduling or intrusive reminders can undermine user control.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
