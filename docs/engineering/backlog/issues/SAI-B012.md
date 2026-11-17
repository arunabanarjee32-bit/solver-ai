# [SAI-B012] Create a consistent private backup and restore procedure for both stores

<!-- solver-ai-backlog:SAI-B012 -->
Order: 13 / Priority: P1 / Phase: 1-safe-pilot
Area: storage-operations / Suggested role: storage/platform engineer

## Problem

Local SQLite databases and the web signing/session secret must be preserved together, but no tested coordinated backup/restore procedure exists. Copying live WAL files casually can produce an unusable or inconsistent recovery.

## Prerequisites

- SAI-B003 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- apps/web/features/accounts/server.ts
- services/api/solver_api/features/submissions/store.py
- scripts/development
- docs/onboarding/DEVELOPMENT.md
- compose.yaml

## Scope

- Implement a trusted operator helper using supported SQLite backup/quiescence semantics for auth and submissions plus required private key material.
- Write a manifest of revision/schema and checksums in a private archive outside Git, with restrictive modes and explicit destination handling.
- Document restore into a fresh temporary workspace and the policy for queued/in-flight work; require confirmation before replacing real state.

## Acceptance criteria

- A temporary fixture backup restores account login/session-key consistency and owned submission history without copying unrelated files.
- A partial/corrupted/missing-key backup is rejected before overwriting destination state.
- Backup files are private, no credential values print, and generated archives remain excluded from Git and application packaging.

## Validation

- Run the new backup/restore helper only against temporary fixture databases and a fresh temporary destination.
- node --test apps/web/tests/auth.test.mjs
- uv run --project services/api --frozen pytest services/api/tests/submissions/test_submissions.py

## Out of scope

- Backing up production data without operator authorization
- Choosing a paid backup vendor
- Claiming encryption-at-rest solely from chmod

## Risk and review

Backups contain credentials and source; accidental publication or destructive restore is a high-impact failure.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
