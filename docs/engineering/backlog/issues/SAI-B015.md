# [SAI-B015] Implement password recovery with bounded single-use reset links

<!-- solver-ai-backlog:SAI-B015 -->
Order: 16 / Priority: P1 / Phase: 1-safe-pilot
Area: identity / Suggested role: identity engineer

Implementation status: planned

## Problem

There is no delivered account recovery flow. Users who lose a password cannot safely recover a pilot account through the current interface.

## Prerequisites

- SAI-B014 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- apps/web/features/accounts/server.ts
- apps/web/features/accounts/account-form.tsx
- apps/web/tests/auth.test.mjs
- tests/e2e/submissions/submissions.spec.ts

## Scope

- Use supported Better Auth reset hooks and the verified delivery abstraction from B014.
- Add request/reset views with neutral account-existence wording, resend limits and explicit expired-link behavior.
- Apply the approved session invalidation policy on reset and disclose the existing short-lived API-token window unless separately changed.

## Acceptance criteria

- A valid reset link changes the intended account password once; used/expired links cannot be replayed.
- Reset requests for absent/present addresses have indistinguishable public response structure.
- The old password fails after reset; session behavior matches the documented policy, and no reset token is logged or persisted in browser storage.

## Validation

- node --test apps/web/tests/auth.test.mjs
- PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e -- tests/e2e/submissions/submissions.spec.ts --workers=2

## Out of scope

- Custom password/token cryptography
- Guaranteeing immediate revocation of already issued stateless API JWTs without an explicit design
- Real email delivery in CI

## Risk and review

Enumeration and reset-link leakage can turn recovery into account takeover; use official library flows and adversarial fixtures.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
