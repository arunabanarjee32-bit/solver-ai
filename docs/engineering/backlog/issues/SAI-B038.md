# [SAI-B038] Improve screen-reader announcements and focus for asynchronous results

<!-- solver-ai-backlog:SAI-B038 -->
Order: 39 / Priority: P1 / Phase: 2-useful-practice
Area: accessibility / Suggested role: accessibility/frontend engineer

## Problem

The app uses role=status/alert in places, but there is no reviewed announcement/focus contract across account errors, hint retry, polled verdicts and opened history details. Repeated polling can be noisy or updates can be missed.

## Prerequisites

- SAI-B037 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- apps/web/features/accounts/account-form.tsx
- apps/web/features/hints/account-hint.tsx
- apps/web/features/submissions/submission-panel.tsx
- apps/web/features/submissions/submission-history.tsx
- tests/e2e/hints/hints.spec.ts
- tests/e2e/submissions/submissions.spec.ts

## Scope

- Define concise live-region announcements for meaningful state changes, with stable labels and error associations.
- Preserve logical focus after retries, modal/confirmation actions and detail opening; avoid shifting focus on every poll.
- Add targeted assertions and a manual screen-reader walkthrough for repaired cases.

## Acceptance criteria

- One transition to a final verdict announces once; unchanged polls do not repeat the same message indefinitely.
- Account field/error relationships and hint result provenance are programmatically exposed.
- After retry/detail close or account change, focus remains on a meaningful visible control and stale private result text is removed.

## Validation

- PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e -- tests/e2e/hints/hints.spec.ts tests/e2e/submissions/submissions.spec.ts --workers=2
- Record manual screen-reader/keyboard findings for the affected states, including the tool/version used.

## Out of scope

- Synthesized voice tutoring
- Changing source provenance semantics
- Claiming automated checks replace assistive-technology review

## Risk and review

Over-announcement and forced focus can make a technically labeled UI unusable; test real interaction timing.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
