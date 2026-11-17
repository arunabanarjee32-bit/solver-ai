# [SAI-B134] Execute the approved bounded SFT adapter training campaign

<!-- solver-ai-backlog:SAI-B134 -->
Order: 134 / Priority: P1 / Phase: ML-3 actual approved training
Area: actual-fine-tuning / Suggested role: ML training lead and compute operator

Implementation status: planned

## Problem

B080 explicitly excludes actual LoRA/QLoRA/GRPO execution. Without this separate task the roadmap can finish admission tooling and still produce no fine-tuned model.

## Prerequisites

- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)
- SAI-B080 (confirm prerequisite state in the catalogue)
- SAI-B129 (confirm prerequisite state in the catalogue)
- SAI-B130 (confirm prerequisite state in the catalogue)
- SAI-B131 (confirm prerequisite state in the catalogue)
- SAI-B132 (confirm prerequisite state in the catalogue)
- SAI-B133 (confirm prerequisite state in the catalogue)

## Current code ownership

- docs/research/MODEL_DATA_EVALUATION.md
- docs/product/DSA_SOLVER_READINESS.md
- docs/governance/OPEN_DECISIONS.md

## Scope

- Execute the approved SFT campaign through the separate ml/training/ runner using the fixed base, allowed adapter method, training/validation corpus, seed, effective batch, schedule and bounded hyperparameter plan from the accepted manifest.
- Use validation data for the preregistered checkpoint/stopping policy, record every attempted run including failed/aborted ones and enforce external compute/time/spend ceilings.
- Produce retained candidate adapters and a complete run report with environment/data/code lineage, losses, step counts, resource measurements and termination reason; keep weights and private data out of Git.

## Acceptance criteria

- At least one actual optimization campaign reaches its declared completion or a clearly recorded failure/early-stop state; documentation completion cannot substitute for execution.
- The saved candidate loads with the exact base/tokenizer and has verified tensor/checkpoint identities; no held-out release task was used to select hyperparameters or checkpoints.
- The report states actual cost/resources and all runs, including negative outcomes. Training completion alone neither promotes the artifact nor asserts improved DSA performance.

## Validation

- Future separately approved execution: run the training command against the signed-off B080 manifest on the approved external host; verify recorded steps, cancellation and spend stops.
- Reconstruct the selected checkpoint from the report and run the declared validation-only evaluation before handing the candidate to B136.

## Out of scope

- Defaulting to a named checkpoint in this planning update
- Unlimited hyperparameter search
- A foundation-model pretraining project or guaranteed performance gain

## Risk and review

Training can overfit, leak evaluation data or exhaust resources; frozen manifests and independent review of run evidence are required.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
