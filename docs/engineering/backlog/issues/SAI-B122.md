# [SAI-B122] Bind controller credentials to registered worker identities

<!-- solver-ai-backlog:SAI-B122 -->
Order: 43 / Priority: P0 / Phase: 1-safe-pilot
Area: worker-auth / Suggested role: Backend security engineer and judge maintainer

## Problem

require_worker currently authenticates one shared bearer, while heartbeat, lease and completion accept a caller-supplied worker_id. Any holder belongs to the entire controller trust domain and can register or impersonate another worker; token-strength and rotation tasks do not establish separate principals.

## Prerequisites

- SAI-B009 (publish/complete prerequisite first)
- SAI-B010 (publish/complete prerequisite first)
- SAI-B013 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/main.py
- services/api/solver_api/features/submissions/store.py
- services/judge/solver_judge/control/worker.py
- services/api/tests/submissions/test_submissions.py
- services/judge/tests/control/test_worker.py
- docs/onboarding/DEVELOPMENT.md

## Scope

- Resolve an authenticated controller credential to one owner-registered stable worker principal and bind every internal route payload to that principal rather than trusting worker_id alone.
- Retain a bounded per-principal current/previous credential overlap using the rotation mechanism from B010; provide an explicit single-worker development configuration rather than an implicit production shared-key fallback.
- Reject unknown identities and cross-principal heartbeat, lease and completion operations with closed safe errors; document credential provisioning and revocation without writing actual secrets into Git.

## Acceptance criteria

- Two configured worker fixtures can operate only under their registered identities; the credential for A cannot register, renew, lease as or complete a lease belonging to B.
- Rotating or revoking A leaves B unaffected and preserves only the deliberately allowed bounded overlap for A.
- The normal configured single-worker local workflow remains supported, while production mode refuses an unbound shared credential; no secret appears in logs or capability output.

## Validation

- uv run --project services/api --frozen pytest services/api/tests/submissions/test_submissions.py
- uv run --project services/api --frozen pytest services/judge/tests/control/test_worker.py

## Out of scope

- Building a certificate authority or automatic worker registration service
- Rotating real deployment credentials without operator approval
- Treating per-worker identity as protection against a malicious trusted Docker host

## Risk and review

An identity migration can lock out valid workers or accidentally widen completion rights; use explicit compatibility and cross-principal denial fixtures.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
