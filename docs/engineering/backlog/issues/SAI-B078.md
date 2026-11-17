# [SAI-B078] Register dataset and model permissions separately from source licenses

<!-- solver-ai-backlog:SAI-B078 -->
Order: 125 / Priority: P1 / Phase: AI-4 evaluation and research gates
Area: Research provenance / Suggested role: Data stewardship and project owner

## Problem

MIT/Apache source notices do not authorize benchmark redistribution, training, commercial use or model-weight deployment; five archived datasets are only pointers.

## Prerequisites

- SAI-B041 (publish/complete prerequisite first)
- SAI-B068 (publish/complete prerequisite first)
- SAI-B077 (publish/complete prerequisite first)
- SAI-B002 (publish/complete prerequisite first)
- SAI-B026 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- docs/governance/DATA_AND_LICENSES.md
- docs/research/MODEL_DATA_EVALUATION.md
- AnalyseFuture/repository-inventory/ARCHIVED_FILES_MANIFEST.txt
- AnalyseFuture/extracted/phi-code-main/datasets/atcoder.jsonl

## Scope

- Define machine-readable provenance with source, owner, version/hash, permitted uses, evidence and unresolved status.
- Require separate flags for evaluate/train/redistribute/commercial/model-serving permissions.
- Represent missing LFS objects explicitly and block activation until content and rights are available.

## Acceptance criteria

- Unknown or absent permission never defaults to allowed.
- A source-code license cannot satisfy an unrelated dataset/model permission field.
- Each approved experiment references complete immutable inputs and review evidence.

## Validation

- Future authorized check: schema fixtures using synthetic rights records; owner review of actual permission evidence without bulk downloads.

## Out of scope

- Legal conclusions without review
- Fetching all missing LFS datasets automatically

## Risk and review

Permission metadata can be incomplete or expire; record review date and responsible owner.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
