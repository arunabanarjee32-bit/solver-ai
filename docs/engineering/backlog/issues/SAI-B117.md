# [SAI-B117] Enforce institutional sponsorship and learner data-use boundaries

<!-- solver-ai-backlog:SAI-B117 -->
Order: 120 / Priority: P1 / Phase: institutional-pilot
Area: institutional-privacy / Suggested role: Backend engineer with policy/privacy owner

## Problem

An institutional pilot needs explicit limits on what an organization controls versus the learner’s personal account.

## Prerequisites

- SAI-B115 (publish/complete prerequisite first)
- SAI-B116 (publish/complete prerequisite first)
- SAI-B003 (publish/complete prerequisite first)
- SAI-B018 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/features/identity
- services/api/solver_api/main.py
- apps/web/features/accounts
- docs/governance/DATA_AND_LICENSES.md
- services/api/tests

## Scope

- Add a proposed institution/cohort sponsorship policy record with accepted terms version and permitted data scopes.
- Ensure institutional administrators can manage sponsored assignments without inheriting personal practice/source access.

## Acceptance criteria

- An institutional administrator is denied unrelated personal history and source detail routes.
- Terms/scope changes require the documented acknowledgement path and an audit record.
- Pilot enrollment fails clearly when the organization’s required policy configuration is missing.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/institutions/test_data_boundaries.py
- npx playwright test tests/e2e/institutions/policy.spec.ts --workers=2

## Out of scope

- Claiming legal compliance certification
- Redesigning the foundational account deletion/retention system

## Risk and review

Institutional roles can unintentionally override personal privacy.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
