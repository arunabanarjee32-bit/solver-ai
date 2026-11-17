# [SAI-B001] Enforce an evidence contract for contributor pull requests

<!-- solver-ai-backlog:SAI-B001 -->
Order: 1 / Priority: P0 / Phase: 0-contribution-gates
Area: foundation / Suggested role: repository maintainer and reviewer

## Problem

The requested multi-tool workflow needs PR submissions that the reviewing assistant can assess consistently. Instructions alone do not show whether a contributor mapped an issue, respected scope or actually ran a claimed check.

## Prerequisites

- No backlog prerequisites; observe the maintainer's release and spending gates.

## Current code ownership

- .github/PULL_REQUEST_TEMPLATE.md
- .github/workflows/ci.yml
- docs/engineering/CODEX_PLAYBOOK.md
- CONTRIBUTING.md

## Scope

- Extend the PR evidence contract with stable backlog ID, before/after behavior, exact changed paths, dependency status, tests actually run with fail/skip/unrun states, security/data impact and rollback.
- Add a narrow pull-request metadata check that reports missing sections or an unknown/missing issue reference; keep implementation review and merge authorization with the designated reviewer.
- Require external AI tools to submit focused PRs and corrections rather than bypassing review; recognize explicit owner overrides for exceptional direct-main work.
- Apply the evidence gate to all contributor PRs; do not infer or classify authorship as AI/human from content.

## Acceptance criteria

- A fixture PR with all required evidence passes the metadata check; fixtures with no issue ID or invented empty test evidence fail with an actionable explanation.
- An explicit not-run explanation is allowed when the owner forbids testing; the check never forces fabricated results.
- The workflow never executes arbitrary PR-body text and never grants write permission or auto-merges a PR.

## Validation

- Inspect the proposed PR template and run the metadata-check fixtures introduced by this issue.
- Inspect workflow permissions and fork-PR handling; do not run pull-request head code with write credentials.

## Out of scope

- Automated code correctness judgment
- Automatically approving or merging all AI contributions
- Reimplementing the repository-wide instructions the owner is already updating

## Risk and review

Untrusted PR text must remain data, and evidence completeness must not be presented as substantive review.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
