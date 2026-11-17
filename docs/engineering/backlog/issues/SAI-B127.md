# [SAI-B127] Enforce owner-approved reviewed-merge rules for the main branch

<!-- solver-ai-backlog:SAI-B127 -->
Order: 2 / Priority: P0 / Phase: 0-contribution-gates
Area: repository governance / Suggested role: Repository owner and designated security reviewer

## Problem

A written review-only workflow does not restrict credentials that can currently write main. The actual GitHub branch rules and reviewer identities must be verified before distributed contributors rely on enforced review.

## Prerequisites

- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- .github/workflows/ci.yml
- .github/PULL_REQUEST_TEMPLATE.md
- CONTRIBUTING.md
- AGENTS.md

## Scope

- Have the repository owner name the actual reviewer identities and approve a narrow emergency-maintenance policy; do not invent an assistant GitHub account.
- Configure supported main-branch rules requiring PR review and the verified check contexts, protecting against forced updates/deletion and documenting any unavoidable owner bypass.
- Record the effective rules and hosting-plan limitations without exposing tokens; preserve access for the designated review/merge workflow.

## Acceptance criteria

- An authorized read of effective branch rules confirms review/check requirements and protected history.
- The owner can identify which principals may merge and which emergency bypasses remain; the documentation does not claim an assistant monitors or approves work continuously.
- If permissions or hosting-plan capabilities block enforcement, the issue remains explicitly blocked with the exact prerequisite rather than claiming policy prose enforced it.

## Validation

- Read the effective GitHub rules/protection configuration using authorized API access and review the required check context names.
- Use a disposable authorized repository/rule fixture for any negative push experiments; never test forced updates or destructive changes on main.

## Out of scope

- Creating or sharing new credentials in chat
- Automatically merging contributor PRs
- Changing repository visibility or purchasing a hosting plan

## Risk and review

Incorrect rules can block maintainers or leave unreviewed writes possible. Owner authorization and verified actual identities are prerequisites.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
