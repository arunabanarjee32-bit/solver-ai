# [SAI-B047] Add deterministic provider transport fixtures without external inference

<!-- solver-ai-backlog:SAI-B047 -->
Order: 62 / Priority: P1 / Phase: AI-1 controlled model hints
Area: Provider adapter verification / Suggested role: AI integration engineer

## Problem

Real transport behavior cannot be validated by relabeling an authored hint or by requiring paid calls in routine checks.

## Prerequisites

- SAI-B043 (publish/complete prerequisite first)
- SAI-B044 (publish/complete prerequisite first)
- SAI-B046 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/tests/hints/test_hints.py
- services/api/solver_api/features/hints/service.py

## Scope

- Create deterministic HTTP transport fixtures for success, refusal, malformed data, rate limiting and disconnects.
- Assert exact outgoing field allowlists and absence of account JWTs, worker tokens, private tests and source.
- Separate fixture provenance from actual model-backed production responses.

## Acceptance criteria

- Fixtures run with all outbound network access denied.
- Tests fail when an extra credential/context field is injected.
- No fixture result is presented as evidence of model quality or paid-provider access.

## Validation

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q

## Out of scope

- Live provider benchmarks
- Adding a public mock backend as a completed AI feature

## Risk and review

A fixture may drift from the selected provider schema; record the reviewed API version.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
