# [SAI-B069] Generate a bounded algorithm-plan record before candidate code

<!-- solver-ai-backlog:SAI-B069 -->
Order: 88 / Priority: P2 / Phase: AI-3 bounded candidate solver
Area: Candidate planning / Suggested role: AI solver engineer

## Problem

CodeSIM provides useful planning/simulation ideas, but its archived framework mixes provider calls and unsafe evaluation. Solver AI needs a small original typed plan stage.

## Prerequisites

- SAI-B045 (publish/complete prerequisite first)
- SAI-B048 (publish/complete prerequisite first)
- SAI-B050 (publish/complete prerequisite first)
- SAI-B068 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/features/hints/service.py
- docs/product/AI_SOLVER.md
- AnalyseFuture/extracted/CodeGenerator-master/src/promptings/CodeSIM.py

## Scope

- Define concise algorithm summary, assumptions, invariant and claimed complexity fields with strict bounds.
- Record model/prompt/problem identity and consume the shared run budget.
- Treat simulation text as a model claim rather than execution or proof.

## Acceptance criteria

- Malformed/oversized plans fail before candidate generation.
- Every plan is attributable to an immutable specification and prompt version.
- No prompt requests hidden chain-of-thought or claims that simulated samples prove correctness.

## Validation

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q; static comparison to the archived design without executing it.

## Out of scope

- Modifying the immutable archive
- Formal verification of arbitrary algorithms

## Risk and review

A convincing plan may be wrong and must not bypass isolated tests.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
