# [SAI-B099] Introduce explicit subtask scoring for separately configured events

<!-- solver-ai-backlog:SAI-B099 -->
Order: 114 / Priority: P3 / Phase: judge-extensibility
Area: judge-validators / Suggested role: Judge engineer and contest product owner

Implementation status: planned

## Problem

Future partial-score tasks need a contract that does not silently reinterpret ICPC AC/WA scoring.

## Prerequisites

- SAI-B096 (confirm prerequisite state in the catalogue)
- SAI-B097 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)
- SAI-B013 (confirm prerequisite state in the catalogue)
- SAI-B027 (confirm prerequisite state in the catalogue)
- SAI-B084 (confirm prerequisite state in the catalogue)

## Current code ownership

- services/judge/solver_judge/grading
- services/judge/solver_judge/control/worker.py
- services/api/solver_api/features/submissions/store.py
- services/api/tests

## Scope

- Add a proposed problem-version subtask/weight contract with bounded aggregate score reporting.
- Keep partial-score events distinct from ICPC scoring and withhold private case details.

## Acceptance criteria

- Weights and dependencies validate before a task is released.
- Hand-calculated pass/fail fixtures yield exact deterministic subtask totals.
- ICPC and ordinary practice results remain byte-compatible in their existing public fields.

## Validation

- uv run --project services/api --frozen pytest services/judge/tests/grading/test_subtask_scoring.py
- uv run --project services/api --frozen pytest services/api/tests/contests/test_partial_scoring.py

## Out of scope

- Changing every existing contest to IOI rules
- Interactive grading

## Risk and review

Mixing score models can silently change rankings.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
