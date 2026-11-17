# [SAI-B007] Add a total JWKS fetch deadline with real transport fixtures

<!-- solver-ai-backlog:SAI-B007 -->
Order: 8 / Priority: P1 / Phase: 1-safe-pilot
Area: identity / Suggested role: backend identity engineer

Implementation status: planned

## Problem

JWKS refresh uses HTTPX operation timeouts and a size cap but has no outer elapsed-time bound. A slow stream can hold authentication refresh longer than the nominal five-second timeout; most existing tests stub the fetch function.

## Prerequisites

- SAI-B006 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/api/solver_api/features/identity/verification.py
- services/api/tests/identity/test_auth.py

## Scope

- Wrap the full JWKS transfer and decoding path in an explicit total deadline with a monotonic/async cancellation mechanism.
- Add HTTPX transport fixtures for slow chunks, redirects, oversized/incorrect Content-Length, invalid JSON and cancellation.
- Preserve refresh cooldown, cache locking, fixed algorithms and safe unavailable-versus-unauthorized responses.

## Acceptance criteria

- A slow trickle terminates at the configured total deadline rather than extending on every chunk.
- Redirects and bodies above 65,536 bytes are rejected, including missing/false length headers.
- Concurrent refresh requests do not create unbounded fetches and valid cached-key behavior remains covered.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/identity/test_auth.py

## Out of scope

- Changing JWT algorithms or trusting token-supplied key URLs
- Adding a second identity authority
- Live calls to arbitrary JWKS hosts in tests

## Risk and review

Cancellation and cache-state changes can accidentally deny all users or accept stale keys; fixtures must exercise both failure and recovery.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
