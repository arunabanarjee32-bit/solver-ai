# Project status — source of truth

Last reviewed: 2026-11-15 (Asia/Calcutta). Earlier gVisor and native integration evidence remains historical local validation; the SAI-010 PR additionally has a verified hosted CI run. Neither establishes a public production release.

## SAI-010: authenticated, provider-neutral offline hint contract

Branch `feat/sai-010-authored-hint-contract` introduces an authenticated `POST /api/v1/hints` API with fixed public catalog context, validated hint levels, explicitly authored (not AI-generated) output, a future-provider interface, bounded response, timeout and fail-safe provider errors. The existing problem page retains its unauthenticated author-written hint ladder. **No real model inference, debugging, generated solver, paid resource or production AI quota exists yet.** This work changes neither submission ownership nor the isolated judge; the new endpoint is not yet used by the browser UI. See [research and architecture audit](AUDIT_AND_AI_PLAN_2026-11-15.md).

**Hosted validation, 2026-11-15:** [GitHub Actions run 43737836616](https://github.com/arunabanarjee32-bit/solver-ai/actions/runs/43737836616) passed for commit `9df915a422c2a45d93d967b66a6cd30a228e6914`: API **137 passed** (29 hint API tests), auth passed, judge unit suite **91 passed / 15 intentionally skipped**, Ruff passed, TypeScript passed, optimized Next.js build and private-state packaging check passed, and Playwright browser suite **17 passed / 1 intentionally skipped**. The real gVisor integration suite and judge-enabled browser test were not run in hosted CI. The API suite emitted one upstream Starlette/HTTPX deprecation warning.

## Present now

- `apps/web`: Next.js/TypeScript practice catalog, original statements/samples, locally bundled Monaco Python/C++17 editor, isolated browser drafts, authored hint ladder and responsive UI.
- Better Auth accounts and session controls, official migrations, private persistent local keys/database, short-lived minimal API JWTs and scoped submission-history screens.
- `services/api`: public catalog, fixed-JWKS EdDSA authentication, durable owned SQLite submission/source history, bounded requests, idempotent writes, quotas, atomic worker leases, safe completion summaries and expiry handling. It never executes learner programs.
- `services/judge`: a separate trusted host control worker, gVisor-only sandbox runner, bounded original Python/C++17 supervisor, original generated grading cases, real sample/run verdicts, strict result protocol, readiness probes, cancellation and diagnostics.
- Native start/build/test commands, Docker web/API images with separate persistent volumes, an isolated sandbox Dockerfile, frozen lockfiles and CI configuration.
- Upstream reuse decisions in [0001](adr/0001-practice-foundation.md), [0002](adr/0002-authenticated-isolated-submissions.md), and [the runtime review](../services/judge/UPSTREAM_REVIEW.md). Better Auth/gVisor are narrow dependency/runtime adoptions; unrelated upstream repositories were not copied wholesale.

## Executed validation

| Check | Result |
| --- | --- |
| API catalog/authentication/queue suite | 108 passed; one visible upstream Starlette/HTTPX deprecation warning |
| Actual Better Auth library tests | 7 passed: key/database permissions, password hashing, cookie session, origins, minimal JWT/JWKS, logout and throttling |
| Judge unit suite | 91 passed |
| Real gVisor integration suite | 15 passed, explicitly enabled and executed |
| Full browser suite with a live judge | 18 passed; no skipped judge flow |
| Active-worker shutdown regression | Real SIGTERM during a sleeping gVisor job; container removed and worker finished in1.78 seconds |
| Source quality | Ruff, TypeScript and diff whitespace checks passed |
| Locked installation / dependency audit | Clean npm installation and audit verified; final build evidence recorded below |

Actual sandbox checks covered three correct Python solutions, a correct C++64-bit solution, WA/CE/RE/TLE/OLE, enforced address-space limits, prohibited forks/network/host files/credentials, temporary-filesystem quota, forged supervisor output, killing the supervisor, and cleanup. Memory-allocation failures without trustworthy aggregate accounting are reported conservatively as RE; program-written diagnostics do not establish MLE.

The full browser run created/restored accounts, exercised guest draft privacy, tested language isolation and editor retry, verified malformed/stalled API recovery, then performed a real sample AC, submission AC and submission WA. Those attempts persisted in owned history; a second account saw no attempts. Browser tests used temporary databases rather than developer accounts.

The normal `test:judge` command explicitly skips the15 sandbox tests unless enabled. Normal `test:e2e` explicitly skips its one full-judge flow. Their enabled runs above are the evidence; skipped tests are not counted as passes.

## Build and deployment evidence

The final native optimized build and web/API container builds passed. A packaging regression check rejected the earlier accidental local-database inclusion; runtime paths are now excluded and fresh native/container builds pass the private-state guard. The production Compose browser smoke passed account signup, authenticated API history via JWT/JWKS, persisted session after restarting both services, Monaco/local draft saving, mobile history and zero browser errors. CI is configured, but a hosted GitHub Actions execution has not been observed. No public deployment was performed.

## Remaining limitations

- This is a bounded local judge prototype, not a security certification. The installed gVisor runtime is `release-20260413.0`, older than the upstream November release observed during review. A public deployment needs maintained runtime infrastructure, independent review, host-wide budgets, broader hostile-code testing and incident/recovery controls.
- The managed rootless daemon has no cgroup memory/PID accounting. Tested gVisor per-process limits, strict process counts, tmpfs bounds and external deadlines apply; these are not aggregate peak-RSS measurements.
- Local email/password accounts have no delivered verification/recovery email. API JWTs can remain usable for up to five minutes after web-session logout. Local auth throttling uses shared per-path buckets until a trusted ingress is configured.
- SQLite and private file permissions support local persistence, not production encrypted storage, backups, retention/deletion policy or multi-region service operation.
- An AC result means a finite public/generated check set passed, not universal correctness or an external benchmark claim. Diagnostics and private grading data are not exposed in completion summaries.
- AI provider integration, generated tutoring/solver loops, training, contest/team/leaderboard features and public operations remain unimplemented. Hints are authored text.
- Original-code/content licensing and inbound contributor policy remain maintainer decisions. Dependency adoption is not a comprehensive legal or security audit.

## Next work

Review the merged implementation and hosted CI, then choose a maintained dedicated judge deployment and production identity/data policies. Preserve the current auth/ownership/queue/runtime tests. Add provider-neutral AI tutoring only behind authorized data and bounded budgets; no paid infrastructure or GPU training is provisioned by this change.

Update this ledger when behavior changes, separating executed tests, commits, hosted CI, environment publication and deployment. The complete P0/P1 product is not claimed finished.
