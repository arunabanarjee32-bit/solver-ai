# [SAI-B088] Add locked ICPC team rosters and event membership rules

<!-- solver-ai-backlog:SAI-B088 -->
Order: 103 / Priority: P2 / Phase: contest-experience
Area: teams / Suggested role: Backend engineer

## Problem

ICPC-style participation needs explicit team identity rather than caller-supplied teammate IDs.

## Prerequisites

- SAI-B082 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/features/identity
- services/api/solver_api/main.py
- services/api/tests

## Scope

- Implement proposed invitation, acceptance, captain and roster-lock rules for a contest team.
- Enforce team-size limits and the policy for one user joining multiple teams in the same event.

## Acceptance criteria

- Only an invited account can accept its own invitation.
- A locked roster rejects membership changes except the documented organizer correction.
- Concurrent acceptance cannot exceed the configured team-size or single-team limit.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/contests/test_team_rosters.py

## Out of scope

- Organization-wide employee directories
- Voice/video collaboration

## Risk and review

Membership races or invitation leakage could grant unintended team access.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
