# [SAI-B036] Add persistent editor display and accessibility preferences

<!-- solver-ai-backlog:SAI-B036 -->
Order: 37 / Priority: P3 / Phase: 2-useful-practice
Area: editor-ux / Suggested role: frontend editor engineer

Implementation status: planned

## Problem

The editor exposes basic mode/reset controls but no deliberate learner control over font size, wrapping or preferred simple-editor mode. These choices affect readability and keyboard accessibility.

## Prerequisites

- SAI-B033 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- apps/web/features/practice/code-pane.tsx
- apps/web/features/practice/workspace.tsx
- apps/web/app/globals.css
- tests/e2e/practice/practice.spec.ts

## Scope

- Add a small bounded preference model for font size, wrapping and editor mode using local non-sensitive storage.
- Apply compatible behavior to Monaco and the simple editor, with a reset-to-default action.
- Keep preferences separate from source drafts and handle unavailable/malformed storage safely.

## Acceptance criteria

- Preferences survive reload and apply consistently without changing source bytes or submission language.
- Out-of-range/malformed saved preferences fall back to supported defaults.
- Controls have accessible names, keyboard operation and usable focus; choosing simple mode does not repeatedly force Monaco back.

## Validation

- PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e -- tests/e2e/practice/practice.spec.ts --workers=2

## Out of scope

- A full design-system replacement
- Cloud preference profiles
- Changing compiler/runtime settings

## Risk and review

Preference initialization can race draft hydration; source must remain unchanged.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
