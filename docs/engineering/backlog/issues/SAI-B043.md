# [SAI-B043] Validate trusted provider destinations and secret configuration

<!-- solver-ai-backlog:SAI-B043 -->
Order: 58 / Priority: P1 / Phase: AI-1 controlled model hints
Area: Provider configuration / Suggested role: Backend security engineer

## Problem

The authored-only selector intentionally fails closed. A future provider must not inherit archive adapters that accept arbitrary endpoints or ambiguous environment state.

## Prerequisites

- SAI-B041 (publish/complete prerequisite first)
- SAI-B006 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/features/hints/service.py
- services/api/tests/hints/test_hints.py
- docs/onboarding/DEVELOPMENT.md

## Scope

- Define administrator-controlled HTTPS destination/model settings with strict URL parsing and an explicit local-development exception policy.
- Reject URL userinfo, unexpected redirects and request-supplied endpoint overrides.
- Validate credential presence without logging values; keep authored as the default.

## Acceptance criteria

- Malformed, unapproved and insecure external destinations fail before transport.
- Missing credentials produce a sanitized configuration failure.
- No browser bundle, OpenAPI example or log contains credential values.

## Validation

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q

## Out of scope

- Collecting credentials in chat
- Changing network policy automatically

## Risk and review

Provider configuration can become an SSRF or credential-forwarding boundary if endpoint control leaks to callers.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
