# [SAI-B110] Implement a revisioned deployment smoke and rollback rehearsal

<!-- solver-ai-backlog:SAI-B110 -->
Order: 53 / Priority: P1 / Phase: operated-pilot
Area: operations-release / Suggested role: Release engineer and service owner

## Problem

Local builds alone do not prove a deployable revision can be promoted or rolled back safely.

## Prerequisites

- SAI-B107 (publish/complete prerequisite first)
- SAI-B108 (publish/complete prerequisite first)
- SAI-B109 (publish/complete prerequisite first)
- SAI-B005 (publish/complete prerequisite first)
- SAI-B013 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- compose.yaml
- compose.cloud.yaml
- apps/web/Dockerfile
- services/api/Dockerfile
- scripts/verification
- docs/onboarding/DEVELOPMENT.md

## Scope

- Add a proposed operator-invoked release rehearsal using immutable built artifact identifiers and isolated state.
- Verify health, account/session continuity, owned history and compatibility before recording a promotion decision.

## Acceptance criteria

- A healthy candidate and a deliberately unhealthy candidate exercise promotion and rollback paths.
- Rollback preserves seeded account/submission state and records the exact application/artifact revisions.
- The helper never publishes externally or modifies the running environment without an explicit operator invocation.

## Validation

- docker compose config --quiet
- npx playwright test tests/e2e/operations/release-smoke.spec.ts --workers=1

## Out of scope

- Automatic production deployment
- Provisioning a hosting account or paid infrastructure

## Risk and review

Rollback across incompatible state versions can corrupt user data.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
