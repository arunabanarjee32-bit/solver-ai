# [SAI-B057] Provide a tested operator kill switch for model hint admission

<!-- solver-ai-backlog:SAI-B057 -->
Order: 72 / Priority: P1 / Phase: AI-1 controlled model hints
Area: AI operations / Suggested role: Backend operations engineer

## Problem

A provider incident or budget concern must disable future external work without breaking the already completed local authored workflow.

## Prerequisites

- SAI-B048 (publish/complete prerequisite first)
- SAI-B049 (publish/complete prerequisite first)
- SAI-B055 (publish/complete prerequisite first)
- SAI-B056 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/features/hints/service.py
- services/api/tests/hints/test_hints.py
- apps/web/features/hints/account-hint.tsx
- docs/onboarding/DEVELOPMENT.md

## Scope

- Define trusted enabled/disabled/draining states and bounded in-flight treatment.
- Make the UI display the effective source/capability rather than a hard-coded model promise.
- Document disable, verify-no-egress and restore procedures.

## Acceptance criteria

- Disabling admission prevents new external calls immediately at the admission boundary.
- In-flight reservation handling follows one documented policy.
- Authored hints, catalog and submissions retain their existing behavior.

## Validation

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q; npm run test:e2e -- tests/e2e/hints/hints.spec.ts --workers=1

## Out of scope

- Disabling account security checks
- Silently labeling fallback text as model output

## Risk and review

A UI-only toggle cannot stop API callers or already admitted upstream work.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
