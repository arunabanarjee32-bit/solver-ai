# [SAI-B026] Extend problem provenance with explicit permitted-use metadata

<!-- solver-ai-backlog:SAI-B026 -->
Order: 27 / Priority: P1 / Phase: 2-useful-practice
Area: content / Suggested role: content engineer and rights reviewer

## Problem

Problem provenance currently records only author/source text. More content needs a machine-readable distinction between original authorship, permission, redistribution and training rights.

## Prerequisites

- SAI-B002 (publish/complete prerequisite first)
- SAI-B003 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/features/catalog/models.py
- services/api/solver_api/features/catalog/content.py
- apps/web/features/practice/api.ts
- apps/web/features/practice/workspace.tsx
- services/api/tests/catalog/test_api.py

## Scope

- Define a bounded public provenance schema with stable content identity, author attribution and approved permitted-use fields; keep private evidence references out of public responses.
- Populate truthful metadata for the three original seed exercises without importing third-party banks.
- Render concise attribution/rights information and validate it in the typed browser contract.

## Acceptance criteria

- Every current seed validates with explicit provenance; unknown/unapproved reuse states cannot silently become approved.
- Public responses expose no private license documents or contributor personal contact data.
- Malformed/oversized metadata is rejected and existing problem rendering/tests remain contract-compatible through an intentional schema change.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/catalog/test_api.py
- PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e -- tests/e2e/practice/practice.spec.ts --workers=2

## Out of scope

- Approving archived datasets
- Inventing legal permission for public websites
- Training any model

## Risk and review

Rights metadata is a recorded authorization, not automatic legal clearance; owner/content review is required.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
