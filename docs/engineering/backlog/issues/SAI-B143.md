# [SAI-B143] Deliver the new-problem solver workspace with explicit evidence and failure states

<!-- solver-ai-backlog:SAI-B143 -->
Order: 143 / Priority: P1 / Phase: AI-6 new-problem coverage
Area: New-problem solving user journey / Suggested role: Web/API engineer with solver evaluation reviewer

Implementation status: planned

## Problem

A trained endpoint and seed-problem solver do not provide a complete user journey for a previously unseen pasted problem. Users need structured input, supported-format limits, bounded generation and truthful test evidence.

## Prerequisites

- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)
- SAI-B069 (confirm prerequisite state in the catalogue)
- SAI-B070 (confirm prerequisite state in the catalogue)
- SAI-B071 (confirm prerequisite state in the catalogue)
- SAI-B072 (confirm prerequisite state in the catalogue)
- SAI-B073 (confirm prerequisite state in the catalogue)
- SAI-B128 (confirm prerequisite state in the catalogue)
- SAI-B142 (confirm prerequisite state in the catalogue)
- SAI-B048 (confirm prerequisite state in the catalogue)
- SAI-B059 (confirm prerequisite state in the catalogue)
- SAI-B129 (confirm prerequisite state in the catalogue)

## Current code ownership

- apps/web/features/solver/
- apps/web/app/solve/
- tests/e2e/solver/
- services/api/solver_api/features/solver/
- docs/product/DSA_SOLVER_READINESS.md

## Scope

- Build an account-owned workspace for B142 structured problem input and missing-information correction, with visible supported language/format policy, consent and immutable problem identity. Preserve existing catalog practice routes.
- Invoke the existing budgeted plan/candidate/execution/repair/ranking workflow through a qualified provider interface. Accept a reviewed untuned baseline supported by B129/B128 evidence; using a trained artifact additionally requires B138 qualification. Display source, explanation, claimed complexity, model/artifact identity, actual validation, consumed budgets and termination reason.
- Separate passed supplied samples, generated-test evidence and independent authorized evaluator acceptance. Display not-solved, no-independent-grader, unsupported, timeout, cancellation and provider failure states; do not turn model confidence or generated tests into an Accepted verdict.

## Acceptance criteria

- A synthetic unseen standard-input problem can be entered, validated and solved or explicitly fail through the complete bounded workflow, with outputs bound to the exact owned problem and generation revisions.
- An intentionally incorrect candidate that passes supplied samples is never labeled independently accepted without the required authorized evaluator. Incomplete/unsupported input receives actionable feedback before model work.
- Cross-user access, cancellation/retry, stale responses, resource exhaustion and unavailable provider fixtures preserve ownership and budgets. Actual qualified-model pilot results are recorded separately from fixture checks and do not imply every unseen problem is solvable.
- The workspace is usable with a rights-approved, owner-admitted qualified untuned baseline if tuning is rejected. An arbitrary unqualified endpoint is not accepted, and choosing the trained route requires the B138 artifact/serving gate.

## Validation

- Run focused browser/API contract fixtures for new statement entry, correction, source output, evidence labels and every terminal state, using deterministic fake model transports.
- After separate owner authorization, run a small new-problem pilot with the qualified untuned baseline or B138-trained artifact and B128 measurements; record actual failures, latency/cost and coverage without training on the sealed release evaluation.

## Out of scope

- Automatic submission to external contest sites
- Unbounded retries, universal any-DSA correctness labels or private test disclosure
- New training runs, autonomous URL scraping or model selection

## Risk and review

Users may mistake generated code or sample-pass evidence for a proven solution. Strong version/ownership binding and explicit provenance/evaluation states are required across retries and concurrent sessions.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
