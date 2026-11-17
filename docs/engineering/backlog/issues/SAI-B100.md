# [SAI-B100] Add an audited C++20 runtime alongside existing C++17

<!-- solver-ai-backlog:SAI-B100 -->
Order: 115 / Priority: P2 / Phase: judge-extensibility
Area: judge-languages / Suggested role: Judge engineer

Implementation status: planned

## Problem

C++20 is a roadmap language, but the current supported contract is C++17.

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

- Add a proposed explicit C++20 language ID/compiler mode while retaining C++17.
- Advertise the runtime only after compiler/version and isolation probes succeed; update editor/submission validation together.

## Acceptance criteria

- A C++20-only original fixture compiles and passes while the existing C++17 suite remains green.
- Compiler errors, time/output limits and cleanup execute through the same isolation boundary.
- A missing compiler mode does not appear as an available language.

## Validation

- npm run test:judge:integration
- npx playwright test tests/e2e/submissions/languages.spec.ts --grep Cpp20 --workers=2

## Out of scope

- Claiming all C++20 library features across compilers
- Upgrading the managed host runtime without approval

## Risk and review

Compiler-mode drift can make editor and judge capabilities disagree.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
