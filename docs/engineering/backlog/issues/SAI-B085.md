# [SAI-B085] Add participant and organizer scoreboard projections with freeze rules

<!-- solver-ai-backlog:SAI-B085 -->
Order: 100 / Priority: P1 / Phase: contest-foundation
Area: contests / Suggested role: Backend engineer

Implementation status: planned

## Problem

Contest standings need different visibility during a scoreboard freeze.

## Prerequisites

- SAI-B084 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/api/solver_api/main.py
- services/api/solver_api/features
- services/api/tests

## Scope

- Build proposed public/participant and organizer projections from the scored event ledger.
- Apply freeze/unfreeze rules before serialization; do not send hidden verdicts for the browser to hide.

## Acceptance criteria

- A participant response contains no post-freeze verdict, timestamp detail or score that reveals the hidden result.
- Authorized organizers see the complete projection and unauthorized users receive 403.
- Unfreezing produces the same final standings as an unfrozen full replay.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/contests/test_scoreboard_projection.py

## Out of scope

- WebSockets
- Public rating formulas

## Risk and review

Aggregate fields can accidentally leak frozen results.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
