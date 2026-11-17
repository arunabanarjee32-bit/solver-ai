# [SAI-B011] Introduce an explicit trusted-ingress identity throttle policy

<!-- solver-ai-backlog:SAI-B011 -->
Order: 12 / Priority: P1 / Phase: 1-safe-pilot
Area: identity / Suggested role: identity/platform engineer

Implementation status: planned

## Problem

Local auth deliberately uses shared per-path buckets because no trusted ingress is configured. This prevents spoofed forwarding bypasses but is not suitable as a complete public per-client abuse policy.

## Prerequisites

- SAI-B003 (confirm prerequisite state in the catalogue)
- SAI-B006 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- apps/web/features/accounts/server.ts
- apps/web/tests/auth.test.mjs
- compose.yaml
- docs/onboarding/DEVELOPMENT.md

## Scope

- Add a disabled-by-default trusted-proxy/header configuration tied to an explicit ingress deployment contract.
- Retain the current safe shared-bucket fallback for direct local access and reject ambiguous forwarding configurations.
- Exercise the same Better Auth sign-in/sign-up rules through trusted and untrusted request fixtures.

## Acceptance criteria

- Spoofed X-Forwarded-For from an untrusted direct caller cannot obtain a new throttle identity.
- A request from the configured trusted ingress resolves only the reviewed client-address field and cannot append arbitrary hops.
- Independent legitimate clients do not all share the same public deployment throttle bucket, while local safe defaults remain unchanged.

## Validation

- node --test apps/web/tests/auth.test.mjs

## Out of scope

- Assuming any forwarding header is trustworthy
- Changing password requirements
- Purchasing an ingress service

## Risk and review

Trusting client-controlled IP headers weakens existing defenses; proxy provenance must be enforced, not inferred from a header name.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
