# [SAI-B019] Bound general API admission and concurrent slow requests

<!-- solver-ai-backlog:SAI-B019 -->
Order: 20 / Priority: P1 / Phase: 1-safe-pilot
Area: ingress-security / Suggested role: API/platform engineer

Implementation status: planned

## Problem

The current 128 KiB body and per-operation deadline do not bound simultaneous callers or whole-process request admission. Submission quotas alone cannot prevent general ingress exhaustion.

## Prerequisites

- SAI-B003 (confirm prerequisite state in the catalogue)
- SAI-B006 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/api/solver_api/main.py
- services/api/solver_api/http/body_limit.py
- services/api/tests/catalog/test_api.py
- compose.yaml
- docs/security/JUDGE_SECURITY.md

## Scope

- Add a configurable bounded admission/concurrency policy appropriate to the existing single-process pilot, with clear limitations for multiple replicas.
- Ensure slow bodies and slow auth requests release capacity on cancellation/timeouts.
- Use safe overload responses and explicit retry information; preserve separate internal-worker capacity or a documented isolation policy.

## Acceptance criteria

- A deterministic concurrent-request fixture reaches the configured cap and receives bounded overload responses rather than unbounded work.
- Cancelled and timed-out requests release permits; the next legitimate request succeeds.
- Worker control traffic cannot be starved indefinitely by public catalog requests, and overload output includes no request body or credential.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/catalog/test_api.py services/api/tests/identity/test_auth.py

## Out of scope

- A distributed DDoS service
- Changing sandbox limits
- Using caller-supplied identities as trusted rate-limit keys

## Risk and review

An in-process cap is not a global multi-replica budget; document deployment scope and avoid self-deadlock on internal work.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
