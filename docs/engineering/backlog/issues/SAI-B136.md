# [SAI-B136] Evaluate tuned candidates against matched baselines and enforce category gates

<!-- solver-ai-backlog:SAI-B136 -->
Order: 136 / Priority: P1 / Phase: ML-4 evaluation and delivery
Area: model-promotion-evaluation / Suggested role: Independent ML evaluation reviewer

Implementation status: planned

## Problem

A decreasing SFT loss or successful adapter load does not show better solving, teaching or cost. Promotion requires independent held-out comparison against the untuned baseline and the declared support matrix.

## Prerequisites

- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)
- SAI-B074 (confirm prerequisite state in the catalogue)
- SAI-B075 (confirm prerequisite state in the catalogue)
- SAI-B077 (confirm prerequisite state in the catalogue)
- SAI-B128 (confirm prerequisite state in the catalogue)
- SAI-B129 (confirm prerequisite state in the catalogue)
- SAI-B134 (confirm prerequisite state in the catalogue)
- SAI-B135 (confirm prerequisite state in the catalogue)

## Current code ownership

- docs/research/MODEL_DATA_EVALUATION.md
- docs/product/DSA_SOLVER_READINESS.md
- docs/product/AI_SOLVER.md
- services/judge/solver_judge/grading/cases.py

## Scope

- Run the frozen immutable candidate and matched untuned base through the existing B074 harness on a sealed final release set disjoint from training and model-selection/validation, using preregistered B128 measurements, equal budgets and approved independent graders.
- Report per-topic/difficulty/language/input-format coverage, compile/runtime/system failures, pass@1/pass@k protocol, uncertainty, cost/latency and relevant hint quality/safety regressions.
- Produce a reviewed promote/reject/limited-scope decision; quarantine contaminated or invalid tasks and invalidate affected claims instead of repairing the score by omission.

## Acceptance criteria

- A deterministic synthetic worse candidate fails promotion, and missing category evidence yields unmeasured/unsupported status rather than a pass.
- The actual trained candidate receives a complete held-out report including weak categories and failures; no improvement claim is made unless supported by the preregistered comparison.
- A rejected or inconclusive run remains documented and the untuned/previous qualified artifact remains usable; no public activation occurs in this issue.
- Repeated model/hyperparameter selection cannot query the same sealed final test for feedback; any exposed set is labeled and replaced with a newly rights-approved untouched release set for later claims.

## Validation

- Future separately approved execution: replay the locked held-out evaluation manifests for base and candidate with the authorized isolated judge and inference budget.
- Independently review a sample of predictions, grading validity and report aggregation; retain hashes and exact eligible sample counts.

## Out of scope

- Using release-set failures as another training batch before preserving an independent holdout
- Claiming all-DSA correctness
- Changing success thresholds after seeing candidate results

## Risk and review

Contamination, faulty oracles and unequal budgets can manufacture gains; evaluator independence and complete negative reporting are essential.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
