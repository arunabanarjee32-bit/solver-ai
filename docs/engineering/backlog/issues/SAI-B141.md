# [SAI-B141] Operate a consented failure-analysis and retraining improvement cycle

<!-- solver-ai-backlog:SAI-B141 -->
Order: 141 / Priority: P2 / Phase: ML-5 conditional improvement research
Area: model-lifecycle / Suggested role: ML lifecycle owner and privacy/evaluation reviewers

Implementation status: planned

## Problem

After release, failures and user feedback need a controlled correction path. Automatically training on reported code or repeatedly optimizing against the same holdout would violate consent and undermine future evidence.

## Prerequisites

- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)
- SAI-B003 (confirm prerequisite state in the catalogue)
- SAI-B063 (confirm prerequisite state in the catalogue)
- SAI-B077 (confirm prerequisite state in the catalogue)
- SAI-B078 (confirm prerequisite state in the catalogue)
- SAI-B128 (confirm prerequisite state in the catalogue)
- SAI-B130 (confirm prerequisite state in the catalogue)
- SAI-B134 (confirm prerequisite state in the catalogue)
- SAI-B135 (confirm prerequisite state in the catalogue)
- SAI-B136 (confirm prerequisite state in the catalogue)
- SAI-B139 (confirm prerequisite state in the catalogue)

## Current code ownership

- docs/research/MODEL_DATA_EVALUATION.md
- docs/product/DSA_SOLVER_READINESS.md
- docs/governance/DATA_AND_LICENSES.md
- docs/status/PROJECT_STATUS.md
- services/api/solver_api/features/hints/service.py

## Scope

- Define bounded operator review of consented/redacted failure categories, with separate source/problem rights checks and no automatic collection of raw private submissions.
- Turn reviewed failures into correction candidates only through the approved corpus pipeline; quarantine any previously exposed evaluation task and preserve a genuinely independent future release set.
- For a justified improvement, create a new approved training/evaluation manifest and execute the existing bounded cycle, comparing to the last released artifact before any owner-authorized rollout. Record no-change/rejected outcomes as well.

## Acceptance criteria

- Opt-out/deleted/private inputs cannot enter a training batch; approved additions retain immutable provenance, consent and split lineage.
- A failure that came from release evaluation cannot silently become both training data and a claimed unseen success in the next report.
- Each actually attempted improvement has distinct run/artifact IDs, before/after category/regression/cost evidence and a tested rollback link; collecting feedback does not by itself trigger training or deployment.

## Validation

- Future authorized checks: synthetic consent/deletion/split-lineage/lifecycle fixtures in ML tooling.
- For a separately approved iteration, replay the retained baseline and candidate manifests and record the actual training, independent evaluation and rollout decision; do not silently reuse old successes as new proof.

## Out of scope

- Continuous autonomous training on user activity
- Default upload of learner code to models or datasets
- A guarantee that every failure can be corrected or every DSA task solved

## Risk and review

Feedback loops can turn private data into training material and destroy holdout independence; keep human/owner review and repeatable negative outcomes.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
