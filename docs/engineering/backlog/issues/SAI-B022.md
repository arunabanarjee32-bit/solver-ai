# [SAI-B022] Apply retention to terminal submission source with a dry-run purge

<!-- solver-ai-backlog:SAI-B022 -->
Order: 23 / Priority: P1 / Phase: 1-safe-pilot
Area: privacy-storage / Suggested role: backend engineer and privacy reviewer

Implementation status: planned

## Problem

Terminal private source/history grows indefinitely. The store has no approved source retention lifecycle, even when account/request quotas are respected.

## Prerequisites

- SAI-B003 (confirm prerequisite state in the catalogue)
- SAI-B013 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/api/solver_api/features/submissions/store.py
- services/api/tests/submissions/test_submissions.py
- scripts/development
- docs/governance/DATA_AND_LICENSES.md

## Scope

- Implement the owner-approved source/summary retention policy for terminal records with an explicit dry-run report and bounded batches.
- Preserve active jobs and any data classes the approved policy must retain; define idempotency behavior for purged source.
- Run purge only through an authorized operator path or scheduled process with safe counts and no source output.

## Acceptance criteria

- Boundary-time fixtures purge only eligible terminal data and retain queued/running/other-owner records as specified.
- Dry-run performs no writes and reports only aggregate counts/bytes; repeat purge is idempotent.
- Detail/history endpoints handle a retained summary with expired source honestly instead of reconstructing or leaking content.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/submissions/test_submissions.py
- Exercise the purge dry-run and apply paths only on temporary fixture databases.

## Out of scope

- Deleting real developer/user history during validation
- Choosing retention periods without B003
- Changing hidden grading data lifecycle

## Risk and review

Retention is deliberate destruction; ensure policy, exclusions and backup behavior are explicit before enabling scheduled writes.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
