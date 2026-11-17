# [SAI-B006] Reject plaintext external identity and worker transport configuration

<!-- solver-ai-backlog:SAI-B006 -->
Order: 7 / Priority: P1 / Phase: 1-safe-pilot
Area: deployment-security / Suggested role: backend security engineer

## Problem

AUTH_JWKS_URL currently permits HTTP for any hostname. Local loopback/Compose routes need support, but the same permissive configuration can be unsafe across an untrusted network.

## Prerequisites

- SAI-B003 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/features/identity/verification.py
- services/api/solver_api/main.py
- services/judge/solver_judge/control/worker.py
- compose.yaml
- docs/onboarding/DEVELOPMENT.md

## Scope

- Define an explicit local/trusted-private transport policy and reject external plaintext JWKS, issuer and worker API routes by default.
- Validate origins, credentials, fragments and configured destinations once at startup with safe error messages.
- Keep documented loopback and explicitly selected private Compose development routes usable without disabling TLS validation.

## Acceptance criteria

- Configuration fixtures accept supported local routes and HTTPS external routes, and reject a public HTTP hostname, embedded credentials and malformed origins.
- A denied configuration fails startup before accepting authenticated traffic; no URL credentials appear in errors.
- Existing fixed-destination, no-redirect JWKS behavior and worker credential separation remain intact.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/identity/test_auth.py
- uv run --project services/api --frozen pytest services/judge/tests/control/test_worker.py

## Out of scope

- Purchasing certificates or deploying publicly
- User-selected provider destinations
- Disabling proxy/CA trust

## Risk and review

A broad private-network exception would recreate the gap; explicit development exemptions need owner-reviewed scope.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
