# [SAI-B014] Add a testable email-verification delivery flow for pilot accounts

<!-- solver-ai-backlog:SAI-B014 -->
Order: 15 / Priority: P1 / Phase: 1-safe-pilot
Area: identity / Suggested role: identity engineer

Implementation status: planned

## Problem

Local email/password accounts do not verify email ownership. A real-user pilot needs a deliberate verification policy before relying on an email address for identity or recovery.

## Prerequisites

- SAI-B003 (confirm prerequisite state in the catalogue)
- SAI-B011 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- apps/web/features/accounts/server.ts
- apps/web/features/accounts/account-form.tsx
- apps/web/tests/auth.test.mjs
- tests/e2e/submissions/submissions.spec.ts
- docs/onboarding/DEVELOPMENT.md

## Scope

- Use Better Auth supported verification hooks with a delivery adapter and local deterministic outbox fixture.
- Implement pending, resend, expired-link and verified UI states without confirming whether arbitrary addresses are registered.
- Keep delivery disabled or local-only until the owner supplies an approved provider/configuration; no paid call by default.

## Acceptance criteria

- A fresh token verifies only its intended address once; expired/reused/mismatched tokens fail safely.
- Resend is bounded and response wording does not enumerate accounts.
- Verified-email requirements follow the approved pilot policy and do not silently lock out existing local development users.

## Validation

- node --test apps/web/tests/auth.test.mjs
- PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e -- tests/e2e/submissions/submissions.spec.ts --workers=2

## Out of scope

- Selecting or purchasing a mail provider without approval
- Implementing custom email-token cryptography
- Sending real verification messages during tests

## Risk and review

Mail links and logs can leak account tokens; use fixture delivery and library-supported semantics.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
