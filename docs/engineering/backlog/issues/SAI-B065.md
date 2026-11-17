# [SAI-B065] Build a public-only execution evidence projection for debugging

<!-- solver-ai-backlog:SAI-B065 -->
Order: 84 / Priority: P1 / Phase: AI-2 consented tutor and debugger
Area: Safe debugger evidence / Suggested role: Judge/API security engineer

## Problem

Worker/API summaries already protect private grading details. Model debugging needs a separately allowlisted evidence projection that cannot accidentally export hidden inputs or raw diagnostics.

## Prerequisites

- SAI-B044 (publish/complete prerequisite first)
- SAI-B064 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/features/submissions/store.py
- services/judge/solver_judge/control/worker.py
- services/judge/solver_judge/grading/cases.py
- services/api/tests/submissions/test_submissions.py

## Scope

- Define structured evidence for owned public sample runs and capped compiler/runtime categories.
- Preserve independent worker and API sanitization; reject private-test manifests and opaque raw logs.
- Associate evidence with source/problem/runtime hashes.

## Acceptance criteria

- Hidden input/output and credential sentinels never enter model evidence.
- Evidence with a mismatched source/problem hash is refused.
- Output limits apply before storage and provider serialization.

## Validation

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/submissions services/judge/tests/control -q

## Out of scope

- Exporting private failing tests
- Weakening current safe_summary controls

## Risk and review

An error message can contain hostile program-written text and must remain untrusted.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
