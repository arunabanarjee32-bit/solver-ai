# [SAI-B131] Create a separate locked training environment and reviewed artifact loader

<!-- solver-ai-backlog:SAI-B131 -->
Order: 131 / Priority: P1 / Phase: ML-2 approved data and training tooling
Area: training-infrastructure / Suggested role: ML infrastructure engineer

Implementation status: planned

## Problem

The active API environment deliberately has no ML training stack. Actual training requires a reproducible separate environment, compatible accelerator libraries and safe artifact loading without importing archived requirements or model remote code into app services.

## Prerequisites

- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)
- SAI-B079 (confirm prerequisite state in the catalogue)
- SAI-B080 (confirm prerequisite state in the catalogue)
- SAI-B129 (confirm prerequisite state in the catalogue)

## Current code ownership

- docs/research/MODEL_DATA_EVALUATION.md
- docs/onboarding/DEVELOPMENT.md
- scripts/verification
- tests/tooling

## Scope

- Create ml/training/ with its own pinned project/lock, supported Python/CUDA/toolchain matrix and noninteractive setup/preflight entry point; retain independent API/web lockfiles.
- Implement an artifact loader tied to the future selected revision and B078/B080 records, verifying approved artifact identities, tokenizer/config files and allowed local paths. Default to no arbitrary trust_remote_code and safe tensor formats.
- Implement dry-run configuration and resource preflight that report required resources, supported precision/adapter modes, environment versions and hard stop conditions without automatically provisioning compute.

## Acceptance criteria

- Installing or importing training tooling does not add ML dependencies to services/api or start a download/training job.
- Synthetic unapproved revision, hash mismatch, path escape and remote-code-required cases fail before loading; trusted artifact handling preserves TLS/checksum verification.
- The exact training environment can be reconstructed and its preflight distinguishes unsupported hardware, missing approved artifact and ready state without pretending a memory estimate is an actual measurement.

## Validation

- Future authorized checks: the new loader/config fixtures run on CPU with tiny local synthetic tensors/configurations and no external requests.
- On separately approved external hardware, run only the documented training preflight and record the actual environment/artifact hashes before a training job.

## Out of scope

- Installing GPU drivers in the application environment
- Copying archive requirements or enabling unreviewed remote code
- Provisioning paid GPUs or running the actual smoke/train job

## Risk and review

Artifact deserialization and accelerator dependencies expand the supply chain; isolate them from app credentials and preserve immutable versions.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
