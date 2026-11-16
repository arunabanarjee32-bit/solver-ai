# Development

Solver AI has a local practice workflow: original problems, Monaco Python/C++17 drafts, Better Auth accounts, owned submission history, and optional real gVisor-backed sample runs and submissions. Authored hints are static educational content; AI inference is not integrated. This is local development infrastructure, not a production judge certification.

## Native setup

Use the existing isolated checkout in cloud tasks; do not create a Git worktree unless explicitly requested. Use Node24.22.1 (`.node-version`), Python3.12.14 (`.python-version`) and uv0.13.6 from its official distribution. No external identity provider, model key, paid service or database server is required.

From the repository root:

```sh
export UV_CACHE_DIR="${UV_CACHE_DIR:-/tmp/solver-ai-uv-cache}"
npm ci
uv sync --project services/api --frozen
npm run dev
```

Open `http://127.0.0.1:3000`. The API is on `127.0.0.1:8000`, with `/health` and `/docs`. The runner stops both processes on Ctrl-C or either child exiting. The API does not auto-reload in this runner; restart after Python changes. Next.js refreshes frontend changes automatically. Normal `npm run dev` supports accounts, catalog, editing and history; execution stays unavailable until an isolated worker advertises verified readiness.

Better Auth applies its official migrations lazily on first use. `npm run auth:migrate` is also available and idempotent. Local signup requires a password of at least12 characters. Email verification and password-recovery delivery are not configured; do not use this local account setup as production identity administration.

To run services independently:

```sh
# Terminal1, from repository root
cd services/api
.venv/bin/uvicorn solver_api.main:app --reload --host 127.0.0.1 --port 8000
```

```sh
# Terminal2, repository root
npm run dev:web
```

## Offline hint API (SAI-010)

The API has an optional authenticated `POST /api/v1/hints` contract, with a JSON object `{"problem_slug":"signal-sum","level":1}` and a valid short-lived `solver-api` Bearer token issued by Better Auth. Levels 1–3 return the existing **author-written** public hint with `source="authored"`, `provider=null`, `ai_generated=false` and `schema_version="1"`. The browser preserves its public authored hint ladder and also mounts the recovered signed-in account-hint service. Its typed client validates provenance, uses the existing JWT boundary and supports cancellation, a ten-second deadline and retry. Neither path makes a model call.

The web feature owners are `features/accounts`, `features/practice`,
`features/hints` and `features/submissions`, below `apps/web`. Framework routes
remain in `app/`, and shared navigation/icons remain in `components/`. See
[repository structure](REPOSITORY_STRUCTURE.md) and the
[path mapping](../AnalyseFuture/ORIGINAL_TO_NEW_PATH_MAPPING.txt).

`SOLVER_HINT_BACKEND=authored` (the default) requires no AI provider key, outbound model request, new database, or paid service. Any other setting fails with `HINT_PROVIDER_UNAVAILABLE` until a separately reviewed provider is implemented. Source code, hidden grading tests and worker credentials are not inputs to this hint API. The future real-provider adapter must supply per-account quotas, token and cost budgets, controlled egress, contest-integrity enforcement and privacy review before enablement.

## Real isolated judging

