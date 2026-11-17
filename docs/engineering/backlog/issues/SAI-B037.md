# [SAI-B037] Complete keyboard navigation for the practice and submission workflow

<!-- solver-ai-backlog:SAI-B037 -->
Order: 38 / Priority: P1 / Phase: 2-useful-practice
Area: accessibility / Suggested role: accessibility/frontend engineer

## Problem

Basic keyboard support exists, but there is no complete documented keyboard-only path through navigation, problem reading, editor entry/exit, language selection, hints and deliberate submission.

## Prerequisites

- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- apps/web/components/shell.tsx
- apps/web/features/practice/workspace.tsx
- apps/web/features/practice/code-pane.tsx
- apps/web/features/submissions/submission-panel.tsx
- tests/e2e/practice/practice.spec.ts

## Scope

- Audit the existing flow with a keyboard and repair concrete focus-order, editor-escape and visible-focus gaps.
- Add a skip-to-main/editor guidance path without trapping Tab inside Monaco or inventing mandatory shortcuts.
- Document supported editor behavior and add focused browser assertions for repaired gaps.

## Acceptance criteria

- A keyboard-only fixture reaches and operates catalog, problem, editor, language and Run/Submit controls without pointer input.
- Users can leave both Monaco and simple editor through a documented accessible mechanism; focus is never trapped.
- Disabled/loading/retry controls expose state and visible focus remains discernible in supported themes.

## Validation

- PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e -- tests/e2e/practice/practice.spec.ts tests/e2e/submissions/submissions.spec.ts --workers=2
- Record a manual keyboard pass for the exact changed workflow; do not claim full WCAG conformance.

## Out of scope

- Replacing Monaco solely for aesthetics
- A full accessibility certification
- Changing judging or authentication rules

## Risk and review

Automation cannot establish all editor assistive-technology behavior; include an actual manual pass and limitations.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
