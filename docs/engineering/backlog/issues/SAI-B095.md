# [SAI-B095] Create a reproducible contest rehearsal and official standings export

<!-- solver-ai-backlog:SAI-B095 -->
Order: 110 / Priority: P1 / Phase: contest-corrections
Area: contest-release / Suggested role: QA engineer and contest operator

## Problem

A contest feature set needs an end-to-end operational gate rather than separate passing screens.

## Prerequisites

- SAI-B090 (publish/complete prerequisite first)
- SAI-B091 (publish/complete prerequisite first)
- SAI-B092 (publish/complete prerequisite first)
- SAI-B094 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- tests/e2e
- services/api/tests
- scripts/verification
- docs/onboarding/DEVELOPMENT.md

## Scope

- Add a proposed deterministic rehearsal using only original fixtures: register, submit AC/WA, freeze, clarify, rejudge and finish.
- Export versioned official standings with event/rules identifiers and exclude private source and grading inputs.

## Acceptance criteria

- The exported standings match a hand-checked expected fixture and replay to identical ordering.
- The rehearsal covers an unauthorized participant, pending job at deadline and a failed rejudge.
- Each export records its event revision; no real learner database is modified by the rehearsal.

## Validation

- npx playwright test tests/e2e/contests/rehearsal.spec.ts --workers=2
- uv run --project services/api --frozen pytest services/api/tests/contests/test_standings_export.py

## Out of scope

- Running a public rated contest
- Publishing participant personal information

## Risk and review

An incomplete rehearsal can hide event-wide correctness failures.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
