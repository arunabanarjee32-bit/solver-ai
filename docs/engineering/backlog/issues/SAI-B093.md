# [SAI-B093] Add contest clarification and appeal records with controlled disclosure

<!-- solver-ai-backlog:SAI-B093 -->
Order: 108 / Priority: P2 / Phase: contest-corrections
Area: contest-admin / Suggested role: Full-stack engineer and contest moderator

Implementation status: planned

## Problem

Participants need a traceable correction channel that does not reveal another team’s private work.

## Prerequisites

- SAI-B091 (confirm prerequisite state in the catalogue)
- SAI-B092 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/api/solver_api/main.py
- apps/web/app
- apps/web/features
- services/api/tests

## Scope

- Add proposed private participant questions, organizer responses and separately approved public clarifications.
- Link a grading appeal to an attempt/rejudge decision with bounded text and a visible state history.

## Acceptance criteria

- A private clarification is visible only to its participant/team and authorized organizers.
- Publishing a clarification requires explicit organizer action and does not auto-copy private source.
- Appeal resolution links to the official result revision without modifying the original report.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/contests/test_clarifications.py
- npx playwright test tests/e2e/contests/clarifications.spec.ts --workers=2

## Out of scope

- Unmoderated public chat
- Automatic AI adjudication

## Risk and review

Support discussions can leak hidden cases or identifiable submissions.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
