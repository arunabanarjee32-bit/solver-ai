# [SAI-B035] Detect cross-tab draft conflicts before overwriting newer code

<!-- solver-ai-backlog:SAI-B035 -->
Order: 36 / Priority: P2 / Phase: 2-useful-practice
Area: editor-reliability / Suggested role: frontend editor engineer

Implementation status: planned

## Problem

Two tabs editing the same local draft overwrite one storage key without revision metadata or a conflict warning. A stale tab can silently replace more recent code.

## Prerequisites

- SAI-B034 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- apps/web/features/practice/code-pane.tsx
- tests/e2e/practice/practice.spec.ts

## Scope

- Record a small local draft revision/timestamp envelope with a migration path for plain v1 text.
- Observe storage events for the active namespace and show a non-destructive conflict choice when another tab changes the saved revision.
- Keep each unsaved in-memory value available for copying/export before choosing one version.

## Acceptance criteria

- Two-tab fixtures trigger a conflict notice instead of silently overwriting a newer saved revision.
- Choosing keep-local, load-other or cancel has deterministic storage/editor outcomes and preserves an exportable losing version until explicit resolution.
- Different problem/language/account namespaces do not trigger conflicts, and storage-unavailable fallback still permits editing.

## Validation

- PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e -- tests/e2e/practice/practice.spec.ts --workers=2

## Out of scope

- Real-time collaboration or CRDT infrastructure
- Server draft persistence
- Pretending timestamps provide distributed conflict-free correctness

## Risk and review

Migration must not mistake existing source text for malformed metadata or discard unsaved code.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
