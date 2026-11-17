# [SAI-B138] Integrate the qualified trained artifact with bounded provider-neutral serving

<!-- solver-ai-backlog:SAI-B138 -->
Order: 138 / Priority: P1 / Phase: ML-4 evaluation and delivery
Area: trained-model-serving / Suggested role: ML serving engineer and backend security reviewer

Implementation status: planned

## Problem

The project has no trained-model inference service. An artifact registry and model score do not connect a qualified checkpoint to authenticated tutor/solver requests with enforceable budget and failure behavior.

## Prerequisites

- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)
- SAI-B043 (confirm prerequisite state in the catalogue)
- SAI-B044 (confirm prerequisite state in the catalogue)
- SAI-B046 (confirm prerequisite state in the catalogue)
- SAI-B050 (confirm prerequisite state in the catalogue)
- SAI-B051 (confirm prerequisite state in the catalogue)
- SAI-B054 (confirm prerequisite state in the catalogue)
- SAI-B055 (confirm prerequisite state in the catalogue)
- SAI-B057 (confirm prerequisite state in the catalogue)
- SAI-B079 (confirm prerequisite state in the catalogue)
- SAI-B135 (confirm prerequisite state in the catalogue)
- SAI-B136 (confirm prerequisite state in the catalogue)
- SAI-B137 (confirm prerequisite state in the catalogue)

## Current code ownership

- services/api/solver_api/features/hints/service.py
- docs/architecture/ARCHITECTURE.md
- docs/onboarding/DEVELOPMENT.md
- docs/product/DSA_SOLVER_READINESS.md
- tests/tooling

## Scope

- Deploy one separately operated approved inference endpoint for the exact qualified artifact and wire it through the existing provider-neutral result/usage contracts; do not load GPU weights in web/API processes.
- Reuse existing destination/secret, output-validation, entitlement, concurrency/budget, deadline/retry and kill-switch controls rather than implement a competing authorization or quota stack.
- Add explicit model/artifact/revision provenance, bounded health/readiness and operator-only diagnostics; support the approved offline/local-model route without requiring a paid external provider.

## Acceptance criteria

- A permitted request reaches only the configured qualified artifact and returns correct provenance; unauthorized/over-budget/oversized/out-of-scope inputs fail before inference as specified.
- Endpoint timeout/crash/malformed output triggers bounded safe behavior and visibly authored fallback only under the existing policy; no fake model output is shown.
- Admission caps hold at the declared serving concurrency, no provider/worker secrets or private tests reach generation context, and a kill switch stops new model work without breaking ordinary practice.

## Validation

- Future authorized checks: deterministic fake-endpoint contract/security/timeout/quota fixtures through the existing provider test harness.
- On the approved isolated inference environment, run a small capped end-to-end request/overload/failure smoke using the exact exported artifact and no private learner data.

## Out of scope

- Choosing or buying serving hardware now
- Replacing B048 transport/entitlement/budget work
- Public activation before the pilot/release gates

## Risk and review

Model-serving isolation and endpoint configuration can bypass established policy if treated as a new shortcut; reuse existing trusted admission controls.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
