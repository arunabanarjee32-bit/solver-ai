# [SAI-B064] Define explicit source-sharing consent and owned debugger input

<!-- solver-ai-backlog:SAI-B064 -->
Order: 83 / Priority: P1 / Phase: AI-2 consented tutor and debugger
Area: Debugger privacy boundary / Suggested role: Privacy and backend authorization engineer

## Problem

The current public-only hint contract intentionally excludes source. A debugger needs a separate deliberate source-sharing boundary rather than reading drafts or stored submissions implicitly.

## Prerequisites

- SAI-B042 (publish/complete prerequisite first)
- SAI-B049 (publish/complete prerequisite first)
- SAI-B056 (publish/complete prerequisite first)
- SAI-B060 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/features/submissions/store.py
- services/api/solver_api/features/hints/service.py
- apps/web/features/practice/code-pane.tsx
- docs/governance/DATA_AND_LICENSES.md

## Scope

- Specify bounded language/source/public-evidence input with a distinct disclosure and explicit user action.
- Resolve stored source only through existing owned-submission checks.
- Record exact source hash and consent version; prohibit background keystroke upload.

## Acceptance criteria

- Foreign submission IDs and forged ownership fields are rejected before model admission.
- No source leaves the browser/API without the debugger-specific action and consent.
- Oversized/unsupported-language input has a stable failure with zero model calls.

## Validation

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints services/api/tests/submissions -q; npm run typecheck

## Out of scope

- Implicit training consent
- Reading other users' solutions or private grading tests

## Risk and review

Source can contain personal information or secrets; the product must disclose this additional processing.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
