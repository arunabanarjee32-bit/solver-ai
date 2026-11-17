# [SAI-B053] Record redacted generation usage and failure telemetry

<!-- solver-ai-backlog:SAI-B053 -->
Order: 68 / Priority: P1 / Phase: AI-1 controlled model hints
Area: AI observability / Suggested role: Backend observability engineer

Implementation status: planned

## Problem

Archive adapters log prompts/responses and simple CSV usage; production troubleshooting needs operational evidence without copying learner content or secrets.

## Prerequisites

- SAI-B044 (confirm prerequisite state in the catalogue)
- SAI-B050 (confirm prerequisite state in the catalogue)
- SAI-B020 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/api/solver_api/features/hints/service.py
- services/api/solver_api/http/errors.py
- services/api/tests/hints/test_hints.py
- docs/governance/DATA_AND_LICENSES.md

## Scope

- Define allowlisted run ID, model/version, context fingerprint, latency, capped usage and termination metadata.
- Redact authorization, provider payloads, source and problem text by construction.
- Set bounded retention and document aggregation versus account-level access.

## Acceptance criteria

- Sentinel credentials/source/private tests never appear in captured logs on success or failure.
- Unknown usage and provider-timeout categories remain distinguishable.
- A learner-visible correlation ID maps to one operational event without revealing another account.

## Validation

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q

## Out of scope

- Collecting full prompts by default
- Claiming estimated token counts equal invoices

## Risk and review

Verbose error logging can defeat an otherwise safe context boundary.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
