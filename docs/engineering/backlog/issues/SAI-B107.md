# [SAI-B107] Define measurable service objectives and test operator alert rules

<!-- solver-ai-backlog:SAI-B107 -->
Order: 50 / Priority: P1 / Phase: operated-pilot
Area: operations-observability / Suggested role: Site reliability engineer and service owner

Implementation status: planned

## Problem

A working local service does not define when operators should treat a deployment as degraded.

## Prerequisites

- SAI-B105 (confirm prerequisite state in the catalogue)
- SAI-B106 (confirm prerequisite state in the catalogue)
- SAI-B003 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- docs/onboarding/DEVELOPMENT.md
- docs/security/JUDGE_SECURITY.md
- scripts/verification
- services/api/tests

## Scope

- Add proposed configuration/runbook rules for queue delay, stale workers, job-control failures and API error rate.
- Create deterministic metric fixtures to exercise alert activation and recovery, with owner-selected thresholds.

## Acceptance criteria

- Each rule has an owner, observation window and tested firing/recovery fixture.
- Expected learner WA/CE/RE outcomes do not count as application incidents.
- A worker-readiness failure prevents an operator from declaring execution healthy.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/operations/test_alert_rules.py
- python3 scripts/verification/repository_inventory.py --help

## Out of scope

- Invented production uptime claims
- Unapproved external paging or paid monitoring

## Risk and review

Noisy alerts can hide actual incidents; broad thresholds can miss failures.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
