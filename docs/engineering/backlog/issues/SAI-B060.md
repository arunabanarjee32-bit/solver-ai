# [SAI-B060] Design a bounded tutoring interaction contract beyond hint levels

<!-- solver-ai-backlog:SAI-B060 -->
Order: 79 / Priority: P2 / Phase: AI-2 consented tutor and debugger
Area: Tutor interaction design / Suggested role: Product and AI interface designer

Implementation status: planned

## Problem

The completed hint ladder handles one level at a time; conceptual questions and learner reasoning require a deliberately scoped interaction rather than an unlimited chat box.

## Prerequisites

- SAI-B059 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- docs/product/AI_SOLVER.md
- services/api/solver_api/features/hints/service.py
- apps/web/features/hints/account-hint.tsx

## Scope

- Specify allowed interaction types, role boundaries, spoiler level, maximum turns and public-only task context.
- Separate concise pedagogical explanations from hidden model reasoning.
- Record compatibility with the existing hint endpoint before adding a new contract.

## Acceptance criteria

- Contract includes exact bounds, account ownership and allowed-context rules.
- Each interaction has a measurable completion/refusal/stop outcome.
- The design does not silently turn hint requests into source review or full-solution generation.

## Validation

- Static contract review against existing API/UI and the approved pilot findings; no model calls for this design issue.

## Out of scope

- Unrestricted general-purpose chat
- Replacing authored hints

## Risk and review

An open-ended conversation broadens privacy and cost exposure beyond the successful pilot.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
