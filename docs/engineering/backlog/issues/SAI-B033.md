# [SAI-B033] Add explicit local draft export and bounded import

<!-- solver-ai-backlog:SAI-B033 -->
Order: 34 / Priority: P2 / Phase: 2-useful-practice
Area: editor / Suggested role: frontend editor engineer

## Problem

Drafts are best-effort browser storage and learners are told to copy their code, but there is no deliberate portable download/import path when storage fails or a browser is replaced.

## Prerequisites

- SAI-B003 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- apps/web/features/practice/code-pane.tsx
- apps/web/features/practice/workspace.tsx
- tests/e2e/practice/practice.spec.ts

## Scope

- Add user-initiated source download with clear problem/language file naming.
- Add a bounded plain-text import flow with preview and explicit replace confirmation; do not execute or upload imported content.
- Preserve the current Monaco/simple-editor and storage-failure behavior.

## Acceptance criteria

- Exported UTF-8 bytes match the selected draft exactly, including non-ASCII text and trailing newline.
- An oversized or unsupported import is rejected before changing the draft; cancel preserves the original bytes.
- Import/export work in the simple-editor fallback and cause no submission, model request or external network call.

## Validation

- PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e -- tests/e2e/practice/practice.spec.ts --workers=2

## Out of scope

- Cloud draft sync
- Archive extraction in the browser
- Automatic code execution after import

## Risk and review

Import is a destructive edit and export may contain private source; require explicit user intent and bounded text handling.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
