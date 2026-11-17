# [SAI-B090] Enforce contest assistance policy across hint and submission routes

<!-- solver-ai-backlog:SAI-B090 -->
Order: 105 / Priority: P1 / Phase: contest-experience
Area: contest-integrity / Suggested role: Backend engineer and contest policy owner

Implementation status: planned

## Problem

Contest rules require server-enforced assistance restrictions; hiding the hint panel is insufficient.

## Prerequisites

- SAI-B081 (confirm prerequisite state in the catalogue)
- SAI-B086 (confirm prerequisite state in the catalogue)
- SAI-B089 (confirm prerequisite state in the catalogue)
- SAI-B049 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/api/solver_api/features/hints/service.py
- services/api/solver_api/main.py
- apps/web/features/hints
- services/api/tests/hints
- apps/web/features/practice/workspace.tsx

## Scope

- Add proposed explicit event assistance modes and policy evaluation shared by relevant API entrypoints.
- Show the effective policy in the workspace and permit post-event review only when event rules allow it.

## Acceptance criteria

- Direct authenticated requests cannot obtain disallowed assistance during a restricted event.
- Allowed practice and post-event modes retain correct authored/model provenance.
- Policy changes are audited and cannot silently weaken an already active event.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/contests/test_assistance_policy.py services/api/tests/hints/test_hints.py
- npx playwright test tests/e2e/contests/assistance-policy.spec.ts --workers=2

## Out of scope

- Detecting all off-platform AI use
- Changing model-provider budgets

## Risk and review

Inconsistent checks across endpoints could bypass event policy.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
