# 0002 — Authenticated, isolated practice submissions

Date: 2026-11-14. Status: implementation for local validation; see PROJECT_STATUS for executed checks.

## Context

The practice foundation needs real accounts, owned submission history and actual program execution. Reusing mature session and sandbox implementations is preferable to writing authentication cryptography or treating an ordinary subprocess as an online judge. The repository has no selected outbound license; this decision does not select one.

## Decisions and upstream reuse

| Component | Exact release / reference | License | Integration |
| --- | --- | --- | --- |
| Better Auth | 1.7.23, `f39e6c66cc657e677b72828d0aff20b6ade2adae` | MIT | Dependency; official Next.js HTTP handlers, email/password sessions, migrations and JWT plugin |
| gVisor | Installed `release-20260413.0`, `b5e83db38775bc5a6e12857c388c84be3cc8871c` | Apache-2.0 | Existing Docker `runsc` runtime; every submitted program runs in this separate sandbox boundary |
| PyJWT | 2.15.1 | MIT | Fixed-algorithm validation of web-issued API tokens |
| cryptography | 50.0.2 | Apache-2.0 OR BSD-3-Clause | Ed25519 signature verification through PyJWT |
| Zod | 4.6.7 | MIT | Runtime validation of browser API contracts instead of unchecked JSON casts |

These projects are reused through their supported dependencies/runtime interfaces. Entire upstream repositories and unrelated product code are not copied into this monorepo. Exact dependency graphs and integrity hashes are recorded in lockfiles. The initial foundation's Next.js/React/Monaco choices remain in [0001](0001-practice-foundation.md).

## Session and ownership boundary

The web service owns Better Auth's SQLite database, password hashing, sessions and signing keys. Only its official HTTP handler performs account mutations, retaining library CSRF/origin checks. Local development generates a persistent random secret with private file permissions; it does not use a public development fallback. Database-backed local accounts do not yet provide verified email, recovery email or production identity administration.

The browser requests a short-lived signed API token using its session cookie. Tokens have a fixed issuer, `solver-api` audience, Ed25519 algorithm, immutable user subject and `token_use=solver_api`. The API obtains public keys only from the configured JWKS endpoint; token-provided key URLs and caller-provided user IDs are never authorities. Bearer tokens are not stored in browser localStorage. Local drafts remain local until an explicit run/submit action sends source code. Logout ends the web session; already issued API tokens can remain valid for up to five minutes.

The API stores submissions in a separate SQLite database, enforces ownership on list/detail, requires idempotency keys for writes, bounds source/request size and queue capacity, and limits per-user requests and concurrent work. A worker credential authorizes internal job leasing/completion and never reaches a submitted program. Job leases prevent two workers from accepting the same queued job; expired work becomes a terminal error rather than silently reexecuting source.

## Execution boundary

The trusted control worker is a separate host process with access to the rootless Docker daemon. Neither the web/API containers nor the submitted-program sandbox receive the Docker socket. The worker advertises readiness only after validating the required sandbox runtime and limits; there is no fallback to ordinary host execution or the default container runtime.

Each sandbox has no network, no workspace/credential mounts, an unprivileged user, dropped capabilities, no-new-privileges, a read-only root and bounded temporary storage. Submission source is passed as bounded input rather than mounted from the host. Compile/runtime CPU, address-space, process, file and output limits are distinct; a trusted external timeout and cleanup cover crashes of the inner harness. Proxy variables and host credentials are excluded from the submitted process environment.

Expected answers stay in the trusted control worker. Public runs use public samples; submission checking adds original generated edge cases. No private test data or expected answers are returned by the API. An accepted result means these finite checks passed, not a proof of correctness for every valid input. Original generators/oracles are committed; private runtime cases are not a copied problem dataset.

The current managed daemon has no cgroup memory/PID controller. Local enforcement therefore uses tested gVisor resource limits and strict process counts; address-space limits are per process, not a claim of cgroup-level aggregate accounting. The installed April runtime is older than upstream's November release. This is a bounded local development integration, not a public multi-tenant production release or independent security certification. A deployment needs maintained runtime images, separate infrastructure review, isolation regression tests, quotas and incident controls described in [Judge security](../../security/JUDGE_SECURITY.md).

## Alternatives inspected

- Stock [Piston](https://github.com/engineer-man/piston), commit `de2b365ac759670a3a0d13ea208a0869a92c7e64`: MIT wrapper, but its Docker deployment is privileged and its default memory limits are unsuitable here. Its pinned Isolate dependency is GPL-2.0-or-later; the full runtime is not an MIT-only licensing decision. Deferred.
- Stock [nsjail](https://github.com/google/nsjail), commit `d1d9af34c61daf834b843d58100a108c7cc2c574`: Apache-2.0; its documented Docker setup requires privileges unavailable to this application design. Deferred as a service foundation.
- Full contest/online-judge repositories: deferred because importing unrelated accounts, contest and operational stacks would replace the modular design and introduce additional licensing/security obligations.

The detailed runtime review and actual probe evidence are in `services/judge/UPSTREAM_REVIEW.md`. This adoption leaves the original project license and production hosting decisions with the maintainer.

## Operational implications

Native development can start the optional control worker after building the sandbox image. Normal web/API development remains usable when a judge is unavailable; execution fails closed with an explicit readiness explanation. Account and submission data persist in ignored local directories or Docker named volumes, separately from application source. Docker Compose does not mount a daemon socket into application containers. Startup, tests and local data handling are documented in [Development](../../onboarding/DEVELOPMENT.md).
