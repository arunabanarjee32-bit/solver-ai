# [SAI-B016] Expose owned session listing and revoke-other-sessions controls

<!-- solver-ai-backlog:SAI-B016 -->
Order: 17 / Priority: P2 / Phase: 1-safe-pilot
Area: identity / Suggested role: identity/frontend engineer

Implementation status: planned

## Problem

The account page provides sign-out but no way to inspect or revoke other active sessions. Users cannot react deliberately to an unfamiliar session after an access concern.

## Prerequisites

- SAI-B015 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- apps/web/features/accounts/server.ts
- apps/web/features/accounts/account-form.tsx
- apps/web/features/accounts/client.ts
- apps/web/tests/auth.test.mjs
- tests/e2e/submissions/submissions.spec.ts

## Scope

- Use Better Auth supported session listing/revocation APIs and render a bounded owner-only session list.
- Require recent authentication for revoke-other-sessions and identify the current session without revealing raw session tokens.
- Show the documented limit that previously issued short-lived API tokens may remain usable for their remaining lifetime.

## Acceptance criteria

- Account A cannot list or revoke Account B sessions by supplying another identifier.
- Revoking another session makes that cookie fail while the chosen current session remains usable.
- Session token values never appear in DOM, API snapshots, logs or exports, and stale list responses are cleared on account change.

## Validation

- node --test apps/web/tests/auth.test.mjs
- PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e -- tests/e2e/submissions/submissions.spec.ts --workers=2

## Out of scope

- Fingerprint-based identity or precise location tracking
- Changing JWT revocation architecture
- Automatically rotating real credentials

## Risk and review

Session metadata is sensitive, and stale browser state must not cross identities.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
