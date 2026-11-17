# [SAI-B072] Implement a finite repair state machine with one shared run budget

<!-- solver-ai-backlog:SAI-B072 -->
Order: 91 / Priority: P1 / Phase: AI-3 bounded candidate solver
Area: Bounded solver repair / Suggested role: Backend workflow engineer

## Problem

A plan/generate/test/repair loop can consume unlimited calls and execution jobs unless state transitions and aggregate stop conditions are explicit.

## Prerequisites

- SAI-B054 (publish/complete prerequisite first)
- SAI-B066 (publish/complete prerequisite first)
- SAI-B069 (publish/complete prerequisite first)
- SAI-B071 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/features/hints/service.py
- services/api/solver_api/features/submissions/store.py
- docs/product/AI_SOLVER.md
- services/api/tests/hints/test_hints.py

## Scope

- Model generation, queued/running evaluation, repair, cancellation and terminal states explicitly.
- Limit total candidates, repair attempts, tokens, test jobs, elapsed time and reserved spend across the complete run.
- Feed back only approved public evidence and preserve every attempted candidate hash.

## Acceptance criteria

- Every transition is covered by a deterministic state-machine fixture.
- Exhausting any limit stops new provider and judge work.
- Restart/retry/cancel cannot restart a terminal run or duplicate reserved work.

## Validation

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints services/api/tests/submissions -q

## Out of scope

- Unlimited autonomous repair
- Leaking private failing cases as feedback

## Risk and review

Per-step limits are insufficient when aggregate attempts can still grow.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
