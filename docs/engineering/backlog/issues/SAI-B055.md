# [SAI-B055] Bound provider retries and add outage admission state

<!-- solver-ai-backlog:SAI-B055 -->
Order: 70 / Priority: P1 / Phase: AI-1 controlled model hints
Area: AI failure policy / Suggested role: Backend reliability engineer

Implementation status: planned

## Problem

Archived clients retry up to twenty times or wait many minutes. A paid hint endpoint needs predictable bounded failures and must not amplify outages.

## Prerequisites

- SAI-B048 (confirm prerequisite state in the catalogue)
- SAI-B051 (confirm prerequisite state in the catalogue)
- SAI-B054 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/api/solver_api/features/hints/service.py
- services/api/tests/hints/test_hints.py
- apps/web/features/hints/api.ts

## Scope

- Classify retryable transport/429 failures separately from invalid output/authentication/refusal.
- Cap attempts within the original deadline and reserve the possible retry cost.
- Add a small observable outage/cooldown admission policy with explicit recovery behavior.

## Acceptance criteria

- Nonretryable fixture errors make exactly one attempt.
- Retryable fixtures never exceed configured attempts, deadline or reserved spend.
- Outage responses preserve stable public errors and keep authored practice usable.

## Validation

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q

## Out of scope

- Automatic fallback to a more expensive provider
- Infinite background retries

## Risk and review

Retries can multiply both latency and charges even after the browser gives up.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
