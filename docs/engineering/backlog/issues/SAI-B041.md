# [SAI-B041] Record the single-provider hint pilot activation decision

<!-- solver-ai-backlog:SAI-B041 -->
Order: 56 / Priority: P1 / Phase: AI-1 controlled model hints
Area: AI activation governance / Suggested role: Project owner with privacy and AI engineering reviewers

## Problem

Authored hints and their UI work, but no provider, data-processing terms, spend owner or activation authority has been selected for real inference.

## Prerequisites

- SAI-B001 (publish/complete prerequisite first)
- SAI-B002 (publish/complete prerequisite first)
- SAI-B003 (publish/complete prerequisite first)
- SAI-B026 (publish/complete prerequisite first)

## Current code ownership

- docs/product/AI_SOLVER.md
- docs/governance/OPEN_DECISIONS.md
- docs/governance/DATA_AND_LICENSES.md

## Scope

- Document one bounded hint pilot and its permitted public-only context.
- Record provider-selection criteria, credential destinations, pricing assumptions, responsible owner and rollback authority.
- Make activation conditional on privacy, admission and transport issues below.

## Acceptance criteria

- Decision separates authored service, optional model pilot and unapproved debugging/training.
- Every unresolved credential, rights or spending prerequisite has an owner and blocks activation.
- No default configuration begins paid inference.

## Validation

- Document review against docs/status/PROJECT_STATUS.md and the existing HintBackend implementation; no provider calls.

## Out of scope

- Provisioning a paid account or GPU
- Replacing existing authored hints

## Risk and review

A written provider name must not be mistaken for permission to send user data or spend money.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
