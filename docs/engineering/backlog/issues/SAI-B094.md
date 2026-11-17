# [SAI-B094] Deliver bounded scoreboard polling with consistent event revisions

<!-- solver-ai-backlog:SAI-B094 -->
Order: 109 / Priority: P2 / Phase: contest-experience
Area: leaderboards / Suggested role: Frontend engineer

## Problem

A leaderboard must refresh reliably without exposing frozen results or creating an unbounded request loop.

## Prerequisites

- SAI-B085 (publish/complete prerequisite first)
- SAI-B086 (publish/complete prerequisite first)
- SAI-B088 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- apps/web/app
- apps/web/features
- services/api/solver_api/main.py
- services/api/tests
- tests/e2e

## Scope

- Add a proposed scoreboard view using bounded polling, conditional/versioned responses and explicit stale/error states.
- Render ties, team names and freeze state from server projections; cancel requests on navigation.

## Acceptance criteria

- A response from an older event revision cannot overwrite a newer display.
- Polling stops on navigation and backs off after failures under fake-clock tests.
- Narrow-screen and keyboard flows expose the same frozen/public data as the API.

## Validation

- npx playwright test tests/e2e/contests/scoreboard.spec.ts --workers=2
- uv run --project services/api --frozen pytest services/api/tests/contests/test_scoreboard_projection.py

## Out of scope

- WebSocket infrastructure
- Global rating or follower systems

## Risk and review

Out-of-order updates and aggressive polling can harm fairness or availability.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
