# [SAI-B092] Implement audited contest rejudging with immutable verdict revisions

<!-- solver-ai-backlog:SAI-B092 -->
Order: 107 / Priority: P1 / Phase: contest-corrections
Area: contest-admin / Suggested role: Backend engineer and judge maintainer

## Problem

Organizers need to correct grading errors without overwriting the evidence behind earlier standings.

## Prerequisites

- SAI-B085 (publish/complete prerequisite first)
- SAI-B086 (publish/complete prerequisite first)
- SAI-B091 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/features/submissions/store.py
- services/api/solver_api/main.py
- services/judge/solver_judge/control/worker.py
- services/api/tests

## Scope

- Add proposed authorized rejudge requests with reason, selected grading version and append-only result revision.
- Recompute affected standings from the chosen official revision while retaining prior visible audit history.

## Acceptance criteria

- Repeated identical rejudge requests enqueue no duplicate active job.
- Unapproved/failed rejudges leave official standings unchanged.
- A completed approved rejudge changes the expected score and records actor, reason and prior revision reference.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/contests/test_rejudge.py
- uv run --project services/api --frozen pytest services/judge/tests/control/test_worker.py

## Out of scope

- Deleting original verdicts
- User-controlled executable graders

## Risk and review

A faulty correction can retroactively invalidate many results.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
