# [SAI-B059] Define and execute a small consented model-hint pilot acceptance gate

<!-- solver-ai-backlog:SAI-B059 -->
Order: 74 / Priority: P1 / Phase: AI-1 controlled model hints
Area: Hint quality pilot / Suggested role: Teaching evaluator with project owner

Implementation status: planned

## Problem

Passing adapter fixtures demonstrates integration behavior, not whether generated hints are correct, useful or appropriately limited in spoilers.

## Prerequisites

- SAI-B045 (confirm prerequisite state in the catalogue)
- SAI-B050 (confirm prerequisite state in the catalogue)
- SAI-B051 (confirm prerequisite state in the catalogue)
- SAI-B056 (confirm prerequisite state in the catalogue)
- SAI-B057 (confirm prerequisite state in the catalogue)
- SAI-B058 (confirm prerequisite state in the catalogue)
- SAI-B124 (confirm prerequisite state in the catalogue)
- SAI-B126 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- docs/product/AI_SOLVER.md
- docs/status/PROJECT_STATUS.md
- docs/research/MODEL_DATA_EVALUATION.md
- services/api/tests/hints/test_hints.py

## Scope

- Choose a small original/permissioned task set with human-reviewed level rubrics.
- Record an explicit owner-approved call/spend ceiling before any live pilot.
- Report usefulness, factual mistakes, spoilers, refusal/outage outcomes and negative results separately.

## Acceptance criteria

- Every evaluated hint records task/context/prompt/model versions and its rubric outcome.
- Pilot costs stay inside the approved cap; no live calls run without that approval.
- Activation recommendation cites failures and sample size rather than claiming general learning improvement.

## Validation

- Future authorized evaluation: run the documented bounded pilot only after owner approval; review fixture suite and publish a redacted result manifest.

## Out of scope

- Unbounded benchmark sweeps
- Claims of causal educational benefit from a small observational pilot

## Risk and review

A provider working on three seed problems is not evidence of broad tutoring quality.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
