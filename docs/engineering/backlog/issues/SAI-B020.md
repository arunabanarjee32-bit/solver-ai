# [SAI-B020] Add structured redacted request and failure logs

<!-- solver-ai-backlog:SAI-B020 -->
Order: 21 / Priority: P1 / Phase: 1-safe-pilot
Area: operations / Suggested role: platform engineer

## Problem

Request IDs and safe client errors exist, but there is no defined structured operational logging contract. Troubleshooting needs correlation and failure categories without exposing source, tokens or hidden cases.

## Prerequisites

- SAI-B003 (publish/complete prerequisite first)
- SAI-B019 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/main.py
- services/api/solver_api/http/errors.py
- services/judge/solver_judge/control/worker.py
- docs/onboarding/DEVELOPMENT.md

## Scope

- Define structured request/failure fields such as service, generated correlation ID, route template, duration and safe error category.
- Redact or exclude authorization/cookies, raw query values, source, grading inputs, provider context and account identifiers beyond approved pseudonymous correlation.
- Document output format and retention/collection assumptions without provisioning a paid logging service.

## Acceptance criteria

- Fixtures containing marker secrets in headers/body/query produce no marker in log output or exception formatting.
- A failed request can be correlated with its safe response request ID and route template.
- Untrusted multiline input cannot forge a second log record; logging failure does not change a valid API result.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/catalog/test_api.py services/api/tests/submissions/test_submissions.py
- uv run --project services/api --frozen pytest services/judge/tests/control/test_worker.py

## Out of scope

- Persisting all request/response bodies
- Installing a telemetry cluster
- Publishing private source or security diagnostics

## Risk and review

Logs are another data export channel; redaction must be tested before deployment collection is enabled.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
