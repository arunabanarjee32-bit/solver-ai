# [SAI-B071] Route authorized AI candidates through the existing isolated judge boundary

<!-- solver-ai-backlog:SAI-B071 -->
Order: 90 / Priority: P1 / Phase: AI-3 bounded candidate solver
Area: Solver-to-judge integration / Suggested role: Judge and backend integration engineer

Implementation status: planned

## Problem

Generated candidates currently have no active execution integration. Archive host evaluators cannot be imported safely, and model runs must not masquerade as learner submissions.

## Prerequisites

- SAI-B050 (confirm prerequisite state in the catalogue)
- SAI-B051 (confirm prerequisite state in the catalogue)
- SAI-B065 (confirm prerequisite state in the catalogue)
- SAI-B068 (confirm prerequisite state in the catalogue)
- SAI-B070 (confirm prerequisite state in the catalogue)
- SAI-B121 (confirm prerequisite state in the catalogue)
- SAI-B123 (confirm prerequisite state in the catalogue)
- SAI-B125 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/api/solver_api/features/submissions/store.py
- services/api/solver_api/main.py
- services/judge/solver_judge/control/worker.py
- services/judge/solver_judge/control/runner.py

## Scope

- Define explicit candidate-job ownership/attribution while reusing queue leases, runtime readiness, limits and cleanup.
- Allow only the evaluation modes approved by ProblemSpec and charge test jobs to a shared run budget.
- Return the public-only evidence projection; preserve normal learner history semantics.

## Acceptance criteria

- Missing isolation/readiness refuses candidate jobs with no host fallback.
- One account cannot poll or cancel another account's candidate run.
- Matching source/runtime hashes connect each result to one candidate; private test data never reaches model context.

## Validation

- Future authorized check: npm run test:judge:integration; uv run --project services/api --frozen pytest services/api/tests/submissions services/api/tests/hints -q

## Out of scope

- Executing programs in the API
- Bypassing worker budgets for research users

## Risk and review

Generated code is equally untrusted as learner code and may target the result protocol.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
