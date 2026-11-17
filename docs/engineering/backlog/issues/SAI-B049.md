# [SAI-B049] Enforce account-level entitlement before model-backed hints

<!-- solver-ai-backlog:SAI-B049 -->
Order: 64 / Priority: P1 / Phase: AI-1 controlled model hints
Area: AI admission policy / Suggested role: Backend authorization engineer

Implementation status: planned

## Problem

The hints route authenticates but discards its user ID because authored lookup does not need a model entitlement. Real inference must authorize an account before transport.

## Prerequisites

- SAI-B041 (confirm prerequisite state in the catalogue)
- SAI-B044 (confirm prerequisite state in the catalogue)
- SAI-B014 (confirm prerequisite state in the catalogue)
- SAI-B016 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/api/solver_api/main.py
- services/api/solver_api/features/hints/service.py
- services/api/solver_api/features/identity/verification.py
- services/api/tests/hints/test_hints.py

## Scope

- Carry the verified internal account identifier into an admission layer, never into model context.
- Define a local pilot allowlist/entitlement source and explicit denied/disabled states.
- Keep public authored hints and existing signed-in authored behavior available.

## Acceptance criteria

- Unauthenticated, unentitled and disabled-account requests make zero provider calls.
- Caller-supplied user IDs and forwarding headers cannot change entitlement.
- Allowed/denied decisions are testable independently of transport.

## Validation

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints services/api/tests/identity -q

## Out of scope

- Billing plans
- Changing existing JWT ownership boundaries

## Risk and review

Authentication alone is insufficient authority to consume external resources.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
