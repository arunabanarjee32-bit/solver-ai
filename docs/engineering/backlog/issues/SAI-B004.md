# [SAI-B004] Pin CI actions to immutable reviewed commits

<!-- solver-ai-backlog:SAI-B004 -->
Order: 5 / Priority: P1 / Phase: 1-safe-pilot
Area: supply-chain / Suggested role: release engineer

## Problem

CI currently references checkout, setup-node, setup-uv and upload-artifact by mutable major tags. Package locks do not pin the executable action implementations.

## Prerequisites

- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- .github/workflows/ci.yml
- docs/engineering/CODEX_PLAYBOOK.md

## Scope

- Resolve each currently used action to an official reviewed commit and record the readable release alongside the digest.
- Keep workflow permissions at the existing minimum and document a bounded update/review process.
- Preserve frozen installs and existing check coverage rather than replacing the workflow.

## Acceptance criteria

- Every third-party uses entry is pinned to a full commit SHA from the official upstream.
- No new token write permission, unsafe pull_request_target execution or secret exposure is introduced.
- The workflow configuration still contains all existing required steps and explicit artifact retention.

## Validation

- Statically inspect all uses entries, source provenance and workflow permissions.
- When check execution is authorized, observe a normal fork-safe PR CI run at the exact commit and record its outcome.

## Out of scope

- Changing application dependencies
- Running untrusted PR code with repository write credentials
- Claiming mutable tags prove compromise

## Risk and review

Incorrect action provenance can install a malicious implementation; digest updates require review.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
