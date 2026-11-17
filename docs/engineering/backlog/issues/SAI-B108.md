# [SAI-B108] Rehearse a timed full-stack disaster restore using the approved backup helper

<!-- solver-ai-backlog:SAI-B108 -->
Order: 51 / Priority: P1 / Phase: operated-pilot
Area: operations-recovery / Suggested role: Site reliability engineer with privacy reviewer

## Problem

B012 provides the backup/restore implementation; operations still need an isolated full-service recovery rehearsal with measured completeness and timing.

## Prerequisites

- SAI-B012 (publish/complete prerequisite first)
- SAI-B013 (publish/complete prerequisite first)
- SAI-B003 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- scripts/verification
- docs/onboarding/DEVELOPMENT.md
- compose.yaml
- apps/web/features/accounts/server.ts
- services/api/solver_api/features/submissions/store.py

## Scope

- Invoke B012 backup/restore tooling and manifest format in fresh disposable service volumes; do not create another backup format or restore implementation.
- Restart web/API against restored data and verify auth/key continuity, ownership and job-recovery policy without changing live developer state.
- Produce a redacted RPO/RTO rehearsal report against B003 targets, including interrupted/missing-generation cases.

## Acceptance criteria

- A seeded account can authenticate and read only its restored attempts after the drill restart.
- Missing key material, corrupt backup and mismatched database generation cause a clear failure.
- The report records measured restore duration and completeness, and proves original state was untouched.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/operations/test_restore_drill.py
- node --test apps/web/tests/auth.test.mjs

## Out of scope

- Designing the foundational backup storage/encryption system
- Uploading backups to a new paid service

## Risk and review

A partial restoration can lose accounts, invalidate sessions or mismatch ownership.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
