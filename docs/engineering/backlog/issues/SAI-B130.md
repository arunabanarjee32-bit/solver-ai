# [SAI-B130] Materialize a permitted validated training corpus with immutable split lineage

<!-- solver-ai-backlog:SAI-B130 -->
Order: 130 / Priority: P1 / Phase: ML-2 approved data and training tooling
Area: training-data / Suggested role: Data engineer and rights/evaluation reviewer

Implementation status: planned

## Problem

B077 and B078 define split/permission records, but no approved corpus has been normalized, validated and materialized for actual training. The archives include incomplete LFS entries and overlapping benchmark variants that cannot be treated as a ready dataset.

## Prerequisites

- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)
- SAI-B077 (confirm prerequisite state in the catalogue)
- SAI-B078 (confirm prerequisite state in the catalogue)
- SAI-B128 (confirm prerequisite state in the catalogue)

## Current code ownership

- docs/governance/DATA_AND_LICENSES.md
- docs/research/MODEL_DATA_EVALUATION.md
- services/judge/solver_judge/grading/cases.py
- scripts/verification
- tests/tooling

## Scope

- Implement a data-only pipeline under new ml/data/ modules that reads only explicitly approved complete inputs and emits immutable train/validation manifests outside Git. Reuse the permission/split registries rather than infer rights from repository licenses.
- Normalize task/solution/language/provenance records, quarantine malformed or duplicate entries and verify solution correctness through authorized independent grading before including solution targets.
- Reserve the held-out release set; record exact and reviewed near-duplicate exclusions, source lineage, content hashes, accepted/rejected counts and a reproducible materialization recipe.

## Acceptance criteria

- Every emitted training record points to complete approved source and a valid immutable task identity; missing LFS objects, unknown training permission and private unconsented submissions are rejected.
- A synthetic variant of a held-out task is excluded even when its file name or wording changes, with reviewable reason/override records.
- The manifest can be rebuilt to matching hashes from the same approved inputs; logs contain metadata/counts rather than raw private code or benchmark bodies.

## Validation

- Future authorized checks: synthetic malformed/rights/duplicate/split fixtures for the new data pipeline.
- Future approved data execution: run the fixed corpus materialization manifest, independently inspect a stratified sample and verify solution targets in the existing isolated judge.

## Out of scope

- Bulk importing all archived datasets
- Using model-created answers as trusted ground truth without independent validation
- Redistributing datasets or downloading missing objects without permission

## Risk and review

Bad solutions, silent rights assumptions and leakage can invalidate both training and evaluation; quarantine uncertain inputs rather than filling gaps automatically.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
