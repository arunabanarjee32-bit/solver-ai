# [SAI-B068] Version authorized solver problem specifications and evaluation modes

<!-- solver-ai-backlog:SAI-B068 -->
Order: 87 / Priority: P1 / Phase: AI-3 bounded candidate solver
Area: Solver input contracts / Suggested role: Backend contract engineer

## Problem

A candidate solver needs immutable problem/context identity and explicit allowed evaluation modes; a slug alone cannot describe changed constraints or permissions.

## Prerequisites

- SAI-B042 (publish/complete prerequisite first)
- SAI-B049 (publish/complete prerequisite first)
- SAI-B064 (publish/complete prerequisite first)
- SAI-B027 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/features/catalog/models.py
- services/api/solver_api/features/catalog/content.py
- services/api/solver_api/features/hints/service.py
- docs/product/AI_SOLVER.md

## Scope

- Project B027 canonical immutable problem/grader revision into a bounded public ProblemSpec with context fingerprint, requested runtime and rights/assistance scope; do not create a competing content-version authority.
- Keep private grading manifests outside model serialization.
- Document how current seed catalog records produce this specification without changing public catalog semantics.

## Acceptance criteria

- Changed public task content creates a different immutable specification ID.
- Unsupported runtime or unauthorized evaluation mode is rejected before generation.
- Serialized specifications contain no private cases or account credentials.

## Validation

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/catalog services/api/tests/hints -q

## Out of scope

- Bulk import of archive benchmarks
- Inventing permission metadata for existing third-party data

## Risk and review

Version labels without immutable content and rights metadata are not reproducible inputs.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
