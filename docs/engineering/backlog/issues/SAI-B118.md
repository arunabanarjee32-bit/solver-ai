# [SAI-B118] Export institution-authorized assignment records with redaction tests

<!-- solver-ai-backlog:SAI-B118 -->
Order: 121 / Priority: P2 / Phase: institutional-pilot
Area: institutional-privacy / Suggested role: Backend engineer and privacy reviewer

## Problem

Institutions need a narrow portable assignment record without receiving unrelated private learner data.

## Prerequisites

- SAI-B116 (publish/complete prerequisite first)
- SAI-B117 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/main.py
- services/api/solver_api/features/submissions/store.py
- scripts/verification
- services/api/tests

## Scope

- Add a proposed versioned export for authorized cohorts/assignments and an explicit field allowlist.
- Default to summary/rubric records; include source only when the assignment consent/policy explicitly permits it.

## Acceptance criteria

- A seeded mixed personal/cohort history exports only the requested institution’s allowed assignment rows.
- Private grading data, tokens, account keys and unrelated identifiers never appear.
- Expired/revoked institution permissions cannot generate or retrieve a fresh export.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/institutions/test_assignment_export.py

## Out of scope

- General database dumps
- Exporting user code for training

## Risk and review

Portable exports can turn a narrow permission mistake into a durable data leak.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
