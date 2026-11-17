# [SAI-B079] Produce a resource-and-integrity feasibility decision for one self-hosted model

<!-- solver-ai-backlog:SAI-B079 -->
Order: 126 / Priority: P2 / Phase: AI-4 evaluation and research gates
Area: Model serving research gate / Suggested role: ML infrastructure researcher

Implementation status: planned

## Problem

Archived ranker/solver code permits remote model code and names consumer-hardware models, but current hardware, artifact integrity, licensing and serving economics are unverified.

## Prerequisites

- SAI-B074 (confirm prerequisite state in the catalogue)
- SAI-B078 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- docs/research/MODEL_DATA_EVALUATION.md
- docs/governance/OPEN_DECISIONS.md
- AnalyseFuture/extracted/phi-code-main/solver/main.py
- AnalyseFuture/planning/TECHNICAL_DEBT.txt

## Scope

- Compare one pinned checkpoint/quantization against the approved provider baseline using documented memory, concurrency and maintenance requirements.
- Review model code/license/artifact hashes and reject arbitrary trust_remote_code loading as a default.
- Specify the separate approval, isolated environment and fixed budget needed for an empirical serving experiment.

## Acceptance criteria

- Decision names an exact artifact/revision and states unknown measurements honestly.
- No weight download, remote-code execution or GPU purchase occurs during the feasibility issue.
- Recommendation includes a measurable evaluation plan and a do-not-proceed outcome when resources are inadequate.

## Validation

- Static artifact/terms/hardware review and comparison table; optional empirical commands remain unexecuted until separately approved.

## Out of scope

- Provisioning inference infrastructure
- Assuming self-hosting is automatically cheaper

## Risk and review

Published memory or benchmark claims may not hold under this project's concurrency and isolation requirements.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
