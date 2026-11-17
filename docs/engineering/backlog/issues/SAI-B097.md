# [SAI-B097] Add isolated versioned custom-checker support for authorized problems

<!-- solver-ai-backlog:SAI-B097 -->
Order: 112 / Priority: P2 / Phase: judge-extensibility
Area: judge-validators / Suggested role: Judge engineer with security reviewer

Implementation status: planned

## Problem

Some original problems need custom validation, but checker code cannot gain host execution privileges.

## Prerequisites

- SAI-B096 (confirm prerequisite state in the catalogue)
- SAI-B124 (confirm prerequisite state in the catalogue)
- SAI-B125 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/judge/solver_judge/control/runner.py
- services/judge/solver_judge/control/worker.py
- services/judge/solver_judge/sandbox/harness.py
- services/judge/tests/sandbox

## Scope

- Design a proposed bounded checker protocol and execute approved checker artifacts through the isolated runtime.
- Separate checker/runtime failure from learner wrong answer and limit feedback to permitted summaries.

## Acceptance criteria

- A valid alternative output is accepted and an invalid witness is rejected by maintained fixtures.
- Checker timeout, malformed result and attempted network/host-file access fail closed with cleanup.
- Private expected data and checker diagnostics never appear in participant responses.

## Validation

- uv run --project services/api --frozen pytest services/judge/tests/grading/test_custom_checkers.py
- SOLVER_JUDGE_INTEGRATION=1 uv run --project services/api --frozen pytest services/judge/tests/sandbox/test_checker_isolation.py

## Out of scope

- User-uploaded arbitrary checkers
- Production approval of an unaudited execution engine

## Risk and review

Checker privileges and diagnostic leakage expand the execution trust boundary.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
