# [SAI-B139] Promote a trained model through a limited pilot and rehearsed rollback

<!-- solver-ai-backlog:SAI-B139 -->
Order: 139 / Priority: P1 / Phase: ML-4 evaluation and delivery
Area: trained-model-release / Suggested role: Release owner, ML evaluation lead and deployment operator

Implementation status: planned

## Problem

A working endpoint is not a release. The trained artifact needs an accountable go/no-go decision, clear supported scope and a real rollback rehearsal before wider learners rely on it.

## Prerequisites

- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)
- SAI-B003 (confirm prerequisite state in the catalogue)
- SAI-B057 (confirm prerequisite state in the catalogue)
- SAI-B059 (confirm prerequisite state in the catalogue)
- SAI-B110 (confirm prerequisite state in the catalogue)
- SAI-B124 (confirm prerequisite state in the catalogue)
- SAI-B126 (confirm prerequisite state in the catalogue)
- SAI-B128 (confirm prerequisite state in the catalogue)
- SAI-B135 (confirm prerequisite state in the catalogue)
- SAI-B136 (confirm prerequisite state in the catalogue)
- SAI-B137 (confirm prerequisite state in the catalogue)
- SAI-B138 (confirm prerequisite state in the catalogue)

## Current code ownership

- docs/product/DSA_SOLVER_READINESS.md
- docs/status/PROJECT_STATUS.md
- docs/onboarding/DEVELOPMENT.md
- docs/governance/OPEN_DECISIONS.md
- apps/web/features/hints/account-hint.tsx
- services/api/solver_api/features/hints/service.py

## Scope

- Run an explicitly approved small consented pilot for the trained artifact with fixed audience, duration, traffic/cost ceilings and the B128 declared coverage.
- Present artifact provenance, assistance mode, limitations, unsupported inputs and finite-evidence wording to users; preserve private data/contest rules and ordinary authored practice.
- Rehearse switching to the last qualified artifact or authored-only mode during in-flight work, then record the actual measured pilot outcomes and owner promotion/rejection decision.

## Acceptance criteria

- The release record binds exact artifact/application revisions, coverage matrix, evaluation evidence, audience/capacity and owner/operator approval.
- Rollback/kill-switch drill stops new model admissions and handles in-flight jobs within their recorded budgets without cross-user results or loss of ordinary practice.
- All preregistered quality/security/resource gates are passed or the pilot remains blocked/rejected; no universal any-DSA or independent security certification claim appears.

## Validation

- Future explicitly approved execution: finite end-to-end pilot and rollback rehearsal on the operated test/pilot deployment; record observed outcomes and unrun checks separately.
- Review UI disclosures and release artifacts against the exact served model identity and held-out report.

## Out of scope

- Unattended permanent public launch
- Automatic model promotion from a training script
- Treating user activity alone as proof of learning improvement

## Risk and review

Promotion changes real-user behavior and recurring spend; require accountable operations, consent, capacity and a tested fallback.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
