# [SAI-B051] Add process-wide provider concurrency and monetary admission ceilings

<!-- solver-ai-backlog:SAI-B051 -->
Order: 66 / Priority: P1 / Phase: AI-1 controlled model hints
Area: Global AI spend control / Suggested role: Backend platform engineer

Implementation status: planned

## Problem

Per-account allowance cannot prevent many accounts from exhausting provider concurrency or a project-wide spending ceiling.

## Prerequisites

- SAI-B050 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/api/solver_api/features/hints/service.py
- services/api/tests/hints/test_hints.py
- docs/onboarding/DEVELOPMENT.md

## Scope

- Define bounded global in-flight admission and an explicitly versioned token-price estimate.
- Reject requests whose maximum reserved cost exceeds a configured project ceiling.
- Fail closed for invalid pricing/ceiling configuration; distinguish estimated from billed cost.

## Acceptance criteria

- An N+1 concurrent request is denied or boundedly queued under an N-slot configuration.
- Worst-case reservations never exceed the configured monetary ceiling.
- Restart semantics and single-process versus multi-process limits are documented honestly.

## Validation

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q

## Out of scope

- Distributed quota infrastructure without a deployment need
- Automatic model upgrades

## Risk and review

A process-local semaphore is not a distributed project-wide spending guarantee.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
