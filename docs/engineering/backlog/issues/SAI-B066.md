# [SAI-B066] Return debugger hypotheses separately from observed failures

<!-- solver-ai-backlog:SAI-B066 -->
Order: 85 / Priority: P2 / Phase: AI-2 consented tutor and debugger
Area: Evidence-backed debugging / Suggested role: AI debugging engineer

## Problem

A wrong-answer verdict alone does not reveal its cause, and generated explanations can invent failure evidence or overstate a proposed correction.

## Prerequisites

- SAI-B048 (publish/complete prerequisite first)
- SAI-B050 (publish/complete prerequisite first)
- SAI-B064 (publish/complete prerequisite first)
- SAI-B065 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/features/hints/service.py
- services/api/solver_api/main.py
- docs/product/AI_SOLVER.md
- services/api/tests/hints/test_hints.py

## Scope

- Implement a bounded debug response with observed evidence references, hypotheses, suggested correction and unverified claims.
- Validate cited evidence IDs and treat unmatched claims as hypotheses or reject them.
- Reuse admission, privacy, token and timeout controls rather than adding an independent unbounded loop.

## Acceptance criteria

- No response can cite evidence not supplied to that run.
- A correction is never labeled tested before the isolated runner has returned matching evidence.
- Provider outage produces a stable failure and leaves source/history intact.

## Validation

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q

## Out of scope

- Guaranteed root-cause detection
- Executing suggested code in API processes

## Risk and review

Well-written model explanations can sound more certain than the supplied evidence allows.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
