# [SAI-B080] Add an explicit admission gate for reproducible fine-tuning experiments

<!-- solver-ai-backlog:SAI-B080 -->
Order: 127 / Priority: P1 / Phase: AI-4 evaluation and research gates
Area: Fine-tuning research controls / Suggested role: ML evaluation lead with project owner

Implementation status: planned

## Problem

The archived trainer can start expensive, nondeterministic work, while Solver AI has no proven baseline, approved complete dataset or production training workflow.

## Prerequisites

- SAI-B074 (confirm prerequisite state in the catalogue)
- SAI-B077 (confirm prerequisite state in the catalogue)
- SAI-B078 (confirm prerequisite state in the catalogue)
- SAI-B079 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- docs/research/MODEL_DATA_EVALUATION.md
- docs/governance/OPEN_DECISIONS.md
- AnalyseFuture/extracted/phi-code-main/ranker/train.py
- AnalyseFuture/planning/PROJECT_VISION_AND_FUTURE_ROADMAP.txt

## Scope

- Define and validate an experiment manifest covering rights-approved disjoint data, base artifact, seed, hyperparameters, external compute, spend ceiling and owner approval.
- Require a matched untuned baseline and an evaluation/negative-result publication plan.
- Reject manifests that request training inside the application workspace or omit rollback/artifact-retention rules.

## Acceptance criteria

- Missing approval, dataset/model permission, budget or disjoint evaluation split prevents experiment admission.
- Manifest validation performs no training, cloud provisioning or model loading.
- Promotion criteria compare quality, cost and regressions; failure to improve is a valid recorded outcome.

## Validation

- Future authorized check: synthetic manifest validation fixtures and owner review; any actual training is a separate approved execution task.

## Out of scope

- Running LoRA/QLoRA/GRPO in this issue
- Promising that tuning improves solver correctness

## Risk and review

Training can memorize evaluation tasks or consume substantial resources without improving product value.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
