# [SAI-B062] Add a consented concept-check interaction with bounded feedback

<!-- solver-ai-backlog:SAI-B062 -->
Order: 81 / Priority: P2 / Phase: AI-2 consented tutor and debugger
Area: Evidence-oriented tutoring / Suggested role: Teaching product engineer

Implementation status: planned

## Problem

Receiving a hint does not show that a learner understands the concept; a small follow-up can collect observable reasoning without assigning unsupported ability labels.

## Prerequisites

- SAI-B060 (confirm prerequisite state in the catalogue)
- SAI-B061 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- apps/web/features/hints/account-hint.tsx
- apps/web/features/hints/api.ts
- services/api/solver_api/features/hints/service.py
- tests/e2e/hints/hints.spec.ts

## Scope

- Offer an optional single concept question tied to the selected public problem and hint level.
- Accept a bounded learner explanation and return rubric-linked feedback with uncertainty.
- Allow skip/stop and preserve authored practice when the service is unavailable.

## Acceptance criteria

- No answer is submitted without an explicit learner action.
- Feedback distinguishes a rubric observation from a diagnosis of learner ability.
- Question, answer and feedback obey the existing conversation/usage limits.

## Validation

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q; npm run test:e2e -- tests/e2e/hints/hints.spec.ts --workers=1

## Out of scope

- Automated grading of overall intelligence
- Forced quizzes before submissions

## Risk and review

A model-generated rubric may be wrong; reviewed questions and appeal/skip behavior are necessary.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
