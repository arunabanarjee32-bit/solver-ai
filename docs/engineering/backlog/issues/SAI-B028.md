# [SAI-B028] Detect public-sample drift between catalog and judge deployments

<!-- solver-ai-backlog:SAI-B028 -->
Order: 29 / Priority: P1 / Phase: 2-useful-practice
Area: content-quality / Suggested role: content/backend engineer

## Problem

Public samples are represented across independent API/judge deployments. Current examples can drift so Run samples checks a different input/output from the problem page.

## Prerequisites

- SAI-B027 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/features/catalog/content.py
- services/judge/solver_judge/grading/cases.py
- services/api/tests/catalog/test_api.py
- services/judge/tests/grading/test_cases.py
- scripts/verification

## Scope

- Add a deterministic public-only sample manifest or cross-component contract fixture keyed by problem revision.
- Compare exact sample inputs/outputs and supported language starter interfaces without coupling API imports to private judge test data.
- Document how an author updates both deployments and how mismatch blocks release.

## Acceptance criteria

- All three current problems have identical public sample contracts across API and judge.
- Changing one sample fixture on either side causes a targeted consistency failure with problem/revision identification.
- The shared/public fixture contains no generated private grading cases or oracle answers beyond public samples.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/catalog/test_api.py services/judge/tests/grading/test_cases.py

## Out of scope

- Merging trusted private grading data into the API package
- Executing arbitrary author code on the API host
- A full data-ingestion pipeline

## Risk and review

A shared manifest must not accidentally package private tests into web/API artifacts.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
