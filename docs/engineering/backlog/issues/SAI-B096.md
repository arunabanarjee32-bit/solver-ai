# [SAI-B096] Version output-comparison policies without changing existing verdicts

<!-- solver-ai-backlog:SAI-B096 -->
Order: 111 / Priority: P1 / Phase: judge-extensibility
Area: judge-validators / Suggested role: Judge engineer

Implementation status: planned

## Problem

Existing grading needs an explicit comparison-policy boundary before supporting richer problem types.

## Prerequisites

- SAI-B027 (confirm prerequisite state in the catalogue)
- SAI-B028 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/judge/solver_judge/grading/cases.py
- services/judge/solver_judge/control/worker.py
- services/judge/tests/grading
- services/api/solver_api/features/catalog

## Scope

- Add a proposed trusted comparison-policy registry with exact and documented whitespace/token policies.
- Bind a policy version to a problem/grading version and retain current seed-problem semantics.

## Acceptance criteria

- Current seed solutions keep their previous verdicts.
- Fixtures distinguish trailing newline, extra tokens, encoding errors and output-size bounds.
- Unknown comparator IDs fail closed rather than selecting a permissive default.

## Validation

- uv run --project services/api --frozen pytest services/judge/tests/grading/test_comparators.py services/judge/tests/grading/test_cases.py
- npm run test:judge:integration

## Out of scope

- Running arbitrary checker scripts on the host
- Changing public API verdict names

## Risk and review

A permissive comparator can accept incorrect programs.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
