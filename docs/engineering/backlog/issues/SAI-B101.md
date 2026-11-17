# [SAI-B101] Add isolated Java support with explicit JVM resource semantics

<!-- solver-ai-backlog:SAI-B101 -->
Order: 116 / Priority: P3 / Phase: judge-extensibility
Area: judge-languages / Suggested role: Judge engineer with runtime reviewer

Implementation status: planned

## Problem

Java support requires JVM-aware startup and limits, not only a language dropdown.

## Prerequisites

- SAI-B096 (confirm prerequisite state in the catalogue)
- SAI-B125 (confirm prerequisite state in the catalogue)
- SAI-B124 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/judge/Dockerfile
- services/judge/solver_judge/sandbox/harness.py
- services/judge/solver_judge/control/runner.py
- services/api/solver_api/features/submissions/store.py
- apps/web/features/practice/code-pane.tsx

## Scope

- Add a proposed pinned JDK toolchain, class/main contract and versioned compilation/run command.
- Document runtime overhead and supported resource accounting before enabling the capability.

## Acceptance criteria

- Original fixtures cover successful execution, compilation failure, uncaught exception and deadline/output limits.
- JVM startup overhead is included in the documented total deadline; host process execution is never used.
- Capability remains unavailable if preflight or resource enforcement fails.

## Validation

- SOLVER_JUDGE_INTEGRATION=1 uv run --project services/api --frozen pytest services/judge/tests/sandbox/test_java_runtime.py
- npx playwright test tests/e2e/submissions/languages.spec.ts --grep Java --workers=2

## Out of scope

- Multiple arbitrary JDK versions
- Claiming aggregate memory measurement without runtime support

## Risk and review

JVM memory reservations can conflict with existing per-process limits.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
