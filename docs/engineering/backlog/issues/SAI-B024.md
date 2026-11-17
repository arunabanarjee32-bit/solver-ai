# [SAI-B024] Avoid loading private source for submission summary pages

<!-- solver-ai-backlog:SAI-B024 -->
Order: 25 / Priority: P2 / Phase: 2-useful-practice
Area: storage-performance / Suggested role: backend engineer

## Problem

History listing uses SELECT * and constructs full details before discarding source. Large retained programs are unnecessarily read and materialized for summary-only pagination.

## Prerequisites

- SAI-B013 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/features/submissions/store.py
- services/api/tests/submissions/test_submissions.py

## Scope

- Select explicit summary columns in the list query and map summaries without building SubmissionDetail.
- Retain stable created_at/id ordering, owner filtering, total count and expiry semantics.
- Add a regression fixture with large source to distinguish summary projection from detail retrieval.

## Acceptance criteria

- History responses are byte-for-byte contract-compatible and never include source_code.
- An instrumented query/row fixture shows list mapping does not request/read the source_code column, while owned detail still returns it.
- Pagination ties, empty pages and cross-owner access retain existing behavior.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/submissions/test_submissions.py

## Out of scope

- A database rewrite or ORM migration
- Speculative caching layers
- Removing owned detail access

## Risk and review

Summary optimization must not bypass expiry/ownership checks or change deterministic pagination.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
