# [SAI-B025] Export an authenticated user-owned submission history bundle

<!-- solver-ai-backlog:SAI-B025 -->
Order: 26 / Priority: P2 / Phase: 2-useful-practice
Area: privacy-product / Suggested role: backend/frontend engineer

## Problem

Users can inspect individual owned attempts but cannot take a bounded portable export of their history. An export must honor retention and avoid becoming a cross-user or bulk-memory leak.

## Prerequisites

- SAI-B003 (publish/complete prerequisite first)
- SAI-B022 (publish/complete prerequisite first)
- SAI-B024 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/main.py
- services/api/solver_api/features/submissions/store.py
- apps/web/features/submissions/api.ts
- apps/web/features/submissions/submission-history.tsx
- services/api/tests/submissions/test_submissions.py

## Scope

- Define a versioned owner export schema with attempts and optional retained source; use bounded batches and an explicit maximum/export continuation policy.
- Add an authenticated download action and make expired-source omissions explicit.
- Exclude tokens, internal worker IDs/leases, private grading cases and raw auth database content.

## Acceptance criteria

- Account A export contains only A records, even with supplied IDs or concurrent account changes.
- A dataset exceeding the batch size exports completely through the documented bounded mechanism without materializing arbitrary history in one response.
- Exported metadata identifies schema/time and omitted expired source; files contain no credentials or private test fields.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/submissions/test_submissions.py
- PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e -- tests/e2e/submissions/submissions.spec.ts --workers=2

## Out of scope

- Exporting all users or auth secrets
- Cloud storage uploads
- An implicit backup/training-consent grant

## Risk and review

Exports are private source artifacts; owner authorization, response limits and cache/download handling need explicit tests.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
