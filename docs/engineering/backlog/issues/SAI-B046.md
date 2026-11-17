# [SAI-B046] Reject malformed model hints before constructing learner responses

<!-- solver-ai-backlog:SAI-B046 -->
Order: 61 / Priority: P1 / Phase: AI-1 controlled model hints
Area: Model output contracts / Suggested role: Backend engineer

## Problem

HintContent already bounds and labels authored/mock/model output, but raw provider responses need a separate defensive normalization boundary.

## Prerequisites

- SAI-B044 (publish/complete prerequisite first)
- SAI-B045 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/features/hints/service.py
- services/api/tests/hints/test_hints.py
- apps/web/features/hints/api.ts

## Scope

- Validate selected provider message content, completion status and text size before HintContent construction.
- Reject empty, oversized, unexpected multimodal/tool-call and incomplete responses with stable sanitized errors.
- Keep raw model text out of exception messages and logs.

## Acceptance criteria

- Every malformed-response fixture produces a stable failure rather than partial success.
- Accepted model hints always have source=model, ai_generated=true and a configured provider identifier.
- Existing frontend provenance/schema checks remain strict.

## Validation

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q; npm run typecheck

## Out of scope

- Rendering provider HTML
- Adding unconstrained chat messages

## Risk and review

String cleanup must not silently convert a refusal or truncated answer into a normal hint.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
