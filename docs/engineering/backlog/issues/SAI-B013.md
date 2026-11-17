# [SAI-B013] Introduce versioned transactional migrations for the submission database

<!-- solver-ai-backlog:SAI-B013 -->
Order: 14 / Priority: P1 / Phase: 1-safe-pilot
Area: storage / Suggested role: backend storage engineer

## Problem

The submission store initializes tables with CREATE IF NOT EXISTS but has no recorded schema version or tested forward migration path. Retention, provenance and deletion changes need safe evolution of existing user data.

## Prerequisites

- SAI-B012 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/features/submissions/store.py
- services/api/tests/submissions/test_submissions.py
- scripts/development
- docs/onboarding/DEVELOPMENT.md

## Scope

- Add a small schema-version registry and ordered transactional migrations for the existing SQLite store.
- Represent the current schema as the supported baseline and fail safely on unknown newer versions.
- Provide operator preflight/backup guidance and a failure rollback strategy without editing Better Auth-owned schema.

## Acceptance criteria

- A fixture built with the current schema upgrades without losing IDs, ownership, source, idempotency or lease semantics.
- A failing migration leaves the prior valid schema/data intact; repeat startup does not reapply an already completed migration.
- A database with a future unknown schema is refused with a safe diagnostic instead of silently modified.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/submissions/test_submissions.py

## Out of scope

- Migrating to PostgreSQL
- Writing custom migrations for Better Auth internal tables
- Running destructive downgrade on real data

## Risk and review

Schema mistakes can corrupt private history; require backup and real old-schema fixtures, not only fresh-database tests.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
