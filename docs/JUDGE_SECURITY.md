# Untrusted code execution and online judge threat model

**Critical:** This is a security design proposal, not a security certification.

## Threats

Submitted programs may try to consume unlimited CPU/memory/disk, fork bombs, read secrets, escape the container, inspect other submissions, connect to the network, query cloud instance metadata or exploit toolchain vulnerabilities. AI-generated code is equally untrusted.

## Required controls

- Compile and execute in workers **isolated from** web/API processes, control-plane credentials and production DB.
- Use a proven isolation boundary (carefully configured containers plus defense in depth, VM/microVM where justified). Containers alone are not automatically safe.
- No default outbound network, host filesystem mounts, privileged mode, Docker socket or cloud metadata access.
- Run as unprivileged user; drop Linux capabilities; apply seccomp/AppArmor/landlock/other OS controls as appropriate.
- Enforce wall-clock/CPU, memory, PID, file size, output size and disk limits; cap compile time separately.
- Use per-job ephemeral filesystems and non-shared working directories; cleanup after execution.
- Bound source code, stdin and stderr size; sanitize rendered output; protect test secrets.
- Validate language runtimes/compiler flags and reject unsafe custom arguments.
- Encrypt/limit access to test cases and grading oracles; redact private tests from user-visible errors and model feedback.
- Authenticate submissions and throttle abuse; queue jobs; handle cancellation, retries, stuck jobs and duplicate callbacks.
- Pin and update compiler/runtime images; scan dependencies; monitor judge errors/escape attempts.
- Test deliberate malicious programs, TLE, OOM, fork/IO abuse and cross-tenant isolation before internet exposure.

## Judge adapter interface

App submits a versioned problem and source artifact to a job queue. Authorized worker obtains test manifest, compiles/runs, applies scoring and emits a structured result. External runner/sandbox is behind adapter. Only the API may authorize user access to status.

Verdict vocabulary: QUEUED, COMPILING, RUNNING, AC, WA, CE, RE, TLE, MLE, OLE, SYSTEM_ERROR. Include deterministic limits, runtime version, exit status and capped logs.

## Piston / alternative judge choice

Self-hosted Piston is one candidate, **not assumed secure by default**. Audit its deployment model and isolation capabilities for internet-facing multi-tenant operation. If requirements are unmet, select a stronger worker architecture or improve containment. Never use a shared public code-execution API for production by assumption.

## Release gate

Independent review of execution isolation and deployment manifests; hostile-code test suite; enforced quotas; incident plan; immutable per-run provenance. No production exposure until these pass.
