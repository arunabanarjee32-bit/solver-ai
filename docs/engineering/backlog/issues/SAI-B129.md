# [SAI-B129] Run an approved untuned checkpoint comparison and record a future selection

<!-- solver-ai-backlog:SAI-B129 -->
Order: 129 / Priority: P1 / Phase: ML-1 measured scope and baseline
Area: model-baseline / Suggested role: ML evaluation engineer with project owner

Implementation status: planned

## Problem

The research catalogue names future candidates but no model has been selected, downloaded or benchmarked here. A fine-tuning choice needs measured task fit, actual resource behavior and license compatibility rather than a nominal parameter count or advertised score.

## Prerequisites

- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)
- SAI-B074 (confirm prerequisite state in the catalogue)
- SAI-B078 (confirm prerequisite state in the catalogue)
- SAI-B079 (confirm prerequisite state in the catalogue)
- SAI-B128 (confirm prerequisite state in the catalogue)

## Current code ownership

- docs/research/FINETUNING_MODEL_RESEARCH.md
- docs/research/MODEL_DATA_EVALUATION.md
- docs/governance/OPEN_DECISIONS.md
- scripts/verification
- tests/tooling

## Scope

- After separate owner authorization for artifacts, hardware and a fixed experiment budget, compare at least two eligible open-weight checkpoints or explicitly justify why only one is eligible. Do not assume any family or size wins.
- Reuse B074 evaluation and B128 coverage on a model-selection/validation split disjoint from training and the sealed final release test; fix prompts/templates, decoding, context limits, candidate/test budgets and exact model revisions. Run single-candidate untuned baselines before adding repair or tuning.
- Measure peak training/inference feasibility separately where authorized, report unknowns and record a reviewed selection or do-not-proceed outcome. Hosted/API models may be optional approved reference baselines, not assumed downloadable LoRA bases.

## Acceptance criteria

- The report includes exact checkpoint/revision, license/usage evidence, tokenizer/template, hardware/software, precision, per-category results, latency, memory, cost and failures.
- All compared scores state task eligibility and comparable budgets; no task used for later held-out evaluation is silently moved into training.
- No checkpoint is selected merely by writing this issue. Actual execution requires recorded artifact/compute permission; absent resources produce an explicit blocked decision without substituting invented measurements.
- Checkpoint selection never inspects the sealed final release-test results; record a separate selection split and freeze the chosen model/criteria before final evaluation.

## Validation

- Future approved execution: use the B074 harness to replay the recorded untuned manifests on the allowed isolated inference host and retain result hashes.
- Reproduce one small manifest twice and investigate nondeterministic/failed outcomes; any paid API baseline requires its own existing approval and cap.

## Out of scope

- Choosing a specific model in this planning update
- Training adapters
- Reproducing every published model benchmark or buying hardware by default

## Risk and review

Model training exposure is often unknown and published hardware figures may not match this workload; report contamination and feasibility uncertainty.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
