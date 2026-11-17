# [SAI-B111] Create a canary qualification gate for judge runtime upgrades

<!-- solver-ai-backlog:SAI-B111 -->
Order: 54 / Priority: P1 / Phase: operated-pilot
Area: operations-release / Suggested role: Judge maintainer and security reviewer

## Problem

Maintaining isolation requires a repeatable way to evaluate a runtime/toolchain update before broad rollout.

## Prerequisites

- SAI-B110 (publish/complete prerequisite first)
- SAI-B125 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/judge/UPSTREAM_REVIEW.md
- services/judge/Dockerfile
- services/judge/tests/sandbox
- services/judge/solver_judge/control/diagnostics.py
- scripts/verification

## Scope

- Add a proposed comparison runbook/report for an operator-provided approved candidate runtime or image.
- Run existing hostile-program, cleanup and language fixtures on the candidate before allowing a canary decision.

## Acceptance criteria

- Reports name old/new runtime and image identifiers and every executed/skipped check.
- A failed isolation/cleanup probe blocks qualification even when correct solutions pass.
- The process does not replace the managed host daemon or silently fall back to ordinary containers.

## Validation

- npm run test:judge:integration
- uv run --project services/api --frozen pytest services/judge/tests/control/test_runner.py

## Out of scope

- Installing host runtimes automatically
- Claiming independent security certification

## Risk and review

A toolchain update can weaken isolation or alter resource semantics.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
