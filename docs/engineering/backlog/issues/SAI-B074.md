# [SAI-B074] Create a reproducible offline solver evaluation run manifest

<!-- solver-ai-backlog:SAI-B074 -->
Order: 93 / Priority: P1 / Phase: AI-4 evaluation and research gates
Area: Solver evaluation / Suggested role: Research evaluation engineer

Implementation status: planned

## Problem

The repository has historical upstream claims but no current model evaluation harness that pins tasks, prompts, runtime and budgets for fair strategy comparisons.

## Prerequisites

- SAI-B053 (confirm prerequisite state in the catalogue)
- SAI-B068 (confirm prerequisite state in the catalogue)
- SAI-B072 (confirm prerequisite state in the catalogue)
- SAI-B073 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- docs/research/MODEL_DATA_EVALUATION.md
- docs/product/AI_SOLVER.md
- services/api/solver_api/features/hints/service.py
- AnalyseFuture/repository-inventory/FEATURE_INVENTORY.txt

## Scope

- Define an offline manifest and bounded harness using only approved tasks and existing isolated execution.
- Compare single-candidate, planning and repair/ranking variants under explicitly comparable budgets.
- Record model/prompt/runtime/task versions, seeds, usage, latency, failures and termination reasons.

## Acceptance criteria

- A deterministic fake-provider run can be replayed without external calls.
- Reports separate completed, failed, skipped and unexecuted tasks.
- pass@1/pass@k include the stated sampling procedure, eligible sample counts and uncertainty; no gains are invented.

## Validation

- Future authorized check: targeted harness tests added beside services/api/tests/hints; any live evaluation requires a separately approved manifest and spend cap.

## Out of scope

- Downloading large benchmark corpora by default
- Claiming the upstream scores were reproduced

## Risk and review

Unequal inference budgets or contaminated tasks can make a comparison misleading.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
