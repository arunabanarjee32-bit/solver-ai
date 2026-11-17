# [SAI-B031] Use bounded server-side pagination for the expanding problem catalog

<!-- solver-ai-backlog:SAI-B031 -->
Order: 32 / Priority: P2 / Phase: 2-useful-practice
Area: catalog / Suggested role: frontend/API engineer

Implementation status: planned

## Problem

The UI currently fetches limit=100 once and filters that page locally. Once the catalog exceeds the first page, learners could miss matching problems while totals imply a larger searchable collection.

## Prerequisites

- SAI-B029 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- apps/web/features/practice/catalog.tsx
- apps/web/features/practice/api.ts
- services/api/solver_api/main.py
- services/api/tests/catalog/test_api.py
- tests/e2e/practice/practice.spec.ts

## Scope

- Drive bounded q/difficulty/tag/limit/offset requests through the existing catalog API instead of pretending the first 100 entries are the whole library.
- Add deliberate pagination/loading/empty states, cancel stale searches and reset offset when filters change.
- Retain the simple existing API store and avoid adding search infrastructure.

## Acceptance criteria

- A fixture with more than 100 problems finds a matching item beyond the original first page.
- Rapid filter changes cannot render stale results or retain an out-of-range offset.
- Displayed totals, page boundaries and empty results match API semantics; keyboard access and existing retry behavior remain usable.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/catalog/test_api.py
- PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e -- tests/e2e/practice/practice.spec.ts tests/e2e/practice/resilience.spec.ts --workers=2

## Out of scope

- Meilisearch or a database migration
- Unbounded client fetching of the entire catalog
- Personalized recommendations

## Risk and review

Stale network responses and partial-page filtering can create misleading results; retain strict schemas and cancellation.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
