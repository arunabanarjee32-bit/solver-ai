# [SAI-B048] Implement one opt-in bounded asynchronous hint provider adapter

<!-- solver-ai-backlog:SAI-B048 -->
Order: 63 / Priority: P1 / Phase: AI-1 controlled model hints
Area: Real provider transport / Suggested role: AI backend engineer

Implementation status: planned

## Problem

select_hint_backend deliberately supports authored only. The first real adapter needs bounded async transport rather than archived sync clients with missing timeouts.

## Prerequisites

- SAI-B043 (confirm prerequisite state in the catalogue)
- SAI-B044 (confirm prerequisite state in the catalogue)
- SAI-B046 (confirm prerequisite state in the catalogue)
- SAI-B047 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/api/solver_api/features/hints/service.py
- services/api/pyproject.toml
- services/api/tests/hints/test_hints.py

## Scope

- Implement the single provider selected in B041 using an existing suitable HTTP dependency where possible.
- Set request/response byte caps, completion-token cap, explicit transport timeouts and destination restrictions.
- Keep registration disabled unless the later entitlement, budget and privacy gates are satisfied.

## Acceptance criteria

- Adapter passes deterministic transport fixtures without real network access.
- Oversized or endless responses terminate within documented limits.
- Default startup and authored hints do not require provider credentials or make external calls.

## Validation

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q; uv run --project services/api --frozen ruff check services/api

## Out of scope

- Automatic activation or spend
- Installing archive requirements or adding a second provider

## Risk and review

Transport completion does not establish content quality, privacy compliance or production readiness.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
