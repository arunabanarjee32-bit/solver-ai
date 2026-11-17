# [SAI-B082] Add permissioned contest registration and eligibility checks

<!-- solver-ai-backlog:SAI-B082 -->
Order: 97 / Priority: P1 / Phase: contest-foundation
Area: contests / Suggested role: Backend engineer

Implementation status: planned

## Problem

An event needs explicit participant eligibility separate from ordinary account access.

## Prerequisites

- SAI-B081 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/api/solver_api/features/identity
- services/api/solver_api/main.py
- services/api/tests

## Scope

- Add proposed contest registration records and join/withdraw endpoints using the existing verified identity boundary.
- Enforce event visibility, registration windows and organizer/participant permissions server-side.

## Acceptance criteria

- An unauthenticated user receives 401 and an ineligible authenticated user receives 403.
- Duplicate registration is idempotent; withdrawal after a locked roster follows the documented policy.
- One user cannot alter another registration or enumerate a private participant list.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/contests/test_registration.py
- npm run test:auth

## Out of scope

- New identity provider
- Payment-based qualification or automatic real-world identity verification

## Risk and review

Registration leakage or weak checks could expose private events.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
