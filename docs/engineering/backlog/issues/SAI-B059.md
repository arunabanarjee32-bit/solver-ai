# [SAI-B059] Define and execute a small consented model-hint pilot acceptance gate

<!-- solver-ai-backlog:SAI-B059 -->
Order: 74 / Priority: P1 / Phase: AI-1 controlled model hints
Area: Hint quality pilot / Suggested role: Teaching evaluator with project owner

## Problem

Passing adapter fixtures demonstrates integration behavior, not whether generated hints are correct, useful or appropriately limited in spoilers.

## Prerequisites

- SAI-B045 (publish/complete prerequisite first)
- SAI-B050 (publish/complete prerequisite first)
- SAI-B051 (publish/complete prerequisite first)
- SAI-B056 (publish/complete prerequisite first)
- SAI-B057 (publish/complete prerequisite first)
- SAI-B058 (publish/complete prerequisite first)
- SAI-B124 (publish/complete prerequisite first)
- SAI-B126 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

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
