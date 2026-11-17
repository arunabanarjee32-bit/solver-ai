# [SAI-B027] Version problem and grader identity on every new submission

<!-- solver-ai-backlog:SAI-B027 -->
Order: 28 / Priority: P1 / Phase: 2-useful-practice
Area: content-contract / Suggested role: backend/content engineer

## Problem

Submissions retain problem slug/title but not an immutable public specification and grading revision. Future content changes could make an old verdict appear to refer to a different problem/test contract.

## Prerequisites

- SAI-B013 (publish/complete prerequisite first)
- SAI-B026 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/features/catalog/models.py
- services/api/solver_api/features/catalog/content.py
- services/api/solver_api/features/submissions/store.py
- services/judge/solver_judge/grading/cases.py
- services/api/tests/submissions/test_submissions.py

## Scope

- Introduce explicit problem revision and grader-manifest identity at creation/lease time without exposing private cases.
- Persist these identities in new submissions via a tested migration and define how legacy records are labeled unknown/legacy.
- Require the worker to reject unsupported revision combinations safely rather than grade with the nearest current slug.

## Acceptance criteria

- Changing current problem content does not relabel the revision recorded on an existing attempt.
- A worker cannot complete an unsupported revision as AC; the job receives a safe explicit system outcome.
- Owned history/detail and exports show revision metadata, while private grading content remains outside public API/model context.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/submissions/test_submissions.py services/api/tests/catalog/test_api.py
- uv run --project services/api --frozen pytest services/judge/tests/grading/test_cases.py services/judge/tests/control/test_worker.py

## Out of scope

- Building a full contest/version administration platform
- Returning hidden test data or expected answers
- Rejudging historical submissions automatically

## Risk and review

Revision mismatches can silently invalidate verdicts; worker/API identity must be checked before execution and preserved in records.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
