# [SAI-B113] Provide learner-controlled progress summaries with assistance provenance

<!-- solver-ai-backlog:SAI-B113 -->
Order: 75 / Priority: P2 / Phase: learning-coaching
Area: learning-analytics / Suggested role: Backend engineer with learning researcher

Implementation status: planned

## Problem

Owned attempt history does not yet offer a careful summary of independent versus assisted practice.

## Prerequisites

- SAI-B003 (confirm prerequisite state in the catalogue)
- SAI-B022 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/api/solver_api/features/submissions/store.py
- services/api/solver_api/main.py
- apps/web/features/submissions
- services/api/tests

## Scope

- Add a proposed summary of completed practice by topic, observed attempts and explicitly recorded assistance state.
- Show the source/limits of each metric and exclude contest results when event policy requires it.

## Acceptance criteria

- Hand-seeded histories produce exact counts with no cross-account rows.
- Unknown assistance remains unknown rather than being labeled independent.
- The interface does not claim learning improvement or skill diagnosis from accepted-answer totals alone.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/learning/test_progress_summaries.py
- npx playwright test tests/e2e/learning/progress.spec.ts --workers=2

## Out of scope

- AI skill prediction
- Public ranking of personal learning data

## Risk and review

Misleading or leaking progress metrics can harm learner trust.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
