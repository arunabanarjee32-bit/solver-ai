# [SAI-B045] Version bounded hint prompts and spoiler policies

<!-- solver-ai-backlog:SAI-B045 -->
Order: 60 / Priority: P1 / Phase: AI-1 controlled model hints
Area: Tutoring prompts / Suggested role: AI engineer and teaching reviewer

## Problem

The three authored levels have clear meaning; a model integration needs repeatable templates that preserve that progression instead of exposing full solutions by default.

## Prerequisites

- SAI-B042 (publish/complete prerequisite first)
- SAI-B044 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/features/hints/service.py
- docs/product/AI_SOLVER.md
- services/api/tests/hints/test_hints.py

## Scope

- Define versioned concept/observation/plan templates and a minimal response format.
- Treat problem text as quoted task data with no authority over permissions or tools.
- Record prompt version with internal run metadata without requesting or storing hidden chain-of-thought.

## Acceptance criteria

- Each level has a reviewed allowed-content rubric and output limit.
- Prompt-injection fixtures cannot add tools, destinations or private context.
- Template changes alter a recorded version/fingerprint and keep authored content untouched.

## Validation

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q; human review of level rubrics.

## Out of scope

- Claiming prompts guarantee compliance
- Copying archive prompts wholesale

## Risk and review

A model may still overshare; prompt instructions require output review and product policy.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
