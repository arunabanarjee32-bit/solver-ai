# [SAI-B128] Implement a declared DSA coverage matrix and preregistered model release measurements

<!-- solver-ai-backlog:SAI-B128 -->
Order: 128 / Priority: P1 / Phase: ML-1 measured scope and baseline
Area: solver-readiness / Suggested role: ML evaluation lead and product owner

Implementation status: planned

## Problem

The readiness document can describe broad ambitions, but training and release need a machine-readable support policy and measurable category coverage. Neither attempting a prompt nor passing a small benchmark demonstrates support for every DSA problem.

## Prerequisites

- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)
- SAI-B074 (confirm prerequisite state in the catalogue)
- SAI-B077 (confirm prerequisite state in the catalogue)
- SAI-B078 (confirm prerequisite state in the catalogue)

## Current code ownership

- docs/product/DSA_SOLVER_READINESS.md
- docs/product/AI_SOLVER.md
- docs/research/MODEL_DATA_EVALUATION.md
- scripts/verification
- tests/tooling

## Scope

- Create a versioned coverage manifest under a new ml/evaluation/ implementation, keyed by algorithm topic/subtopic, problem format, difficulty band, supported language/runtime, constraint range and evaluation budget. Reuse B068 problem identities and B074 run records instead of creating another identity authority.
- Bind rights-approved held-out task manifests and independent graders to declared cells; represent missing evidence, out-of-distribution inputs and unsupported formats explicitly.
- Record owner-reviewed per-category quality, reliability, latency/cost and regression thresholds before tuned results are inspected. Define attemptable, measured-supported and unsupported states, including safe refusal/abstention.

## Acceptance criteria

- Synthetic fixtures distinguish an untested category from a measured pass, a failed category and an unsupported input; no empty cell counts as success.
- Release aggregation records eligible task counts, pass@1/pass@k sampling policy, uncertainty and execution failures for each declared category without hiding weak categories in an overall score.
- A model cannot receive a universal any-DSA label, an untested language/interactive format cannot be advertised as supported, and threshold changes retain dated review provenance.

## Validation

- Future authorized checks: deterministic manifest/report fixtures introduced under tests/tooling; no weights, model calls or GPU access are needed for these schema checks.
- Review the coverage manifest and preregistration against DSA_SOLVER_READINESS.md with the evaluation lead and owner.

## Out of scope

- Selecting a checkpoint now
- Claiming formal correctness from finite tests
- Implementing a general natural-language problem parser or replacing B074 evaluation orchestration

## Risk and review

Coverage can be gamed by easy tasks or thresholds chosen after results; preserve category counts, lineage, uncertainty and preregistration.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
