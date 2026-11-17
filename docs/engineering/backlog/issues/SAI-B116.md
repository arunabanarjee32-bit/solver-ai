# [SAI-B116] Add permissioned assignments and human rubric feedback

<!-- solver-ai-backlog:SAI-B116 -->
Order: 78 / Priority: P2 / Phase: learning-coaching
Area: coaching / Suggested role: Full-stack engineer and educator reviewer

## Problem

Coaching needs an assignment boundary and visible human feedback rather than ad hoc access to all submissions.

## Prerequisites

- SAI-B113 (publish/complete prerequisite first)
- SAI-B115 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/features/catalog
- services/api/solver_api/main.py
- apps/web/app
- apps/web/features
- services/api/tests

## Scope

- Add proposed cohort assignments using authorized problem versions and explicit deadlines.
- Support a bounded human rubric/comment record attached only to submitted assignment work.

## Acceptance criteria

- A learner sees only assigned work and feedback allowed for that cohort.
- A coach cannot attach feedback to an unrelated private practice attempt.
- Rubric edits retain attribution/revision and render as safe text in browser tests.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/coaching/test_assignments.py
- npx playwright test tests/e2e/coaching/assignments.spec.ts --workers=2

## Out of scope

- Automatic AI grading of educational ability
- Live classroom video or plagiarism accusations

## Risk and review

Feedback permissions and immutable problem references must remain consistent.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
