# [SAI-B105] Add a bounded metrics exporter consuming the existing private operational surface

<!-- solver-ai-backlog:SAI-B105 -->
Order: 48 / Priority: P1 / Phase: operated-pilot
Area: operations-observability / Suggested role: Backend engineer and operator

## Problem

Once B021 supplies canonical private queue/readiness measurements, operators need a stable low-cardinality exporter/report adapter without a second metrics authority.

## Prerequisites

- SAI-B021 (publish/complete prerequisite first)
- SAI-B020 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/main.py
- services/api/solver_api/features/submissions/store.py
- services/judge/solver_judge/control/worker.py
- services/api/tests

## Scope

- Consume B021 aggregate measurements through its existing authenticated operator boundary; do not create another queue/readiness endpoint.
- Add a versioned bounded export adapter for outcome/latency histograms and worker health, with an explicitly reviewed scrape/rotation policy.
- Reuse B020 redaction and cardinality rules; keep user/source/token data out of metrics.

## Acceptance criteria

- Exporter fixtures match B021 canonical counters and handle unhealthy/stale input honestly.
- No second metrics endpoint, competing source of truth or unbounded identity labels are introduced.
- Unauthorized scrapes and unavailable source state fail safely without exposing underlying data.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/operations/test_metrics.py
- uv run --project services/api --frozen pytest services/judge/tests/control/test_worker.py

## Out of scope

- Provisioning paid telemetry vendors
- Logging full submissions

## Risk and review

Metrics labels and endpoints can leak private activity or overload storage.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
