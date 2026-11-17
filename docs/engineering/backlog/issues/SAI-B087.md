# [SAI-B087] Implement isolated virtual-contest sessions with personal start times

<!-- solver-ai-backlog:SAI-B087 -->
Order: 102 / Priority: P2 / Phase: contest-experience
Area: contests / Suggested role: Full-stack engineer

Implementation status: planned

## Problem

A learner cannot replay a contest under a personal timer without changing the shared event.

## Prerequisites

- SAI-B081 (confirm prerequisite state in the catalogue)
- SAI-B083 (confirm prerequisite state in the catalogue)
- SAI-B084 (confirm prerequisite state in the catalogue)
- SAI-B086 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/api/solver_api/main.py
- services/api/solver_api/features
- services/api/tests
- apps/web/app

## Scope

- Add proposed virtual-session state referencing an immutable published problem set and duration.
- Keep personal timing/scoring separate from official standings and provide a recoverable resume view.

## Acceptance criteria

- Two learners starting at different times receive independent deadlines and standings.
- Reloading or opening a second tab cannot reset or extend a started session.
- Virtual attempts never appear in official rankings.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/contests/test_virtual_sessions.py
- npx playwright test tests/e2e/contests/virtual.spec.ts --workers=2

## Out of scope

- Anti-cheat guarantees for self-directed practice
- Paid virtual events

## Risk and review

Shared identifiers could mix personal and official attempts.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
