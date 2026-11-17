# [SAI-B030] Add one original prefix-sum range-query teaching exercise

<!-- solver-ai-backlog:SAI-B030 -->
Order: 31 / Priority: P2 / Phase: 2-useful-practice
Area: content / Suggested role: problem author and judge reviewer

Implementation status: planned

## Problem

The three current seeds cover summation, contiguous growth and sliding windows. There is no original exercise teaching preprocessing with repeated range queries.

## Prerequisites

- SAI-B029 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/api/solver_api/features/catalog/content.py
- services/judge/solver_judge/grading/cases.py
- services/judge/tests/grading/test_cases.py
- services/judge/tests/sandbox/test_sandbox.py
- tests/e2e/practice/practice.spec.ts

## Scope

- Author one original statement, constraints, two informative public samples, Python/C++17 starter code and three progressive authored hints.
- Add a small independent reference oracle and generated boundary cases for one-based/zero-based endpoints, full-range queries, negatives and 64-bit totals.
- Use the provenance, revision and authoring gates already introduced; keep expected private cases in the trusted judge.

## Acceptance criteria

- A correct Python and C++17 solution receive AC on the authorized finite tests; off-by-one and repeated-linear-scan fixtures demonstrate the intended failure limits.
- Both public samples agree with the independent oracle and the rendered statement.
- The content has explicit original authorship and no copied third-party problem text; explanation states O(n+q) reasoning without a universal-correctness claim.

## Validation

- uv run --project services/api --frozen pytest services/judge/tests/grading/test_cases.py services/api/tests/catalog/test_api.py
- In a supported isolated runtime: npm run test:judge:integration
- PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e -- tests/e2e/practice/practice.spec.ts --workers=2

## Out of scope

- Adding a bulk problem bank
- Changing language runtime support
- Claiming finite grading proves all-input correctness

## Risk and review

Poor constraints/oracles can invalidate teaching and verdicts; require independent content review.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
