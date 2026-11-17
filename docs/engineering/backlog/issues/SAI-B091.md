# [SAI-B091] Build an organizer workflow for contest draft, preview and publication

<!-- solver-ai-backlog:SAI-B091 -->
Order: 106 / Priority: P2 / Phase: contest-experience
Area: contest-admin / Suggested role: Full-stack engineer

## Problem

Organizers have no supported interface to prepare a validated contest.

## Prerequisites

- SAI-B081 (publish/complete prerequisite first)
- SAI-B082 (publish/complete prerequisite first)
- SAI-B083 (publish/complete prerequisite first)
- SAI-B085 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- apps/web/app
- apps/web/features
- services/api/solver_api/main.py
- tests/e2e

## Scope

- Create a proposed organizer feature with draft editing, problem ordering, timing and assistance-policy preview.
- Require explicit publication confirmation showing the final immutable rules and validation errors.

## Acceptance criteria

- A participant cannot access organizer mutations even by calling their API directly.
- A draft with missing problem versions or invalid times cannot publish.
- A complete original-problem event can be prepared, previewed and published in an end-to-end test.

## Validation

- npx playwright test tests/e2e/contests/organizer.spec.ts --workers=2
- npm run typecheck

## Out of scope

- New design system
- Bulk third-party problem ingestion

## Risk and review

Administrative forms can expose mutation permissions or conceal critical rules.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
