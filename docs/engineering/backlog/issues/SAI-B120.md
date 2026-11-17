# [SAI-B120] Extend existing pilot grants with expiring institutional scopes

<!-- solver-ai-backlog:SAI-B120 -->
Order: 123 / Priority: P2 / Phase: institutional-pilot
Area: business-release / Suggested role: Backend engineer and project owner

## Problem

A limited pilot needs enforceable access grants and a recorded go/no-go decision before any commercial expansion.

## Prerequisites

- SAI-B110 (publish/complete prerequisite first)
- SAI-B112 (publish/complete prerequisite first)
- SAI-B117 (publish/complete prerequisite first)
- SAI-B119 (publish/complete prerequisite first)
- SAI-B049 (publish/complete prerequisite first)
- SAI-B003 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)
- SAI-B050 (publish/complete prerequisite first)
- SAI-B051 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/features/identity
- services/api/solver_api/main.py
- apps/web/features/accounts
- docs/product/ROADMAP.md
- services/api/tests

## Scope

- Extend B049 admission authority with owner-approved institutional scope, expiry and revocation; do not add a parallel entitlement or budget ledger.
- Use B117 sponsorship/data-use boundaries and B119 resource reports to decide an explicitly approved pilot envelope.
- Make revocation stop new admission while documenting bounded treatment of in-flight authorized jobs.
- Reuse B050/B051 reservations and spend limits for institutional grants; no parallel accounting store.

## Acceptance criteria

- Expired/revoked grants cannot access the gated workflow; existing ordinary practice remains available.
- A grant cannot override contest assistance rules, ownership boundaries or hard execution/model budgets.
- The release record lists the tested revision, approved audience/capacity, unresolved risks and accountable owner.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/institutions/test_pilot_entitlements.py
- npx playwright test tests/e2e/institutions/pilot-access.spec.ts --workers=2

## Out of scope

- Automatic charging or creating paid subscriptions
- Declaring public production readiness from the existence of a grant

## Risk and review

A commercial access flag must not become a bypass for safety or privacy policy.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