The trusted control worker requires a working **rootless** Docker daemon with the gVisor `runsc` runtime registered. This managed image supplies it. Ordinary Docker containers or host subprocesses are never a fallback. Other development machines need a supported gVisor installation; see [upstream instructions](https://gvisor.dev/docs/user_guide/install/). Do not change the managed cloud daemon or install an unrelated VPN to bypass restrictions.

Build the sandbox, then start all three processes:

```sh
# Ordinary developer machine
npm run judge:build
npm run dev:judge
```

In this managed cloud, retain its TLS trust for networked build steps:

```sh
npm run judge:build:cloud
npm run dev:judge
```

The worker performs finite isolation/resource/compiler probes before advertising readiness. Create an account, open a problem, edit your solution, then choose **Run samples** or **Submit solution**. The first uses public samples; submissions add original worker-generated edge cases. The UI polls actual queued/running/finished status and stores the real result in your account history. Passing finite checks is not proof of correctness on every input. Source is sent only when you explicitly run or submit; ordinary editing remains in browser storage.

The worker has no API/web credentials inside its sandbox. Expected answers remain outside the sandbox. CPU, address-space, process, output and temporary-file limits are enforced, with an external wall deadline and cleanup on shutdown. Memory limits are per process; this rootless environment lacks cgroup aggregate accounting. Allocation failures without trustworthy memory accounting are reported conservatively as runtime errors, not inferred from program-written text. See [the decision](adr/0002-authenticated-isolated-submissions.md) and [runtime review](../services/judge/UPSTREAM_REVIEW.md).

## Data and credentials

- Browser drafts are separate per problem/language in localStorage. They are best effort and not account backups; copy important work elsewhere.
- `apps/web/.local` contains the Better Auth SQLite database and a generated private signing/session secret. `services/api/.local` contains owned submission data. `.local/judge-worker-token` is the generated local worker credential. These directories are ignored by Git and excluded from Docker build contexts.
- Preserve the web database and its secret together to retain working sessions/keys. Do not commit or share these files. A fresh local workspace generates its own high-entropy secret; there is no shared development key.
- The API uses public JWKS verification, not the web's secret or caller-supplied user IDs. Bearer tokens last five minutes; existing tokens can remain valid briefly after web-session logout.
- Local SQLite data is protected by file permissions, not a claim of production encrypted storage, retention controls or backups. Deleting local databases removes their local accounts/history; do that only deliberately after stopping the services.

Configuration names are `AUTH_URL` (default local origin), `AUTH_DB_PATH`, optional `AUTH_SECRET_PATH`/`BETTER_AUTH_SECRET`, API `AUTH_ISSUER`/`AUTH_JWKS_URL`/`SOLVER_DB_PATH`, and worker `JUDGE_API_URL`/`JUDGE_SANDBOX_IMAGE`/`JUDGE_WORKER_TOKEN`. External origins require HTTPS. The native runner generates and passes the local worker credential without logging it. `API_BASE_URL` remains a server-only Next.js rewrite setting; set it before build/dev when changing the API upstream.

## Verification

From the root with dependencies installed:

```sh
npm run test:api
npm run test:auth
npm run test:judge
uv run --project services/api --frozen ruff check services/api services/judge scripts
npm run typecheck
npm run build
npx playwright install chromium
npm run test:e2e
```

The normal judge suite explicitly skips real sandbox tests; the normal browser suite explicitly skips the full judge flow. To execute those checks after building the sandbox image:

```sh
npm run test:judge:integration
npm run test:e2e:judge
```

Tests start their own API/web/optional worker and require free ports3000/8000. Browser tests use separate temporary account/submission databases, preserving developer data. Local shutdown tests exercise active-container cleanup. The suites distinguish disabled/unrun integration tests from passes.

This managed image has `/usr/bin/chromium`; run browser suites with `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium` to use it. The current policy blocks `cdn.playwright.dev`, so local validation uses installed Chromium. Normal CI/developer machines can use Playwright's pinned download; Linux dependencies may require `npx playwright install --with-deps chromium`. Set `PLAYWRIGHT_BROWSERS_PATH=/tmp/solver-ai-browsers` for installation and testing if a home cache is not writable. Root `.npmrc` already uses a writable task cache.

CI runs API/auth/judge unit tests, lint, type checking, the optimized build and browser checks. Its standard runner does not supply the audited rootless gVisor runtime, so actual sandbox/full-judge checks are separately executed locally and gated explicitly. Adding or pushing a workflow does not establish a hosted CI pass.

The root build also checks standalone packaging: runtime databases, local keys, Git metadata and environment files must stay out of the distributable artifact. Runtime authentication paths are excluded from tracing; keep this guard when changing state locations or build configuration.

## Docker Compose

Compose provides persistent account/submission volumes and read-only, nonroot web/API containers. Application containers have no Docker socket. The default Compose configuration intentionally does not enable a control worker; use the native full-judge workflow above for execution.

```sh
docker compose up --build --wait
curl --fail http://127.0.0.1:8000/health
curl --fail http://127.0.0.1:3000/api/v1/problems
docker compose down
```

For managed TLS inspection:

```sh
docker compose -f compose.yaml -f compose.cloud.yaml build
docker compose up --wait --no-build
```

The optional build file mounts the system CA bundle as a BuildKit secret only during networked steps. Never disable TLS verification or bake session CA material into images. Named volumes preserve local accounts and history across `down`/`up`; do not use `down --volumes` unless you intend to erase them. Published ports bind only to loopback. The web image bakes its API rewrite to `http://api:8000` and initializes account tables through the official migration path on first use.

For a native production-mode smoke, stop dev, keep the API running, run `npm run build` then `npm run start:web`. This is a build-mode check, not a deployment. The installed April gVisor runtime is older than upstream's November release; a public release requires maintained runtime/security review, production identity, operational quotas and the gates in JUDGE_SECURITY.md.

## Dependency reuse

Monaco and its worker are bundled locally with the pinned patched sanitizer and distributed notices; no editor CDN, remote font or model call is required. Better Auth is reused as a dependency and gVisor as an existing isolated runtime. Stock Piston/nsjail deployments were reviewed and deferred; they were not copied into the application. See [upstream decisions](adr/0002-authenticated-isolated-submissions.md). Original project licensing remains a maintainer decision.
