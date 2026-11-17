# [SAI-B034] Offer explicit draft ownership and clear-on-shared-device controls

<!-- solver-ai-backlog:SAI-B034 -->
Order: 35 / Priority: P2 / Phase: 2-useful-practice
Area: editor-privacy / Suggested role: frontend engineer and privacy reviewer

## Problem

The current draft key is scoped by browser/problem/language, not by signed-in account. The disclosure is honest, but shared-device users have no deliberate account-scoping or local-clear workflow.

## Prerequisites

- SAI-B003 (publish/complete prerequisite first)
- SAI-B033 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- apps/web/features/practice/code-pane.tsx
- apps/web/features/accounts/account-form.tsx
- apps/web/features/practice/workspace.tsx
- tests/e2e/practice/practice.spec.ts
- tests/e2e/submissions/submissions.spec.ts

## Scope

- Define separate guest and signed-in local namespaces without treating localStorage as encrypted account backup.
- Offer explicit export/keep/move choices for existing guest drafts and a bounded clear-local-drafts control.
- Never silently upload drafts or erase another browser identity on sign-out; explain shared-device behavior.

## Acceptance criteria

- Switching A to B cannot silently display A private draft under B namespace.
- Existing v1 guest drafts remain recoverable until the user chooses migration or deletion; cancelled prompts preserve bytes.
- Clear-local-drafts affects only the selected namespace and explicit confirmation; no server source is deleted or uploaded.

## Validation

- PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e -- tests/e2e/practice/practice.spec.ts tests/e2e/submissions/submissions.spec.ts --workers=2

## Out of scope

- Claiming browser storage is encrypted or secure against local device access
- Automatic cloud synchronization
- Silent deletion on logout

## Risk and review

Local identity migration can lose code or cross account boundaries; migration must be reversible through explicit export.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
