# [SAI-B009] Validate production worker credential strength before enabling internal routes

<!-- solver-ai-backlog:SAI-B009 -->
Order: 10 / Priority: P1 / Phase: 1-safe-pilot
Area: worker-auth / Suggested role: backend security engineer

Implementation status: planned

## Problem

The native runner generates a strong local worker token, but the API accepts configured worker bearer material without an independent strength check. A manually supplied weak production value can define the whole controller trust domain.

## Prerequisites

- SAI-B006 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/api/solver_api/main.py
- scripts/development/local_config.py
- services/judge/solver_judge/control/worker.py
- services/api/tests/submissions/test_submissions.py
- docs/onboarding/DEVELOPMENT.md

## Scope

- Centralize worker credential validation for configured internal-route enablement, with a documented minimum entropy/length policy and no public fallback key.
- Keep the existing secure local generation path and distinguish deliberately disabled judging from invalid configured credentials.
- Reject invalid credentials at configuration time without logging their value.

## Acceptance criteria

- Empty/unset worker auth leaves execution unavailable as documented; a nonempty weak configured value fails clearly.
- Generated local tokens and a valid production-format fixture enable the existing authenticated control flow.
- Logs, API errors and diagnostics contain no token values or token-derived reversible representation.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/submissions/test_submissions.py
- uv run --project services/api --frozen pytest services/judge/tests/control/test_worker.py

## Out of scope

- Implementing multi-worker certificate identities
- Changing sandbox isolation
- Printing or requesting real secret values

## Risk and review

Overly broad validation could break deliberate no-judge development; disabled mode and invalid mode need distinct tests.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
