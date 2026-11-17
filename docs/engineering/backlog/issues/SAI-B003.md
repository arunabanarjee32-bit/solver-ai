# [SAI-B003] Approve a small pilot charter and data lifecycle contract

<!-- solver-ai-backlog:SAI-B003 -->
Order: 4 / Priority: P0 / Phase: 0-contribution-gates
Area: product / Suggested role: project owner and privacy/product reviewer

Implementation status: planned

## Problem

The existing local app can support learning, but first audience, public-hosting responsibility, retention periods, deletion and provider-sharing consent remain unresolved. These decisions are prerequisites for handling real learner data.

## Prerequisites

- SAI-B002 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- docs/governance/OPEN_DECISIONS.md
- docs/governance/DATA_AND_LICENSES.md
- docs/product/PRODUCT_REQUIREMENTS.md
- docs/product/PROJECT_VISION.md

## Scope

- Document a deliberately small first pilot audience and the existing practice/account/history features included.
- Have the owner specify retention and deletion rules for source, accounts, logs, exports and backups, including how in-flight jobs and legal exceptions are handled.
- Record who operates the pilot, its approved resource ceiling, incident contact and whether external model sharing is disabled; keep paid services off by default.

## Acceptance criteria

- A decision table names each stored data class, purpose, owner, retention trigger and deletion/export behavior.
- No private submission is eligible for training or external provider transfer without explicit separately recorded consent.
- Pilot launch criteria distinguish local readiness, controlled pilot access and public production exposure; unapproved budget or hosting choices remain blocked.

## Validation

- Review the charter against current source locations and the technical-debt privacy/operations gates.
- Have the owner approve the decision record; no runtime or paid-service call is required.

## Out of scope

- Implementing billing or an AI provider
- Claiming production readiness
- Inventing a retention period or hosting budget without owner approval

## Risk and review

Policy choices affect irreversible deletion and public trust; engineering must follow recorded owner decisions.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
