# [SAI-B073] Rank candidates by explicit execution evidence with deterministic ties

<!-- solver-ai-backlog:SAI-B073 -->
Order: 92 / Priority: P2 / Phase: AI-3 bounded candidate solver
Area: Candidate ranking / Suggested role: AI evaluation engineer

Implementation status: planned

## Problem

phi-code ranks sample passes and embedding similarity, but similarity is not correctness and zero or incomparable test sets must not produce an acceptance claim.

## Prerequisites

- SAI-B070 (confirm prerequisite state in the catalogue)
- SAI-B071 (confirm prerequisite state in the catalogue)
- SAI-B072 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/api/solver_api/features/hints/service.py
- docs/product/AI_SOLVER.md
- AnalyseFuture/extracted/phi-code-main/solver/terminal.py

## Scope

- Define versioned comparable-evidence requirements and deterministic ranking/tie rules.
- Label untested, failed and finite-check-passed candidates separately.
- Keep embedding or model-confidence scores optional research signals outside correctness claims.

## Acceptance criteria

- Ranking is stable across repeated ordering of identical records.
- Candidates with different test manifests are not compared as equivalent evidence.
- Zero-test candidates cannot be labeled accepted or preferred on correctness grounds.

## Validation

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q; review adversarial ranking fixtures.

## Out of scope

- Claiming mathematical verification
- Loading the archived ranker model

## Risk and review

Optimizing public tests can overfit them; show exactly which finite checks informed selection.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
