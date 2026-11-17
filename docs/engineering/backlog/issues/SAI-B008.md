# [SAI-B008] Describe protected endpoints with an accurate OpenAPI bearer scheme

<!-- solver-ai-backlog:SAI-B008 -->
Order: 9 / Priority: P2 / Phase: 1-safe-pilot
Area: api-contract / Suggested role: API engineer

Implementation status: planned

## Problem

Manual bearer parsing enforces authentication but does not expose a usable security scheme in interactive API docs. A docs-only scheme must not relax duplicate-header or strict signature checks.

## Prerequisites

- SAI-B007 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/api/solver_api/main.py
- services/api/solver_api/features/identity/verification.py
- services/api/tests/catalog/test_api.py
- services/api/tests/identity/test_auth.py

## Scope

- Declare bearer security metadata for protected learner endpoints while retaining require_user as the authorization authority.
- Keep public catalog/health endpoints public and worker-only routes visibly separate from learner token authentication.
- Extend schema assertions to verify correct security declarations, not merely path presence.

## Acceptance criteria

- OpenAPI contains one documented learner bearer scheme and protected submission/hint endpoints reference it.
- Public catalog endpoints do not advertise a mandatory bearer token.
- Duplicate authorization headers, wrong issuer/audience/algorithm and token-supplied URLs still fail exactly as before.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/catalog/test_api.py services/api/tests/identity/test_auth.py

## Out of scope

- Changing authentication semantics
- Exposing worker credentials through Swagger
- Adding a new API-key login mechanism

## Risk and review

Convenience helpers can mask duplicate headers or bypass the existing verifier; the security dependency must remain authoritative.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
