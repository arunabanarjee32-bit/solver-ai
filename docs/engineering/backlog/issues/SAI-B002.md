# [SAI-B002] Record owner-approved original-code licensing and inbound contribution rights

<!-- solver-ai-backlog:SAI-B002 -->
Order: 3 / Priority: P0 / Phase: 0-contribution-gates
Area: governance / Suggested role: project owner with legal/IP reviewer

Implementation status: planned

## Problem

The original project has no selected outbound license or settled inbound IP policy. Inviting many AI-assisted contributors without an explicit rights decision leaves reuse and contribution expectations unclear.

## Prerequisites

- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- docs/governance/OPEN_DECISIONS.md
- docs/governance/DATA_AND_LICENSES.md
- CONTRIBUTING.md
- AGENTS.md

## Scope

- Prepare a short decision record comparing owner-selected licensing options and how external human/AI-assisted contributions are accepted.
- Obtain the actual owner decision, record its date and scope, and only then add or amend license/notice files and contributor declarations.
- Distinguish original application rights from preserved upstream MIT/Apache code, datasets, problems and model artifacts.

## Acceptance criteria

- The owner-approved decision states exact rights for original code and the inbound contribution mechanism; undecided points remain explicitly blocked.
- Contributor instructions identify third-party attribution and provenance requirements without claiming ownership of upstream or user code.
- A PR containing this change includes the owner decision reference and reviewer evidence required by B001.

## Validation

- Statically review the decision, selected license text and contributor notice for consistency.
- Review the diff to ensure preserved upstream notices and archive hashes were not changed.

## Out of scope

- Choosing a license without owner authority
- Re-licensing archived dependencies or datasets
- Legal certification

## Risk and review

An assistant cannot invent licensing consent or assign rights it does not own.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
