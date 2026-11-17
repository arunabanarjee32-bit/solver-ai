# [SAI-B032] Make catalog filters and page position shareable through the URL

<!-- solver-ai-backlog:SAI-B032 -->
Order: 33 / Priority: P2 / Phase: 2-useful-practice
Area: catalog-ux / Suggested role: frontend engineer

Implementation status: planned

## Problem

Search, difficulty and topic exist only in component state. Refresh, browser navigation and shared links lose the chosen practice view.

## Prerequisites

- SAI-B031 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- apps/web/features/practice/catalog.tsx
- apps/web/app/page.tsx
- tests/e2e/practice/practice.spec.ts

## Scope

- Map supported filter/page values to validated query parameters and restore them on initial navigation.
- Update browser history intentionally without placing sensitive data in the URL.
- Normalize unknown/overlong values and provide an accessible clear-filters action that resets the URL and pagination together.

## Acceptance criteria

- A copied filtered URL restores the same API query and visible result set after reload.
- Back/forward navigation restores the previous valid filter state without duplicate stale fetches.
- Invalid or overlong parameters are normalized safely, and no source, token or account ID enters the URL.

## Validation

- PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e -- tests/e2e/practice/practice.spec.ts --workers=2

## Out of scope

- Saving private learner profiles
- A new routing framework
- Analytics tracking parameters

## Risk and review

URL state must be bounded and must not introduce navigation loops or expose private drafts.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
