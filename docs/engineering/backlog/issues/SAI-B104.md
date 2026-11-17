# [SAI-B104] Add isolated Rust compilation with a fixed edition and no dependency fetch

<!-- solver-ai-backlog:SAI-B104 -->
Order: 119 / Priority: P3 / Phase: judge-extensibility
Area: judge-languages / Suggested role: Judge engineer

Implementation status: planned

## Problem

Rust submissions require a toolchain/edition contract and compile budgets separate from application builds.

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

- Add a proposed pinned rustc toolchain and standard-library-only edition contract.
- Bound compilation and program execution independently; reject Cargo dependency retrieval.

## Acceptance criteria

- Original success, borrow/type-error, panic, output-limit and compile-timeout fixtures produce documented results.
- No job downloads crates or modifies a shared writable compiler cache.
- Unavailable toolchain/preflight prevents advertising Rust support.

## Validation

- SOLVER_JUDGE_INTEGRATION=1 uv run --project services/api --frozen pytest services/judge/tests/sandbox/test_rust_runtime.py
- npx playwright test tests/e2e/submissions/languages.spec.ts --grep Rust --workers=2

## Out of scope

- Arbitrary Cargo packages
- Nightly or user-selected toolchains

## Risk and review

Long compilation or shared cache mutation can exhaust capacity or contaminate jobs.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
