# [SAI-B063] Collect minimal account-owned hint quality feedback

<!-- solver-ai-backlog:SAI-B063 -->
Order: 82 / Priority: P2 / Phase: AI-2 consented tutor and debugger
Area: AI feedback and correction / Suggested role: Full-stack product engineer

Implementation status: planned

## Problem

Pilot quality reports need a way to identify confusing, incorrect or spoiler-heavy hints without collecting unrelated source or inventing learning metrics.

## Prerequisites

- SAI-B053 (confirm prerequisite state in the catalogue)
- SAI-B059 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- apps/web/features/hints/account-hint.tsx
- services/api/solver_api/features/hints/service.py
- services/api/solver_api/main.py
- docs/governance/DATA_AND_LICENSES.md

## Scope

- Add bounded helpful/incorrect/spoiler feedback keyed to an owned generation ID.
- Deduplicate submissions, constrain optional text and define correction/retention ownership.
- Expose aggregate review counts separately from model correctness or learning claims.

## Acceptance criteria

- Feedback cannot reference another account's private run.
- One account/run/action cannot inflate aggregate counts through retries.
- Logs and exports omit account tokens and editor source.

## Validation

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q; npm run typecheck

## Out of scope

- Training automatically from feedback
- Public account rankings

## Risk and review

Self-selected ratings are product feedback, not a controlled educational study.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
