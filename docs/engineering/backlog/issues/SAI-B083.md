# [SAI-B083] Freeze versioned problem sets for each contest

<!-- solver-ai-backlog:SAI-B083 -->
Order: 98 / Priority: P1 / Phase: contest-foundation
Area: contests / Suggested role: Backend engineer and problem curator

Implementation status: planned

## Problem

A contest must not silently change when the practice catalog or grading cases are updated.

## Prerequisites

- SAI-B081 (confirm prerequisite state in the catalogue)
- SAI-B027 (confirm prerequisite state in the catalogue)
- SAI-B029 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/api/solver_api/features/catalog
- services/api/solver_api/main.py
- services/api/tests
- services/judge/solver_judge/grading

## Scope

- Add a proposed immutable contest problem-set reference with ordered problem/version identifiers.
- Reject set edits after the documented publication lock and record the permitted correction process.

## Acceptance criteria

- A scheduled event resolves every configured problem version before it opens.
- Changing the active practice problem does not alter an already locked event.
- Participants cannot read unreleased statements or private grading metadata through contest endpoints.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/contests/test_problem_sets.py
- uv run --project services/api --frozen pytest services/judge/tests/grading/test_cases.py

## Out of scope

- Bulk competitor content import
- Interactive problem types

## Risk and review

Incorrect version linkage changes fairness and reproducibility.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
