# [SAI-B121] Persist owned sandbox records and reconcile crash-orphaned containers

<!-- solver-ai-backlog:SAI-B121 -->
Order: 42 / Priority: P0 / Phase: 1-safe-pilot
Area: judge-recovery / Suggested role: Judge maintainer and recovery reviewer

Implementation status: planned

## Problem

The corrected runner retains failed cleanup names in _active and stops readiness, but that set disappears if the worker process crashes. A restart cannot distinguish its leftover sandboxes from unrelated containers, and the existing incident exercise does not implement recovery authority.

## Prerequisites

- SAI-B003 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/judge/solver_judge/control/runner.py
- services/judge/solver_judge/control/diagnostics.py
- services/judge/tests/control/test_runner.py
- docs/security/JUDGE_SECURITY.md
- docs/onboarding/DEVELOPMENT.md

## Scope

- Introduce a minimal private, atomically persisted sandbox-ownership journal written before container creation and cleared only after confirmed absence. Store generated container identity, approved image identity and lifecycle generation; never store source, test input, account identifiers or bearer material.
- Label newly created sandboxes with the same trusted ownership generation. On startup, perform one bounded reconciliation pass that validates both journal and actual container labels/image before removing an owned orphan.
- Treat malformed journal data, mismatched ownership, unreachable Docker and unresolved cleanup as unavailable readiness with sanitized diagnostics; preserve the record for an explicit operator retry.

## Acceptance criteria

- A simulated crash after create and before normal cleanup leaves a recoverable record; a fresh runner instance removes only the matching owned sandbox before becoming ready.
- An unrelated container or a journal entry with a mismatched ownership label/image is never removed automatically and cannot grant readiness.
- Journal permissions, atomic replacement, bounded size and redacted failure output are exercised; duplicate reconciliation is safe and no host execution fallback exists.

## Validation

- uv run --project services/api --frozen pytest services/judge/tests/control/test_runner.py
- On an explicitly approved isolated gVisor test host, run a finite one-container crash/restart fixture and record cleanup plus unchanged unrelated-container identity.

## Out of scope

- Sweeping every Docker container or deleting unknown state
- Persisting private program data or worker secrets
- A general distributed container orchestrator

## Risk and review

Automatic orphan cleanup is destructive unless ownership is established independently of an untrusted filename or container name; refuse ambiguous recovery.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
