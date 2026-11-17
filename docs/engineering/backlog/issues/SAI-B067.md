# [SAI-B067] Show a source-hash-bound debugger patch preview with explicit apply

<!-- solver-ai-backlog:SAI-B067 -->
Order: 86 / Priority: P2 / Phase: AI-2 consented tutor and debugger
Area: Debugger editor UX / Suggested role: Frontend editor engineer

Implementation status: planned

## Problem

Model suggestions must not overwrite a learner's newer draft or silently change another problem/language after an asynchronous request.

## Prerequisites

- SAI-B064 (confirm prerequisite state in the catalogue)
- SAI-B066 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- apps/web/features/practice/code-pane.tsx
- apps/web/features/practice/workspace.tsx
- apps/web/features/hints/api.ts
- tests/e2e/practice/practice.spec.ts

## Scope

- Display an inert before/after patch tied to the exact requested source hash.
- Require explicit apply/copy and refuse automatic application if the current draft changed.
- Preserve undo behavior and existing per-problem/language draft isolation.

## Acceptance criteria

- Editing while a request runs causes a visible stale-patch state rather than overwrite.
- Switching account/problem/language cannot apply a prior suggestion.
- Dismiss/apply/copy actions never execute code or submit a job implicitly.

## Validation

- Future authorized check: npm run typecheck; npm run test:e2e -- tests/e2e/practice/practice.spec.ts --workers=1

## Out of scope

- Autonomous editing agents
- Automatic submission of generated code

## Risk and review

Applying a correct-looking diff can still introduce a bug; retain original source and label evidence limits.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
