# [SAI-B102] Add isolated JavaScript support with denied network and bounded runtime

<!-- solver-ai-backlog:SAI-B102 -->
Order: 117 / Priority: P3 / Phase: judge-extensibility
Area: judge-languages / Suggested role: Judge engineer

Implementation status: planned

## Problem

JavaScript submissions need an independent untrusted-code runtime, not the application Node process.

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

- Add a proposed pinned sandbox Node runtime and a documented stdin/stdout/module contract.
- Disable package installation and retain sandbox network, process, filesystem and output restrictions.

## Acceptance criteria

- Original success, syntax-error, rejected-network, process-spawn and infinite-loop fixtures produce documented results.
- Learner code cannot read application state or inherit provider/worker credentials.
- The browser and API reject JavaScript submissions when its preflight is not ready.

## Validation

- SOLVER_JUDGE_INTEGRATION=1 uv run --project services/api --frozen pytest services/judge/tests/sandbox/test_javascript_runtime.py
- npx playwright test tests/e2e/submissions/languages.spec.ts --grep JavaScript --workers=2

## Out of scope

- npm packages in learner submissions
- Browser DOM execution

## Risk and review

Reusing the application runtime would collapse the isolation boundary.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
