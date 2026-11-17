# [SAI-B098] Implement bounded floating-point answer validation

<!-- solver-ai-backlog:SAI-B098 -->
Order: 113 / Priority: P2 / Phase: judge-extensibility
Area: judge-validators / Suggested role: Judge engineer and numerical-problem author

## Problem

Numerical problems require explicit tolerance semantics rather than ad hoc string conversion.

## Prerequisites

- SAI-B096 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/judge/solver_judge/grading
- services/judge/tests/grading
- services/api/solver_api/features/catalog

## Scope

- Add a proposed versioned comparator with approved absolute/relative tolerance and token-count rules.
- Reject malformed numbers, non-finite values and unsupported locale formats deterministically.

## Acceptance criteria

- Boundary fixtures cover both tolerance limits, signed zero, scientific notation and extreme finite magnitudes.
- NaN/infinity/extra-token outputs cannot bypass validation.
- Problem metadata cannot choose unbounded or negative tolerances.

## Validation

- uv run --project services/api --frozen pytest services/judge/tests/grading/test_float_comparator.py

## Out of scope

- Arbitrary precision symbolic proofs
- Changing existing integer-problem grading

## Risk and review

Floating-point edge cases can produce false acceptance or rejection.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
