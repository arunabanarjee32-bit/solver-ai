# [SAI-B135] Publish immutable private model artifacts and complete adapter lineage

<!-- solver-ai-backlog:SAI-B135 -->
Order: 135 / Priority: P1 / Phase: ML-3 actual approved training
Area: model-artifacts / Suggested role: ML platform engineer and data/model steward

Implementation status: planned

## Problem

A training checkpoint directory is not a reproducible deliverable. Consumers need to know which base/tokenizer/license/data/run produced an adapter and must not accidentally load a mismatched or modified artifact.

## Prerequisites

- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)
- SAI-B078 (confirm prerequisite state in the catalogue)
- SAI-B129 (confirm prerequisite state in the catalogue)
- SAI-B130 (confirm prerequisite state in the catalogue)
- SAI-B131 (confirm prerequisite state in the catalogue)
- SAI-B134 (confirm prerequisite state in the catalogue)

## Current code ownership

- docs/research/MODEL_DATA_EVALUATION.md
- docs/governance/DATA_AND_LICENSES.md
- docs/product/DSA_SOLVER_READINESS.md
- scripts/verification
- tests/tooling

## Scope

- Implement an immutable artifact manifest/registry interface under ml/ for base, tokenizer, adapter/config, training run and intended compatible inference precisions, storing approved large artifacts outside Git.
- Record hashes, size, code/environment versions, data/split lineage, license/NOTICE/redistribution restrictions and retention/access policy; do not publish private training examples.
- Provide a fetch/verify/reconstruct command that requires exact identities, rejects unauthorized artifacts and records a retained last-known-good candidate for rollback.

## Acceptance criteria

- Reconstruction with the correct authorized base/tokenizer/adapter succeeds to matching identities; mismatched bases, altered tensors and missing required files fail before serving.
- Registry entries are immutable/versioned, contain every required provenance link and distinguish unpublished/private from approved redistributable artifacts.
- No weight, credential, private corpus or raw learner code enters the application repository or public model-card evidence.

## Validation

- Future authorized checks: synthetic registry/manifest/hash/access fixtures in the separate ML tooling.
- For the trained candidate, fetch only the approved artifacts into an isolated temporary inference workspace and verify the complete reconstruction record.

## Out of scope

- Making weights public without permission
- Buying an artifact-store service by default
- Silently merging an adapter into an unidentified base

## Risk and review

Ambiguous lineage or unrestricted artifact publication can violate licenses and make rollback impossible; retain exact reconstructible identities.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
