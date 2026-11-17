# [SAI-B124] Require a verified aggregate resource envelope for a production judge host

<!-- solver-ai-backlog:SAI-B124 -->
Order: 46 / Priority: P0 / Phase: 1-safe-pilot
Area: judge-isolation / Suggested role: Judge infrastructure engineer and security reviewer

Implementation status: planned

## Problem

The present managed rootless runtime lacks aggregate cgroup memory/PID accounting. Per-process rlimits and per-container tmpfs caps are real finite controls, but adding workers can exceed host-wide CPU, memory, process or temporary-storage budgets. B109 measures capacity; it does not enforce these limits.

## Prerequisites

- SAI-B003 (confirm prerequisite state in the catalogue)
- SAI-B121 (confirm prerequisite state in the catalogue)
- SAI-B123 (confirm prerequisite state in the catalogue)
- SAI-B125 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/judge/solver_judge/control/runner.py
- services/judge/solver_judge/control/diagnostics.py
- services/judge/tests/control/test_runner.py
- services/judge/tests/sandbox
- docs/security/JUDGE_SECURITY.md
- docs/onboarding/DEVELOPMENT.md

## Scope

- Define one explicit operator-provisioned dedicated-host production resource envelope, including aggregate CPU, memory, PID, running-sandbox and temporary-storage ceilings; preserve the current bounded development mode as a clearly separate mode.
- Add production preflight that verifies supported aggregate controls and the selected host/cgroup assignment before advertising readiness. Pass only reviewed fixed resource arguments to Docker and retain existing per-process, no-network and output controls.
- Fail production readiness when accounting/enforcement cannot be verified or owned orphan usage exceeds the declared envelope. Do not install or reconfigure the managed daemon or claim that a CLI flag alone proves enforcement.

## Acceptance criteria

- Mocked unsupported/missing/mismatched aggregate-control states refuse production readiness and cannot silently select the development policy.
- On an approved dedicated test host, finite original multi-process/concurrent sandbox fixtures demonstrate the declared aggregate caps and controlled recovery; report which resource dimensions were actually measured.
- The supported development configuration retains its explicit limitations, and no new accurate-MLE or sandbox-certification claim is made without trustworthy evidence.

## Validation

- uv run --project services/api --frozen pytest services/judge/tests/control/test_runner.py
- Run only the new explicitly enabled, finite aggregate-budget fixtures on an operator-approved dedicated gVisor host; mark them blocked rather than passed on the current unsupported managed runtime.

## Out of scope

- Provisioning paid hosts or changing the cloud daemon automatically
- A multi-host scheduler or unlimited stress testing
- Claiming protection from --memory or --pids-limit when the daemon reports no enforcement

## Risk and review

Resource flags can be ignored by unsupported runtimes; readiness must depend on observed controls, not desired configuration. Host provisioning remains an external operator prerequisite.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
