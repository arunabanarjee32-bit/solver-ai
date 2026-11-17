# [SAI-B081] Implement contest lifecycle and authoritative event timing

<!-- solver-ai-backlog:SAI-B081 -->
Order: 96 / Priority: P1 / Phase: contest-foundation
Area: contests / Suggested role: Backend engineer with contest product owner

Implementation status: planned

## Problem

Contests are proposed but no active event lifecycle or authoritative clock exists.

## Prerequisites

- SAI-B003 (confirm prerequisite state in the catalogue)
- SAI-B027 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/api/solver_api/main.py
- services/api/solver_api/features
- services/api/tests
- docs/product/PRODUCT_REQUIREMENTS.md

## Scope

- Add a proposed contests feature module with draft, scheduled, running, frozen and finished transitions.
- Specify UTC storage, inclusive/exclusive start/end boundaries and organizer-only transition rules before adding routes.

## Acceptance criteria

- A transition table rejects every invalid state change.
- Boundary tests cover one instant before, at and after start/end; browser time cannot extend an event.
- Practice submissions remain unaffected when no contest is selected.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/contests/test_lifecycle.py
- uv run --project services/api --frozen ruff check services/api

## Out of scope

- Rated public events
- External clock services or paid infrastructure

## Risk and review

Ambiguous deadlines can accept late work or invalidate legitimate attempts.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
