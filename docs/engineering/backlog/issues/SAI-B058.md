# [SAI-B058] Add shared golden fixtures for hint API and browser schema parity

<!-- solver-ai-backlog:SAI-B058 -->
Order: 73 / Priority: P2 / Phase: AI-1 controlled model hints
Area: Cross-runtime AI contracts / Suggested role: Full-stack contract engineer

## Problem

Pydantic and Zod intentionally validate the same bounded contract independently; future provider fields could drift between implementations.

## Prerequisites

- SAI-B044 (publish/complete prerequisite first)
- SAI-B046 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/features/hints/service.py
- apps/web/features/hints/api.ts
- services/api/tests/hints/test_hints.py
- tests/e2e/hints/hints.spec.ts

## Scope

- Define public golden authored/model/mock/error fixtures and explicit incompatible examples.
- Exercise both validators against provenance, level, slug, length and response-correlation cases.
- Document additive internal metadata versus HTTP schema version changes.

## Acceptance criteria

- Both runtimes accept every valid golden fixture and reject every invalid one.
- A changed provider/source/ai_generated combination cannot bypass either validator.
- Fixtures contain no credentials, private cases or account identifiers.

## Validation

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q; npm run test:e2e -- tests/e2e/hints/hints.spec.ts --workers=1

## Out of scope

- Replacing runtime validation with TypeScript types only
- Changing public API v1 unnecessarily

## Risk and review

Generated types alone do not validate hostile network payloads.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
