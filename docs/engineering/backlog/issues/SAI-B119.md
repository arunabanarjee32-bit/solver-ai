# [SAI-B119] Produce a redacted pilot cost ledger and resource-envelope report

<!-- solver-ai-backlog:SAI-B119 -->
Order: 122 / Priority: P2 / Phase: institutional-pilot
Area: business-operations / Suggested role: Operations engineer and project owner

## Problem

A sustainable pilot needs measured usage and declared prices rather than assumptions that self-hosting or AI is free.

## Prerequisites

- SAI-B105 (publish/complete prerequisite first)
- SAI-B109 (publish/complete prerequisite first)
- SAI-B003 (publish/complete prerequisite first)
- SAI-B021 (publish/complete prerequisite first)
- SAI-B053 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- scripts/verification
- services/api/solver_api/main.py
- docs/product/ROADMAP.md
- services/api/tests

## Scope

- Add a proposed offline report combining bounded usage aggregates with operator-supplied nonsecret unit prices.
- Separate measured consumption, estimated allocation and unpriced items; never infer a paid purchase from report generation.
- Consume B021/B053 measurements and the B003 approved envelope; never create another online token/budget reservation ledger.

## Acceptance criteria

- Known usage/price fixtures produce exact totals and missing prices remain explicitly unknown.
- The report excludes source, personal identifiers and provider credentials.
- A budget scenario exceeding its approved resource envelope is flagged with the contributing categories.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/operations/test_cost_ledger.py

## Out of scope

- Buying infrastructure or model credits
- Live invoicing, payment processing or guaranteed profitability

## Risk and review

False precision can hide unpriced support, capacity or provider costs.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
