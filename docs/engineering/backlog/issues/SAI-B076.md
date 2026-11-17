# [SAI-B076] Reduce consented public counterexamples under a finite execution budget

<!-- solver-ai-backlog:SAI-B076 -->
Order: 95 / Priority: P2 / Phase: AI-4 evaluation and research gates
Area: Counterexample debugging / Suggested role: Judge tooling engineer

## Problem

A large permitted failing input can be hard to explain; reduction is useful only if it preserves task validity and the observed failure without exposing private cases.

## Prerequisites

- SAI-B064 (publish/complete prerequisite first)
- SAI-B065 (publish/complete prerequisite first)
- SAI-B071 (publish/complete prerequisite first)
- SAI-B075 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/judge/solver_judge/grading/cases.py
- services/api/solver_api/features/hints/service.py
- apps/web/features/practice/workspace.tsx
- docs/product/AI_SOLVER.md

## Scope

- Implement one reviewed task-specific reducer with explicit validity checks and execution ceiling.
- Accept only user-supplied or approved public/generated inputs with a trustworthy failure predicate.
- Label the result as a smaller observed counterexample, not a globally minimal one.

## Acceptance criteria

- Every returned input remains valid and reproduces the same selected failure.
- Exhausted budgets return the best observed input with a clear stop reason.
- Private test IDs/manifests are rejected at intake.

## Validation

- Future authorized check: task-scoped grading fixtures in services/judge/tests/grading and debugger contract fixtures in services/api/tests/hints.

## Out of scope

- General-purpose automatic minimization for every problem
- Recovering hidden tests

## Risk and review

Naive reduction can leave the input domain or change the failure being explained.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
