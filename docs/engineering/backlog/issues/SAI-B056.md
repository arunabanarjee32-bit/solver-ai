# [SAI-B056] Require clear external-AI disclosure before opt-in hint requests

<!-- solver-ai-backlog:SAI-B056 -->
Order: 71 / Priority: P1 / Phase: AI-1 controlled model hints
Area: AI privacy UX / Suggested role: Product privacy and frontend engineer

## Problem

The completed UI accurately advertises authored hints. Introducing external generation changes where context is processed and requires an honest, explicit choice.

## Prerequisites

- SAI-B041 (publish/complete prerequisite first)
- SAI-B049 (publish/complete prerequisite first)
- SAI-B053 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- apps/web/features/hints/account-hint.tsx
- apps/web/features/hints/api.ts
- services/api/solver_api/features/hints/service.py
- docs/governance/DATA_AND_LICENSES.md
- tests/e2e/hints/hints.spec.ts

## Scope

- Expose trusted capability/disclosure information without provider credentials or editable destinations.
- Explain the exact public context sent, retention policy and optional nature of model help.
- Record the accepted disclosure version for model admission while leaving authored hints accessible.

## Acceptance criteria

- No external generation occurs before the required explicit choice.
- Switching back to authored mode removes model provenance claims.
- UI and API agree on the disclosure version; stale/absent consent blocks model requests.

## Validation

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q; npm run test:e2e -- tests/e2e/hints/hints.spec.ts --workers=1

## Out of scope

- Consent to training on private submissions
- Uploading editor drafts

## Risk and review

A blanket consent checkbox cannot authorize unspecified future source sharing.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
