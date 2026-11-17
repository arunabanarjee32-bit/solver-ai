# [SAI-B084] Implement deterministic ICPC scoring as a tested pure calculation

<!-- solver-ai-backlog:SAI-B084 -->
Order: 99 / Priority: P1 / Phase: contest-foundation
Area: contests / Suggested role: Backend engineer with experienced contest reviewer

Implementation status: planned

## Problem

The repository has verdicts but no ICPC score or penalty semantics.

## Prerequisites

- SAI-B081 (confirm prerequisite state in the catalogue)
- SAI-B083 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/api/solver_api/features
- services/api/tests
- docs/product/PRODUCT_REQUIREMENTS.md

## Scope

- Add a proposed scoring module with solved-count priority, configurable wrong-attempt penalty and explicit tie ordering.
- Define how pending, canceled, compiler-error and rejudged attempts affect each problem.

## Acceptance criteria

- Hand-calculated fixtures cover tied solved counts, multiple wrong attempts, first acceptance and submissions after acceptance.
- The same event ledger always yields identical standings independent of input row order.
- Pending/untrusted worker messages cannot create an accepted score.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/contests/test_icpc_scoring.py

## Out of scope

- Global user rating
- IOI partial scoring

## Risk and review

A small scoring rule mistake can change winners.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
