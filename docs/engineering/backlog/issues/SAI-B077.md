# [SAI-B077] Separate evaluation splits and report archive contamination candidates

<!-- solver-ai-backlog:SAI-B077 -->
Order: 124 / Priority: P1 / Phase: AI-4 evaluation and research gates
Area: Evaluation integrity / Suggested role: Data evaluation engineer

## Problem

Archived benchmark variants contain overlapping tasks, and public model training history is incomplete. Reusing them naively can contaminate training/evaluation comparisons.

## Prerequisites

- SAI-B068 (publish/complete prerequisite first)
- SAI-B074 (publish/complete prerequisite first)
- SAI-B026 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- docs/research/MODEL_DATA_EVALUATION.md
- AnalyseFuture/manifest.json
- AnalyseFuture/extracted/CodeGenerator-master/data/HumanEval/HumanEval.jsonl
- AnalyseFuture/extracted/CodeGenerator-master/data/HumanEval/HumanEvalET.jsonl

## Scope

- Define immutable split manifests by problem/source/date lineage rather than file name alone.
- Compute permitted exact/normalized overlap fingerprints and flag near-duplicate candidates for review.
- Record unknown model-training exposure as uncertainty rather than claiming a clean benchmark.

## Acceptance criteria

- The same task cannot enter training and evaluation splits under different variant filenames.
- Every exclusion/override records its reason and owner.
- Original archives stay byte-identical; analysis outputs contain hashes/metadata rather than copied benchmark bodies.

## Validation

- Future authorized check: deterministic synthetic overlap fixtures; static manifest review before any real-data analysis.

## Out of scope

- Claiming zero contamination for closed models
- Training on archived benchmark solutions

## Risk and review

Approximate deduplication needs human review and cannot establish unseen model pretraining data.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
