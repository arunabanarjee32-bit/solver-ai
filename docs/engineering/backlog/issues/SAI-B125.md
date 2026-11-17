# [SAI-B125] Gate production readiness on an approved supported runtime identity

<!-- solver-ai-backlog:SAI-B125 -->
Order: 45 / Priority: P0 / Phase: 1-safe-pilot
Area: runtime-maintenance / Suggested role: Judge operator, security reviewer and project owner

## Problem

Preflight establishes that runsc exists, rootless Docker is selected and finite probes pass. It does not enforce a maintained approved runtime identity or support window. The historical review explicitly records an outdated installed runtime; B111 qualifies candidates later but does not establish this prerequisite policy.

## Prerequisites

- SAI-B003 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/judge/UPSTREAM_REVIEW.md
- services/judge/solver_judge/control/runner.py
- services/judge/solver_judge/control/diagnostics.py
- services/judge/tests/control/test_runner.py
- docs/security/JUDGE_SECURITY.md
- docs/onboarding/DEVELOPMENT.md

## Scope

- Record an owner/operator-approved production runtime support policy: trusted deployment inventory source, approved runtime/image identities, review owner, review deadline and rollback identity.
- Require production startup/diagnostics to validate the current daemon runtime identity against that approved inventory. An unverifiable identity or expired review must prevent readiness rather than infer patch status from the word runsc.
- Keep operator deployment/update actions separate from application configuration. Feed the approved policy into the existing B111 canary qualification work instead of creating another upgrade rehearsal.

## Acceptance criteria

- Fixtures for approved, unapproved, unverifiable and expired-review identities produce explicit safe readiness outcomes.
- Diagnostics distinguish declared identity, independently available runtime evidence and unknown provenance; hashing a local binary is not mislabeled proof of a remote daemon runtime.
- No host package is installed or runtime replaced by application startup, and documented development-only use of an older managed runtime cannot be described as production patched.

## Validation

- uv run --project services/api --frozen pytest services/judge/tests/control/test_runner.py
- Statically review the operator-approved runtime policy and inventory provenance; a real production approval cannot be invented by a coding agent.

## Out of scope

- Automatic host runtime upgrades
- A second canary implementation duplicating B111
- Independent sandbox certification or guaranteed freedom from vulnerabilities

## Risk and review

A self-asserted or stale inventory can create false confidence; policy approval and actual deployment evidence must have a named operator and expiry.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
