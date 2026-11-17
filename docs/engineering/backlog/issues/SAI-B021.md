# [SAI-B021] Expose private bounded operational readiness and queue metrics

<!-- solver-ai-backlog:SAI-B021 -->
Order: 22 / Priority: P2 / Phase: 1-safe-pilot
Area: operations / Suggested role: platform/backend engineer

Implementation status: planned

## Problem

Public health only reports process liveness and capabilities report recent worker readiness. Operators lack a private bounded view of queue age, expired leases and storage pressure without inspecting user records.

## Prerequisites

- SAI-B020 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/api/solver_api/main.py
- services/api/solver_api/features/submissions/store.py
- services/api/tests/submissions/test_submissions.py
- services/judge/solver_judge/control/diagnostics.py

## Scope

- Add an operator-only metrics/readiness surface that reuses trusted store state and does not return source, tests, bearer material or high-cardinality identifiers.
- Separate liveness, deployment readiness and worker execution availability so a missing optional local judge is not mislabeled an API crash.
- Document scrape/authentication and metric cardinality bounds; keep public responses minimal.

## Acceptance criteria

- Anonymous/learner credentials cannot read private operational metrics.
- Seeded queued/running/expired fixtures yield exact aggregate counts and oldest-job age, with no source or user IDs.
- Metrics collection remains bounded and unavailable storage produces a safe readiness failure rather than a false healthy state.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/submissions/test_submissions.py services/api/tests/catalog/test_api.py

## Out of scope

- A public admin dashboard
- Accurate aggregate sandbox peak-memory claims
- Installing Prometheus or paid monitoring by default

## Risk and review

Operator endpoints can expose sensitive topology and state; require a separate credential/policy and low-cardinality output.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
