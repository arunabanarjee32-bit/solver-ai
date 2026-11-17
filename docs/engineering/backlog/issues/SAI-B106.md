# [SAI-B106] Propagate redacted correlation identifiers across accepted jobs

<!-- solver-ai-backlog:SAI-B106 -->
Order: 49 / Priority: P2 / Phase: operated-pilot
Area: operations-observability / Suggested role: Backend engineer

## Problem

Request-level diagnostics are difficult to connect to leased jobs and worker completion safely.

## Prerequisites

- SAI-B105 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)
- SAI-B020 (publish/complete prerequisite first)
- SAI-B027 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/main.py
- services/api/solver_api/features/submissions/store.py
- services/judge/solver_judge/control/worker.py
- services/api/tests

## Scope

- Carry B020 existing server-generated request correlation ID into accepted job, worker lease and sanitized completion lineage.
- Validate length/format and use bounded diagnostics; identifiers remain telemetry and cannot grant ownership or select hidden tests.
- Reuse the existing log/telemetry schema instead of creating another request-ID authority.

## Acceptance criteria

- A request/job/worker fixture can be followed by one correlation identifier without including source or credentials.
- Malformed and oversized supplied identifiers cannot inject log lines or labels.
- Lease retries retain the intended job lineage while attempts remain distinguishable.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/operations/test_correlation.py
- uv run --project services/api --frozen pytest services/judge/tests/control/test_worker.py

## Out of scope

- A distributed tracing vendor deployment
- Publishing internal identifiers in unrestricted public analytics

## Risk and review

Improper correlation data can become an injection or cross-user tracking vector.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
