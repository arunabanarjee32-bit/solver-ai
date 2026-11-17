# [SAI-B140] Run a separately approved execution-reward preference or RL experiment

<!-- solver-ai-backlog:SAI-B140 -->
Order: 140 / Priority: P2 / Phase: ML-5 conditional improvement research
Area: optional-model-research / Suggested role: ML researcher, independent grader reviewer and compute owner

Implementation status: planned

## Problem

SFT may leave systematic failures, but preference tuning or GRPO/RL can reward test exploitation and spend significant compute. The existing roadmap only mentions later research; it implements and runs no RL training stage.

## Prerequisites

- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)
- SAI-B075 (confirm prerequisite state in the catalogue)
- SAI-B077 (confirm prerequisite state in the catalogue)
- SAI-B078 (confirm prerequisite state in the catalogue)
- SAI-B080 (confirm prerequisite state in the catalogue)
- SAI-B128 (confirm prerequisite state in the catalogue)
- SAI-B130 (confirm prerequisite state in the catalogue)
- SAI-B131 (confirm prerequisite state in the catalogue)
- SAI-B132 (confirm prerequisite state in the catalogue)
- SAI-B133 (confirm prerequisite state in the catalogue)
- SAI-B134 (confirm prerequisite state in the catalogue)
- SAI-B135 (confirm prerequisite state in the catalogue)
- SAI-B136 (confirm prerequisite state in the catalogue)

## Current code ownership

- docs/research/MODEL_DATA_EVALUATION.md
- docs/product/DSA_SOLVER_READINESS.md
- services/judge/solver_judge/grading/cases.py
- services/judge/solver_judge/sandbox/harness.py
- tests/tooling

## Scope

- First record a falsifiable hypothesis and a separately approved method/reward/data/compute manifest comparing one narrow preference or execution-reward method against the retained SFT baseline and equal-budget inference alternatives.
- Reuse approved data/artifact tooling; build audited reward checks around independently reviewed finite execution evidence, with bounded generation/judge budgets and anti-reward-hacking fixtures.
- Execute a tiny approved reward/training smoke, then only if valid execute the specifically approved bounded experiment; preserve actual checkpoints, costs, failed runs and independent held-out results.

## Acceptance criteria

- Synthetic exploit candidates that print forged success, exploit grader assumptions or consume unbounded resources do not earn a valid success reward.
- The actual approved experiment records optimizer updates and full resource/termination evidence; missing approval/valid reward prevents any job, and no improvement is a valid outcome.
- Independent evaluation reports quality, regressions and total cost versus SFT and inference-only alternatives; the candidate is not promoted automatically.
- Method and checkpoint selection use validation data; final RL comparison uses a newly reserved sealed set if earlier SFT/export evaluation exposed the prior set, with the unchanged baseline evaluated under the same protocol.

## Validation

- Future authorized checks: deterministic reward/manifest fixtures with original finite sandbox cases and no live training.
- Only after separate approval, run the recorded external smoke/experiment and replay the untouched held-out comparison under its fixed budget.

## Out of scope

- Making RL a prerequisite for releasing a useful SFT/tutor product
- Unlimited GRPO rollouts or unknown reward oracles
- Claiming finite rewards prove general reasoning or correctness

## Risk and review

Reward hacking, data leakage and resource amplification can produce misleading gains; this optional issue requires an explicit stop/no-go outcome.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
