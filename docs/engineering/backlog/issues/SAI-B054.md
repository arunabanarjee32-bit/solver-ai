# [SAI-B054] Propagate total generation deadlines and explicit cancellation states

<!-- solver-ai-backlog:SAI-B054 -->
Order: 69 / Priority: P1 / Phase: AI-1 controlled model hints
Area: AI cancellation and deadlines / Suggested role: Full-stack AI integration engineer

## Problem

Authored hints use a three-second server bound and the client already cancels requests, but real provider transport and quota settlement need a total lifecycle contract.

## Prerequisites

- SAI-B048 (publish/complete prerequisite first)
- SAI-B050 (publish/complete prerequisite first)
- SAI-B053 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/features/hints/service.py
- apps/web/features/hints/api.ts
- apps/web/features/hints/account-hint.tsx
- services/api/tests/hints/test_hints.py
- tests/e2e/hints/hints.spec.ts

## Scope

- Define bounded server generation, transport cleanup and caller-abandonment states.
- Propagate cancellation to async transport and reconcile reservations conservatively.
- Preserve the existing UI cancellation/stale-result protection; avoid claiming upstream billing stopped without evidence.

## Acceptance criteria

- Slow-chunk fixtures cannot exceed the total configured deadline.
- Cancel/level-change/account-change never renders a stale result.
- Interrupted requests have exactly one documented settlement outcome.

## Validation

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q; npm run test:e2e -- tests/e2e/hints/hints.spec.ts --workers=1

## Out of scope

- Unlimited timeout increases
- Guaranteeing remote provider cancellation

## Risk and review

Local cancellation and remote resource consumption can diverge.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
