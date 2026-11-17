# [SAI-B133] Run an approved external LoRA smoke experiment with stop and resume evidence

<!-- solver-ai-backlog:SAI-B133 -->
Order: 133 / Priority: P1 / Phase: ML-3 actual approved training
Area: training-smoke / Suggested role: ML training engineer and authorized compute operator

Implementation status: planned

## Problem

Admission validation and CPU fixtures do not demonstrate that the selected base, tokenizer, adapter configuration and accelerator stack can train safely. A finite external smoke experiment must precede a larger job.

## Prerequisites

- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)
- SAI-B080 (confirm prerequisite state in the catalogue)
- SAI-B129 (confirm prerequisite state in the catalogue)
- SAI-B130 (confirm prerequisite state in the catalogue)
- SAI-B131 (confirm prerequisite state in the catalogue)
- SAI-B132 (confirm prerequisite state in the catalogue)

## Current code ownership

- docs/research/MODEL_DATA_EVALUATION.md
- docs/product/DSA_SOLVER_READINESS.md
- docs/governance/OPEN_DECISIONS.md
- tests/tooling

## Scope

- Implement a bounded LoRA/QLoRA-compatible training command under ml/training/ consuming the accepted B080 manifest and fixed tiny approved corpus slice; choose only a supported precision/method for the future selected model.
- Execute the smoke only on separately authorized external hardware with a recorded low step/time/spend ceiling, cancellation and OOM behavior.
- Save a checkpoint, deliberately stop within the fixture budget, resume under the same configuration and evaluate a small allowed sanity set without using held-out release results for tuning.

## Acceptance criteria

- Evidence records a real approved run: optimizer updates occurred, losses/gradients are finite, intended adapter parameters changed and frozen base parameters remained unchanged.
- Checkpoint resume restores the documented optimizer/scheduler/RNG state or explicitly reports nondeterministic limits; cancellation and budget exhaustion stop the job and leave a usable manifest.
- Memory/time/cost measurements and failed/OOM outcomes are recorded honestly; a dry-run or five-minute demonstration is not marked as a completed full training campaign.

## Validation

- Future approved execution: run the new smoke command with the accepted manifest on the authorized external host, then run its bounded stop/resume scenario.
- Verify checkpoint/base/tokenizer/data hashes and run only the declared finite sanity evaluation; do not load model-generated programs on the host.

## Out of scope

- Selecting a model now
- Training inside Codex/application services
- Launching an unconstrained full corpus job or assuming successful smoke establishes quality

## Risk and review

Even smoke runs incur compute and artifact risk; enforce hard limits in the runner and stop on invalid gradients, loss or artifact state.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
