# [SAI-B042] Bound and fingerprint the existing public-only hint context

<!-- solver-ai-backlog:SAI-B042 -->
Order: 57 / Priority: P1 / Phase: AI-1 controlled model hints
Area: Safe model context / Suggested role: Backend engineer

Implementation status: planned

## Problem

PublicHintContext already excludes private tests and identity, but future inference needs explicit per-field and aggregate bounds and a stable content fingerprint.

## Prerequisites

- SAI-B041 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/api/solver_api/features/hints/service.py
- services/api/solver_api/features/catalog/models.py
- services/api/tests/hints/test_hints.py

## Scope

- Add validated context-size limits and deterministic canonical fingerprinting without introducing private grading fields.
- Define overflow rejection or documented deterministic truncation for each public field.
- Keep authored lookup behavior and the public HTTP v1 response compatible.

## Acceptance criteria

- Private test/source/credential sentinels never enter serialized model context.
- Identical authorized catalog content produces the same fingerprint; changed samples change it.
- Boundary and one-byte-over-limit inputs have deterministic outcomes.

## Validation

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q

## Out of scope

- Reading owned submission source
- Sending a model request

## Risk and review

Silent truncation could remove a constraint and produce misleading hints.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
