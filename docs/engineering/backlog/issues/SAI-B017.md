# [SAI-B017] Record privacy-safe account security events

<!-- solver-ai-backlog:SAI-B017 -->
Order: 18 / Priority: P2 / Phase: 1-safe-pilot
Area: identity-observability / Suggested role: identity engineer and privacy reviewer

Implementation status: planned

## Problem

The project has no owner-facing security activity history for password recovery, session revocation or account administration. Operators and users need limited evidence without storing credentials or excessive personal data.

## Prerequisites

- SAI-B003 (confirm prerequisite state in the catalogue)
- SAI-B016 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- apps/web/features/accounts/server.ts
- apps/web/features/accounts/account-form.tsx
- apps/web/tests/auth.test.mjs
- docs/governance/DATA_AND_LICENSES.md

## Scope

- Define a small versioned security-event vocabulary and retention policy for completed recovery/session actions.
- Record only approved metadata and expose a bounded owner-only activity list through supported account hooks.
- Avoid raw token, password, mail-link, full IP or user-agent logging unless separately justified and approved.

## Acceptance criteria

- Fixtures produce exactly the intended event for reset/revocation success and distinguish failure without storing secret input.
- A second user cannot query another account activity, and pagination/retention bounds are enforced.
- The privacy document names stored fields and retention; event ingestion cannot be used for arbitrary log injection.

## Validation

- node --test apps/web/tests/auth.test.mjs

## Out of scope

- A general SIEM or analytics platform
- Indefinite IP/device tracking
- Claiming activity logs identify an attacker

## Risk and review

Additional audit data creates privacy and storage obligations; collect the smallest useful record.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
