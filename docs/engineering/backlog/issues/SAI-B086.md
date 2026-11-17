# [SAI-B086] Connect contest submissions to event eligibility and immutable attempt context

<!-- solver-ai-backlog:SAI-B086 -->
Order: 101 / Priority: P1 / Phase: contest-foundation
Area: contests / Suggested role: Backend engineer

Implementation status: planned

## Problem

Existing owned attempts cannot yet prove which contest, problem version or event window they belong to.

## Prerequisites

- SAI-B081 (confirm prerequisite state in the catalogue)
- SAI-B082 (confirm prerequisite state in the catalogue)
- SAI-B083 (confirm prerequisite state in the catalogue)
- SAI-B084 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/api/solver_api/features/submissions/store.py
- services/api/solver_api/main.py
- services/api/tests/submissions
- services/judge/solver_judge/control/worker.py

## Scope

- Add a proposed optional contest context without changing ordinary practice behavior.
- Bind event eligibility, authoritative receipt time, problem version and scoring identity atomically when accepting a request.

## Acceptance criteria

- Early, late, unregistered and mismatched-problem attempts are rejected before queuing.
- Idempotent retries preserve one receipt time and one scored attempt.
- Queued work finishing after the deadline is handled by the documented receipt-time policy; practice regression tests pass.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/contests/test_contest_submissions.py services/api/tests/submissions/test_submissions.py
- uv run --project services/api --frozen pytest services/judge/tests/control/test_worker.py

## Out of scope

- Changing the worker trust boundary
- Multi-database distributed transactions

## Risk and review

Race conditions between registration, deadline and enqueue could create unfair attempts.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
