# [SAI-B132] Implement tokenizer-aware SFT examples and answer-only loss masking

<!-- solver-ai-backlog:SAI-B132 -->
Order: 132 / Priority: P1 / Phase: ML-2 approved data and training tooling
Area: training-preprocessing / Suggested role: ML data/training engineer

Implementation status: planned

## Problem

A clean text corpus is insufficient for SFT: the chosen tokenizer/chat template, truncation, special tokens and labels determine what the model actually learns. Incorrect masking can train on user/system text or cut away the solution.

## Prerequisites

- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)
- SAI-B129 (confirm prerequisite state in the catalogue)
- SAI-B130 (confirm prerequisite state in the catalogue)
- SAI-B131 (confirm prerequisite state in the catalogue)

## Current code ownership

- docs/research/MODEL_DATA_EVALUATION.md
- docs/product/DSA_SOLVER_READINESS.md
- tests/tooling

## Scope

- Implement preprocessing under ml/training/ using the selected artifact tokenizer/template and materialized corpus lineage, with versioned formatting and no fabricated private chain-of-thought targets.
- Define explicit maximum lengths, special-token handling, sample packing/attention policy and assistant-target loss masking; reject or separately report examples that cannot fit validly.
- Produce an immutable tokenization manifest containing tokenizer/template/config hashes, retained/dropped counts and non-sensitive inspection summaries.

## Acceptance criteria

- Synthetic multi-turn, empty-answer, Unicode, long-source and boundary-token examples have exact expected masks; prompt/system/user tokens and padding do not receive unintended loss.
- No included example silently loses its required answer or crosses split boundaries through packing.
- Reprocessing the same corpus/tokenizer/config reproduces the manifest; inspection summaries do not publish full private examples.

## Validation

- Future authorized checks: deterministic tokenizer/masking/packing fixtures with a tiny local tokenizer under the separate training environment.
- After artifact approval, manually inspect a small stratified token/label sample and record truncation/drop rates before smoke training.

## Out of scope

- An actual optimization run
- Automatic generation of reasoning traces from private model internals
- Silently changing the corpus or selected tokenizer to make examples fit

## Risk and review

Loss-mask/template errors can create a seemingly successful training curve while teaching the wrong objective; inspect labels, not just batch shapes.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
