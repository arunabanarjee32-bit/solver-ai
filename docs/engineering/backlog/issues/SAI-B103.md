# [SAI-B103] Add isolated Go compilation with offline standard-library execution

<!-- solver-ai-backlog:SAI-B103 -->
Order: 118 / Priority: P3 / Phase: judge-extensibility
Area: judge-languages / Suggested role: Judge engineer

Implementation status: planned

## Problem

Go is feasible only with a reproducible offline compiler and bounded compilation/runtime behavior.

## Prerequisites

- SAI-B096 (confirm prerequisite state in the catalogue)
- SAI-B125 (confirm prerequisite state in the catalogue)
- SAI-B124 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/judge/Dockerfile
- services/judge/solver_judge/sandbox/harness.py
- services/judge/solver_judge/control/runner.py
- apps/web/features/practice/code-pane.tsx
- services/judge/tests/sandbox

## Scope

- Add a proposed pinned Go toolchain and standard-library-only submission contract.
- Set deterministic compilation environment and forbid module downloads inside jobs.

## Acceptance criteria

- Success, compile-error, excessive goroutine/output and timeout fixtures remain bounded and cleaned up.
- An attempted remote module import cannot cause outbound fetch.
- Existing Python/C++ grading remains unchanged and capabilities reflect actual Go readiness.

## Validation

- SOLVER_JUDGE_INTEGRATION=1 uv run --project services/api --frozen pytest services/judge/tests/sandbox/test_go_runtime.py
- npx playwright test tests/e2e/submissions/languages.spec.ts --grep Go --workers=2

## Out of scope

- Arbitrary Go modules
- Paid compilation services

## Risk and review

Compiler caches, network resolution and concurrent goroutines need bounded policy.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
