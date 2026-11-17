# [SAI-B061] Implement account-owned expiring tutor conversation state

<!-- solver-ai-backlog:SAI-B061 -->
Order: 80 / Priority: P2 / Phase: AI-2 consented tutor and debugger
Area: Tutor context lifecycle / Suggested role: Backend privacy engineer

## Problem

Multiple tutoring turns must not reuse another account's context, grow without bound or persist private discussion indefinitely.

## Prerequisites

- SAI-B050 (publish/complete prerequisite first)
- SAI-B053 (publish/complete prerequisite first)
- SAI-B056 (publish/complete prerequisite first)
- SAI-B060 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/features/hints/service.py
- services/api/solver_api/main.py
- apps/web/features/hints/api.ts
- services/api/tests/hints/test_hints.py

## Scope

- Implement the approved turn contract with account/problem/version ownership, expiration and deletion.
- Apply per-turn and aggregate context/token limits before each model request.
- Invalidate client state on account/problem changes using the existing cancellation pattern.

## Acceptance criteria

- A second account cannot read, append or delete another conversation.
- Expired or maximum-turn conversations stop without external work.
- No hidden tests or worker credentials can be represented in stored turns.

## Validation

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q; npm run typecheck

## Out of scope

- Cross-problem permanent memory
- Training from conversation content

## Risk and review

Conversation history can become an uncontrolled source of retained personal data.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
