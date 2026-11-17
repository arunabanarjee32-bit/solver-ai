# Project status — source of truth

Last reviewed: 2026-11-17 (Asia/Kolkata). Earlier gVisor and native integration evidence remains historical local validation; the merged SAI-010 work additionally has a recorded hosted CI run. Neither establishes a public production release.

## Post-relocation validation and contributor backlog (2026-11-17)

The owner resumed testing after the functional moves. API **137**, auth **7**,
judge **118** (including all **15** live gVisor cases), browser **25**, and
publication safety **11** cases passed. Ruff, TypeScript, optimized build and
private-state guard, frozen installation and local production Compose build/smoke
passed. The only layout-related failure was import formatting in a relocated
judge test; it was fixed. The archived research applications remain inactive.

A [127-task ordered backlog](../engineering/backlog/README.md) now gives other
implementation tools concrete ownership paths, dependencies, scope and acceptance
criteria. [Review instructions](../engineering/AI_CONTRIBUTION_WORKFLOW.md) require
review before authorized merges. These are plans, not implemented AI/contest
features or an unattended assistant service.

**Actual GitHub publication is blocked:** the environment denies `api.github.com`
before API requests reach GitHub. The publisher stopped before any issue POST;
**zero remote issues were created**. The additive network draft is saved but
requires review/save and environment publication. Existing API credentials are
present; issue-write permissions cannot be tested until networking permits it.
See the [actual receipt](../engineering/backlog/publication.json) and
[current validation record](../../AnalyseFuture/validation/TEST_AND_VALIDATION_REPORT.txt).

## Historical functional organization update — testing paused (2026-11-17)

The owner explicitly requested functional file grouping without running tests or
builds. Active documentation is now grouped under `docs/onboarding`,
`docs/architecture`, `docs/product`, `docs/research`, `docs/governance`,
`docs/engineering`, `docs/security` and `docs/status`; `docs/INDEX.md` remains the
entry point. The earlier root project idea is retained in
`docs/product/PROJECT_IDEA.txt`. Existing working edits were preserved during
the moves, and relative documentation links were updated.

No tests, lint, builds, runtime startup or validation scripts were run for this
reorganization, as instructed. The results below are historical evidence from
earlier revisions and work phases; they do not validate the newly moved layout.
This organization change is not a new production-readiness claim.

## Repository organization and project proposal (2026-11-17)

The existing web/API/judge paths are retained. Both uploaded ZIPs and all 122
extracted files are preserved in `AnalyseFuture/`, with original path and SHA-256
inventories and a verifier included in CI. Five supplied dataset files are LFS
pointers; their underlying data is not present. Upstream code was not installed,
run or adopted as an active feature. The review does not attribute the owner's
reported repository disruption. See [repository structure](../architecture/REPOSITORY_STRUCTURE.md)
and the detailed [project idea](../product/PROJECT_IDEA.txt).

Docker context and standalone tracing exclude the preservation folder, and the
packaging guard rejects its inclusion. Current local validation of source and
configuration commit `596d9c2` is recorded separately from historical results;
subsequent commits in this task update documentation only.

Current local checks after the preservation/configuration changes: API **137
passed**, Better Auth **7 passed**, judge suite **106 passed** including all **15
gVisor integration tests**, Ruff passed, TypeScript passed, optimized Next.js
build and private-state/reference-folder packaging guard passed. Archive/index
verification passed for both ZIPs and all 122 members. The API emitted one
upstream Starlette/HTTPX deprecation warning. The full-judge Playwright browser
suite **passed all 18 tests, with no skips**, including actual isolated runs,
submissions and private history (50.2 seconds). A deliberate reference-folder
injection was rejected by the packaging guard, then removed and the clean
artifact passed again. All 109 baseline tracked files remain at their recorded
paths (including both archive moves); no file was discarded. No new hosted CI
or public deployment result is claimed here.

## SAI-010: authenticated, provider-neutral offline hint contract

The merged SAI-010 implementation provides an authenticated `POST /api/v1/hints` API with fixed public catalog context, validated hint levels, explicitly authored (not AI-generated) output, a future-provider interface, bounded response, timeout and fail-safe provider errors. The existing problem page retains its unauthenticated author-written hint ladder. **No real model inference, debugging, generated solver, paid resource or production AI quota exists yet.** This work changes neither submission ownership nor the isolated judge; the new endpoint is not yet used by the browser UI. See [research and architecture audit](../research/AUDIT_AND_AI_PLAN_2026-11-15.md).

**Hosted validation, 2026-11-15:** [GitHub Actions run 43737836616](https://github.com/arunabanarjee32-bit/solver-ai/actions/runs/43737836616) passed for commit `9df915a422c2a45d93d967b66a6cd30a228e6914`: API **137 passed** (29 hint API tests), auth passed, judge unit suite **91 passed / 15 intentionally skipped**, Ruff passed, TypeScript passed, optimized Next.js build and private-state packaging check passed, and Playwright browser suite **17 passed / 1 intentionally skipped**. The real gVisor integration suite and judge-enabled browser test were not run in hosted CI. The API suite emitted one upstream Starlette/HTTPX deprecation warning.

## Present now

- `apps/web`: Next.js/TypeScript practice catalog, original statements/samples, locally bundled Monaco Python/C++17 editor, isolated browser drafts, authored hint ladder and responsive UI.
- Better Auth accounts and session controls, official migrations, private persistent local keys/database, short-lived minimal API JWTs and scoped submission-history screens.
- `services/api`: public catalog, fixed-JWKS EdDSA authentication, durable owned SQLite submission/source history, bounded requests, idempotent writes, quotas, atomic worker leases, safe completion summaries and expiry handling. It never executes learner programs.
- `services/judge`: a separate trusted host control worker, gVisor-only sandbox runner, bounded original Python/C++17 supervisor, original generated grading cases, real sample/run verdicts, strict result protocol, readiness probes, cancellation and diagnostics.
- Native start/build/test commands, Docker web/API images with separate persistent volumes, an isolated sandbox Dockerfile, frozen lockfiles and CI configuration.
- Upstream reuse decisions in [0001](../architecture/adr/0001-practice-foundation.md), [0002](../architecture/adr/0002-authenticated-isolated-submissions.md), and [the runtime review](../../services/judge/UPSTREAM_REVIEW.md). Better Auth/gVisor are narrow dependency/runtime adoptions; upstream research snapshots are preserved only in `AnalyseFuture` and are not adopted into the application.

## Historical local validation before SAI-010

The 108-test API result below predates the 137-test SAI-010 suite recorded above.
These historical results are retained rather than treated as this revision's run.

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

The historical native optimized build and web/API container builds passed. A packaging regression check rejected the earlier accidental local-database inclusion; runtime paths were excluded and fresh native/container builds passed the private-state guard. The historical production Compose browser smoke passed account signup, authenticated API history via JWT/JWKS, persisted session after restarting both services, Monaco/local draft saving, mobile history and zero browser errors. The later hosted SAI-010 run is recorded above; these earlier container results are not checks of the current revision. No public deployment was performed.

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
