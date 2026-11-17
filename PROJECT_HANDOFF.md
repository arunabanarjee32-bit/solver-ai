# Solver AI: project guide and complete implementation handoff

This is the homepage handoff for **Solver AI**, the DSA, competitive-programming
and ICPC practice project in `arunabanarjee32-bit/solver-ai`. Give another coding
tool this file together with [AGENTS.md](AGENTS.md). It explains what works,
where every tracked file belongs, and the detailed work still to complete.

This document is generated from the reviewed file inventory, feature inventory
and canonical task catalogue. Update their sources and regenerate it when the
implementation changes; the maintenance commands are at the end.

## Navigation

- [Main goal and current user journey](#main-goal-and-current-user-journey)
- [DSA solver and fine-tuning delivery](#dsa-solver-and-fine-tuning-delivery)
- [Current evidence and remaining limits](#current-evidence-and-remaining-limits)
- [How another tool should continue](#how-another-tool-should-continue)
- [Every feature: implemented, partial and proposed](#feature-register)
- [Every folder and its responsibility](#complete-folder-map)
- [Every tracked file and its purpose](#complete-file-map)
- [Ordered task index](#ordered-task-index)
- [Complete task specifications](#complete-task-specifications)
- [PR review and merge process](#pr-review-and-merge-process)
- [Keeping this handoff current](#keeping-this-handoff-current)

## Main goal and current user journey

Build an independently controlled learning platform where people can practice
authorized algorithm problems, write code, receive isolated judge verdicts,
understand mistakes, and eventually get measured AI tutoring. Later milestones
add virtual contests, ICPC team practice, bounded candidate solution generation
and licensed-data model research. Product quality, original or authorized content,
privacy and reproducible evidence are the foundations.

The current local journey is: browse/search/filter the three original seed
problems → open a statement and samples → edit Python or C++17 in Monaco → keep
private browser drafts → create/sign into a local account → run or submit through
the separate gVisor judge → inspect the owned submission history and finite
verdict. Public author-written hints and an authenticated author-written hint
request interface are available. These hints are authored content; live AI
generation has not been implemented.

The architecture keeps three boundaries: Next.js/TypeScript owns the browser and
account service; FastAPI/Python owns the catalog, authenticated APIs and durable
submission queue; the trusted Python judge worker controls separate gVisor
sandboxes for learner Python/C++17 programs. Expected answers and host credentials
stay outside the learner sandbox. SQLite supports local state. PostgreSQL and
larger-scale service operations are future work.

Keeping TypeScript for browser/Next.js code and Python for API/judge control is
intentional. Learner languages are a separate product capability. A rewrite into
one language is unnecessary for this handoff and is not an assigned task; shared
HTTP contracts and feature ownership connect the existing services.

## DSA solver and fine-tuning delivery

The main ambition is broad competence on previously unseen DSA problems. A ready
system must attempt supported formats within a budget, generate/explain code,
test it through the isolated judge and report observed results or a clear failure.
No completed task list, model checkpoint or finite evaluation guarantees solving
every possible problem. Track coverage by topic, difficulty, language and format.

Read the [complete readiness checklist](docs/product/DSA_SOLVER_READINESS.md) and
[fine-tuning model research catalogue](docs/research/FINETUNING_MODEL_RESEARCH.md).
**No checkpoint or model family is selected.** The catalogue compares a broad
set of open-weight families and API-baseline alternatives for future research;
it does not claim to enumerate every model or declare a universal best model.

The solver delivery work includes supported-problem contracts; reviewed
evaluators; permitted disjoint training/evaluation data; empirical model
comparison; reproducible SFT/LoRA/QLoRA tooling; approved external smoke and real
training runs; artifact/base/tokenizer lineage; matched-budget held-out and
regression evaluation; qualified inference, pilot and rollback; and controlled
failure-driven improvement. Optional preference/RL work follows reliable rewards
and separate approval. No weights, GPU job, provider or training is activated here.

**B080 is only the training admission gate.** Appended training-delivery tasks
cover actual future implementation and execution beyond it. They remain planned.
Use each card's prerequisites; unrelated contest/business tasks do not become
mandatory ML dependencies merely because they appear earlier in the index.

## Current evidence and remaining limits

The full `npm run test:all` gate passed with exit status **0** at source revision
`33ed42f0b42b43e228c547cfc106c5c874bc61d1`: **337 cases** (137 API, 7 auth,
118 judge including 15 real gVisor cases, 50 repository-tooling cases, and
25 enabled browser cases), plus lint, TypeScript, optimized build and the
private-state packaging guard. The current handoff change is documentation and
documentation generation; that earlier run is named-revision evidence, not a
claim that new application behavior was tested here. See the
[status ledger](docs/status/PROJECT_STATUS.md) and
[validation report](AnalyseFuture/validation/TEST_AND_VALIDATION_REPORT.txt).

Local production-mode builds/Compose smoke checks are recorded. A public
production release, production security certification, current hosted full
gVisor CI, real AI provider, verified general solver, contests, model training,
payments and institution operations are **not implemented**. Finite judge cases
do not prove correctness on every possible input. Perfect AI solving and guaranteed
future model breakthroughs cannot be promised. One-year/two-year/later research
horizons in the [future vision](AnalyseFuture/planning/PROJECT_VISION_AND_FUTURE_ROADMAP.txt)
are conditional plans rather than deadlines or completed features.

Both uploaded ZIPs, all 122 extracted members and 23 historical branch snapshots
are preserved in `AnalyseFuture/`. They are inactive evidence/research, not adopted
product modules. Five archived dataset files contain LFS pointers without their
underlying datasets. Preserve their bytes and provenance. The repository audit
does not establish who caused the reported disruption or certify that a GitHub
account compromise has been resolved.

Git fetch/push works. GitHub API access is currently blocked by the environment's
`api.github.com` network policy. The local task cards are prepared, but **zero
remote issues have been confirmed created**. An additive network-settings draft
requires review/save and environment publication; permissions must then be
verified. Consult the [publication receipt](docs/engineering/backlog/publication.json)
before claiming any issue exists. No background assistant monitor or automatic
merge service is running.

## How another tool should continue

1. Read this file, [AGENTS.md](AGENTS.md), the
   [current status](docs/status/PROJECT_STATUS.md),
   [development guide](docs/onboarding/DEVELOPMENT.md) and the relevant feature code.
   Search for existing implementation before adding another version.
2. Claim **one** ready task below. Use the **Order** column, not the numeric ID
   suffix. Verify its prerequisites; independent ready tasks can proceed in
   parallel when their ownership and contracts do not conflict.
3. The next governance tasks include **SAI-B127** (actual reviewer identities and
   branch rules), **SAI-B002** (owner licensing/contribution decision) and
   **SAI-B003** (pilot/privacy/data lifecycle charter). These require their named
   owner decisions. Ready engineering work such as **SAI-B004** can proceed within
   its scope while those decisions are pending. Do not invent approvals.
4. Keep changes in the named functional collection. Preserve account ownership,
   queue leases, hidden grading data and the sandbox boundary. Never run learner
   programs in the host/API/web process or substitute ordinary containers when
   gVisor is unavailable. Preserve old/uncertain work with provenance in
   `AnalyseFuture/`; keep secrets/private runtime data outside Git.
5. Create a focused branch and PR for other-tool implementation. Include the
   stable local task ID/card if no GitHub issue exists, exact head revision,
   observed before/after behavior, changed paths, prerequisites, checks actually
   run, remaining risks and rollback. Fill the PR evidence record honestly.
6. Run the checks relevant to the task and the required gates. Record failures,
   skips and unrun checks. Do not weaken security or fabricate test results.
7. Update status, feature/file records and this handoff for behavior actually
   implemented. Request maintainer/assistant review; do not self-merge.

Do not purchase compute, activate a paid provider, send private submissions to
external services, train on datasets, settle licensing or release to production
without the stated owner approval. Task assignment does not grant those choices.
The owner has separately authorized this maintenance session's direct-to-`main`
checkpoint commits; other-tool contributions use the reviewed PR workflow.

## Feature register

Reviewed feature records: **44**. The status below describes the feature, not whether every production hardening task is complete. An active workflow can still have recorded gaps.

| Status | Meaning |
| --- | --- |
| Implemented locally | Active source workflow with recorded local evidence; production gaps can remain. |
| Partial | Some supporting work exists; the complete workflow is blocked or unfinished. |
| Planned | Feasible proposal; not an implemented product feature. |
| Research only | Inactive upstream experiment or future investigation; not product integration. |

### F001: Monorepo toolchain and native startup

**Status:** Implemented locally. **Owner:** repository orchestration.

One product with independent web/API/trusted worker processes, pinned tools and generated private local worker credential.

**Files / evidence:** [package.json](package.json); [.node-version](.node-version); [.python-version](.python-version); [scripts/development/dev.py](scripts/development/dev.py); [scripts/development/local_config.py](scripts/development/local_config.py); [scripts/development/judge-worker.py](scripts/development/judge-worker.py).

**Dependencies:** Node 24; Python 3.12; uv; npm workspaces.

**Recorded checks / references:** `npm run dev`; `npm run dev:judge`.

**Remaining gaps / conditions:**

- Live processes restart in each task; environment-specific runtime assumptions must be checked.

### F002: Continuous checks and regression orchestration

**Status:** Implemented locally. **Owner:** repository CI.

Run meaningful source/unit/browser/build checks and retain failure artifacts.

**Files / evidence:** [.github/workflows/ci.yml](.github/workflows/ci.yml); [playwright.config.ts](playwright.config.ts); [package.json](package.json).

**Dependencies:** GitHub Actions; pytest; Ruff; TypeScript; Playwright.

**Recorded checks / references:** `API/auth/judge suites`; `typecheck`; `build`; `browser suites`.

**Remaining gaps / conditions:**

- Hosted default CI skips real sandbox/full-judge integrations; pin Actions immutably and keep separate integration evidence.

### F003: Catalog search, filters and pagination

**Status:** Implemented locally. **Owner:** web + API.

Search/filter original exercises through validated API-backed UI.

**Files / evidence:** [apps/web/features/practice/catalog.tsx](apps/web/features/practice/catalog.tsx); [apps/web/features/practice/api.ts](apps/web/features/practice/api.ts); [apps/web/app/page.tsx](apps/web/app/page.tsx); [services/api/solver_api/main.py](services/api/solver_api/main.py).

**Dependencies:** Next.js; FastAPI; validated catalog contract.

**Recorded checks / references:** `services/api/tests/catalog/test_api.py`; `tests/e2e/practice/practice.spec.ts`; `tests/e2e/practice/resilience.spec.ts`.

**Remaining gaps / conditions:**

- Only three seed problems; current client fetch cap is 100; no large catalog search/indexing.

### F004: Original statements, samples, starters and provenance

**Status:** Implemented locally. **Owner:** API content + web workspace.

Three original problems expose readable constraints, examples, starter code and author/source information without hidden cases.

**Files / evidence:** [services/api/solver_api/features/catalog/content.py](services/api/solver_api/features/catalog/content.py); [services/api/solver_api/features/catalog/models.py](services/api/solver_api/features/catalog/models.py); [apps/web/features/practice/workspace.tsx](apps/web/features/practice/workspace.tsx); [apps/web/app/problems/[slug]/page.tsx](apps/web/app/problems/%5Bslug%5D/page.tsx).

**Dependencies:** Pydantic; original problem content; Python/C++17 starter templates.

**Recorded checks / references:** `services/api/tests/catalog/test_api.py`; `tests/e2e/practice/practice.spec.ts`.

**Remaining gaps / conditions:**

- No permissioned authoring/versioning/import workflow yet.

### F005: Responsive shared UI and basic accessibility

**Status:** Implemented locally. **Owner:** web.

Shared navigation/layout, labels, focus/reduced-motion/mobile behavior and useful missing-page states.

**Files / evidence:** [apps/web/components/shell.tsx](apps/web/components/shell.tsx); [apps/web/components/icons.tsx](apps/web/components/icons.tsx); [apps/web/app/layout.tsx](apps/web/app/layout.tsx); [apps/web/app/not-found.tsx](apps/web/app/not-found.tsx); [apps/web/app/globals.css](apps/web/app/globals.css).

**Dependencies:** Next.js; React; CSS.

**Recorded checks / references:** `tests/e2e/practice/practice.spec.ts`.

**Remaining gaps / conditions:**

- No dedicated accessibility conformance audit or localization testing.

### F006: Local Monaco editor and private browser drafts

**Status:** Implemented locally. **Owner:** web practice.

Bundle editor locally; preserve per-problem/language guest drafts, fallback/retry and storage-failure behavior without automatic source upload.

**Files / evidence:** [apps/web/features/practice/code-pane.tsx](apps/web/features/practice/code-pane.tsx); [apps/web/scripts/copy-monaco.mjs](apps/web/scripts/copy-monaco.mjs).

**Dependencies:** Monaco; React Monaco wrapper; pinned patched DOMPurify; localStorage.

**Recorded checks / references:** `tests/e2e/practice/practice.spec.ts`; `tests/e2e/submissions/submissions.spec.ts`.

**Remaining gaps / conditions:**

- Storage is local best effort, not encrypted per-account cloud sync or a backup.

### F007: Public author-written hint ladder

**Status:** Implemented locally. **Owner:** web practice + API content.

Reveal three author-written hints with honest offline provenance.

**Files / evidence:** [apps/web/features/practice/workspace.tsx](apps/web/features/practice/workspace.tsx); [services/api/solver_api/features/catalog/content.py](services/api/solver_api/features/catalog/content.py).

**Dependencies:** original catalog hints.

**Recorded checks / references:** `tests/e2e/practice/practice.spec.ts`.

**Remaining gaps / conditions:**

- Not model inference; separate authenticated request UI is F011.

### F008: Local accounts, sessions and signing keys

**Status:** Implemented locally. **Owner:** web accounts.

Signup/signin/signout, migrations, hashed passwords, cookie sessions, origin/redirect controls and private persistent local signing material.

**Files / evidence:** [apps/web/features/accounts/account-form.tsx](apps/web/features/accounts/account-form.tsx); [apps/web/features/accounts/server.ts](apps/web/features/accounts/server.ts); [apps/web/features/accounts/client.ts](apps/web/features/accounts/client.ts); [apps/web/app/api/auth/[...all]/route.ts](apps/web/app/api/auth/%5B...all%5D/route.ts); [apps/web/scripts/auth-migrate.mjs](apps/web/scripts/auth-migrate.mjs).

**Dependencies:** Better Auth; Node SQLite; private local key/database; Ed25519 JWT plugin.

**Recorded checks / references:** `apps/web/tests/auth.test.mjs`; `tests/e2e/submissions/submissions.spec.ts`.

**Remaining gaps / conditions:**

- No delivered email verification/recovery, trusted production ingress policy or full data lifecycle operations.

### F009: Fixed-JWKS API identity verification

**Status:** Implemented locally. **Owner:** API identity.

Validate exactly one bounded Bearer token with fixed EdDSA/issuer/audience/use/lifetime and cached bounded fixed-source JWKS.

**Files / evidence:** [services/api/solver_api/features/identity/verification.py](services/api/solver_api/features/identity/verification.py); [apps/web/features/accounts/server.ts](apps/web/features/accounts/server.ts).

**Dependencies:** PyJWT; cryptography; HTTPX; Better Auth JWKS.

**Recorded checks / references:** `services/api/tests/identity/test_auth.py`; `apps/web/tests/auth.test.mjs`.

**Remaining gaps / conditions:**

- Offline API JWT can remain valid for up to five minutes after web logout; production transport trust and total fetch deadline need attention.

### F010: Versioned authenticated authored hint API

**Status:** Implemented locally. **Owner:** API hints.

Strict levels 1-3, public-only context, honest authored/mock/model provenance, bounded output, timeout and safe provider failures.

**Files / evidence:** [services/api/solver_api/features/hints/service.py](services/api/solver_api/features/hints/service.py); [services/api/solver_api/main.py](services/api/solver_api/main.py); [services/api/tests/hints/test_hints.py](services/api/tests/hints/test_hints.py).

**Dependencies:** FastAPI; Pydantic; JWT dependency; authored backend.

**Recorded checks / references:** `services/api/tests/hints/test_hints.py`.

**Remaining gaps / conditions:**

- Only authored backend is configured; no real provider request, source debugging or model quotas. SAI-010 is already squash-integrated and counted once.

### F011: Recovered authenticated hint request frontend SAI-011

**Status:** Implemented locally. **Owner:** web hints.

Recover unique unmerged SAI-011 request/cancel/retry/signin UI and client into a dedicated hints feature.

**Files / evidence:** [apps/web/features/hints/account-hint.tsx](apps/web/features/hints/account-hint.tsx); [apps/web/features/hints/api.ts](apps/web/features/hints/api.ts); [apps/web/features/practice/workspace.tsx](apps/web/features/practice/workspace.tsx); [tests/e2e/hints/hints.spec.ts](tests/e2e/hints/hints.spec.ts).

**Dependencies:** F008; F009; F010; AbortController; validated provenance schema.

**Recorded checks / references:** `tests/e2e/hints/hints.spec.ts`.

**Remaining gaps / conditions:**

- Author-written content only; no real inference or model provider.

### F012: Bounded API requests and safe correlated errors

**Status:** Implemented locally. **Owner:** API shared middleware.

Bound each body to 128 KiB/ten-second receive time; generate request IDs and redact validation/internal failures.

**Files / evidence:** [services/api/solver_api/http/body_limit.py](services/api/solver_api/http/body_limit.py); [services/api/solver_api/http/errors.py](services/api/solver_api/http/errors.py); [services/api/solver_api/main.py](services/api/solver_api/main.py).

**Dependencies:** Starlette ASGI; FastAPI; asyncio.

**Recorded checks / references:** `services/api/tests/catalog/test_api.py`; `services/api/tests/submissions/test_submissions.py`; `services/api/tests/hints/test_hints.py`.

**Remaining gaps / conditions:**

- Per-request bounds do not cap aggregate ingress concurrency or provide operational observability.

### F013: Idempotent owned submission queue and quotas

**Status:** Implemented locally. **Owner:** API submissions.

Deliberate run/submit, UTF-8 source bounds, per-account idempotency and in-flight/rate/global active queue controls.

**Files / evidence:** [services/api/solver_api/features/submissions/store.py](services/api/solver_api/features/submissions/store.py); [services/api/solver_api/main.py](services/api/solver_api/main.py); [apps/web/features/submissions/submission-panel.tsx](apps/web/features/submissions/submission-panel.tsx); [apps/web/features/submissions/api.ts](apps/web/features/submissions/api.ts).

**Dependencies:** SQLite WAL; Pydantic; authenticated account ID; UUID idempotency.

**Recorded checks / references:** `services/api/tests/submissions/test_submissions.py`; `tests/e2e/submissions/submissions.spec.ts`.

**Remaining gaps / conditions:**

- Local SQLite queue; no production scheduling fairness, cumulative retention/storage budget or distributed queue deployment.

### F014: Private attempt source and verdict history

**Status:** Implemented locally. **Owner:** API storage + web submissions.

Persist source and actual finite verdicts; list summaries and detail only for the owning account.

**Files / evidence:** [services/api/solver_api/features/submissions/store.py](services/api/solver_api/features/submissions/store.py); [apps/web/features/submissions/submission-history.tsx](apps/web/features/submissions/submission-history.tsx); [apps/web/features/submissions/api.ts](apps/web/features/submissions/api.ts); [apps/web/app/submissions/page.tsx](apps/web/app/submissions/page.tsx).

**Dependencies:** SQLite; verified ownership; bounded validated responses.

**Recorded checks / references:** `services/api/tests/submissions/test_submissions.py`; `tests/e2e/submissions/submissions.spec.ts`.

**Remaining gaps / conditions:**

- No retention/deletion/backup/encryption operations; summary query unnecessarily materializes source before dropping it.

### F015: Worker readiness, heartbeat and exclusive expiring leases

**Status:** Implemented locally. **Owner:** API authority + judge controller.

Advertise verified runtime/languages, admit jobs only with fresh workers, lease once and accept one bounded authenticated completion.

**Files / evidence:** [services/api/solver_api/features/submissions/store.py](services/api/solver_api/features/submissions/store.py); [services/api/solver_api/main.py](services/api/solver_api/main.py); [services/judge/solver_judge/control/worker.py](services/judge/solver_judge/control/worker.py).

**Dependencies:** dedicated worker bearer; per-job hashed random lease tokens; SQLite transactions.

**Recorded checks / references:** `services/api/tests/submissions/test_submissions.py`; `services/judge/tests/control/test_worker.py`.

**Remaining gaps / conditions:**

- Shared controller trust domain requires private transport, rotation and production identity operations.

### F016: gVisor-isolated Python and C++17 execution

**Status:** Implemented locally. **Owner:** judge sandbox.

Run learner programs only inside required isolated per-job containers; host controller retains credentials and expected answers.

**Files / evidence:** [services/judge/Dockerfile](services/judge/Dockerfile); [services/judge/solver_judge/control/runner.py](services/judge/solver_judge/control/runner.py); [services/judge/solver_judge/sandbox/harness.py](services/judge/solver_judge/sandbox/harness.py).

**Dependencies:** rootless Docker; runsc; Linux rlimits; g++; Python isolated mode.

**Recorded checks / references:** `services/judge/tests/sandbox/test_sandbox.py`; `services/judge/tests/control/test_runner.py`.

**Remaining gaps / conditions:**

- Local bounded prototype, runtime maintenance and aggregate host accounting required; no ordinary-container/host fallback or security certification.

### F017: Original finite grading cases and trusted oracles

**Status:** Implemented locally. **Owner:** judge grading.

Two public cases for run mode and eight finite checks per submission for each original problem; compare outside sandbox.

**Files / evidence:** [services/judge/solver_judge/grading/cases.py](services/judge/solver_judge/grading/cases.py); [services/judge/solver_judge/control/runner.py](services/judge/solver_judge/control/runner.py).

**Dependencies:** original public samples; worker-generated bounded cases; independent expected-answer computation.

**Recorded checks / references:** `services/judge/tests/grading/test_cases.py`; `services/judge/tests/sandbox/test_sandbox.py`.

**Remaining gaps / conditions:**

- No arbitrary correctness proof, authoring/versioning system or interactive/custom validator ecosystem.

### F018: Bounded process transport, cancellation and cleanup

**Status:** Implemented locally. **Owner:** judge controller + sandbox.

Use one bounded transport helper in host control and image supervisor; cancel/shutdown work and clean resources.

**Files / evidence:** [services/judge/solver_judge/bounded.py](services/judge/solver_judge/bounded.py); [services/judge/solver_judge/control/runner.py](services/judge/solver_judge/control/runner.py); [services/judge/solver_judge/control/worker.py](services/judge/solver_judge/control/worker.py).

**Dependencies:** selectors; bounded stdin/stdout/stderr; deadlines; process groups; Docker cleanup.

**Recorded checks / references:** `services/judge/tests/sandbox/test_bounded.py`; `services/judge/tests/control/test_runner.py`; `services/judge/tests/control/test_worker.py`.

**Remaining gaps / conditions:**

- JUDGE-001 fixed and regression-tested. API capability display retains its existing60-second stale-heartbeat window; host-wide budgets and process-crash reconciliation remain operational work.

### F019: Finite runtime preflight and readiness diagnostics

**Status:** Implemented locally. **Owner:** judge operations.

Fail closed before worker heartbeat and print controlled readiness/check fields.

**Files / evidence:** [services/judge/solver_judge/control/diagnostics.py](services/judge/solver_judge/control/diagnostics.py); [services/judge/solver_judge/control/runner.py](services/judge/solver_judge/control/runner.py); [services/judge/solver_judge/sandbox/harness.py](services/judge/solver_judge/sandbox/harness.py).

**Dependencies:** required runtime inspection; finite compiler/isolation/resource probes.

**Recorded checks / references:** `services/judge/tests/control/test_runner.py`; `services/judge/tests/sandbox/test_sandbox.py`; `services/judge/tests/control/test_worker.py`.

**Remaining gaps / conditions:**

- Point-in-time probes do not replace continuous host health, patching or independent review.

### F020: Production-mode build, Compose and private-state packaging guard

**Status:** Implemented locally. **Owner:** web/API packaging.

Build distributable web/API components excluding credentials/local state and inactive AnalyseFuture content; preserve local account/submission volumes.

**Files / evidence:** [apps/web/Dockerfile](apps/web/Dockerfile); [services/api/Dockerfile](services/api/Dockerfile); [apps/web/next.config.ts](apps/web/next.config.ts); [compose.yaml](compose.yaml); [compose.cloud.yaml](compose.cloud.yaml); [scripts/verification/check-standalone.mjs](scripts/verification/check-standalone.mjs); [.dockerignore](.dockerignore).

**Dependencies:** Next standalone; nonroot containers; private volumes; optional managed TLS CA secret.

**Recorded checks / references:** `npm run build`; `scripts/verification/check-standalone.mjs`; `Compose smoke workflow in docs/DEVELOPMENT.md`.

**Remaining gaps / conditions:**

- Build mode is not deployment; API/web base tags and Actions refs need maintained immutable reproducibility policy.

### F021: Archive and history preservation with integrity inventories

**Status:** Implemented locally. **Owner:** repository evidence.

Keep original archives and all 122 member contents, map renamed Git controls and preserve historical variants outside runtime.

**Files / evidence:** [AnalyseFuture/manifest.json](AnalyseFuture/manifest.json); [AnalyseFuture/archives/](AnalyseFuture/archives/); [AnalyseFuture/extracted/](AnalyseFuture/extracted/); [scripts/verification/verify_preserved_archives.py](scripts/verification/verify_preserved_archives.py); [AnalyseFuture/repository-inventory/](AnalyseFuture/repository-inventory/).

**Dependencies:** SHA-256 inventories; original ZIPs; Git blobs/history.

**Recorded checks / references:** `python3 scripts/verify_preserved_archives.py`; `python3 scripts/verify_preserved_archives.py --git-index`.

**Remaining gaps / conditions:**

- Five supplied datasets are only LFS pointers; hashes prove byte preservation, not safety, rights or recovery of unavailable history.

### F022: Project intent, decisions, historical memory and delivery evidence

**Status:** Implemented locally. **Owner:** documentation governance.

Preserve competing historical proposals while maintaining discoverable current status, decisions, future vision and progress.

**Files / evidence:** [README.md](README.md); [docs/product/PROJECT_IDEA.txt](docs/product/PROJECT_IDEA.txt); [docs/status/PROJECT_STATUS.md](docs/status/PROJECT_STATUS.md); [docs/INDEX.md](docs/INDEX.md); [docs/adr/](docs/adr/); [AnalyseFuture/historical-implementations/](AnalyseFuture/historical-implementations/).

**Dependencies:** reviewed source/history; owner decisions; honest validation ledger.

**Recorded checks / references:** `link/path review`; `root validation record`.

**Remaining gaps / conditions:**

- Dated proposals must not override current implementation; account compromise attribution and inaccessible deleted work remain unproven.

### F023: Bounded live model-backed tutor provider

**Status:** Planned. **Owner:** future API hints.

Add one reviewed provider behind the existing public hint context, with explicit model provenance and outages/quotas.

**Files / evidence:** [services/api/solver_api/features/hints/service.py](services/api/solver_api/features/hints/service.py); [docs/product/AI_SOLVER.md](docs/product/AI_SOLVER.md).

**Dependencies:** F009; F010; approved model endpoint; per-account token/cost/time quotas; consent and rights policy.

**Recorded checks / references:** None executed for this proposed capability.

**Remaining gaps / conditions:**

- No provider implemented; cannot enable by setting an arbitrary backend name; provider selection, credentials and spending require owner decision.

### F024: Consent-driven debugging and bounded repair

**Status:** Planned. **Owner:** future API orchestration + judge.

Use deliberately supplied source/evidence to form bounded diagnosis/repair hypotheses and test them through isolated execution.

**Files / evidence:** [docs/product/AI_SOLVER.md](docs/product/AI_SOLVER.md); [docs/security/JUDGE_SECURITY.md](docs/security/JUDGE_SECURITY.md).

**Dependencies:** F013; F016; F023; approved user source/public evidence; privacy controls.

**Recorded checks / references:** None executed for this proposed capability.

**Remaining gaps / conditions:**

- No debugger workflow exists; do not leak private grading data or claim model diagnosis is observed fact.

### F025: Budgeted candidate solver and evidence-based selection

**Status:** Planned. **Owner:** future solver orchestration.

Plan, generate a limited candidate set, run permitted tests, optionally repair and rank by authorized execution evidence.

**Files / evidence:** [docs/product/AI_SOLVER.md](docs/product/AI_SOLVER.md); [docs/research/MODEL_DATA_EVALUATION.md](docs/research/MODEL_DATA_EVALUATION.md); [docs/product/DSA_SOLVER_READINESS.md](docs/product/DSA_SOLVER_READINESS.md).

**Dependencies:** F016; F017; F023; candidate/test/token/time budget; authorized tasks.

**Recorded checks / references:** None executed for this proposed capability.

**Remaining gaps / conditions:**

- No active generated solver; similarity/confidence/finite acceptance do not prove correctness; no unlimited retries.

### F026: Rights-approved held-out AI evaluation and research reports

**Status:** Planned. **Owner:** future offline evaluation.

Compare baselines and candidate/repair/ranking strategies using pass@1/pass@k, latency, cost and failures.

**Files / evidence:** [docs/research/MODEL_DATA_EVALUATION.md](docs/research/MODEL_DATA_EVALUATION.md); [docs/governance/DATA_AND_LICENSES.md](docs/governance/DATA_AND_LICENSES.md); [docs/product/DSA_SOLVER_READINESS.md](docs/product/DSA_SOLVER_READINESS.md).

**Dependencies:** approved datasets; disjoint splits; fixed model/prompt/seed/budget; isolated judge.

**Recorded checks / references:** None executed for this proposed capability.

**Remaining gaps / conditions:**

- No new benchmark results reproduced; archive output anecdotes are not project performance evidence.

### F027: Original content authoring, versioning and validators

**Status:** Planned. **Owner:** future API content + judge content.

Manage licensed/original statements, sample correctness, validators, test versions and content provenance.

**Files / evidence:** [docs/product/PRODUCT_REQUIREMENTS.md](docs/product/PRODUCT_REQUIREMENTS.md); [docs/governance/DATA_AND_LICENSES.md](docs/governance/DATA_AND_LICENSES.md).

**Dependencies:** F004; F017; author permissions; versioned problem/test contracts.

**Recorded checks / references:** None executed for this proposed capability.

**Remaining gaps / conditions:**

- No authoring/import pipeline or permissioned content administration yet.

### F028: Learning paths, reflection and progress retention

**Status:** Planned. **Owner:** future learning features.

Offer progressive topic practice, mistake reflection and transfer/retention measures.

**Files / evidence:** [docs/product/PRODUCT_REQUIREMENTS.md](docs/product/PRODUCT_REQUIREMENTS.md); [docs/product/PROJECT_VISION.md](docs/product/PROJECT_VISION.md).

**Dependencies:** F008; F014; consented learning data; original problem taxonomy.

**Recorded checks / references:** None executed for this proposed capability.

**Remaining gaps / conditions:**

- No personalized progress system; acceptance counts/time alone do not prove learning.

### F029: Virtual contests, ICPC teams and scoring

**Status:** Planned. **Owner:** future event features.

Support timed original/permissioned events, team workflows and post-contest review.

**Files / evidence:** [docs/product/PRODUCT_REQUIREMENTS.md](docs/product/PRODUCT_REQUIREMENTS.md); [docs/product/ROADMAP.md](docs/product/ROADMAP.md).

**Dependencies:** F008; F013; F016; server-enforced assistance policy; scoreboard/time/freeze tests.

**Recorded checks / references:** None executed for this proposed capability.

**Remaining gaps / conditions:**

- Contests/teams/scoreboards are not implemented; rules and abuse/integrity controls remain prerequisites.

### F030: Additional audited learner runtime languages

**Status:** Planned. **Owner:** future judge runtimes.

Add Java, JavaScript, Rust, Go or C++20 individually behind reviewed runtime contracts.

**Files / evidence:** [docs/product/PRODUCT_REQUIREMENTS.md](docs/product/PRODUCT_REQUIREMENTS.md); [docs/security/JUDGE_SECURITY.md](docs/security/JUDGE_SECURITY.md).

**Dependencies:** F016; compiler/runtime lifecycle; protocol limits/diagnostics; hostile fixtures.

**Recorded checks / references:** None executed for this proposed capability.

**Remaining gaps / conditions:**

- Current supported execution languages are Python/C++17 only. A UI dropdown is insufficient.

### F031: Production identity, recovery and data administration

**Status:** Planned. **Owner:** future account operations.

Make accounts and private learning data operable with verified recovery, access review and safe lifecycle controls.

**Files / evidence:** [docs/architecture/adr/0002-authenticated-isolated-submissions.md](docs/architecture/adr/0002-authenticated-isolated-submissions.md); [docs/governance/OPEN_DECISIONS.md](docs/governance/OPEN_DECISIONS.md).

**Dependencies:** F008; F009; trusted ingress; email delivery; retention/deletion/backup policy.

**Recorded checks / references:** None executed for this proposed capability.

**Remaining gaps / conditions:**

- No production identity/recovery operation, immediate API-token revocation or full deletion/restore capability.

### F032: Maintained public judge operations and host-wide budgets

**Status:** Planned. **Owner:** future judge infrastructure.

Operate a maintained dedicated execution host with audited updates, monitoring, cleanup reconciliation and bounded capacity.

**Files / evidence:** [services/judge/UPSTREAM_REVIEW.md](services/judge/UPSTREAM_REVIEW.md); [docs/security/JUDGE_SECURITY.md](docs/security/JUDGE_SECURITY.md).

**Dependencies:** F016; F018; maintained runtime; aggregate CPU/memory/PID/disk limits; independent review; incident drills.

**Recorded checks / references:** None executed for this proposed capability.

**Remaining gaps / conditions:**

- Local prototype is not certified; old recorded runtime and missing aggregate accounting block public-readiness claims.

### F033: Solver fine-tuning, artifact lineage and release qualification

**Status:** Planned. **Owner:** future offline ML training and model delivery.

Research candidate models without assuming a selection; prepare permitted disjoint data; implement reproducible SFT/LoRA/QLoRA tooling; run approved external smoke and real training; compare held-out results; qualify artifacts, serving and rollback.

**Files / evidence:** [docs/research/MODEL_DATA_EVALUATION.md](docs/research/MODEL_DATA_EVALUATION.md); [docs/research/FINETUNING_MODEL_RESEARCH.md](docs/research/FINETUNING_MODEL_RESEARCH.md); [docs/product/DSA_SOLVER_READINESS.md](docs/product/DSA_SOLVER_READINESS.md).

**Dependencies:** F026; separate data/model rights; approved external compute/spend; baseline comparison.

**Recorded checks / references:** None executed for this proposed capability.

**Remaining gaps / conditions:**

- No model is selected or trained; no weights, GPU job or training stack is installed. B080 is admission only; appended training-delivery tasks cover actual future execution and release.
- Readiness must name measured DSA coverage and failures; no fine-tuning or finite tests guarantee every possible problem can be solved.
- Five supplied archive datasets are LFS pointers without underlying data.

### F034: Coach, educator and institutional workspaces

**Status:** Planned. **Owner:** future product features.

Support permissioned content assignment, learning evidence and policy-bound assessments.

**Files / evidence:** [docs/product/PRODUCT_REQUIREMENTS.md](docs/product/PRODUCT_REQUIREMENTS.md); [docs/product/PROJECT_VISION.md](docs/product/PROJECT_VISION.md).

**Dependencies:** F008; F027; F028; role permissions; consented reports and assessment policy.

**Recorded checks / references:** None executed for this proposed capability.

**Remaining gaps / conditions:**

- No coach dashboard or institution deployment exists; pilot user need and privacy controls required.

### F035: Self-hosted model inference and independent providers

**Status:** Research only. **Owner:** future model operations.

Compare hosted APIs and owned inference without making one provider permanent infrastructure.

**Files / evidence:** [docs/product/AI_SOLVER.md](docs/product/AI_SOLVER.md); [docs/governance/OPEN_DECISIONS.md](docs/governance/OPEN_DECISIONS.md).

**Dependencies:** F023; approved model license; hardware/economics/security review.

**Recorded checks / references:** None executed for this proposed capability.

**Remaining gaps / conditions:**

- No weights or inference daemon installed; self-hosting is not automatically cheaper and requires ongoing operations.

### F036: CodeSIM/MapCoder planning and ablation strategies

**Status:** Research only. **Owner:** archived CodeGenerator.

Study direct/analogical/self-planning/CodeSIM/MapCoder methods and purposeful stage ablations.

**Files / evidence:** [AnalyseFuture/extracted/CodeGenerator-master/src/promptings/](AnalyseFuture/extracted/CodeGenerator-master/src/promptings/); [AnalyseFuture/extracted/CodeGenerator-master/README.md](AnalyseFuture/extracted/CodeGenerator-master/README.md).

**Dependencies:** archived provider interfaces; research prompts; benchmark adapters.

**Recorded checks / references:** None executed for this proposed capability.

**Remaining gaps / conditions:**

- Archive strategies not executed or adopted; require held-out authorized evaluation and strict budgets.

### F037: Archived provider adapters and token accounting

**Status:** Research only. **Owner:** archived CodeGenerator.

Preserve generation provider abstractions and accounting/resume approaches as references.

**Files / evidence:** [AnalyseFuture/extracted/CodeGenerator-master/src/models/](AnalyseFuture/extracted/CodeGenerator-master/src/models/); [AnalyseFuture/extracted/CodeGenerator-master/src/results/](AnalyseFuture/extracted/CodeGenerator-master/src/results/).

**Dependencies:** OpenAI/Azure/OpenRouter/Anthropic/Gemini/Groq external SDKs; archived accounting.

**Recorded checks / references:** None executed for this proposed capability.

**Remaining gaps / conditions:**

- Unpinned/incomplete dependencies, no product quotas, privacy/deadline gaps and Gemini undefined model_name defect; no compatible drop-in integration.

### F038: Archived benchmark loaders, variants and result analysis

**Status:** Research only. **Owner:** archived CodeGenerator + phi outputs.

Preserve dataset normalization, sample/test variants, results/resume and published contest-output evidence.

**Files / evidence:** [AnalyseFuture/extracted/CodeGenerator-master/src/datasets/](AnalyseFuture/extracted/CodeGenerator-master/src/datasets/); [AnalyseFuture/extracted/CodeGenerator-master/src/results/](AnalyseFuture/extracted/CodeGenerator-master/src/results/); [AnalyseFuture/extracted/CodeGenerator-master/data/](AnalyseFuture/extracted/CodeGenerator-master/data/); [AnalyseFuture/extracted/phi-code-main/contests_results/](AnalyseFuture/extracted/phi-code-main/contests_results/).

**Dependencies:** benchmark formats; JSON/JSONL; unverified upstream result files.

**Recorded checks / references:** None executed for this proposed capability.

**Remaining gaps / conditions:**

- Source-code licenses do not settle dataset/contest/model rights; projection overlaps do not justify deleting variants or prove evaluation independence.

### F039: Archived host/external execution helpers

**Status:** Research only. **Owner:** archived execution research.

Keep original evaluator mechanics inspectable as supplied evidence.

**Files / evidence:** [AnalyseFuture/extracted/CodeGenerator-master/src/evaluations/](AnalyseFuture/extracted/CodeGenerator-master/src/evaluations/); [AnalyseFuture/extracted/CodeGenerator-master/src/utils/runEP.py](AnalyseFuture/extracted/CodeGenerator-master/src/utils/runEP.py); [AnalyseFuture/extracted/phi-code-main/solver/leetcode.py](AnalyseFuture/extracted/phi-code-main/solver/leetcode.py); [AnalyseFuture/extracted/phi-code-main/solver/atcoder.py](AnalyseFuture/extracted/phi-code-main/solver/atcoder.py); [AnalyseFuture/extracted/phi-code-main/solver/codeforces.py](AnalyseFuture/extracted/phi-code-main/solver/codeforces.py).

**Dependencies:** exec/multiprocessing/subprocess; external execution endpoint; developer-specific shell/Docker mounts.

**Recorded checks / references:** None executed for this proposed capability.

**Remaining gaps / conditions:**

- Critical if transplanted into app: host execution of untrusted code, shell construction, missing current sandbox/credential boundary. Never activate as fallback.

### F040: phi-code multi-candidate sample/rank pipeline

**Status:** Research only. **Owner:** archived phi-code solver.

Study diverse Python attempts and ranking by passed examples followed by embedding similarity.

**Files / evidence:** [AnalyseFuture/extracted/phi-code-main/solver/terminal.py](AnalyseFuture/extracted/phi-code-main/solver/terminal.py); [AnalyseFuture/extracted/phi-code-main/solver/atcoder.py](AnalyseFuture/extracted/phi-code-main/solver/atcoder.py); [AnalyseFuture/extracted/phi-code-main/solver/codeforces.py](AnalyseFuture/extracted/phi-code-main/solver/codeforces.py); [AnalyseFuture/extracted/phi-code-main/solver/leetcode.py](AnalyseFuture/extracted/phi-code-main/solver/leetcode.py); [AnalyseFuture/extracted/phi-code-main/solver/utils.py](AnalyseFuture/extracted/phi-code-main/solver/utils.py).

**Dependencies:** LLM endpoint; sentence-transformers ranker; site-specific parsers.

**Recorded checks / references:** None executed for this proposed capability.

**Remaining gaps / conditions:**

- Host code execution unsuitable; ranking semantics, safe execution, rights, deadlines and cost budgets unresolved; upstream contest claims not reproduced.

### F041: phi-code ranker data preparation and training

**Status:** Research only. **Owner:** archived phi-code ranker.

Preserve token-length filtering, dataset sampling and triplet/contrastive ranker training references.

**Files / evidence:** [AnalyseFuture/extracted/phi-code-main/ranker/](AnalyseFuture/extracted/phi-code-main/ranker/); [AnalyseFuture/extracted/phi-code-main/datasets/](AnalyseFuture/extracted/phi-code-main/datasets/).

**Dependencies:** sentence-transformers; Transformers; datasets; five missing LFS data objects.

**Recorded checks / references:** None executed for this proposed capability.

**Remaining gaps / conditions:**

- Unpinned remote-code-enabled model loads, incomplete dependencies, missing datasets, nondeterministic splits and unreviewed data rights; no training executed.

### F042: phi-code standalone CLI, curses and Gradio interfaces

**Status:** Research only. **Owner:** archived phi-code UI.

Preserve alternative standalone research interaction modes as examples, not additional active products.

**Files / evidence:** [AnalyseFuture/extracted/phi-code-main/solver/main.py](AnalyseFuture/extracted/phi-code-main/solver/main.py); [AnalyseFuture/extracted/phi-code-main/solver/web_ui.py](AnalyseFuture/extracted/phi-code-main/solver/web_ui.py); [AnalyseFuture/extracted/phi-code-main/solver/curses_ui.py](AnalyseFuture/extracted/phi-code-main/solver/curses_ui.py); [AnalyseFuture/extracted/phi-code-main/solver/terminal.py](AnalyseFuture/extracted/phi-code-main/solver/terminal.py).

**Dependencies:** Gradio; curses; Python; archived solver pipeline.

**Recorded checks / references:** None executed for this proposed capability.

**Remaining gaps / conditions:**

- No application account/ownership policy; static None-statement and return-arity defects; no current runtime validation.

### F043: Ordered multi-tool contribution backlog and safe issue publisher

**Status:** Partial. **Owner:** repository engineering/GitHub workflow.

Validate and render 141 ordered scoped cards, reconcile remote markers, publish missing issues only after explicit --publish, record actual confirmed issue numbers and support reviewed contributor PR handoff.

**Files / evidence:** [scripts/github/publish_issues.py](scripts/github/publish_issues.py); [scripts/github/build_backlog.py](scripts/github/build_backlog.py); [tests/tooling/github/test_publish_issues.py](tests/tooling/github/test_publish_issues.py); [docs/engineering/AI_CONTRIBUTION_WORKFLOW.md](docs/engineering/AI_CONTRIBUTION_WORKFLOW.md); [docs/engineering/backlog/issues.json](docs/engineering/backlog/issues.json); [docs/engineering/backlog/publication.json](docs/engineering/backlog/publication.json).

**Dependencies:** Existing gh authentication; api.github.com egress; Repository issue-write permission.

**Recorded checks / references:** `tests/tooling/github/test_publish_issues.py`.

**Remaining gaps / conditions:**

- Live GitHub issue creation blocked by network policy;0issuePOSTs attempted. Server-side branch-rule enforcement and unattended review are not enabled.

### F044: Contributor PR evidence metadata contract

**Status:** Implemented locally. **Owner:** repository review workflow.

Validate one bounded structured evidence block against catalogue ID/order, current PR head, prerequisites, changed paths and explicit check outcomes; commands remain inert and diagnostics do not echo PR data.

**Files / evidence:** [scripts/github/check_pr_evidence.py](scripts/github/check_pr_evidence.py); [.github/workflows/pr-evidence.yml](.github/workflows/pr-evidence.yml); [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md); [tests/tooling/github/test_pr_evidence.py](tests/tooling/github/test_pr_evidence.py); [docs/engineering/PR_EVIDENCE.md](docs/engineering/PR_EVIDENCE.md).

**Dependencies:** Trusted base commit and canonical backlog; Standard-library JSON parsing; Read-only pull_request event payload.

**Recorded checks / references:** `tests/tooling/github/test_pr_evidence.py`.

**Remaining gaps / conditions:**

- Hosted Actions run not observed. Metadata completeness does not establish that checks ran or authorize review/merge; GitHub branch rules remain B127 work.

## Complete folder map

**114 folders including the root**, derived from all **462 tracked files**. Counts include nested descendants. Folders are functional owners; preserved upstream internal structure remains evidence.

| Folder | Responsibility | Tracked files below it |
| --- | --- | --- |
| [./](.) | One modular Solver AI repository joining the working practice application, independently bounded services, development tooling, planned tasks and preserved research evidence. | 462 |
| [.github/](.github) | Repository-hosted contributor templates and read-only GitHub Actions configuration. | 3 |
| [.github/workflows/](.github/workflows) | Hosted application checks and trusted-base pull-request evidence validation workflows. | 2 |
| [AnalyseFuture/](AnalyseFuture) | Organized recovery evidence, inventories, migration records and inactive upstream or historical material kept outside application execution. | 181 |
| [AnalyseFuture/archives/](AnalyseFuture/archives) | Unchanged original uploaded ZIPs preserved as inactive provenance evidence rather than installed application packages. | 2 |
| [AnalyseFuture/audits/](AnalyseFuture/audits) | Evidence-scoped repository, Git history and security review findings with attribution and investigation limits. | 2 |
| [AnalyseFuture/continuation/](AnalyseFuture/continuation) | Persistent progress and next-developer instructions for resuming work without relying on chat memory. | 2 |
| [AnalyseFuture/extracted/](AnalyseFuture/extracted) | All uploaded ZIP members preserved as inactive research snapshots with source provenance, not application dependencies. | 122 |
| [AnalyseFuture/extracted/CodeGenerator-master/](AnalyseFuture/extracted/CodeGenerator-master) | Inactive CodeGenerator upload snapshot preserving original research source, dependencies, licenses, benchmark material and images, without active application adoption. | 73 |
| [AnalyseFuture/extracted/CodeGenerator-master/data/](AnalyseFuture/extracted/CodeGenerator-master/data) | Inactive uploaded CodeGenerator benchmark fixtures preserved with separate dataset-rights review still required. | 10 |
| [AnalyseFuture/extracted/CodeGenerator-master/data/APPS/](AnalyseFuture/extracted/CodeGenerator-master/data/APPS) | Inactive uploaded APPS selection preserved as research data with provenance and reuse limits unverified. | 1 |
| [AnalyseFuture/extracted/CodeGenerator-master/data/HumanEval/](AnalyseFuture/extracted/CodeGenerator-master/data/HumanEval) | Inactive uploaded HumanEval-family evaluation fixtures preserved as research data rather than production problem content. | 3 |
| [AnalyseFuture/extracted/CodeGenerator-master/data/MBPPEval/](AnalyseFuture/extracted/CodeGenerator-master/data/MBPPEval) | Inactive uploaded MBPP evaluation variants preserved as research data rather than approved training material. | 3 |
| [AnalyseFuture/extracted/CodeGenerator-master/data/xCodeEval/](AnalyseFuture/extracted/CodeGenerator-master/data/xCodeEval) | Inactive uploaded xCodeEval descriptions, cases and evaluation records preserved without validating their reuse rights. | 3 |
| [AnalyseFuture/extracted/CodeGenerator-master/images/](AnalyseFuture/extracted/CodeGenerator-master/images) | Inactive uploaded research diagrams and result graphics preserved as upstream artifacts, not reproduced performance evidence. | 4 |
| [AnalyseFuture/extracted/CodeGenerator-master/src/](AnalyseFuture/extracted/CodeGenerator-master/src) | Inactive uploaded Python research pipeline source retained for reference without installation or execution. | 54 |
| [AnalyseFuture/extracted/CodeGenerator-master/src/constants/](AnalyseFuture/extracted/CodeGenerator-master/src/constants) | Inactive uploaded language, path and verbosity configuration for the upstream research pipeline. | 4 |
| [AnalyseFuture/extracted/CodeGenerator-master/src/datasets/](AnalyseFuture/extracted/CodeGenerator-master/src/datasets) | Inactive uploaded benchmark adapters, dataset factory and conversion utilities retained for provenance. | 10 |
| [AnalyseFuture/extracted/CodeGenerator-master/src/evaluations/](AnalyseFuture/extracted/CodeGenerator-master/src/evaluations) | Inactive uploaded execution and benchmark-scoring helpers whose host or external execution paths are not adopted by Solver AI. | 8 |
| [AnalyseFuture/extracted/CodeGenerator-master/src/models/](AnalyseFuture/extracted/CodeGenerator-master/src/models) | Inactive uploaded provider adapters retained as upstream research source without credentials or configured model calls. | 7 |
| [AnalyseFuture/extracted/CodeGenerator-master/src/promptings/](AnalyseFuture/extracted/CodeGenerator-master/src/promptings) | Inactive uploaded planning, code-generation and repair strategies preserved for conceptual study. | 14 |
| [AnalyseFuture/extracted/CodeGenerator-master/src/promptings/variations/](AnalyseFuture/extracted/CodeGenerator-master/src/promptings/variations) | Inactive uploaded CodeSIM strategy variants retained for research comparison rather than current product features. | 5 |
| [AnalyseFuture/extracted/CodeGenerator-master/src/results/](AnalyseFuture/extracted/CodeGenerator-master/src/results) | Inactive uploaded research result persistence helpers retained with their source provenance. | 2 |
| [AnalyseFuture/extracted/CodeGenerator-master/src/utils/](AnalyseFuture/extracted/CodeGenerator-master/src/utils) | Inactive uploaded parsing, cost, data and execution utilities retained without importing their execution behavior. | 8 |
| [AnalyseFuture/extracted/phi-code-main/](AnalyseFuture/extracted/phi-code-main) | Inactive phi-code upload snapshot preserving candidate-generation, ranking and alternate UI research with its original notices. | 49 |
| [AnalyseFuture/extracted/phi-code-main/contests_results/](AnalyseFuture/extracted/phi-code-main/contests_results) | Inactive uploaded contest statements, commands and candidate outputs preserved without asserting content rights or reproduced scores. | 20 |
| [AnalyseFuture/extracted/phi-code-main/contests_results/leetcode_weekly_476/](AnalyseFuture/extracted/phi-code-main/contests_results/leetcode_weekly_476) | Inactive uploaded weekly-contest 476 statements and experiment outputs retained solely as supplied research artifacts. | 12 |
| [AnalyseFuture/extracted/phi-code-main/contests_results/leetcode_weekly_476/gpt_oss_20B/](AnalyseFuture/extracted/phi-code-main/contests_results/leetcode_weekly_476/gpt_oss_20B) | Inactive uploaded weekly-contest 476 commands and candidate records labeled by upstream as a model experiment. | 8 |
| [AnalyseFuture/extracted/phi-code-main/contests_results/leetcode_weekly_477/](AnalyseFuture/extracted/phi-code-main/contests_results/leetcode_weekly_477) | Inactive uploaded weekly-contest 477 statements and experiment outputs retained solely as supplied research artifacts. | 8 |
| [AnalyseFuture/extracted/phi-code-main/contests_results/leetcode_weekly_477/gpt_oss_20B/](AnalyseFuture/extracted/phi-code-main/contests_results/leetcode_weekly_477/gpt_oss_20B) | Inactive uploaded weekly-contest 477 candidate records retained as upstream artifacts rather than verified benchmark evidence. | 4 |
| [AnalyseFuture/extracted/phi-code-main/datasets/](AnalyseFuture/extracted/phi-code-main/datasets) | Inactive uploaded Git LFS pointer files preserved exactly, with the referenced dataset objects absent from the ZIP. | 5 |
| [AnalyseFuture/extracted/phi-code-main/ranker/](AnalyseFuture/extracted/phi-code-main/ranker) | Inactive uploaded embedding-ranker data and training utilities retained without model downloads or training execution. | 5 |
| [AnalyseFuture/extracted/phi-code-main/solver/](AnalyseFuture/extracted/phi-code-main/solver) | Inactive uploaded model-client, candidate-execution and alternate-interface source whose host execution paths are not adopted. | 12 |
| [AnalyseFuture/historical-implementations/](AnalyseFuture/historical-implementations) | Inactive branch snapshots preserved with original source commits and hashes for recoverability, not active imports or instructions. | 23 |
| [AnalyseFuture/historical-implementations/project-memory/](AnalyseFuture/historical-implementations/project-memory) | Inactive original project-memory branch documents preserved with source-commit provenance rather than treated as current instructions. | 9 |
| [AnalyseFuture/historical-implementations/project-memory/docs/](AnalyseFuture/historical-implementations/project-memory/docs) | Inactive original continuity, handbook and development prose preserved as historical branch evidence, not authoritative current guidance. | 7 |
| [AnalyseFuture/historical-implementations/sai-011/](AnalyseFuture/historical-implementations/sai-011) | Inactive original SAI-011 branch versions preserved with source-commit provenance alongside the separately recovered active feature. | 14 |
| [AnalyseFuture/historical-implementations/sai-011/apps/](AnalyseFuture/historical-implementations/sai-011/apps) | Inactive historical SAI-011 application-tree evidence, not an additional runnable application. | 4 |
| [AnalyseFuture/historical-implementations/sai-011/apps/web/](AnalyseFuture/historical-implementations/sai-011/apps/web) | Inactive original SAI-011 web changes retained for comparison with the recovered feature implementation. | 4 |
| [AnalyseFuture/historical-implementations/sai-011/apps/web/app/](AnalyseFuture/historical-implementations/sai-011/apps/web/app) | Inactive historical hint styling snapshot preserved without inclusion in the active web build. | 1 |
| [AnalyseFuture/historical-implementations/sai-011/apps/web/components/](AnalyseFuture/historical-implementations/sai-011/apps/web/components) | Inactive original account-hint and workspace component versions preserved before feature-folder migration. | 2 |
| [AnalyseFuture/historical-implementations/sai-011/apps/web/lib/](AnalyseFuture/historical-implementations/sai-011/apps/web/lib) | Inactive original hint API client retained with its branch provenance rather than imported by the application. | 1 |
| [AnalyseFuture/historical-implementations/sai-011/docs/](AnalyseFuture/historical-implementations/sai-011/docs) | Inactive branch-specific status, research, backlog and handoff prose retained without replacing current documentation. | 9 |
| [AnalyseFuture/historical-implementations/sai-011/tests/](AnalyseFuture/historical-implementations/sai-011/tests) | Inactive original SAI-011 test tree retained as historical evidence rather than current test discovery. | 1 |
| [AnalyseFuture/historical-implementations/sai-011/tests/e2e/](AnalyseFuture/historical-implementations/sai-011/tests/e2e) | Inactive original hint browser-spec snapshot preserved before relocation and additional cancellation regressions. | 1 |
| [AnalyseFuture/migration-records/](AnalyseFuture/migration-records) | Original-to-current path mappings, consolidation decisions and preservation summaries for structural changes. | 3 |
| [AnalyseFuture/planning/](AnalyseFuture/planning) | Detailed future product vision and prioritized technical debt, with feasibility and delivery limits separated from implementation claims. | 2 |
| [AnalyseFuture/repository-inventory/](AnalyseFuture/repository-inventory) | Machine-readable and plain-text file, feature, dependency, baseline and preservation ledgers. | 20 |
| [AnalyseFuture/repository-inventory/reviews/](AnalyseFuture/repository-inventory/reviews) | Frozen per-scope static source assessments whose original findings remain historical evidence rather than fresh runtime claims. | 8 |
| [AnalyseFuture/validation/](AnalyseFuture/validation) | Named-revision validation records distinguishing successful, failed, expected-failure and unexecuted checks. | 1 |
| [apps/](apps) | User-facing applications with framework-owned entry points and feature modules. | 31 |
| [apps/web/](apps/web) | Next.js and TypeScript practice interface, account authority, browser feature modules and web-owned build tooling. | 31 |
| [apps/web/app/](apps/web/app) | Next.js App Router entry points, root layout and global styles that compose the feature modules. | 8 |
| [apps/web/app/account/](apps/web/app/account) | Account route that passes a constrained continuation path to the sign-in and registration interface. | 1 |
| [apps/web/app/api/](apps/web/app/api) | Framework HTTP route adapters served by the web process. | 1 |
| [apps/web/app/api/auth/](apps/web/app/api/auth) | Better Auth HTTP route namespace for session, JWT and public-key operations. | 1 |
| [apps/web/app/api/auth/[...all]/](apps/web/app/api/auth/%5B...all%5D) | Node-runtime catch-all Better Auth adapter that initializes supported migrations before handling authentication requests. | 1 |
| [apps/web/app/problems/](apps/web/app/problems) | Problem route namespace for individual practice workspaces. | 1 |
| [apps/web/app/problems/[slug]/](apps/web/app/problems/%5Bslug%5D) | Dynamic problem route that resolves the public slug and mounts the practice workspace. | 1 |
| [apps/web/app/submissions/](apps/web/app/submissions) | Route entry point for the authenticated learner submission-history interface. | 1 |
| [apps/web/components/](apps/web/components) | Shared navigation shell and SVG icon components reused by the application features. | 2 |
| [apps/web/features/](apps/web/features) | Product-owned browser and server modules grouped by accounts, authored hints, practice and submissions. | 12 |
| [apps/web/features/accounts/](apps/web/features/accounts) | Account form, browser session client and server-side Better Auth authority with persistent local state. | 3 |
| [apps/web/features/hints/](apps/web/features/hints) | Authenticated authored-hint requests and UI with bounded contracts, provenance validation, cancellation and safe errors. | 2 |
| [apps/web/features/practice/](apps/web/features/practice) | Problem catalog, public response validation, practice workspace and locally persisted Monaco or textarea editing. | 4 |
| [apps/web/features/submissions/](apps/web/features/submissions) | Explicit run and submit actions, bounded API requests, capability checks and private saved-result history. | 3 |
| [apps/web/scripts/](apps/web/scripts) | Web-owned official auth migration and locally bundled Monaco asset preparation commands. | 2 |
| [apps/web/tests/](apps/web/tests) | Real Better Auth integration checks using isolated temporary databases and keys. | 1 |
| [docs/](docs) | Active product and engineering documentation indexed by functional responsibility. | 172 |
| [docs/architecture/](docs/architecture) | Current and proposed service boundaries, repository organization and recorded architecture decisions. | 4 |
| [docs/architecture/adr/](docs/architecture/adr) | Dated decisions documenting the practice foundation and authenticated isolated judging boundaries. | 2 |
| [docs/engineering/](docs/engineering) | Contributor workflow, scoped implementation tasks and coding-agent practices. | 149 |
| [docs/engineering/backlog/](docs/engineering/backlog) | Canonical ordered task catalogue, generated issue cards and actual publication receipts. | 144 |
| [docs/engineering/backlog/issues/](docs/engineering/backlog/issues) | One generated Markdown card per stable backlog task with prerequisites, ownership paths and acceptance criteria. | 141 |
| [docs/governance/](docs/governance) | Maintainer decisions, original-code and content rights, and build-versus-reuse policies. | 3 |
| [docs/onboarding/](docs/onboarding) | Contributor orientation and reproducible installation, startup, validation and deployment instructions. | 2 |
| [docs/product/](docs/product) | Product vision, requirements, roadmap and the retained detailed idea and solver proposals. | 6 |
| [docs/research/](docs/research) | Dated audits, upstream study references, competitive positioning and model-evaluation proposals. | 5 |
| [docs/security/](docs/security) | Judge threat model, untrusted-execution boundaries and production release controls. | 1 |
| [docs/status/](docs/status) | Named-revision implementation evidence, current limitations and historical validation distinctions. | 1 |
| [scripts/](scripts) | Repository command implementations for local development, explicit GitHub tooling and verification. | 10 |
| [scripts/development/](scripts/development) | Native web, API and worker lifecycle orchestration and private local worker-token selection. | 3 |
| [scripts/github/](scripts/github) | Offline backlog generation, explicit safe issue publication and inert pull-request evidence checking. | 3 |
| [scripts/verification/](scripts/verification) | Packaging exclusion guards and deterministic inventory and preservation checks. | 4 |
| [services/](services) | Independently bounded application services and the trusted judge control plane. | 43 |
| [services/api/](services/api) | Python FastAPI application, frozen dependencies, container definition and service-owned tests. | 24 |
| [services/api/solver_api/](services/api/solver_api) | Stable API entry point composing feature modules and shared HTTP behavior. | 15 |
| [services/api/solver_api/features/](services/api/solver_api/features) | Server feature boundaries for catalog, authored hints, fixed identity verification and owned submissions. | 10 |
| [services/api/solver_api/features/catalog/](services/api/solver_api/features/catalog) | Original public problem content and validated catalog response models. | 3 |
| [services/api/solver_api/features/hints/](services/api/solver_api/features/hints) | Authenticated authored-hint contract and a bounded future-provider interface without real model inference. | 2 |
| [services/api/solver_api/features/identity/](services/api/solver_api/features/identity) | Fixed-issuer and fixed-JWKS bearer authentication for account-owned API access. | 2 |
| [services/api/solver_api/features/submissions/](services/api/solver_api/features/submissions) | Durable owned SQLite jobs, source history, quotas, idempotency and worker lease completion. | 2 |
| [services/api/solver_api/http/](services/api/solver_api/http) | Shared bounded request bodies, correlated safe error handling and HTTP support. | 3 |
| [services/api/tests/](services/api/tests) | API-owned regression suites grouped by their server feature responsibility. | 4 |
| [services/api/tests/catalog/](services/api/tests/catalog) | Catalog and shared request or error contract tests. | 1 |
| [services/api/tests/hints/](services/api/tests/hints) | Authored-hint authentication, provenance, provider-boundary and failure-contract tests. | 1 |
| [services/api/tests/identity/](services/api/tests/identity) | JWT, JWKS, issuer and authentication-boundary tests. | 1 |
| [services/api/tests/submissions/](services/api/tests/submissions) | Ownership, durable queue, quotas, idempotency, lease and completion regression tests. | 1 |
| [services/judge/](services/judge) | Trusted host judge controller, sandbox image definition and independently gated execution tests. | 19 |
| [services/judge/solver_judge/](services/judge/solver_judge) | Judge control, grading and restricted-program modules with deliberately shared bounded process transport. | 10 |
| [services/judge/solver_judge/control/](services/judge/solver_judge/control) | Trusted Docker and gVisor runner, worker lifecycle and read-only readiness diagnostics. | 4 |
| [services/judge/solver_judge/grading/](services/judge/solver_judge/grading) | Original problem grading cases and trusted expected-answer computations kept outside learner programs. | 2 |
| [services/judge/solver_judge/sandbox/](services/judge/solver_judge/sandbox) | Restricted learner-program supervisor copied into the isolated sandbox image. | 2 |
| [services/judge/tests/](services/judge/tests) | Judge tests grouped by trusted control, grading and actual isolation boundaries. | 5 |
| [services/judge/tests/control/](services/judge/tests/control) | Runner protocol, worker leasing and container lifecycle cleanup regression tests. | 2 |
| [services/judge/tests/grading/](services/judge/tests/grading) | Deterministic original grading-case and expected-answer checks. | 1 |
| [services/judge/tests/sandbox/](services/judge/tests/sandbox) | Bounded process transport checks and explicitly enabled live gVisor isolation tests. | 2 |
| [tests/](tests) | Cross-service browser regressions and repository-tooling safety tests. | 6 |
| [tests/e2e/](tests/e2e) | Recursive Playwright browser suites grouped by user-facing functionality. | 4 |
| [tests/e2e/hints/](tests/e2e/hints) | Guest and authenticated hint provenance, failure, timeout, cancellation and context-change browser checks. | 1 |
| [tests/e2e/practice/](tests/e2e/practice) | Catalog, editor, draft privacy, layout and API resilience browser checks. | 2 |
| [tests/e2e/submissions/](tests/e2e/submissions) | Account lifecycle, explicit isolated judging and cross-user private-history browser checks. | 1 |
| [tests/tooling/](tests/tooling) | Repository automation tests isolated from application services and remote side effects. | 2 |
| [tests/tooling/github/](tests/tooling/github) | Fake-client issue-publication and pull-request evidence safety checks without real GitHub writes. | 2 |

Ignored local folders such as `.local/`, `.venv/`, `node_modules/`, `.next/`, generated `public/monaco/`, browser reports and caches are runtime, dependency or generated data. They are intentionally outside the tracked source catalogue. Private state must remain ignored; it is not copied into preservation.

## Complete file map

Every one of the **462 tracked paths** appears once below, grouped by its immediate owning folder. Each entry explains its reviewed role. The linked full inventory records direct imports/dependencies and provenance. Product task ownership is defined by the target paths in the complete task specifications.

The [full inventory](AnalyseFuture/repository-inventory/COMPLETE_FILE_INVENTORY.txt) also records baseline assessments, risks, review provenance, sizes and hashes. Preserved material is marked inactive below, even when its upstream code describes an implemented research experiment. Documentation and configuration support a feature; their existence alone does not implement the planned behavior.

<details>
<summary>./ — 16 files</summary>

One modular Solver AI repository joining the working practice application, independently bounded services, development tooling, planned tasks and preserved research evidence.

| File | Purpose / feature |
| --- | --- |
| [.dockerignore](.dockerignore) | Exclude Git, runtime state, dependency/build caches and all AnalyseFuture evidence from web image context. |
| [.gitignore](.gitignore) | Keep private runtime state, credentials, dependencies and generated outputs out of Git. |
| [.node-version](.node-version) | Pin native/CI Node toolchain to 24.22.1. |
| [.npmrc](.npmrc) | Use writable task npm cache and disable funding chatter; no credentials configured. |
| [.python-version](.python-version) | Pin native Python toolchain to 3.12.14. |
| [AGENTS.md](AGENTS.md) | Agent operating rules and project priorities. |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contributor workflow, scope, review and licensing expectations. |
| [PROJECT_HANDOFF.md](PROJECT_HANDOFF.md) | Root homepage handoff: project goal, implemented/planned features, every tracked file/folder and full ordered task specifications. |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | Current functional ownership and location guide for the complete monorepo, preservation collections and post-relocation validation. |
| [README.md](README.md) | Primary orientation, current capabilities and development entry point. |
| [SECURITY.md](SECURITY.md) | Private vulnerability reporting and key execution/data boundaries. |
| [compose.cloud.yaml](compose.cloud.yaml) | Optional BuildKit system-CA secret for verified TLS during managed-cloud image builds. |
| [compose.yaml](compose.yaml) | Run separate nonroot/read-only web and API containers with persistent local-state volumes and loopback ports. |
| [package-lock.json](package-lock.json) | Frozen npm registry/workspace dependency graph with integrity hashes; reviewed structurally in history audit. |
| [package.json](package.json) | Root npm workspace and explicit API/web/auth/judge/build/browser command entrypoints. |
| [playwright.config.ts](playwright.config.ts) | Browser suite web/API/optional judge orchestration with temporary DBs and system browser override |

</details>

<details>
<summary>.github/ — 1 files</summary>

Repository-hosted contributor templates and read-only GitHub Actions configuration.

| File | Purpose / feature |
| --- | --- |
| [PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md) | Contributor review template with one explicitly incomplete fenced evidence record to fill. |

</details>

<details>
<summary>.github/workflows/ — 2 files</summary>

Hosted application checks and trusted-base pull-request evidence validation workflows.

| File | Purpose / feature |
| --- | --- |
| [ci.yml](.github/workflows/ci.yml) | Read-only-permission hosted dependency, source, test, browser and archive-preservation validation. |
| [pr-evidence.yml](.github/workflows/pr-evidence.yml) | Metadata-only PR open/edit/head synchronization check using trusted base SHA and read-only checkout. |

</details>

<details>
<summary>AnalyseFuture/ — 4 files</summary>

Organized recovery evidence, inventories, migration records and inactive upstream or historical material kept outside application execution.

| File | Purpose / feature |
| --- | --- |
| [.gitattributes](AnalyseFuture/.gitattributes) | Preservation-folder Git inclusion and byte/filter policy |
| [.gitignore](AnalyseFuture/.gitignore) | Preservation-folder Git inclusion and byte/filter policy |
| [README.md](AnalyseFuture/README.md) | Preservation rationale, inventory map and inactive-reference boundaries |
| [manifest.json](AnalyseFuture/manifest.json) | Original tracked-path inventory, archive/member SHA-256 hashes and preserved destinations |

</details>

<details>
<summary>AnalyseFuture/archives/ — 2 files</summary>

Unchanged original uploaded ZIPs preserved as inactive provenance evidence rather than installed application packages.

| File | Purpose / feature |
| --- | --- |
| [CodeGenerator-master.zip](AnalyseFuture/archives/CodeGenerator-master.zip) | **Inactive preserved material.** Original user-supplied research archive, byte-preserved evidence |
| [phi-code-main.zip](AnalyseFuture/archives/phi-code-main.zip) | **Inactive preserved material.** Original user-supplied research archive, byte-preserved evidence |

</details>

<details>
<summary>AnalyseFuture/audits/ — 2 files</summary>

Evidence-scoped repository, Git history and security review findings with attribution and investigation limits.

| File | Purpose / feature |
| --- | --- |
| [REPOSITORY_AUDIT.txt](AnalyseFuture/audits/REPOSITORY_AUDIT.txt) | SOLVER AI — COMPLETE REPOSITORY REVIEW |
| [SECURITY_AUDIT.txt](AnalyseFuture/audits/SECURITY_AUDIT.txt) | SOLVER AI — SECURITY AND HISTORY REVIEW |

</details>

<details>
<summary>AnalyseFuture/continuation/ — 2 files</summary>

Persistent progress and next-developer instructions for resuming work without relying on chat memory.

| File | Purpose / feature |
| --- | --- |
| [NEXT_DEVELOPER_INSTRUCTIONS.txt](AnalyseFuture/continuation/NEXT_DEVELOPER_INSTRUCTIONS.txt) | SOLVER AI — NEXT DEVELOPER CONTINUATION GUIDE |
| [WORK_PROGRESS.txt](AnalyseFuture/continuation/WORK_PROGRESS.txt) | WORK PROGRESS - 17 November 2026, Asia/Kolkata |

</details>

<details>
<summary>AnalyseFuture/extracted/CodeGenerator-master/ — 5 files</summary>

Inactive CodeGenerator upload snapshot preserving original research source, dependencies, licenses, benchmark material and images, without active application adoption.

| File | Purpose / feature |
| --- | --- |
| [.env.example](AnalyseFuture/extracted/CodeGenerator-master/.env.example) | **Inactive preserved material.** Research provider configuration example with empty credential fields |
| [.gitignore.upstream](AnalyseFuture/extracted/CodeGenerator-master/.gitignore.upstream) | **Inactive preserved material.** Preserved upstream Git ignore/attribute policy, renamed so it has no Git effect |
| [LICENSE](AnalyseFuture/extracted/CodeGenerator-master/LICENSE) | **Inactive preserved material.** Original MIT source license notice |
| [README.md](AnalyseFuture/extracted/CodeGenerator-master/README.md) | **Inactive preserved material.** Research framework purpose, setup and benchmark claims |
| [requirements.txt](AnalyseFuture/extracted/CodeGenerator-master/requirements.txt) | **Inactive preserved material.** Archived research dependency declarations |

</details>

<details>
<summary>AnalyseFuture/extracted/CodeGenerator-master/data/APPS/ — 1 files</summary>

Inactive uploaded APPS selection preserved as research data with provenance and reuse limits unverified.

| File | Purpose / feature |
| --- | --- |
| [selected150.jsonl](AnalyseFuture/extracted/CodeGenerator-master/data/APPS/selected150.jsonl) | **Inactive preserved material.** Preserved APPS benchmark problem/completion/test records |

</details>

<details>
<summary>AnalyseFuture/extracted/CodeGenerator-master/data/HumanEval/ — 3 files</summary>

Inactive uploaded HumanEval-family evaluation fixtures preserved as research data rather than production problem content.

| File | Purpose / feature |
| --- | --- |
| [HumanEval.jsonl](AnalyseFuture/extracted/CodeGenerator-master/data/HumanEval/HumanEval.jsonl) | **Inactive preserved material.** Preserved HumanEval benchmark problem/completion/test records |
| [HumanEvalET.jsonl](AnalyseFuture/extracted/CodeGenerator-master/data/HumanEval/HumanEvalET.jsonl) | **Inactive preserved material.** Preserved HumanEval benchmark problem/completion/test records |
| [HumanEvalIncreasedSampleIO.jsonl](AnalyseFuture/extracted/CodeGenerator-master/data/HumanEval/HumanEvalIncreasedSampleIO.jsonl) | **Inactive preserved material.** Preserved HumanEval benchmark problem/completion/test records |

</details>

<details>
<summary>AnalyseFuture/extracted/CodeGenerator-master/data/MBPPEval/ — 3 files</summary>

Inactive uploaded MBPP evaluation variants preserved as research data rather than approved training material.

| File | Purpose / feature |
| --- | --- |
| [MBPP.jsonl](AnalyseFuture/extracted/CodeGenerator-master/data/MBPPEval/MBPP.jsonl) | **Inactive preserved material.** Preserved MBPPEval benchmark problem/completion/test records |
| [MBPP_ET.jsonl](AnalyseFuture/extracted/CodeGenerator-master/data/MBPPEval/MBPP_ET.jsonl) | **Inactive preserved material.** Preserved MBPPEval benchmark problem/completion/test records |
| [mbpp-py.jsonl](AnalyseFuture/extracted/CodeGenerator-master/data/MBPPEval/mbpp-py.jsonl) | **Inactive preserved material.** Preserved MBPPEval benchmark problem/completion/test records |

</details>

<details>
<summary>AnalyseFuture/extracted/CodeGenerator-master/data/xCodeEval/ — 3 files</summary>

Inactive uploaded xCodeEval descriptions, cases and evaluation records preserved without validating their reuse rights.

| File | Purpose / feature |
| --- | --- |
| [problem_descriptions.jsonl](AnalyseFuture/extracted/CodeGenerator-master/data/xCodeEval/problem_descriptions.jsonl) | **Inactive preserved material.** Preserved xCodeEval benchmark problem/completion/test records |
| [prog_syn_val.jsonl](AnalyseFuture/extracted/CodeGenerator-master/data/xCodeEval/prog_syn_val.jsonl) | **Inactive preserved material.** Preserved xCodeEval benchmark problem/completion/test records |
| [unittest_db.json](AnalyseFuture/extracted/CodeGenerator-master/data/xCodeEval/unittest_db.json) | **Inactive preserved material.** xCodeEval source-ID to reference test-list database |

</details>

<details>
<summary>AnalyseFuture/extracted/CodeGenerator-master/images/ — 4 files</summary>

Inactive uploaded research diagrams and result graphics preserved as upstream artifacts, not reproduced performance evidence.

| File | Purpose / feature |
| --- | --- |
| [CodeSim-Overview.png](AnalyseFuture/extracted/CodeGenerator-master/images/CodeSim-Overview.png) | **Inactive preserved material.** Research pipeline illustration or reported benchmark figure |
| [basic-results.png](AnalyseFuture/extracted/CodeGenerator-master/images/basic-results.png) | **Inactive preserved material.** Research pipeline illustration or reported benchmark figure |
| [contest-results.png](AnalyseFuture/extracted/CodeGenerator-master/images/contest-results.png) | **Inactive preserved material.** Research pipeline illustration or reported benchmark figure |
| [opensource-llm-results.png](AnalyseFuture/extracted/CodeGenerator-master/images/opensource-llm-results.png) | **Inactive preserved material.** Research pipeline illustration or reported benchmark figure |

</details>

<details>
<summary>AnalyseFuture/extracted/CodeGenerator-master/src/ — 1 files</summary>

Inactive uploaded Python research pipeline source retained for reference without installation or execution.

| File | Purpose / feature |
| --- | --- |
| [main.py](AnalyseFuture/extracted/CodeGenerator-master/src/main.py) | **Inactive preserved material.** CLI benchmark experiment orchestration, model/dataset/strategy selection, result resume and extended-test summaries |

</details>

<details>
<summary>AnalyseFuture/extracted/CodeGenerator-master/src/constants/ — 4 files</summary>

Inactive uploaded language, path and verbosity configuration for the upstream research pipeline.

| File | Purpose / feature |
| --- | --- |
| [__init__.py](AnalyseFuture/extracted/CodeGenerator-master/src/constants/__init__.py) | **Inactive preserved material.** Empty research package marker |
| [lang_mappings.py](AnalyseFuture/extracted/CodeGenerator-master/src/constants/lang_mappings.py) | **Inactive preserved material.** Map research language labels to external ExecEval runtime names |
| [paths.py](AnalyseFuture/extracted/CodeGenerator-master/src/constants/paths.py) | **Inactive preserved material.** Relative benchmark data and output path constants |
| [verboseType.py](AnalyseFuture/extracted/CodeGenerator-master/src/constants/verboseType.py) | **Inactive preserved material.** Verbosity level constants |

</details>

<details>
<summary>AnalyseFuture/extracted/CodeGenerator-master/src/datasets/ — 10 files</summary>

Inactive uploaded benchmark adapters, dataset factory and conversion utilities retained for provenance.

| File | Purpose / feature |
| --- | --- |
| [APPSDataset.py](AnalyseFuture/extracted/CodeGenerator-master/src/datasets/APPSDataset.py) | **Inactive preserved material.** APPS statement/sample/full-test adapter for external execution |
| [CodeContestDataset.py](AnalyseFuture/extracted/CodeGenerator-master/src/datasets/CodeContestDataset.py) | **Inactive preserved material.** CodeContests statement/sample/full-test adapter for external execution |
| [Dataset.py](AnalyseFuture/extracted/CodeGenerator-master/src/datasets/Dataset.py) | **Inactive preserved material.** Abstract JSONL dataset loader and evaluation/prompt interface |
| [DatasetFactory.py](AnalyseFuture/extracted/CodeGenerator-master/src/datasets/DatasetFactory.py) | **Inactive preserved material.** Resolve benchmark dataset names to adapter classes |
| [HumanEvalDataset.py](AnalyseFuture/extracted/CodeGenerator-master/src/datasets/HumanEvalDataset.py) | **Inactive preserved material.** HumanEval functional-test and prompt adapter |
| [MBPPDataset.py](AnalyseFuture/extracted/CodeGenerator-master/src/datasets/MBPPDataset.py) | **Inactive preserved material.** MBPP functional-test and prompt adapter |
| [XCodeDataset.py](AnalyseFuture/extracted/CodeGenerator-master/src/datasets/XCodeDataset.py) | **Inactive preserved material.** xCodeEval standard-input/sample/full-test adapter |
| [__init__.py](AnalyseFuture/extracted/CodeGenerator-master/src/datasets/__init__.py) | **Inactive preserved material.** Empty research package marker |
| [convert-apps-xcode.py](AnalyseFuture/extracted/CodeGenerator-master/src/datasets/convert-apps-xcode.py) | **Inactive preserved material.** Select and convert APPS data into external-executor record format |
| [convert-cc-xcode.py](AnalyseFuture/extracted/CodeGenerator-master/src/datasets/convert-cc-xcode.py) | **Inactive preserved material.** Convert CodeContests parquet public/private/generated tests to executor record format |

</details>

<details>
<summary>AnalyseFuture/extracted/CodeGenerator-master/src/evaluations/ — 8 files</summary>

Inactive uploaded execution and benchmark-scoring helpers whose host or external execution paths are not adopted by Solver AI.

| File | Purpose / feature |
| --- | --- |
| [__init__.py](AnalyseFuture/extracted/CodeGenerator-master/src/evaluations/__init__.py) | **Inactive preserved material.** Empty research package marker |
| [api_comm.py](AnalyseFuture/extracted/CodeGenerator-master/src/evaluations/api_comm.py) | **Inactive preserved material.** External ExecEval HTTP client and result dataclasses |
| [evalute.py](AnalyseFuture/extracted/CodeGenerator-master/src/evaluations/evalute.py) | **Inactive preserved material.** Invoke external execution and construct test-result feedback |
| [exec_outcome.py](AnalyseFuture/extracted/CodeGenerator-master/src/evaluations/exec_outcome.py) | **Inactive preserved material.** External execution verdict enum |
| [executor_utils.py](AnalyseFuture/extracted/CodeGenerator-master/src/evaluations/executor_utils.py) | **Inactive preserved material.** Thread timeout/result propagation and JSONL utility |
| [func_evaluate.py](AnalyseFuture/extracted/CodeGenerator-master/src/evaluations/func_evaluate.py) | **Inactive preserved material.** Execute generated Python with functional/assertion tests in host globals |
| [limits_by_lang.yaml](AnalyseFuture/extracted/CodeGenerator-master/src/evaluations/limits_by_lang.yaml) | **Inactive preserved material.** Requested per-runtime resource limits for external executor |
| [resource_limit.py](AnalyseFuture/extracted/CodeGenerator-master/src/evaluations/resource_limit.py) | **Inactive preserved material.** Resource-limit dataclass and prlimit-string example; not sandbox enforcement |

</details>

<details>
<summary>AnalyseFuture/extracted/CodeGenerator-master/src/models/ — 7 files</summary>

Inactive uploaded provider adapters retained as upstream research source without credentials or configured model calls.

| File | Purpose / feature |
| --- | --- |
| [Anthropic.py](AnalyseFuture/extracted/CodeGenerator-master/src/models/Anthropic.py) | **Inactive preserved material.** Anthropic-branded OpenRouter chat adapter with token accounting |
| [Base.py](AnalyseFuture/extracted/CodeGenerator-master/src/models/Base.py) | **Inactive preserved material.** Abstract provider prompt interface |
| [Gemini.py](AnalyseFuture/extracted/CodeGenerator-master/src/models/Gemini.py) | **Inactive preserved material.** Gemini generation adapter with metadata and retry |
| [GroqModel.py](AnalyseFuture/extracted/CodeGenerator-master/src/models/GroqModel.py) | **Inactive preserved material.** Groq chat adapter with retry and token accounting |
| [ModelFactory.py](AnalyseFuture/extracted/CodeGenerator-master/src/models/ModelFactory.py) | **Inactive preserved material.** Provider name to adapter selection; eagerly imports providers |
| [OpenAI.py](AnalyseFuture/extracted/CodeGenerator-master/src/models/OpenAI.py) | **Inactive preserved material.** OpenAI/Azure SDK and raw HTTP chat adapters with token logs |
| [__init__.py](AnalyseFuture/extracted/CodeGenerator-master/src/models/__init__.py) | **Inactive preserved material.** Empty research package marker |

</details>

<details>
<summary>AnalyseFuture/extracted/CodeGenerator-master/src/promptings/ — 9 files</summary>

Inactive uploaded planning, code-generation and repair strategies preserved for conceptual study.

| File | Purpose / feature |
| --- | --- |
| [Analogical.py](AnalyseFuture/extracted/CodeGenerator-master/src/promptings/Analogical.py) | **Inactive preserved material.** Analogical exemplar-based generation strategy |
| [Base.py](AnalyseFuture/extracted/CodeGenerator-master/src/promptings/Base.py) | **Inactive preserved material.** Benchmark loop, resume handling, pass budget and result accumulation |
| [CoT.py](AnalyseFuture/extracted/CodeGenerator-master/src/promptings/CoT.py) | **Inactive preserved material.** Dataset-conditioned few-shot reasoning/code prompt strategy |
| [CodeSIM.py](AnalyseFuture/extracted/CodeGenerator-master/src/promptings/CodeSIM.py) | **Inactive preserved material.** Exemplar/plan simulation, refinement, code generation and bounded debug strategy |
| [Direct.py](AnalyseFuture/extracted/CodeGenerator-master/src/promptings/Direct.py) | **Inactive preserved material.** Single direct generation strategy |
| [MapCoder.py](AnalyseFuture/extracted/CodeGenerator-master/src/promptings/MapCoder.py) | **Inactive preserved material.** Multiple exemplar plans, confidence ordering and sample-based repair strategy |
| [PromptingFactory.py](AnalyseFuture/extracted/CodeGenerator-master/src/promptings/PromptingFactory.py) | **Inactive preserved material.** Select named prompting/ablation strategy |
| [SelfPlanning.py](AnalyseFuture/extracted/CodeGenerator-master/src/promptings/SelfPlanning.py) | **Inactive preserved material.** Two-stage dataset-conditioned planning then implementation strategy |
| [__init__.py](AnalyseFuture/extracted/CodeGenerator-master/src/promptings/__init__.py) | **Inactive preserved material.** Empty research package marker |

</details>

<details>
<summary>AnalyseFuture/extracted/CodeGenerator-master/src/promptings/variations/ — 5 files</summary>

Inactive uploaded CodeSIM strategy variants retained for research comparison rather than current product features.

| File | Purpose / feature |
| --- | --- |
| [CodeSIMA.py](AnalyseFuture/extracted/CodeGenerator-master/src/promptings/variations/CodeSIMA.py) | **Inactive preserved material.** CodeSIM additional generated assertions variant (consensus/intersection of tests) |
| [CodeSIMC.py](AnalyseFuture/extracted/CodeGenerator-master/src/promptings/variations/CodeSIMC.py) | **Inactive preserved material.** CodeSIM competitive prompting variant |
| [CodeSIMWD.py](AnalyseFuture/extracted/CodeGenerator-master/src/promptings/variations/CodeSIMWD.py) | **Inactive preserved material.** CodeSIM ablation omitting debugging |
| [CodeSIMWPV.py](AnalyseFuture/extracted/CodeGenerator-master/src/promptings/variations/CodeSIMWPV.py) | **Inactive preserved material.** CodeSIM ablation omitting plan verification |
| [CodeSIMWPVD.py](AnalyseFuture/extracted/CodeGenerator-master/src/promptings/variations/CodeSIMWPVD.py) | **Inactive preserved material.** CodeSIM ablation omitting plan verification and debugging |

</details>

<details>
<summary>AnalyseFuture/extracted/CodeGenerator-master/src/results/ — 2 files</summary>

Inactive uploaded research result persistence helpers retained with their source provenance.

| File | Purpose / feature |
| --- | --- |
| [Results.py](AnalyseFuture/extracted/CodeGenerator-master/src/results/Results.py) | **Inactive preserved material.** Load, append, persist and index resumable experiment JSONL results |
| [__init__.py](AnalyseFuture/extracted/CodeGenerator-master/src/results/__init__.py) | **Inactive preserved material.** Empty research package marker |

</details>

<details>
<summary>AnalyseFuture/extracted/CodeGenerator-master/src/utils/ — 8 files</summary>

Inactive uploaded parsing, cost, data and execution utilities retained without importing their execution behavior.

| File | Purpose / feature |
| --- | --- |
| [__init__.py](AnalyseFuture/extracted/CodeGenerator-master/src/utils/__init__.py) | **Inactive preserved material.** Empty research package marker |
| [evaluateET.py](AnalyseFuture/extracted/CodeGenerator-master/src/utils/evaluateET.py) | **Inactive preserved material.** Re-evaluate HumanEval/MBPP completions against extended tests |
| [generateEP.py](AnalyseFuture/extracted/CodeGenerator-master/src/utils/generateEP.py) | **Inactive preserved material.** Format completions for optional EvalPlus evaluation |
| [jsonl.py](AnalyseFuture/extracted/CodeGenerator-master/src/utils/jsonl.py) | **Inactive preserved material.** JSONL read/write/append helpers with output directory creation |
| [parse.py](AnalyseFuture/extracted/CodeGenerator-master/src/utils/parse.py) | **Inactive preserved material.** Extract final fenced source code or numbered plans from provider text |
| [runEP.py](AnalyseFuture/extracted/CodeGenerator-master/src/utils/runEP.py) | **Inactive preserved material.** Optional shell-based EvalPlus Docker invocation with fixed developer mounts |
| [summary.py](AnalyseFuture/extracted/CodeGenerator-master/src/utils/summary.py) | **Inactive preserved material.** Aggregate solved counts, token usage, API calls and elapsed time |
| [tokenCount.py](AnalyseFuture/extracted/CodeGenerator-master/src/utils/tokenCount.py) | **Inactive preserved material.** Approximate chat token counting with fixed tokenizer heuristics |

</details>

<details>
<summary>AnalyseFuture/extracted/phi-code-main/ — 7 files</summary>

Inactive phi-code upload snapshot preserving candidate-generation, ranking and alternate UI research with its original notices.

| File | Purpose / feature |
| --- | --- |
| [.gitattributes.upstream](AnalyseFuture/extracted/phi-code-main/.gitattributes.upstream) | **Inactive preserved material.** Preserved upstream Git ignore/attribute policy, renamed so it has no Git effect |
| [.gitignore.upstream](AnalyseFuture/extracted/phi-code-main/.gitignore.upstream) | **Inactive preserved material.** Preserved upstream Git ignore/attribute policy, renamed so it has no Git effect |
| [LICENSE](AnalyseFuture/extracted/phi-code-main/LICENSE) | **Inactive preserved material.** Original Apache-2.0 source license notice |
| [README.md](AnalyseFuture/extracted/phi-code-main/README.md) | **Inactive preserved material.** Research framework purpose, setup and benchmark claims |
| [curses_ui.png](AnalyseFuture/extracted/phi-code-main/curses_ui.png) | **Inactive preserved material.** Research UI screenshot |
| [terminal_mode.png](AnalyseFuture/extracted/phi-code-main/terminal_mode.png) | **Inactive preserved material.** Research UI screenshot |
| [webui.png](AnalyseFuture/extracted/phi-code-main/webui.png) | **Inactive preserved material.** Research UI screenshot |

</details>

<details>
<summary>AnalyseFuture/extracted/phi-code-main/contests_results/leetcode_weekly_476/ — 4 files</summary>

Inactive uploaded weekly-contest 476 statements and experiment outputs retained solely as supplied research artifacts.

| File | Purpose / feature |
| --- | --- |
| [3745_statement.txt](AnalyseFuture/extracted/phi-code-main/contests_results/leetcode_weekly_476/3745_statement.txt) | **Inactive preserved material.** Historical contest problem statement |
| [3746_statement.txt](AnalyseFuture/extracted/phi-code-main/contests_results/leetcode_weekly_476/3746_statement.txt) | **Inactive preserved material.** Historical contest problem statement |
| [3747_statement.txt](AnalyseFuture/extracted/phi-code-main/contests_results/leetcode_weekly_476/3747_statement.txt) | **Inactive preserved material.** Historical contest problem statement |
| [3748_statment.txt](AnalyseFuture/extracted/phi-code-main/contests_results/leetcode_weekly_476/3748_statment.txt) | **Inactive preserved material.** Historical research command/output log |

</details>

<details>
<summary>AnalyseFuture/extracted/phi-code-main/contests_results/leetcode_weekly_476/gpt_oss_20B/ — 8 files</summary>

Inactive uploaded weekly-contest 476 commands and candidate records labeled by upstream as a model experiment.

| File | Purpose / feature |
| --- | --- |
| [3745_command.txt](AnalyseFuture/extracted/phi-code-main/contests_results/leetcode_weekly_476/gpt_oss_20B/3745_command.txt) | **Inactive preserved material.** Historical research command/output log |
| [3745_solutions.jsonl](AnalyseFuture/extracted/phi-code-main/contests_results/leetcode_weekly_476/gpt_oss_20B/3745_solutions.jsonl) | **Inactive preserved material.** Historical generated candidate solutions, sample-pass counts and embedding scores |
| [3746_command.txt](AnalyseFuture/extracted/phi-code-main/contests_results/leetcode_weekly_476/gpt_oss_20B/3746_command.txt) | **Inactive preserved material.** Historical research command/output log |
| [3746_solutions.jsonl](AnalyseFuture/extracted/phi-code-main/contests_results/leetcode_weekly_476/gpt_oss_20B/3746_solutions.jsonl) | **Inactive preserved material.** Historical generated candidate solutions, sample-pass counts and embedding scores |
| [3747_command.txt](AnalyseFuture/extracted/phi-code-main/contests_results/leetcode_weekly_476/gpt_oss_20B/3747_command.txt) | **Inactive preserved material.** Historical research command/output log |
| [3747_solutions.jsonl](AnalyseFuture/extracted/phi-code-main/contests_results/leetcode_weekly_476/gpt_oss_20B/3747_solutions.jsonl) | **Inactive preserved material.** Historical generated candidate solutions, sample-pass counts and embedding scores |
| [3748_command.txt](AnalyseFuture/extracted/phi-code-main/contests_results/leetcode_weekly_476/gpt_oss_20B/3748_command.txt) | **Inactive preserved material.** Historical research command/output log |
| [3748_solutions.jsonl](AnalyseFuture/extracted/phi-code-main/contests_results/leetcode_weekly_476/gpt_oss_20B/3748_solutions.jsonl) | **Inactive preserved material.** Historical generated candidate solutions, sample-pass counts and embedding scores |

</details>

<details>
<summary>AnalyseFuture/extracted/phi-code-main/contests_results/leetcode_weekly_477/ — 4 files</summary>

Inactive uploaded weekly-contest 477 statements and experiment outputs retained solely as supplied research artifacts.

| File | Purpose / feature |
| --- | --- |
| [3754.txt](AnalyseFuture/extracted/phi-code-main/contests_results/leetcode_weekly_477/3754.txt) | **Inactive preserved material.** Historical contest problem statement |
| [3755.txt](AnalyseFuture/extracted/phi-code-main/contests_results/leetcode_weekly_477/3755.txt) | **Inactive preserved material.** Historical contest problem statement |
| [3756.txt](AnalyseFuture/extracted/phi-code-main/contests_results/leetcode_weekly_477/3756.txt) | **Inactive preserved material.** Historical contest problem statement |
| [3757.txt](AnalyseFuture/extracted/phi-code-main/contests_results/leetcode_weekly_477/3757.txt) | **Inactive preserved material.** Historical contest problem statement |

</details>

<details>
<summary>AnalyseFuture/extracted/phi-code-main/contests_results/leetcode_weekly_477/gpt_oss_20B/ — 4 files</summary>

Inactive uploaded weekly-contest 477 candidate records retained as upstream artifacts rather than verified benchmark evidence.

| File | Purpose / feature |
| --- | --- |
| [3754.jsonl](AnalyseFuture/extracted/phi-code-main/contests_results/leetcode_weekly_477/gpt_oss_20B/3754.jsonl) | **Inactive preserved material.** Historical generated candidate solutions, sample-pass counts and embedding scores |
| [3755.jsonl](AnalyseFuture/extracted/phi-code-main/contests_results/leetcode_weekly_477/gpt_oss_20B/3755.jsonl) | **Inactive preserved material.** Historical generated candidate solutions, sample-pass counts and embedding scores |
| [3756.jsonl](AnalyseFuture/extracted/phi-code-main/contests_results/leetcode_weekly_477/gpt_oss_20B/3756.jsonl) | **Inactive preserved material.** Historical generated candidate solutions, sample-pass counts and embedding scores |
| [3757.jsonl](AnalyseFuture/extracted/phi-code-main/contests_results/leetcode_weekly_477/gpt_oss_20B/3757.jsonl) | **Inactive preserved material.** Historical generated candidate solutions, sample-pass counts and embedding scores |

</details>

<details>
<summary>AnalyseFuture/extracted/phi-code-main/datasets/ — 5 files</summary>

Inactive uploaded Git LFS pointer files preserved exactly, with the referenced dataset objects absent from the ZIP.

| File | Purpose / feature |
| --- | --- |
| [atcoder.jsonl](AnalyseFuture/extracted/phi-code-main/datasets/atcoder.jsonl) | **Inactive preserved material.** Git LFS pointer to upstream ranker dataset, not dataset contents |
| [codechef.jsonl](AnalyseFuture/extracted/phi-code-main/datasets/codechef.jsonl) | **Inactive preserved material.** Git LFS pointer to upstream ranker dataset, not dataset contents |
| [codeforces.jsonl](AnalyseFuture/extracted/phi-code-main/datasets/codeforces.jsonl) | **Inactive preserved material.** Git LFS pointer to upstream ranker dataset, not dataset contents |
| [codeforces_positive.jsonl](AnalyseFuture/extracted/phi-code-main/datasets/codeforces_positive.jsonl) | **Inactive preserved material.** Git LFS pointer to upstream ranker dataset, not dataset contents |
| [leetcode.jsonl](AnalyseFuture/extracted/phi-code-main/datasets/leetcode.jsonl) | **Inactive preserved material.** Git LFS pointer to upstream ranker dataset, not dataset contents |

</details>

<details>
<summary>AnalyseFuture/extracted/phi-code-main/ranker/ — 5 files</summary>

Inactive uploaded embedding-ranker data and training utilities retained without model downloads or training execution.

| File | Purpose / feature |
| --- | --- |
| [check_datasets.py](AnalyseFuture/extracted/phi-code-main/ranker/check_datasets.py) | **Inactive preserved material.** Inspect triplet/pair dataset field and token-length compatibility with selected ranker |
| [filter_datasets.py](AnalyseFuture/extracted/phi-code-main/ranker/filter_datasets.py) | **Inactive preserved material.** Write dataset subsets fitting the ranker tokenizer length limit |
| [log_config.py](AnalyseFuture/extracted/phi-code-main/ranker/log_config.py) | **Inactive preserved material.** Install file/console logging handlers for research utilities |
| [sample_dataset.py](AnalyseFuture/extracted/phi-code-main/ranker/sample_dataset.py) | **Inactive preserved material.** Randomly sample a chosen percentage of JSONL records |
| [train.py](AnalyseFuture/extracted/phi-code-main/ranker/train.py) | **Inactive preserved material.** Fine-tune sentence-transformer ranker using triplet/contrastive losses and multiple datasets |

</details>

<details>
<summary>AnalyseFuture/extracted/phi-code-main/solver/ — 12 files</summary>

Inactive uploaded model-client, candidate-execution and alternate-interface source whose host execution paths are not adopted.

| File | Purpose / feature |
| --- | --- |
| [atcoder.py](AnalyseFuture/extracted/phi-code-main/solver/atcoder.py) | **Inactive preserved material.** Parse AtCoder samples and score generated Python via host subprocesses |
| [codeforces.py](AnalyseFuture/extracted/phi-code-main/solver/codeforces.py) | **Inactive preserved material.** Parse Codeforces samples and score generated Python via host subprocesses |
| [curses_ui.py](AnalyseFuture/extracted/phi-code-main/solver/curses_ui.py) | **Inactive preserved material.** Interactive curses viewer/generation/save controls for ranked code candidates |
| [general_prompt.txt](AnalyseFuture/extracted/phi-code-main/solver/general_prompt.txt) | **Inactive preserved material.** Python standard-input program generation prompt template |
| [leetcode.py](AnalyseFuture/extracted/phi-code-main/solver/leetcode.py) | **Inactive preserved material.** Parse LeetCode examples and score generated Solution classes through exec in multiprocessing |
| [leetcode_prompt.txt](AnalyseFuture/extracted/phi-code-main/solver/leetcode_prompt.txt) | **Inactive preserved material.** Python Solution-class generation prompt template with optional sortedcontainers |
| [log_config.py](AnalyseFuture/extracted/phi-code-main/solver/log_config.py) | **Inactive preserved material.** Install file/console logging handlers for research solver |
| [main.py](AnalyseFuture/extracted/phi-code-main/solver/main.py) | **Inactive preserved material.** Configure local-model endpoint/ranker/site/interface and launch solver UI/CLI |
| [requirements.txt](AnalyseFuture/extracted/phi-code-main/solver/requirements.txt) | **Inactive preserved material.** Archived research dependency declarations |
| [terminal.py](AnalyseFuture/extracted/phi-code-main/solver/terminal.py) | **Inactive preserved material.** Generate multiple candidates, run sample tests, embed/rank and sort by pass count then similarity |
| [utils.py](AnalyseFuture/extracted/phi-code-main/solver/utils.py) | **Inactive preserved material.** Request compatible chat completions and save candidate JSONL output |
| [web_ui.py](AnalyseFuture/extracted/phi-code-main/solver/web_ui.py) | **Inactive preserved material.** Gradio interface for generation, evidence display and candidate navigation |

</details>

<details>
<summary>AnalyseFuture/historical-implementations/project-memory/ — 2 files</summary>

Inactive original project-memory branch documents preserved with source-commit provenance rather than treated as current instructions.

| File | Purpose / feature |
| --- | --- |
| [AGENTS.md.upstream](AnalyseFuture/historical-implementations/project-memory/AGENTS.md.upstream) | **Inactive preserved material.** Inert historical agent-instruction snapshot adding continuity-document reading requirements. |
| [README.md](AnalyseFuture/historical-implementations/project-memory/README.md) | **Inactive preserved material.** Historical root orientation augmented with project-memory, RTF handbook and continuity links. |

</details>

<details>
<summary>AnalyseFuture/historical-implementations/project-memory/docs/ — 7 files</summary>

Inactive original continuity, handbook and development prose preserved as historical branch evidence, not authoritative current guidance.

| File | Purpose / feature |
| --- | --- |
| [CHAT_CONTINUITY_LOG.md](AnalyseFuture/historical-implementations/project-memory/docs/CHAT_CONTINUITY_LOG.md) | **Inactive preserved material.** Historical accessible-conversation summaries, explicit excerpts, engineering timeline, decision table and handoff template. |
| [INDEX.md](AnalyseFuture/historical-implementations/project-memory/docs/INDEX.md) | **Inactive preserved material.** Historical navigation introducing memory, RTF, master spec, chat log and resume prompt. |
| [MASTER_DEVELOPMENT_SPEC.md](AnalyseFuture/historical-implementations/project-memory/docs/MASTER_DEVELOPMENT_SPEC.md) | **Inactive preserved material.** Historical structured restatement of the owner's ten-task development brief and original project constraints. |
| [PROJECT_MEMORY.md](AnalyseFuture/historical-implementations/project-memory/docs/PROJECT_MEMORY.md) | **Inactive preserved material.** Historical comprehensive continuity handbook: original intent, code map, diagrams, 20 references, two primary solvers, P0-P4 backlog, owner decisions and commands. |
| [RESUME_PROMPT.md](AnalyseFuture/historical-implementations/project-memory/docs/RESUME_PROMPT.md) | **Inactive preserved material.** Historical copy/paste startup prompt preserving continuity, source verification and next provider-design idea. |
| [SOLVER_AI_COMPLETE_HANDBOOK.rtf](AnalyseFuture/historical-implementations/project-memory/docs/SOLVER_AI_COMPLETE_HANDBOOK.rtf) | **Inactive preserved material.** Historical Word-readable compilation of project memory, conversation log, master development specification and resume prompt. |
| [START_HERE.md](AnalyseFuture/historical-implementations/project-memory/docs/START_HERE.md) | **Inactive preserved material.** Historical onboarding augmented with continuity-pack instructions and RTF link. |

</details>

<details>
<summary>AnalyseFuture/historical-implementations/sai-011/apps/web/app/ — 1 files</summary>

Inactive historical hint styling snapshot preserved without inclusion in the active web build.

| File | Purpose / feature |
| --- | --- |
| [globals.css](AnalyseFuture/historical-implementations/sai-011/apps/web/app/globals.css) | **Inactive preserved material.** Inactive original SAI-011 apps/web/app/globals.css version; retained before feature recovery/import repair. |

</details>

<details>
<summary>AnalyseFuture/historical-implementations/sai-011/apps/web/components/ — 2 files</summary>

Inactive original account-hint and workspace component versions preserved before feature-folder migration.

| File | Purpose / feature |
| --- | --- |
| [account-hint.tsx](AnalyseFuture/historical-implementations/sai-011/apps/web/components/account-hint.tsx) | **Inactive preserved material.** Inactive original SAI-011 apps/web/components/account-hint.tsx version; retained before feature recovery/import repair. |
| [workspace.tsx](AnalyseFuture/historical-implementations/sai-011/apps/web/components/workspace.tsx) | **Inactive preserved material.** Inactive original SAI-011 apps/web/components/workspace.tsx version; retained before feature recovery/import repair. |

</details>

<details>
<summary>AnalyseFuture/historical-implementations/sai-011/apps/web/lib/ — 1 files</summary>

Inactive original hint API client retained with its branch provenance rather than imported by the application.

| File | Purpose / feature |
| --- | --- |
| [hints.ts](AnalyseFuture/historical-implementations/sai-011/apps/web/lib/hints.ts) | **Inactive preserved material.** Inactive original SAI-011 apps/web/lib/hints.ts version; retained before feature recovery/import repair. |

</details>

<details>
<summary>AnalyseFuture/historical-implementations/sai-011/docs/ — 9 files</summary>

Inactive branch-specific status, research, backlog and handoff prose retained without replacing current documentation.

| File | Purpose / feature |
| --- | --- |
| [AI_ARCHITECTURE_PLAN.md](AnalyseFuture/historical-implementations/sai-011/docs/AI_ARCHITECTURE_PLAN.md) | **Inactive preserved material.** Historical staged AI architecture with exact authored provenance, bounded UI requests and future provider/debugger/solver gates. |
| [CODEX_PLAYBOOK.md](AnalyseFuture/historical-implementations/sai-011/docs/CODEX_PLAYBOOK.md) | **Inactive preserved material.** Historical corrected agent playbook recognizing implemented foundation and identifying SAI-011/provider ADR next steps. |
| [IMPLEMENTATION_BACKLOG.md](AnalyseFuture/historical-implementations/sai-011/docs/IMPLEMENTATION_BACKLOG.md) | **Inactive preserved material.** Historical P0-P4 backlog with user value, source paths, dependencies, acceptance, cost and rollback. |
| [IMPLEMENTATION_PROGRESS.md](AnalyseFuture/historical-implementations/sai-011/docs/IMPLEMENTATION_PROGRESS.md) | **Inactive preserved material.** Historical SAI-011 change log, hosted evidence, test-selector regression and resume handoff. |
| [INDEX.md](AnalyseFuture/historical-implementations/sai-011/docs/INDEX.md) | **Inactive preserved material.** Historical navigation for five SAI-011 research/backlog documents plus existing handbook. |
| [PRIMARY_RESEARCH_REPOS.md](AnalyseFuture/historical-implementations/sai-011/docs/PRIMARY_RESEARCH_REPOS.md) | **Inactive preserved material.** Historical exact-two-reference assessment of CodeSIM/MapCoder and phi-code, source modules, unsafe execution and acceptance gates. |
| [PROJECT_STATUS.md](AnalyseFuture/historical-implementations/sai-011/docs/PROJECT_STATUS.md) | **Inactive preserved material.** Historical implementation ledger distinguishing merged SAI-010, branch-only SAI-011 and recorded tests. |
| [PUBLIC_REPOSITORIES_AND_RESOURCES.txt](AnalyseFuture/historical-implementations/sai-011/docs/PUBLIC_REPOSITORIES_AND_RESOURCES.txt) | **Inactive preserved material.** Historical complete 20-repository inventory with refreshed November 16 verification note and adoption boundaries. |
| [REPOSITORY_AUDIT.md](AnalyseFuture/historical-implementations/sai-011/docs/REPOSITORY_AUDIT.md) | **Inactive preserved material.** Historical source-path audit of main 9952f8b and refreshed 20-reference default-head matrix. |

</details>

<details>
<summary>AnalyseFuture/historical-implementations/sai-011/tests/e2e/ — 1 files</summary>

Inactive original hint browser-spec snapshot preserved before relocation and additional cancellation regressions.

| File | Purpose / feature |
| --- | --- |
| [hints.spec.ts](AnalyseFuture/historical-implementations/sai-011/tests/e2e/hints.spec.ts) | **Inactive preserved material.** Inactive original SAI-011 tests/e2e/hints.spec.ts version; retained before feature recovery/import repair. |

</details>

<details>
<summary>AnalyseFuture/migration-records/ — 3 files</summary>

Original-to-current path mappings, consolidation decisions and preservation summaries for structural changes.

| File | Purpose / feature |
| --- | --- |
| [CONSOLIDATION_REPORT.txt](AnalyseFuture/migration-records/CONSOLIDATION_REPORT.txt) | SOLVER AI — CONSOLIDATION DECISIONS AND IMPLEMENTATION |
| [MIGRATION_SUMMARY.txt](AnalyseFuture/migration-records/MIGRATION_SUMMARY.txt) | SOLVER AI — MIGRATION SUMMARY |
| [ORIGINAL_TO_NEW_PATH_MAPPING.txt](AnalyseFuture/migration-records/ORIGINAL_TO_NEW_PATH_MAPPING.txt) | ORIGINAL TO NEW PATH MAPPING |

</details>

<details>
<summary>AnalyseFuture/planning/ — 2 files</summary>

Detailed future product vision and prioritized technical debt, with feasibility and delivery limits separated from implementation claims.

| File | Purpose / feature |
| --- | --- |
| [PROJECT_VISION_AND_FUTURE_ROADMAP.txt](AnalyseFuture/planning/PROJECT_VISION_AND_FUTURE_ROADMAP.txt) | SOLVER AI |
| [TECHNICAL_DEBT.txt](AnalyseFuture/planning/TECHNICAL_DEBT.txt) | SOLVER AI — TECHNICAL DEBT AND RELEASE GATES |

</details>

<details>
<summary>AnalyseFuture/repository-inventory/ — 12 files</summary>

Machine-readable and plain-text file, feature, dependency, baseline and preservation ledgers.

| File | Purpose / feature |
| --- | --- |
| [ARCHIVED_FILES_MANIFEST.txt](AnalyseFuture/repository-inventory/ARCHIVED_FILES_MANIFEST.txt) | ARCHIVED FILES MANIFEST |
| [COMPLETE_FILE_INVENTORY.txt](AnalyseFuture/repository-inventory/COMPLETE_FILE_INVENTORY.txt) | Complete generated per-file responsibility, dependency, status, risk and hash ledger. |
| [DEPENDENCY_MAP.txt](AnalyseFuture/repository-inventory/DEPENDENCY_MAP.txt) | SOLVER AI — RUNTIME AND DEPENDENCY MAP |
| [DUPLICATE_ANALYSIS.txt](AnalyseFuture/repository-inventory/DUPLICATE_ANALYSIS.txt) | SOLVER AI — DUPLICATE AND CONSOLIDATION ANALYSIS |
| [FEATURE_INVENTORY.txt](AnalyseFuture/repository-inventory/FEATURE_INVENTORY.txt) | SOLVER AI — FEATURE INVENTORY |
| [baseline.json](AnalyseFuture/repository-inventory/baseline.json) | Structured baseline evidence backing the complete recovery reports; provenance retained. |
| [current-files.json](AnalyseFuture/repository-inventory/current-files.json) | Machine-readable complete current tracked-file ledger; self hashes omitted to avoid recursion. |
| [features.json](AnalyseFuture/repository-inventory/features.json) | Structured features evidence backing the complete recovery reports; provenance retained. |
| [functional-baseline.json](AnalyseFuture/repository-inventory/functional-baseline.json) | Immutable293-path published baseline before complete functional reorganization. |
| [functional-moves.json](AnalyseFuture/repository-inventory/functional-moves.json) | Exact68 current functional moves and preserved runtime-boundary decisions. |
| [historical-branches.json](AnalyseFuture/repository-inventory/historical-branches.json) | Structured historical-branches evidence backing the complete recovery reports; provenance retained. |
| [moves.json](AnalyseFuture/repository-inventory/moves.json) | Structured moves evidence backing the complete recovery reports; provenance retained. |

</details>

<details>
<summary>AnalyseFuture/repository-inventory/reviews/ — 8 files</summary>

Frozen per-scope static source assessments whose original findings remain historical evidence rather than fresh runtime claims.

| File | Purpose / feature |
| --- | --- |
| [api.json](AnalyseFuture/repository-inventory/reviews/api.json) | Structured api evidence backing the complete recovery reports; provenance retained. |
| [archive.json](AnalyseFuture/repository-inventory/reviews/archive.json) | Structured archive evidence backing the complete recovery reports; provenance retained. |
| [docs.json](AnalyseFuture/repository-inventory/reviews/docs.json) | Structured docs evidence backing the complete recovery reports; provenance retained. |
| [history.json](AnalyseFuture/repository-inventory/reviews/history.json) | Structured history evidence backing the complete recovery reports; provenance retained. |
| [judge.json](AnalyseFuture/repository-inventory/reviews/judge.json) | Structured judge evidence backing the complete recovery reports; provenance retained. |
| [recovered-web.json](AnalyseFuture/repository-inventory/reviews/recovered-web.json) | Structured recovered-web evidence backing the complete recovery reports; provenance retained. |
| [support.json](AnalyseFuture/repository-inventory/reviews/support.json) | Structured support evidence backing the complete recovery reports; provenance retained. |
| [web.json](AnalyseFuture/repository-inventory/reviews/web.json) | Structured web evidence backing the complete recovery reports; provenance retained. |

</details>

<details>
<summary>AnalyseFuture/validation/ — 1 files</summary>

Named-revision validation records distinguishing successful, failed, expected-failure and unexecuted checks.

| File | Purpose / feature |
| --- | --- |
| [TEST_AND_VALIDATION_REPORT.txt](AnalyseFuture/validation/TEST_AND_VALIDATION_REPORT.txt) | SOLVER AI — CURRENT VALIDATION RECORD |

</details>

<details>
<summary>apps/web/ — 6 files</summary>

Next.js and TypeScript practice interface, account authority, browser feature modules and web-owned build tooling.

| File | Purpose / feature |
| --- | --- |
| [AGENTS.md](apps/web/AGENTS.md) | Installed Next.js-version development instructions |
| [Dockerfile](apps/web/Dockerfile) | Multi-stage Node image: install/build standalone then nonroot persistent-auth runtime |
| [next-env.d.ts](apps/web/next-env.d.ts) | Framework-generated type references for Next routing |
| [next.config.ts](apps/web/next.config.ts) | Standalone packaging, private/archive tracing exclusion and server-only API rewrite |
| [package.json](apps/web/package.json) | Web workspace dependencies and dev/build/typecheck scripts |
| [tsconfig.json](apps/web/tsconfig.json) | Strict app TypeScript compilation and @/ root alias |

</details>

<details>
<summary>apps/web/app/ — 4 files</summary>

Next.js App Router entry points, root layout and global styles that compose the feature modules.

| File | Purpose / feature |
| --- | --- |
| [globals.css](apps/web/app/globals.css) | Shared visual tokens, layout, catalog/editor/account/history and responsive accessibility rules |
| [layout.tsx](apps/web/app/layout.tsx) | Root HTML/metadata/global stylesheet and shared application shell |
| [not-found.tsx](apps/web/app/not-found.tsx) | Framework missing-route UI and return link |
| [page.tsx](apps/web/app/page.tsx) | Catalog home route entrypoint |

</details>

<details>
<summary>apps/web/app/account/ — 1 files</summary>

Account route that passes a constrained continuation path to the sign-in and registration interface.

| File | Purpose / feature |
| --- | --- |
| [page.tsx](apps/web/app/account/page.tsx) | Account route resolving optional next query into account form |

</details>

<details>
<summary>apps/web/app/api/auth/[...all]/ — 1 files</summary>

Node-runtime catch-all Better Auth adapter that initializes supported migrations before handling authentication requests.

| File | Purpose / feature |
| --- | --- |
| [route.ts](apps/web/app/api/auth/%5B...all%5D/route.ts) | Node-runtime Better Auth HTTP entrypoint with lazy official migrations |

</details>

<details>
<summary>apps/web/app/problems/[slug]/ — 1 files</summary>

Dynamic problem route that resolves the public slug and mounts the practice workspace.

| File | Purpose / feature |
| --- | --- |
| [page.tsx](apps/web/app/problems/%5Bslug%5D/page.tsx) | Async dynamic problem route passes slug into workspace |

</details>

<details>
<summary>apps/web/app/submissions/ — 1 files</summary>

Route entry point for the authenticated learner submission-history interface.

| File | Purpose / feature |
| --- | --- |
| [page.tsx](apps/web/app/submissions/page.tsx) | Submission-history route entrypoint |

</details>

<details>
<summary>apps/web/components/ — 2 files</summary>

Shared navigation shell and SVG icon components reused by the application features.

| File | Purpose / feature |
| --- | --- |
| [icons.tsx](apps/web/components/icons.tsx) | Typed original SVG icon component shared by feature interfaces |
| [shell.tsx](apps/web/components/shell.tsx) | Navigation, session summary, signout and shared page framing |

</details>

<details>
<summary>apps/web/features/accounts/ — 3 files</summary>

Account form, browser session client and server-side Better Auth authority with persistent local state.

| File | Purpose / feature |
| --- | --- |
| [account-form.tsx](apps/web/features/accounts/account-form.tsx) | Signup/signin/signout form and same-origin redirect validation |
| [client.ts](apps/web/features/accounts/client.ts) | Better Auth React/JWT client singleton |
| [server.ts](apps/web/features/accounts/server.ts) | Single session authority, SQLite/JWKS, persisted secret, origin policy and lazy migrations |

</details>

<details>
<summary>apps/web/features/hints/ — 2 files</summary>

Authenticated authored-hint requests and UI with bounded contracts, provenance validation, cancellation and safe errors.

| File | Purpose / feature |
| --- | --- |
| [account-hint.tsx](apps/web/features/hints/account-hint.tsx) | Optional account-owned hint UI alongside public ladder: signin affordance, loading/error/retry/cancel, contextual abort and explicit authored/mock/model provenance rendering. |
| [api.ts](apps/web/features/hints/api.ts) | Authenticated authored-hint API adapter: strict bounded Zod request/response, matched slug/level and provenance, short-lived Better Auth JWT, timeout/cancel/retry-safe errors. |

</details>

<details>
<summary>apps/web/features/practice/ — 4 files</summary>

Problem catalog, public response validation, practice workspace and locally persisted Monaco or textarea editing.

| File | Purpose / feature |
| --- | --- |
| [api.ts](apps/web/features/practice/api.ts) | Bounded Zod catalog/detail contracts, 10s request timeout and cancellation-safe errors |
| [catalog.tsx](apps/web/features/practice/catalog.tsx) | Public catalog retrieval and combined client search/topic/difficulty filtering |
| [code-pane.tsx](apps/web/features/practice/code-pane.tsx) | Local Monaco load/retry and textarea fallback; per-problem/language draft persistence |
| [workspace.tsx](apps/web/features/practice/workspace.tsx) | Public statement/examples/hint ladder/editor composition and submission controls |

</details>

<details>
<summary>apps/web/features/submissions/ — 3 files</summary>

Explicit run and submit actions, bounded API requests, capability checks and private saved-result history.

| File | Purpose / feature |
| --- | --- |
| [api.ts](apps/web/features/submissions/api.ts) | Typed capabilities and authenticated submission API with schemas and bounded requests |
| [submission-history.tsx](apps/web/features/submissions/submission-history.tsx) | Owned, paginated history and source/result detail with abortable requests |
| [submission-panel.tsx](apps/web/features/submissions/submission-panel.tsx) | Capability checks, explicit run/submit, idempotency, bounded polling and reusable result rendering |

</details>

<details>
<summary>apps/web/scripts/ — 2 files</summary>

Web-owned official auth migration and locally bundled Monaco asset preparation commands.

| File | Purpose / feature |
| --- | --- |
| [auth-migrate.mjs](apps/web/scripts/auth-migrate.mjs) | Idempotent official Better Auth schema migration preserving web cwd |
| [copy-monaco.mjs](apps/web/scripts/copy-monaco.mjs) | Local editor/worker bundle and notices with enforced patched sanitizer substitution |

</details>

<details>
<summary>apps/web/tests/ — 1 files</summary>

Real Better Auth integration checks using isolated temporary databases and keys.

| File | Purpose / feature |
| --- | --- |
| [auth.test.mjs](apps/web/tests/auth.test.mjs) | 7 real-library auth tests with isolated temporary state and repeated migrations |

</details>

<details>
<summary>docs/ — 1 files</summary>

Active product and engineering documentation indexed by functional responsibility.

| File | Purpose / feature |
| --- | --- |
| [INDEX.md](docs/INDEX.md) | Navigation and truth convention for project documents. |

</details>

<details>
<summary>docs/architecture/ — 2 files</summary>

Current and proposed service boundaries, repository organization and recorded architecture decisions.

| File | Purpose / feature |
| --- | --- |
| [ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md) | Current local boundaries and proposed larger architecture. |
| [REPOSITORY_STRUCTURE.md](docs/architecture/REPOSITORY_STRUCTURE.md) | Current tree, preservation rationale, hashes, boundaries and recovery limitations. |

</details>

<details>
<summary>docs/architecture/adr/ — 2 files</summary>

Dated decisions documenting the practice foundation and authenticated isolated judging boundaries.

| File | Purpose / feature |
| --- | --- |
| [0001-practice-foundation.md](docs/architecture/adr/0001-practice-foundation.md) | Historical first-increment decision and exact initial dependency choices. |
| [0002-authenticated-isolated-submissions.md](docs/architecture/adr/0002-authenticated-isolated-submissions.md) | Local identity/ownership/gVisor decisions, alternatives and limits. |

</details>

<details>
<summary>docs/engineering/ — 5 files</summary>

Contributor workflow, scoped implementation tasks and coding-agent practices.

| File | Purpose / feature |
| --- | --- |
| [AI_CONTRIBUTION_WORKFLOW.md](docs/engineering/AI_CONTRIBUTION_WORKFLOW.md) | Implementation assignment, exact-head review, validation evidence and authorized merge policy. |
| [CODEX_PLAYBOOK.md](docs/engineering/CODEX_PLAYBOOK.md) | Agent scope, verification ladder and implementation discipline. |
| [CONTRIBUTOR_TASKS.md](docs/engineering/CONTRIBUTOR_TASKS.md) | Suggested issue backlog, initial sequencing and acceptance template. |
| [PR_EVIDENCE.md](docs/engineering/PR_EVIDENCE.md) | Version1 field contract, size/path/head rules, trust boundaries and metadata limitations. |
| [handoff-directories.json](docs/engineering/handoff-directories.json) | Concrete functional responsibilities for every tracked ancestor folder, including inactive archive and historical collections. |

</details>

<details>
<summary>docs/engineering/backlog/ — 3 files</summary>

Canonical ordered task catalogue, generated issue cards and actual publication receipts.

| File | Purpose / feature |
| --- | --- |
| [README.md](docs/engineering/backlog/README.md) | Generated execution-order index and publication instructions for contributor handoff. |
| [issues.json](docs/engineering/backlog/issues.json) | Canonical127-task future implementation plan with topological order and feature ownership. |
| [publication.json](docs/engineering/backlog/publication.json) | Actual confirmed remote issue links and publication/access status. |

</details>

<details>
<summary>docs/engineering/backlog/issues/ — 141 files</summary>

One generated Markdown card per stable backlog task with prerequisites, ownership paths and acceptance criteria.

| File | Purpose / feature |
| --- | --- |
| [SAI-B001.md](docs/engineering/backlog/issues/SAI-B001.md) | Completed-local B001 task and evidence; preserved as prerequisite history. |
| [SAI-B002.md](docs/engineering/backlog/issues/SAI-B002.md) | Planned SAI-B002: Record owner-approved original-code licensing and inbound contribution rights; current owning area governance. |
| [SAI-B003.md](docs/engineering/backlog/issues/SAI-B003.md) | Planned SAI-B003: Approve a small pilot charter and data lifecycle contract; current owning area product. |
| [SAI-B004.md](docs/engineering/backlog/issues/SAI-B004.md) | Planned SAI-B004: Pin CI actions to immutable reviewed commits; current owning area supply-chain. |
| [SAI-B005.md](docs/engineering/backlog/issues/SAI-B005.md) | Planned SAI-B005: Pin web and API container bases and align intended Python patch versions; current owning area supply-chain. |
| [SAI-B006.md](docs/engineering/backlog/issues/SAI-B006.md) | Planned SAI-B006: Reject plaintext external identity and worker transport configuration; current owning area deployment-security. |
| [SAI-B007.md](docs/engineering/backlog/issues/SAI-B007.md) | Planned SAI-B007: Add a total JWKS fetch deadline with real transport fixtures; current owning area identity. |
| [SAI-B008.md](docs/engineering/backlog/issues/SAI-B008.md) | Planned SAI-B008: Describe protected endpoints with an accurate OpenAPI bearer scheme; current owning area api-contract. |
| [SAI-B009.md](docs/engineering/backlog/issues/SAI-B009.md) | Planned SAI-B009: Validate production worker credential strength before enabling internal routes; current owning area worker-auth. |
| [SAI-B010.md](docs/engineering/backlog/issues/SAI-B010.md) | Planned SAI-B010: Support bounded worker bearer rotation without an outage; current owning area worker-auth. |
| [SAI-B011.md](docs/engineering/backlog/issues/SAI-B011.md) | Planned SAI-B011: Introduce an explicit trusted-ingress identity throttle policy; current owning area identity. |
| [SAI-B012.md](docs/engineering/backlog/issues/SAI-B012.md) | Planned SAI-B012: Create a consistent private backup and restore procedure for both stores; current owning area storage-operations. |
| [SAI-B013.md](docs/engineering/backlog/issues/SAI-B013.md) | Planned SAI-B013: Introduce versioned transactional migrations for the submission database; current owning area storage. |
| [SAI-B014.md](docs/engineering/backlog/issues/SAI-B014.md) | Planned SAI-B014: Add a testable email-verification delivery flow for pilot accounts; current owning area identity. |
| [SAI-B015.md](docs/engineering/backlog/issues/SAI-B015.md) | Planned SAI-B015: Implement password recovery with bounded single-use reset links; current owning area identity. |
| [SAI-B016.md](docs/engineering/backlog/issues/SAI-B016.md) | Planned SAI-B016: Expose owned session listing and revoke-other-sessions controls; current owning area identity. |
| [SAI-B017.md](docs/engineering/backlog/issues/SAI-B017.md) | Planned SAI-B017: Record privacy-safe account security events; current owning area identity-observability. |
| [SAI-B018.md](docs/engineering/backlog/issues/SAI-B018.md) | Planned SAI-B018: Implement deliberate account deletion across auth and owned submission state; current owning area privacy. |
| [SAI-B019.md](docs/engineering/backlog/issues/SAI-B019.md) | Planned SAI-B019: Bound general API admission and concurrent slow requests; current owning area ingress-security. |
| [SAI-B020.md](docs/engineering/backlog/issues/SAI-B020.md) | Planned SAI-B020: Add structured redacted request and failure logs; current owning area operations. |
| [SAI-B021.md](docs/engineering/backlog/issues/SAI-B021.md) | Planned SAI-B021: Expose private bounded operational readiness and queue metrics; current owning area operations. |
| [SAI-B022.md](docs/engineering/backlog/issues/SAI-B022.md) | Planned SAI-B022: Apply retention to terminal submission source with a dry-run purge; current owning area privacy-storage. |
| [SAI-B023.md](docs/engineering/backlog/issues/SAI-B023.md) | Planned SAI-B023: Enforce cumulative owned-source storage budgets at submission admission; current owning area storage-abuse. |
| [SAI-B024.md](docs/engineering/backlog/issues/SAI-B024.md) | Planned SAI-B024: Avoid loading private source for submission summary pages; current owning area storage-performance. |
| [SAI-B025.md](docs/engineering/backlog/issues/SAI-B025.md) | Planned SAI-B025: Export an authenticated user-owned submission history bundle; current owning area privacy-product. |
| [SAI-B026.md](docs/engineering/backlog/issues/SAI-B026.md) | Planned SAI-B026: Extend problem provenance with explicit permitted-use metadata; current owning area content. |
| [SAI-B027.md](docs/engineering/backlog/issues/SAI-B027.md) | Planned SAI-B027: Version problem and grader identity on every new submission; current owning area content-contract. |
| [SAI-B028.md](docs/engineering/backlog/issues/SAI-B028.md) | Planned SAI-B028: Detect public-sample drift between catalog and judge deployments; current owning area content-quality. |
| [SAI-B029.md](docs/engineering/backlog/issues/SAI-B029.md) | Planned SAI-B029: Validate trusted problem authoring inputs before catalog publication; current owning area content-tooling. |
| [SAI-B030.md](docs/engineering/backlog/issues/SAI-B030.md) | Planned SAI-B030: Add one original prefix-sum range-query teaching exercise; current owning area content. |
| [SAI-B031.md](docs/engineering/backlog/issues/SAI-B031.md) | Planned SAI-B031: Use bounded server-side pagination for the expanding problem catalog; current owning area catalog. |
| [SAI-B032.md](docs/engineering/backlog/issues/SAI-B032.md) | Planned SAI-B032: Make catalog filters and page position shareable through the URL; current owning area catalog-ux. |
| [SAI-B033.md](docs/engineering/backlog/issues/SAI-B033.md) | Planned SAI-B033: Add explicit local draft export and bounded import; current owning area editor. |
| [SAI-B034.md](docs/engineering/backlog/issues/SAI-B034.md) | Planned SAI-B034: Offer explicit draft ownership and clear-on-shared-device controls; current owning area editor-privacy. |
| [SAI-B035.md](docs/engineering/backlog/issues/SAI-B035.md) | Planned SAI-B035: Detect cross-tab draft conflicts before overwriting newer code; current owning area editor-reliability. |
| [SAI-B036.md](docs/engineering/backlog/issues/SAI-B036.md) | Planned SAI-B036: Add persistent editor display and accessibility preferences; current owning area editor-ux. |
| [SAI-B037.md](docs/engineering/backlog/issues/SAI-B037.md) | Planned SAI-B037: Complete keyboard navigation for the practice and submission workflow; current owning area accessibility. |
| [SAI-B038.md](docs/engineering/backlog/issues/SAI-B038.md) | Planned SAI-B038: Improve screen-reader announcements and focus for asynchronous results; current owning area accessibility. |
| [SAI-B039.md](docs/engineering/backlog/issues/SAI-B039.md) | Planned SAI-B039: Repair contrast, reduced-motion and zoom reflow gaps; current owning area accessibility. |
| [SAI-B040.md](docs/engineering/backlog/issues/SAI-B040.md) | Planned SAI-B040: Add a focused automated accessibility regression gate; current owning area accessibility-quality. |
| [SAI-B041.md](docs/engineering/backlog/issues/SAI-B041.md) | Planned SAI-B041: Record the single-provider hint pilot activation decision; current owning area AI activation governance. |
| [SAI-B042.md](docs/engineering/backlog/issues/SAI-B042.md) | Planned SAI-B042: Bound and fingerprint the existing public-only hint context; current owning area Safe model context. |
| [SAI-B043.md](docs/engineering/backlog/issues/SAI-B043.md) | Planned SAI-B043: Validate trusted provider destinations and secret configuration; current owning area Provider configuration. |
| [SAI-B044.md](docs/engineering/backlog/issues/SAI-B044.md) | Planned SAI-B044: Define an internal generation result and usage contract; current owning area Provider-neutral contracts. |
| [SAI-B045.md](docs/engineering/backlog/issues/SAI-B045.md) | Planned SAI-B045: Version bounded hint prompts and spoiler policies; current owning area Tutoring prompts. |
| [SAI-B046.md](docs/engineering/backlog/issues/SAI-B046.md) | Planned SAI-B046: Reject malformed model hints before constructing learner responses; current owning area Model output contracts. |
| [SAI-B047.md](docs/engineering/backlog/issues/SAI-B047.md) | Planned SAI-B047: Add deterministic provider transport fixtures without external inference; current owning area Provider adapter verification. |
| [SAI-B048.md](docs/engineering/backlog/issues/SAI-B048.md) | Planned SAI-B048: Implement one opt-in bounded asynchronous hint provider adapter; current owning area Real provider transport. |
| [SAI-B049.md](docs/engineering/backlog/issues/SAI-B049.md) | Planned SAI-B049: Enforce account-level entitlement before model-backed hints; current owning area AI admission policy. |
| [SAI-B050.md](docs/engineering/backlog/issues/SAI-B050.md) | Planned SAI-B050: Reserve and reconcile durable per-account hint budgets atomically; current owning area AI token and request quotas. |
| [SAI-B051.md](docs/engineering/backlog/issues/SAI-B051.md) | Planned SAI-B051: Add process-wide provider concurrency and monetary admission ceilings; current owning area Global AI spend control. |
| [SAI-B052.md](docs/engineering/backlog/issues/SAI-B052.md) | Planned SAI-B052: Deduplicate model hint retries with account-scoped idempotency; current owning area AI request reliability. |
| [SAI-B053.md](docs/engineering/backlog/issues/SAI-B053.md) | Planned SAI-B053: Record redacted generation usage and failure telemetry; current owning area AI observability. |
| [SAI-B054.md](docs/engineering/backlog/issues/SAI-B054.md) | Planned SAI-B054: Propagate total generation deadlines and explicit cancellation states; current owning area AI cancellation and deadlines. |
| [SAI-B055.md](docs/engineering/backlog/issues/SAI-B055.md) | Planned SAI-B055: Bound provider retries and add outage admission state; current owning area AI failure policy. |
| [SAI-B056.md](docs/engineering/backlog/issues/SAI-B056.md) | Planned SAI-B056: Require clear external-AI disclosure before opt-in hint requests; current owning area AI privacy UX. |
| [SAI-B057.md](docs/engineering/backlog/issues/SAI-B057.md) | Planned SAI-B057: Provide a tested operator kill switch for model hint admission; current owning area AI operations. |
| [SAI-B058.md](docs/engineering/backlog/issues/SAI-B058.md) | Planned SAI-B058: Add shared golden fixtures for hint API and browser schema parity; current owning area Cross-runtime AI contracts. |
| [SAI-B059.md](docs/engineering/backlog/issues/SAI-B059.md) | Planned SAI-B059: Define and execute a small consented model-hint pilot acceptance gate; current owning area Hint quality pilot. |
| [SAI-B060.md](docs/engineering/backlog/issues/SAI-B060.md) | Planned SAI-B060: Design a bounded tutoring interaction contract beyond hint levels; current owning area Tutor interaction design. |
| [SAI-B061.md](docs/engineering/backlog/issues/SAI-B061.md) | Planned SAI-B061: Implement account-owned expiring tutor conversation state; current owning area Tutor context lifecycle. |
| [SAI-B062.md](docs/engineering/backlog/issues/SAI-B062.md) | Planned SAI-B062: Add a consented concept-check interaction with bounded feedback; current owning area Evidence-oriented tutoring. |
| [SAI-B063.md](docs/engineering/backlog/issues/SAI-B063.md) | Planned SAI-B063: Collect minimal account-owned hint quality feedback; current owning area AI feedback and correction. |
| [SAI-B064.md](docs/engineering/backlog/issues/SAI-B064.md) | Planned SAI-B064: Define explicit source-sharing consent and owned debugger input; current owning area Debugger privacy boundary. |
| [SAI-B065.md](docs/engineering/backlog/issues/SAI-B065.md) | Planned SAI-B065: Build a public-only execution evidence projection for debugging; current owning area Safe debugger evidence. |
| [SAI-B066.md](docs/engineering/backlog/issues/SAI-B066.md) | Planned SAI-B066: Return debugger hypotheses separately from observed failures; current owning area Evidence-backed debugging. |
| [SAI-B067.md](docs/engineering/backlog/issues/SAI-B067.md) | Planned SAI-B067: Show a source-hash-bound debugger patch preview with explicit apply; current owning area Debugger editor UX. |
| [SAI-B068.md](docs/engineering/backlog/issues/SAI-B068.md) | Planned SAI-B068: Version authorized solver problem specifications and evaluation modes; current owning area Solver input contracts. |
| [SAI-B069.md](docs/engineering/backlog/issues/SAI-B069.md) | Planned SAI-B069: Generate a bounded algorithm-plan record before candidate code; current owning area Candidate planning. |
| [SAI-B070.md](docs/engineering/backlog/issues/SAI-B070.md) | Planned SAI-B070: Normalize bounded source candidates without archive parser assumptions; current owning area Candidate generation. |
| [SAI-B071.md](docs/engineering/backlog/issues/SAI-B071.md) | Planned SAI-B071: Route authorized AI candidates through the existing isolated judge boundary; current owning area Solver-to-judge integration. |
| [SAI-B072.md](docs/engineering/backlog/issues/SAI-B072.md) | Planned SAI-B072: Implement a finite repair state machine with one shared run budget; current owning area Bounded solver repair. |
| [SAI-B073.md](docs/engineering/backlog/issues/SAI-B073.md) | Planned SAI-B073: Rank candidates by explicit execution evidence with deterministic ties; current owning area Candidate ranking. |
| [SAI-B074.md](docs/engineering/backlog/issues/SAI-B074.md) | Planned SAI-B074: Create a reproducible offline solver evaluation run manifest; current owning area Solver evaluation. |
| [SAI-B075.md](docs/engineering/backlog/issues/SAI-B075.md) | Planned SAI-B075: Admit only reviewed differential and metamorphic test specifications; current owning area Authorized test generation. |
| [SAI-B076.md](docs/engineering/backlog/issues/SAI-B076.md) | Planned SAI-B076: Reduce consented public counterexamples under a finite execution budget; current owning area Counterexample debugging. |
| [SAI-B077.md](docs/engineering/backlog/issues/SAI-B077.md) | Planned SAI-B077: Separate evaluation splits and report archive contamination candidates; current owning area Evaluation integrity. |
| [SAI-B078.md](docs/engineering/backlog/issues/SAI-B078.md) | Planned SAI-B078: Register dataset and model permissions separately from source licenses; current owning area Research provenance. |
| [SAI-B079.md](docs/engineering/backlog/issues/SAI-B079.md) | Planned SAI-B079: Produce a resource-and-integrity feasibility decision for one self-hosted model; current owning area Model serving research gate. |
| [SAI-B080.md](docs/engineering/backlog/issues/SAI-B080.md) | Planned SAI-B080: Add an explicit admission gate for reproducible fine-tuning experiments; current owning area Fine-tuning research controls. |
| [SAI-B081.md](docs/engineering/backlog/issues/SAI-B081.md) | Planned SAI-B081: Implement contest lifecycle and authoritative event timing; current owning area contests. |
| [SAI-B082.md](docs/engineering/backlog/issues/SAI-B082.md) | Planned SAI-B082: Add permissioned contest registration and eligibility checks; current owning area contests. |
| [SAI-B083.md](docs/engineering/backlog/issues/SAI-B083.md) | Planned SAI-B083: Freeze versioned problem sets for each contest; current owning area contests. |
| [SAI-B084.md](docs/engineering/backlog/issues/SAI-B084.md) | Planned SAI-B084: Implement deterministic ICPC scoring as a tested pure calculation; current owning area contests. |
| [SAI-B085.md](docs/engineering/backlog/issues/SAI-B085.md) | Planned SAI-B085: Add participant and organizer scoreboard projections with freeze rules; current owning area contests. |
| [SAI-B086.md](docs/engineering/backlog/issues/SAI-B086.md) | Planned SAI-B086: Connect contest submissions to event eligibility and immutable attempt context; current owning area contests. |
| [SAI-B087.md](docs/engineering/backlog/issues/SAI-B087.md) | Planned SAI-B087: Implement isolated virtual-contest sessions with personal start times; current owning area contests. |
| [SAI-B088.md](docs/engineering/backlog/issues/SAI-B088.md) | Planned SAI-B088: Add locked ICPC team rosters and event membership rules; current owning area teams. |
| [SAI-B089.md](docs/engineering/backlog/issues/SAI-B089.md) | Planned SAI-B089: Scope contest attempts and source visibility to authorized team members; current owning area teams. |
| [SAI-B090.md](docs/engineering/backlog/issues/SAI-B090.md) | Planned SAI-B090: Enforce contest assistance policy across hint and submission routes; current owning area contest-integrity. |
| [SAI-B091.md](docs/engineering/backlog/issues/SAI-B091.md) | Planned SAI-B091: Build an organizer workflow for contest draft, preview and publication; current owning area contest-admin. |
| [SAI-B092.md](docs/engineering/backlog/issues/SAI-B092.md) | Planned SAI-B092: Implement audited contest rejudging with immutable verdict revisions; current owning area contest-admin. |
| [SAI-B093.md](docs/engineering/backlog/issues/SAI-B093.md) | Planned SAI-B093: Add contest clarification and appeal records with controlled disclosure; current owning area contest-admin. |
| [SAI-B094.md](docs/engineering/backlog/issues/SAI-B094.md) | Planned SAI-B094: Deliver bounded scoreboard polling with consistent event revisions; current owning area leaderboards. |
| [SAI-B095.md](docs/engineering/backlog/issues/SAI-B095.md) | Planned SAI-B095: Create a reproducible contest rehearsal and official standings export; current owning area contest-release. |
| [SAI-B096.md](docs/engineering/backlog/issues/SAI-B096.md) | Planned SAI-B096: Version output-comparison policies without changing existing verdicts; current owning area judge-validators. |
| [SAI-B097.md](docs/engineering/backlog/issues/SAI-B097.md) | Planned SAI-B097: Add isolated versioned custom-checker support for authorized problems; current owning area judge-validators. |
| [SAI-B098.md](docs/engineering/backlog/issues/SAI-B098.md) | Planned SAI-B098: Implement bounded floating-point answer validation; current owning area judge-validators. |
| [SAI-B099.md](docs/engineering/backlog/issues/SAI-B099.md) | Planned SAI-B099: Introduce explicit subtask scoring for separately configured events; current owning area judge-validators. |
| [SAI-B100.md](docs/engineering/backlog/issues/SAI-B100.md) | Planned SAI-B100: Add an audited C++20 runtime alongside existing C++17; current owning area judge-languages. |
| [SAI-B101.md](docs/engineering/backlog/issues/SAI-B101.md) | Planned SAI-B101: Add isolated Java support with explicit JVM resource semantics; current owning area judge-languages. |
| [SAI-B102.md](docs/engineering/backlog/issues/SAI-B102.md) | Planned SAI-B102: Add isolated JavaScript support with denied network and bounded runtime; current owning area judge-languages. |
| [SAI-B103.md](docs/engineering/backlog/issues/SAI-B103.md) | Planned SAI-B103: Add isolated Go compilation with offline standard-library execution; current owning area judge-languages. |
| [SAI-B104.md](docs/engineering/backlog/issues/SAI-B104.md) | Planned SAI-B104: Add isolated Rust compilation with a fixed edition and no dependency fetch; current owning area judge-languages. |
| [SAI-B105.md](docs/engineering/backlog/issues/SAI-B105.md) | Planned SAI-B105: Add a bounded metrics exporter consuming the existing private operational surface; current owning area operations-observability. |
| [SAI-B106.md](docs/engineering/backlog/issues/SAI-B106.md) | Planned SAI-B106: Propagate redacted correlation identifiers across accepted jobs; current owning area operations-observability. |
| [SAI-B107.md](docs/engineering/backlog/issues/SAI-B107.md) | Planned SAI-B107: Define measurable service objectives and test operator alert rules; current owning area operations-observability. |
| [SAI-B108.md](docs/engineering/backlog/issues/SAI-B108.md) | Planned SAI-B108: Rehearse a timed full-stack disaster restore using the approved backup helper; current owning area operations-recovery. |
| [SAI-B109.md](docs/engineering/backlog/issues/SAI-B109.md) | Planned SAI-B109: Measure bounded capacity and overload behavior using original fixtures; current owning area operations-capacity. |
| [SAI-B110.md](docs/engineering/backlog/issues/SAI-B110.md) | Planned SAI-B110: Implement a revisioned deployment smoke and rollback rehearsal; current owning area operations-release. |
| [SAI-B111.md](docs/engineering/backlog/issues/SAI-B111.md) | Planned SAI-B111: Create a canary qualification gate for judge runtime upgrades; current owning area operations-release. |
| [SAI-B112.md](docs/engineering/backlog/issues/SAI-B112.md) | Planned SAI-B112: Run a bounded incident exercise for worker outage and recovery; current owning area operations-recovery. |
| [SAI-B113.md](docs/engineering/backlog/issues/SAI-B113.md) | Planned SAI-B113: Provide learner-controlled progress summaries with assistance provenance; current owning area learning-analytics. |
| [SAI-B114.md](docs/engineering/backlog/issues/SAI-B114.md) | Planned SAI-B114: Add editable practice plans and deterministic review reminders; current owning area learning-plans. |
| [SAI-B115.md](docs/engineering/backlog/issues/SAI-B115.md) | Planned SAI-B115: Implement opt-in coach cohorts with explicit sharing permissions; current owning area coaching. |
| [SAI-B116.md](docs/engineering/backlog/issues/SAI-B116.md) | Planned SAI-B116: Add permissioned assignments and human rubric feedback; current owning area coaching. |
| [SAI-B117.md](docs/engineering/backlog/issues/SAI-B117.md) | Planned SAI-B117: Enforce institutional sponsorship and learner data-use boundaries; current owning area institutional-privacy. |
| [SAI-B118.md](docs/engineering/backlog/issues/SAI-B118.md) | Planned SAI-B118: Export institution-authorized assignment records with redaction tests; current owning area institutional-privacy. |
| [SAI-B119.md](docs/engineering/backlog/issues/SAI-B119.md) | Planned SAI-B119: Produce a redacted pilot cost ledger and resource-envelope report; current owning area business-operations. |
| [SAI-B120.md](docs/engineering/backlog/issues/SAI-B120.md) | Planned SAI-B120: Extend existing pilot grants with expiring institutional scopes; current owning area business-release. |
| [SAI-B121.md](docs/engineering/backlog/issues/SAI-B121.md) | Planned SAI-B121: Persist owned sandbox records and reconcile crash-orphaned containers; current owning area judge-recovery. |
| [SAI-B122.md](docs/engineering/backlog/issues/SAI-B122.md) | Planned SAI-B122: Bind controller credentials to registered worker identities; current owning area worker-auth. |
| [SAI-B123.md](docs/engineering/backlog/issues/SAI-B123.md) | Planned SAI-B123: Enforce an atomic active-lease allowance per worker principal; current owning area judge-admission. |
| [SAI-B124.md](docs/engineering/backlog/issues/SAI-B124.md) | Planned SAI-B124: Require a verified aggregate resource envelope for a production judge host; current owning area judge-isolation. |
| [SAI-B125.md](docs/engineering/backlog/issues/SAI-B125.md) | Planned SAI-B125: Gate production readiness on an approved supported runtime identity; current owning area runtime-maintenance. |
| [SAI-B126.md](docs/engineering/backlog/issues/SAI-B126.md) | Planned SAI-B126: Withdraw worker readiness and reconcile its current lease on retirement; current owning area judge-lifecycle. |
| [SAI-B127.md](docs/engineering/backlog/issues/SAI-B127.md) | Planned SAI-B127: Enforce owner-approved reviewed-merge rules for the main branch; current owning area repository governance. |
| [SAI-B128.md](docs/engineering/backlog/issues/SAI-B128.md) | Planned SAI-B128: Implement a declared DSA coverage matrix and preregistered model release measurements; ownership area solver-readiness. |
| [SAI-B129.md](docs/engineering/backlog/issues/SAI-B129.md) | Planned SAI-B129: Run an approved untuned checkpoint comparison and record a future selection; ownership area model-baseline. |
| [SAI-B130.md](docs/engineering/backlog/issues/SAI-B130.md) | Planned SAI-B130: Materialize a permitted validated training corpus with immutable split lineage; ownership area training-data. |
| [SAI-B131.md](docs/engineering/backlog/issues/SAI-B131.md) | Planned SAI-B131: Create a separate locked training environment and reviewed artifact loader; ownership area training-infrastructure. |
| [SAI-B132.md](docs/engineering/backlog/issues/SAI-B132.md) | Planned SAI-B132: Implement tokenizer-aware SFT examples and answer-only loss masking; ownership area training-preprocessing. |
| [SAI-B133.md](docs/engineering/backlog/issues/SAI-B133.md) | Planned SAI-B133: Run an approved external LoRA smoke experiment with stop and resume evidence; ownership area training-smoke. |
| [SAI-B134.md](docs/engineering/backlog/issues/SAI-B134.md) | Planned SAI-B134: Execute the approved bounded SFT adapter training campaign; ownership area actual-fine-tuning. |
| [SAI-B135.md](docs/engineering/backlog/issues/SAI-B135.md) | Planned SAI-B135: Publish immutable private model artifacts and complete adapter lineage; ownership area model-artifacts. |
| [SAI-B136.md](docs/engineering/backlog/issues/SAI-B136.md) | Planned SAI-B136: Evaluate tuned candidates against matched baselines and enforce category gates; ownership area model-promotion-evaluation. |
| [SAI-B137.md](docs/engineering/backlog/issues/SAI-B137.md) | Planned SAI-B137: Qualify inference export and quantization at the deployed precision; ownership area inference-qualification. |
| [SAI-B138.md](docs/engineering/backlog/issues/SAI-B138.md) | Planned SAI-B138: Integrate the qualified trained artifact with bounded provider-neutral serving; ownership area trained-model-serving. |
| [SAI-B139.md](docs/engineering/backlog/issues/SAI-B139.md) | Planned SAI-B139: Promote a trained model through a limited pilot and rehearsed rollback; ownership area trained-model-release. |
| [SAI-B140.md](docs/engineering/backlog/issues/SAI-B140.md) | Planned SAI-B140: Run a separately approved execution-reward preference or RL experiment; ownership area optional-model-research. |
| [SAI-B141.md](docs/engineering/backlog/issues/SAI-B141.md) | Planned SAI-B141: Operate a consented failure-analysis and retraining improvement cycle; ownership area model-lifecycle. |

</details>

<details>
<summary>docs/governance/ — 3 files</summary>

Maintainer decisions, original-code and content rights, and build-versus-reuse policies.

| File | Purpose / feature |
| --- | --- |
| [DATA_AND_LICENSES.md](docs/governance/DATA_AND_LICENSES.md) | Original-code, content, dataset, model and privacy rights boundaries. |
| [OPEN_DECISIONS.md](docs/governance/OPEN_DECISIONS.md) | Maintainer-owned licensing, audience, runtime, provider and policy decisions. |
| [OPEN_SOURCE_STRATEGY.md](docs/governance/OPEN_SOURCE_STRATEGY.md) | Build/reuse policy and dependency/service/reference candidate matrix. |

</details>

<details>
<summary>docs/onboarding/ — 2 files</summary>

Contributor orientation and reproducible installation, startup, validation and deployment instructions.

| File | Purpose / feature |
| --- | --- |
| [DEVELOPMENT.md](docs/onboarding/DEVELOPMENT.md) | Pinned native setup, startup, tests, local secrets and Compose workflows. |
| [START_HERE.md](docs/onboarding/START_HERE.md) | First-day reading, local workflow and contribution expectations. |

</details>

<details>
<summary>docs/product/ — 6 files</summary>

Product vision, requirements, roadmap and the retained detailed idea and solver proposals.

| File | Purpose / feature |
| --- | --- |
| [AI_SOLVER.md](docs/product/AI_SOLVER.md) | Design proposal for tutor/debugger/candidate solver contracts. |
| [DSA_SOLVER_READINESS.md](docs/product/DSA_SOLVER_READINESS.md) | Complete future DSA solver readiness checklist: supported coverage, evaluated correctness, data/model research, actual approved training, artifacts, serving and release gates. |
| [PRODUCT_REQUIREMENTS.md](docs/product/PRODUCT_REQUIREMENTS.md) | Proposed P0/P1/P2 features, modes and acceptance conditions. |
| [PROJECT_IDEA.txt](docs/product/PROJECT_IDEA.txt) | Earlier detailed plain-text product proposal. |
| [PROJECT_VISION.md](docs/product/PROJECT_VISION.md) | Original mission, users, product pillars and non-goals. |
| [ROADMAP.md](docs/product/ROADMAP.md) | Dependency-ordered phases and acceptance gates. |

</details>

<details>
<summary>docs/research/ — 5 files</summary>

Dated audits, upstream study references, competitive positioning and model-evaluation proposals.

| File | Purpose / feature |
| --- | --- |
| [AUDIT_AND_AI_PLAN_2026-11-15.md](docs/research/AUDIT_AND_AI_PLAN_2026-11-15.md) | Dated source audit and provider-neutral AI delivery plan with upstream triage. |
| [COMPETITIVE_LANDSCAPE.md](docs/research/COMPETITIVE_LANDSCAPE.md) | Qualitative user jobs, positioning and differentiation hypotheses. |
| [FINETUNING_MODEL_RESEARCH.md](docs/research/FINETUNING_MODEL_RESEARCH.md) | Dated non-ranked research catalogue of 20 fine-tuning model/baseline families, official source evidence, metadata limitations, licensing/hardware questions and future decision checklist. |
| [MODEL_DATA_EVALUATION.md](docs/research/MODEL_DATA_EVALUATION.md) | Future permitted data pipeline, model baselines, tuning and evaluation. |
| [PUBLIC_REPOSITORIES_AND_RESOURCES.txt](docs/research/PUBLIC_REPOSITORIES_AND_RESOURCES.txt) | Complete 20-repository and model/dataset study inventory. |

</details>

<details>
<summary>docs/security/ — 1 files</summary>

Judge threat model, untrusted-execution boundaries and production release controls.

| File | Purpose / feature |
| --- | --- |
| [JUDGE_SECURITY.md](docs/security/JUDGE_SECURITY.md) | Threat model, required controls, judge vocabulary and public-release gate. |

</details>

<details>
<summary>docs/status/ — 1 files</summary>

Named-revision implementation evidence, current limitations and historical validation distinctions.

| File | Purpose / feature |
| --- | --- |
| [PROJECT_STATUS.md](docs/status/PROJECT_STATUS.md) | Executed implementation, test evidence, limitations and current facts. |

</details>

<details>
<summary>scripts/development/ — 3 files</summary>

Native web, API and worker lifecycle orchestration and private local worker-token selection.

| File | Purpose / feature |
| --- | --- |
| [dev.py](scripts/development/dev.py) | Start API/web/optional trusted judge; generate/select worker token and stop owned child process groups. |
| [judge-worker.py](scripts/development/judge-worker.py) | Launch trusted worker with local credential without logging it. |
| [local_config.py](scripts/development/local_config.py) | Generate and preserve private local worker credential using atomic file publication and restrictive permissions. |

</details>

<details>
<summary>scripts/github/ — 3 files</summary>

Offline backlog generation, explicit safe issue publication and inert pull-request evidence checking.

| File | Purpose / feature |
| --- | --- |
| [build_backlog.py](scripts/github/build_backlog.py) | Offline deterministic issue cards and ordered index generated from the canonical task catalogue. |
| [check_pr_evidence.py](scripts/github/check_pr_evidence.py) | Offline bounded PR-event evidence validation without network, command execution or raw-body logging. |
| [publish_issues.py](scripts/github/publish_issues.py) | Explicit GitHub issue publication with validated order, remote-marker reconciliation, pacing and durable receipts. |

</details>

<details>
<summary>scripts/verification/ — 4 files</summary>

Packaging exclusion guards and deterministic inventory and preservation checks.

| File | Purpose / feature |
| --- | --- |
| [check-standalone.mjs](scripts/verification/check-standalone.mjs) | Reject private runtime state or preserved research in Next standalone artifacts. |
| [project_handoff.py](scripts/verification/project_handoff.py) | Render or verify the complete root Markdown handoff from staged file annotations, canonical features, directory ownership and detailed tasks. |
| [repository_inventory.py](scripts/verification/repository_inventory.py) | Generate/check complete tracked-file ledger from source assessments and static imports, without source execution. |
| [verify_preserved_archives.py](scripts/verification/verify_preserved_archives.py) | Verify ZIP/member and branch-snapshot bytes/hashes and optional staged Git blobs without importing evidence. |

</details>

<details>
<summary>services/api/ — 5 files</summary>

Python FastAPI application, frozen dependencies, container definition and service-owned tests.

| File | Purpose / feature |
| --- | --- |
| [.dockerignore](services/api/.dockerignore) | Exclude local environments, caches, tests, private local state and env files from API image build context. |
| [.python-version](services/api/.python-version) | Select the API project Python 3.12 interpreter family. |
| [Dockerfile](services/api/Dockerfile) | Build nonroot FastAPI/Uvicorn runtime with frozen production dependencies and optional build-time managed CA. |
| [pyproject.toml](services/api/pyproject.toml) | Declare five pinned runtime packages, pytest/Ruff dev packages and test/lint settings. |
| [uv.lock](services/api/uv.lock) | Lock Python package resolution and SHA-256-verified distribution artifacts. |

</details>

<details>
<summary>services/api/solver_api/ — 2 files</summary>

Stable API entry point composing feature modules and shared HTTP behavior.

| File | Purpose / feature |
| --- | --- |
| [__init__.py](services/api/solver_api/__init__.py) | Package marker stating that learner programs are never executed by this service. |
| [main.py](services/api/solver_api/main.py) | Compose FastAPI routes, request IDs/errors, public catalog, authenticated hints/history and worker-only control endpoints. |

</details>

<details>
<summary>services/api/solver_api/features/ — 1 files</summary>

Server feature boundaries for catalog, authored hints, fixed identity verification and owned submissions.

| File | Purpose / feature |
| --- | --- |
| [__init__.py](services/api/solver_api/features/__init__.py) | Empty Python package marker for the features functional domain; no initialization side effects. |

</details>

<details>
<summary>services/api/solver_api/features/catalog/ — 3 files</summary>

Original public problem content and validated catalog response models.

| File | Purpose / feature |
| --- | --- |
| [__init__.py](services/api/solver_api/features/catalog/__init__.py) | Empty Python package marker for the catalog functional domain; no initialization side effects. |
| [content.py](services/api/solver_api/features/catalog/content.py) | Define three original public exercises including statements, two samples, Python/C++ starter templates and three authored hints. |
| [models.py](services/api/solver_api/features/catalog/models.py) | Immutable public catalog/summary/sample/starter/provenance/error response models. |

</details>

<details>
<summary>services/api/solver_api/features/hints/ — 2 files</summary>

Authenticated authored-hint contract and a bounded future-provider interface without real model inference.

| File | Purpose / feature |
| --- | --- |
| [__init__.py](services/api/solver_api/features/hints/__init__.py) | Empty Python package marker for the hints functional domain; no initialization side effects. |
| [service.py](services/api/solver_api/features/hints/service.py) | Strict versioned authenticated hint contracts, public-only model boundary, truthful provenance, authored backend and timeout/error handling. |

</details>

<details>
<summary>services/api/solver_api/features/identity/ — 2 files</summary>

Fixed-issuer and fixed-JWKS bearer authentication for account-owned API access.

| File | Purpose / feature |
| --- | --- |
| [__init__.py](services/api/solver_api/features/identity/__init__.py) | Empty Python package marker for the identity functional domain; no initialization side effects. |
| [verification.py](services/api/solver_api/features/identity/verification.py) | Verify bounded Bearer JWTs against fixed configured Ed25519 JWKS with issuer, audience, subject, use, expiry and refresh controls. |

</details>

<details>
<summary>services/api/solver_api/features/submissions/ — 2 files</summary>

Durable owned SQLite jobs, source history, quotas, idempotency and worker lease completion.

| File | Purpose / feature |
| --- | --- |
| [__init__.py](services/api/solver_api/features/submissions/__init__.py) | Empty Python package marker for the submissions functional domain; no initialization side effects. |
| [store.py](services/api/solver_api/features/submissions/store.py) | Persist owned SQLite submissions and source, enforce idempotency/quotas, advertise worker capabilities and issue/complete atomic expiring leases. |

</details>

<details>
<summary>services/api/solver_api/http/ — 3 files</summary>

Shared bounded request bodies, correlated safe error handling and HTTP support.

| File | Purpose / feature |
| --- | --- |
| [__init__.py](services/api/solver_api/http/__init__.py) | Empty Python package marker for the http functional domain; no initialization side effects. |
| [body_limit.py](services/api/solver_api/http/body_limit.py) | ASGI middleware bounding declared/streamed HTTP request bytes to 128 KiB and receive duration to ten seconds. |
| [errors.py](services/api/solver_api/http/errors.py) | Represent deliberately public status/code/message/header errors without exposing internal details. |

</details>

<details>
<summary>services/api/tests/catalog/ — 1 files</summary>

Catalog and shared request or error contract tests.

| File | Purpose / feature |
| --- | --- |
| [test_api.py](services/api/tests/catalog/test_api.py) | Exercise real routes, catalog filtering/pagination, data provenance, sample oracles, safe errors, authentication requirement and OpenAPI presence. |

</details>

<details>
<summary>services/api/tests/hints/ — 1 files</summary>

Authored-hint authentication, provenance, provider-boundary and failure-contract tests.

| File | Purpose / feature |
| --- | --- |
| [test_hints.py](services/api/tests/hints/test_hints.py) | Exercise authored hints, provenance, invalid/injected input, authentication, public-only context, size limits, provider failures and timeout. |

</details>

<details>
<summary>services/api/tests/identity/ — 1 files</summary>

JWT, JWKS, issuer and authentication-boundary tests.

| File | Purpose / feature |
| --- | --- |
| [test_auth.py](services/api/tests/identity/test_auth.py) | Exercise real Ed25519 JWTs and fixed JWKS logic: claims, header attacks, rotation, cache cooldown/failures and concurrency. |

</details>

<details>
<summary>services/api/tests/submissions/ — 1 files</summary>

Ownership, durable queue, quotas, idempotency, lease and completion regression tests.

| File | Purpose / feature |
| --- | --- |
| [test_submissions.py](services/api/tests/submissions/test_submissions.py) | Exercise persistence, ownership, source/body limits, idempotency, quotas, atomic leasing/completion, expiry and worker authentication. |

</details>

<details>
<summary>services/judge/ — 4 files</summary>

Trusted host judge controller, sandbox image definition and independently gated execution tests.

| File | Purpose / feature |
| --- | --- |
| [.dockerignore](services/judge/.dockerignore) | Exclude caches, virtualenv and tests from sandbox image context |
| [Dockerfile](services/judge/Dockerfile) | Build nonroot Python/C++17 supervisor image from digest-pinned Python base with signed Debian compiler packages |
| [UPSTREAM_REVIEW.md](services/judge/UPSTREAM_REVIEW.md) | Record runtime selection, installed gVisor age, limits, boundary and finite checks |
| [pytest.ini](services/judge/pytest.ini) | Configure judge Python import and test roots |

</details>

<details>
<summary>services/judge/solver_judge/ — 2 files</summary>

Judge control, grading and restricted-program modules with deliberately shared bounded process transport.

| File | Purpose / feature |
| --- | --- |
| [__init__.py](services/judge/solver_judge/__init__.py) | Mark trusted judge controller package |
| [bounded.py](services/judge/solver_judge/bounded.py) | Supervise trusted control or sandbox processes using bounded nonblocking stdin/stdout/stderr, deadlines and process-group cleanup |

</details>

<details>
<summary>services/judge/solver_judge/control/ — 4 files</summary>

Trusted Docker and gVisor runner, worker lifecycle and read-only readiness diagnostics.

| File | Purpose / feature |
| --- | --- |
| [__init__.py](services/judge/solver_judge/control/__init__.py) | Empty Python package marker for the control functional domain; no initialization side effects. |
| [diagnostics.py](services/judge/solver_judge/control/diagnostics.py) | Run finite sandbox preflight and print controlled readiness/check fields |
| [runner.py](services/judge/solver_judge/control/runner.py) | Resolve immutable image identity, require rootless runsc, create per-job isolated containers, validate protocol and grade outputs externally |
| [worker.py](services/judge/solver_judge/control/worker.py) | Validate leased jobs and trusted API origin, maintain readiness heartbeat, run one lease at a time, sanitize completion and handle shutdown |

</details>

<details>
<summary>services/judge/solver_judge/grading/ — 2 files</summary>

Original problem grading cases and trusted expected-answer computations kept outside learner programs.

| File | Purpose / feature |
| --- | --- |
| [__init__.py](services/judge/solver_judge/grading/__init__.py) | Empty Python package marker for the grading functional domain; no initialization side effects. |
| [cases.py](services/judge/solver_judge/grading/cases.py) | Provide three original problem oracles, two public examples and six bounded generated submission cases per problem |

</details>

<details>
<summary>services/judge/solver_judge/sandbox/ — 2 files</summary>

Restricted learner-program supervisor copied into the isolated sandbox image.

| File | Purpose / feature |
| --- | --- |
| [__init__.py](services/judge/solver_judge/sandbox/__init__.py) | Empty Python package marker for the sandbox functional domain; no initialization side effects. |
| [harness.py](services/judge/solver_judge/sandbox/harness.py) | Trusted image entrypoint that validates source/input bounds, compiles Python/C++17, applies rlimits and emits one bounded response |

</details>

<details>
<summary>services/judge/tests/control/ — 2 files</summary>

Runner protocol, worker leasing and container lifecycle cleanup regression tests.

| File | Purpose / feature |
| --- | --- |
| [test_runner.py](services/judge/tests/control/test_runner.py) | Mock sandbox exchange to test no expected-answer transmission, protocol failure, count/output/exit validation and no runc fallback |
| [test_worker.py](services/judge/tests/control/test_worker.py) | Use fakes/local HTTP to check lease validation, retry, startup readiness, shutdown, response limits and no bearer redirects |

</details>

<details>
<summary>services/judge/tests/grading/ — 1 files</summary>

Deterministic original grading-case and expected-answer checks.

| File | Purpose / feature |
| --- | --- |
| [test_cases.py](services/judge/tests/grading/test_cases.py) | Check oracle correctness, public/generated bounds, deterministic test seed and failure cases |

</details>

<details>
<summary>services/judge/tests/sandbox/ — 2 files</summary>

Bounded process transport checks and explicitly enabled live gVisor isolation tests.

| File | Purpose / feature |
| --- | --- |
| [test_bounded.py](services/judge/tests/sandbox/test_bounded.py) | Exercise fixed trusted probes for output cap, deadline and nonblocking large input |
| [test_sandbox.py](services/judge/tests/sandbox/test_sandbox.py) | Opt-in real gVisor integration fixtures: three Python AC, C++64-bit AC, WA/CE/RE/TLE/OLE, isolation, forged output, supervisor kill and tmpfs quota |

</details>

<details>
<summary>tests/e2e/hints/ — 1 files</summary>

Guest and authenticated hint provenance, failure, timeout, cancellation and context-change browser checks.

| File | Purpose / feature |
| --- | --- |
| [hints.spec.ts](tests/e2e/hints/hints.spec.ts) | Seven browser regressions for guest hints, JWT-backed authored results, provenance, safe failure/recovery, timeout, explicit cancellation and level-change abort; one read-only hint account per worker with fresh per-test signin sessions. |

</details>

<details>
<summary>tests/e2e/practice/ — 2 files</summary>

Catalog, editor, draft privacy, layout and API resilience browser checks.

| File | Purpose / feature |
| --- | --- |
| [practice.spec.ts](tests/e2e/practice/practice.spec.ts) | 7 browser tests: catalog filters, local Monaco, isolated drafts, errors, fallback/retry and responsive layout |
| [resilience.spec.ts](tests/e2e/practice/resilience.spec.ts) | 6 API-client/browser resilience tests for malformed bodies, timeout and cancellation |

</details>

<details>
<summary>tests/e2e/submissions/ — 1 files</summary>

Account lifecycle, explicit isolated judging and cross-user private-history browser checks.

| File | Purpose / feature |
| --- | --- |
| [submissions.spec.ts](tests/e2e/submissions/submissions.spec.ts) | 5 browser tests for accounts, safe redirect, guest privacy, unavailable judge and real private submission flow |

</details>

<details>
<summary>tests/tooling/github/ — 2 files</summary>

Fake-client issue-publication and pull-request evidence safety checks without real GitHub writes.

| File | Purpose / feature |
| --- | --- |
| [test_pr_evidence.py](tests/tooling/github/test_pr_evidence.py) | Offline evidence validation, malformed input, stale heads, dependency and injection regressions. |
| [test_publish_issues.py](tests/tooling/github/test_publish_issues.py) | Safety regressions for bulk issue posting; all external requests replaced by fake clients. |

</details>

## Ordered task index

**141 detailed tasks: 140 pending, 1 completed locally.** Preserve stable IDs and use the execution order below. Completion requires observed acceptance/validation evidence; a task card or generated file is not completion.

Actual GitHub publication receipt: **blocked_network**; **0** confirmed remote issue links. Until access is restored, assign and reference these local cards.

| Order | Task | State | Priority | Area / phase | Prerequisites |
| --- | --- | --- | --- | --- | --- |
| 1 | [SAI-B001](#sai-b001): Enforce an evidence contract for contributor pull requests | Completed locally | P0 | foundation / 0-contribution-gates | None |
| 2 | [SAI-B127](#sai-b127): Enforce owner-approved reviewed-merge rules for the main branch | Pending | P0 | repository governance / 0-contribution-gates | [SAI-B001](#sai-b001) |
| 3 | [SAI-B002](#sai-b002): Record owner-approved original-code licensing and inbound contribution rights | Pending | P0 | governance / 0-contribution-gates | [SAI-B001](#sai-b001) |
| 4 | [SAI-B003](#sai-b003): Approve a small pilot charter and data lifecycle contract | Pending | P0 | product / 0-contribution-gates | [SAI-B002](#sai-b002), [SAI-B001](#sai-b001) |
| 5 | [SAI-B004](#sai-b004): Pin CI actions to immutable reviewed commits | Pending | P1 | supply-chain / 1-safe-pilot | [SAI-B001](#sai-b001) |
| 6 | [SAI-B005](#sai-b005): Pin web and API container bases and align intended Python patch versions | Pending | P1 | supply-chain / 1-safe-pilot | [SAI-B004](#sai-b004), [SAI-B001](#sai-b001) |
| 7 | [SAI-B006](#sai-b006): Reject plaintext external identity and worker transport configuration | Pending | P1 | deployment-security / 1-safe-pilot | [SAI-B003](#sai-b003), [SAI-B001](#sai-b001) |
| 8 | [SAI-B007](#sai-b007): Add a total JWKS fetch deadline with real transport fixtures | Pending | P1 | identity / 1-safe-pilot | [SAI-B006](#sai-b006), [SAI-B001](#sai-b001) |
| 9 | [SAI-B008](#sai-b008): Describe protected endpoints with an accurate OpenAPI bearer scheme | Pending | P2 | api-contract / 1-safe-pilot | [SAI-B007](#sai-b007), [SAI-B001](#sai-b001) |
| 10 | [SAI-B009](#sai-b009): Validate production worker credential strength before enabling internal routes | Pending | P1 | worker-auth / 1-safe-pilot | [SAI-B006](#sai-b006), [SAI-B001](#sai-b001) |
| 11 | [SAI-B010](#sai-b010): Support bounded worker bearer rotation without an outage | Pending | P1 | worker-auth / 1-safe-pilot | [SAI-B009](#sai-b009), [SAI-B001](#sai-b001) |
| 12 | [SAI-B011](#sai-b011): Introduce an explicit trusted-ingress identity throttle policy | Pending | P1 | identity / 1-safe-pilot | [SAI-B003](#sai-b003), [SAI-B006](#sai-b006), [SAI-B001](#sai-b001) |
| 13 | [SAI-B012](#sai-b012): Create a consistent private backup and restore procedure for both stores | Pending | P1 | storage-operations / 1-safe-pilot | [SAI-B003](#sai-b003), [SAI-B001](#sai-b001) |
| 14 | [SAI-B013](#sai-b013): Introduce versioned transactional migrations for the submission database | Pending | P1 | storage / 1-safe-pilot | [SAI-B012](#sai-b012), [SAI-B001](#sai-b001) |
| 15 | [SAI-B014](#sai-b014): Add a testable email-verification delivery flow for pilot accounts | Pending | P1 | identity / 1-safe-pilot | [SAI-B003](#sai-b003), [SAI-B011](#sai-b011), [SAI-B001](#sai-b001) |
| 16 | [SAI-B015](#sai-b015): Implement password recovery with bounded single-use reset links | Pending | P1 | identity / 1-safe-pilot | [SAI-B014](#sai-b014), [SAI-B001](#sai-b001) |
| 17 | [SAI-B016](#sai-b016): Expose owned session listing and revoke-other-sessions controls | Pending | P2 | identity / 1-safe-pilot | [SAI-B015](#sai-b015), [SAI-B001](#sai-b001) |
| 18 | [SAI-B017](#sai-b017): Record privacy-safe account security events | Pending | P2 | identity-observability / 1-safe-pilot | [SAI-B003](#sai-b003), [SAI-B016](#sai-b016), [SAI-B001](#sai-b001) |
| 19 | [SAI-B018](#sai-b018): Implement deliberate account deletion across auth and owned submission state | Pending | P1 | privacy / 1-safe-pilot | [SAI-B003](#sai-b003), [SAI-B016](#sai-b016), [SAI-B013](#sai-b013), [SAI-B001](#sai-b001) |
| 20 | [SAI-B019](#sai-b019): Bound general API admission and concurrent slow requests | Pending | P1 | ingress-security / 1-safe-pilot | [SAI-B003](#sai-b003), [SAI-B006](#sai-b006), [SAI-B001](#sai-b001) |
| 21 | [SAI-B020](#sai-b020): Add structured redacted request and failure logs | Pending | P1 | operations / 1-safe-pilot | [SAI-B003](#sai-b003), [SAI-B019](#sai-b019), [SAI-B001](#sai-b001) |
| 22 | [SAI-B021](#sai-b021): Expose private bounded operational readiness and queue metrics | Pending | P2 | operations / 1-safe-pilot | [SAI-B020](#sai-b020), [SAI-B001](#sai-b001) |
| 23 | [SAI-B022](#sai-b022): Apply retention to terminal submission source with a dry-run purge | Pending | P1 | privacy-storage / 1-safe-pilot | [SAI-B003](#sai-b003), [SAI-B013](#sai-b013), [SAI-B001](#sai-b001) |
| 24 | [SAI-B023](#sai-b023): Enforce cumulative owned-source storage budgets at submission admission | Pending | P1 | storage-abuse / 1-safe-pilot | [SAI-B003](#sai-b003), [SAI-B013](#sai-b013), [SAI-B022](#sai-b022), [SAI-B001](#sai-b001) |
| 25 | [SAI-B024](#sai-b024): Avoid loading private source for submission summary pages | Pending | P2 | storage-performance / 2-useful-practice | [SAI-B013](#sai-b013), [SAI-B001](#sai-b001) |
| 26 | [SAI-B025](#sai-b025): Export an authenticated user-owned submission history bundle | Pending | P2 | privacy-product / 2-useful-practice | [SAI-B003](#sai-b003), [SAI-B022](#sai-b022), [SAI-B024](#sai-b024), [SAI-B001](#sai-b001) |
| 27 | [SAI-B026](#sai-b026): Extend problem provenance with explicit permitted-use metadata | Pending | P1 | content / 2-useful-practice | [SAI-B002](#sai-b002), [SAI-B003](#sai-b003), [SAI-B001](#sai-b001) |
| 28 | [SAI-B027](#sai-b027): Version problem and grader identity on every new submission | Pending | P1 | content-contract / 2-useful-practice | [SAI-B013](#sai-b013), [SAI-B026](#sai-b026), [SAI-B001](#sai-b001) |
| 29 | [SAI-B028](#sai-b028): Detect public-sample drift between catalog and judge deployments | Pending | P1 | content-quality / 2-useful-practice | [SAI-B027](#sai-b027), [SAI-B001](#sai-b001) |
| 30 | [SAI-B029](#sai-b029): Validate trusted problem authoring inputs before catalog publication | Pending | P2 | content-tooling / 2-useful-practice | [SAI-B026](#sai-b026), [SAI-B027](#sai-b027), [SAI-B028](#sai-b028), [SAI-B001](#sai-b001) |
| 31 | [SAI-B030](#sai-b030): Add one original prefix-sum range-query teaching exercise | Pending | P2 | content / 2-useful-practice | [SAI-B029](#sai-b029), [SAI-B001](#sai-b001) |
| 32 | [SAI-B031](#sai-b031): Use bounded server-side pagination for the expanding problem catalog | Pending | P2 | catalog / 2-useful-practice | [SAI-B029](#sai-b029), [SAI-B001](#sai-b001) |
| 33 | [SAI-B032](#sai-b032): Make catalog filters and page position shareable through the URL | Pending | P2 | catalog-ux / 2-useful-practice | [SAI-B031](#sai-b031), [SAI-B001](#sai-b001) |
| 34 | [SAI-B033](#sai-b033): Add explicit local draft export and bounded import | Pending | P2 | editor / 2-useful-practice | [SAI-B003](#sai-b003), [SAI-B001](#sai-b001) |
| 35 | [SAI-B034](#sai-b034): Offer explicit draft ownership and clear-on-shared-device controls | Pending | P2 | editor-privacy / 2-useful-practice | [SAI-B003](#sai-b003), [SAI-B033](#sai-b033), [SAI-B001](#sai-b001) |
| 36 | [SAI-B035](#sai-b035): Detect cross-tab draft conflicts before overwriting newer code | Pending | P2 | editor-reliability / 2-useful-practice | [SAI-B034](#sai-b034), [SAI-B001](#sai-b001) |
| 37 | [SAI-B036](#sai-b036): Add persistent editor display and accessibility preferences | Pending | P3 | editor-ux / 2-useful-practice | [SAI-B033](#sai-b033), [SAI-B001](#sai-b001) |
| 38 | [SAI-B037](#sai-b037): Complete keyboard navigation for the practice and submission workflow | Pending | P1 | accessibility / 2-useful-practice | [SAI-B001](#sai-b001) |
| 39 | [SAI-B038](#sai-b038): Improve screen-reader announcements and focus for asynchronous results | Pending | P1 | accessibility / 2-useful-practice | [SAI-B037](#sai-b037), [SAI-B001](#sai-b001) |
| 40 | [SAI-B039](#sai-b039): Repair contrast, reduced-motion and zoom reflow gaps | Pending | P2 | accessibility / 2-useful-practice | [SAI-B037](#sai-b037), [SAI-B001](#sai-b001) |
| 41 | [SAI-B040](#sai-b040): Add a focused automated accessibility regression gate | Pending | P2 | accessibility-quality / 2-useful-practice | [SAI-B037](#sai-b037), [SAI-B038](#sai-b038), [SAI-B039](#sai-b039), [SAI-B001](#sai-b001) |
| 42 | [SAI-B121](#sai-b121): Persist owned sandbox records and reconcile crash-orphaned containers | Pending | P0 | judge-recovery / 1-safe-pilot | [SAI-B003](#sai-b003), [SAI-B001](#sai-b001) |
| 43 | [SAI-B122](#sai-b122): Bind controller credentials to registered worker identities | Pending | P0 | worker-auth / 1-safe-pilot | [SAI-B009](#sai-b009), [SAI-B010](#sai-b010), [SAI-B013](#sai-b013), [SAI-B001](#sai-b001) |
| 44 | [SAI-B123](#sai-b123): Enforce an atomic active-lease allowance per worker principal | Pending | P0 | judge-admission / 1-safe-pilot | [SAI-B122](#sai-b122), [SAI-B013](#sai-b013), [SAI-B001](#sai-b001) |
| 45 | [SAI-B125](#sai-b125): Gate production readiness on an approved supported runtime identity | Pending | P0 | runtime-maintenance / 1-safe-pilot | [SAI-B003](#sai-b003), [SAI-B001](#sai-b001) |
| 46 | [SAI-B124](#sai-b124): Require a verified aggregate resource envelope for a production judge host | Pending | P0 | judge-isolation / 1-safe-pilot | [SAI-B003](#sai-b003), [SAI-B121](#sai-b121), [SAI-B123](#sai-b123), [SAI-B125](#sai-b125), [SAI-B001](#sai-b001) |
| 47 | [SAI-B126](#sai-b126): Withdraw worker readiness and reconcile its current lease on retirement | Pending | P1 | judge-lifecycle / 1-safe-pilot | [SAI-B013](#sai-b013), [SAI-B121](#sai-b121), [SAI-B122](#sai-b122), [SAI-B123](#sai-b123), [SAI-B001](#sai-b001) |
| 48 | [SAI-B105](#sai-b105): Add a bounded metrics exporter consuming the existing private operational surface | Pending | P1 | operations-observability / operated-pilot | [SAI-B021](#sai-b021), [SAI-B020](#sai-b020), [SAI-B001](#sai-b001) |
| 49 | [SAI-B106](#sai-b106): Propagate redacted correlation identifiers across accepted jobs | Pending | P2 | operations-observability / operated-pilot | [SAI-B105](#sai-b105), [SAI-B001](#sai-b001), [SAI-B020](#sai-b020), [SAI-B027](#sai-b027) |
| 50 | [SAI-B107](#sai-b107): Define measurable service objectives and test operator alert rules | Pending | P1 | operations-observability / operated-pilot | [SAI-B105](#sai-b105), [SAI-B106](#sai-b106), [SAI-B003](#sai-b003), [SAI-B001](#sai-b001) |
| 51 | [SAI-B108](#sai-b108): Rehearse a timed full-stack disaster restore using the approved backup helper | Pending | P1 | operations-recovery / operated-pilot | [SAI-B012](#sai-b012), [SAI-B013](#sai-b013), [SAI-B003](#sai-b003), [SAI-B001](#sai-b001) |
| 52 | [SAI-B109](#sai-b109): Measure bounded capacity and overload behavior using original fixtures | Pending | P1 | operations-capacity / operated-pilot | [SAI-B105](#sai-b105), [SAI-B107](#sai-b107), [SAI-B124](#sai-b124), [SAI-B001](#sai-b001) |
| 53 | [SAI-B110](#sai-b110): Implement a revisioned deployment smoke and rollback rehearsal | Pending | P1 | operations-release / operated-pilot | [SAI-B107](#sai-b107), [SAI-B108](#sai-b108), [SAI-B109](#sai-b109), [SAI-B005](#sai-b005), [SAI-B013](#sai-b013), [SAI-B001](#sai-b001) |
| 54 | [SAI-B111](#sai-b111): Create a canary qualification gate for judge runtime upgrades | Pending | P1 | operations-release / operated-pilot | [SAI-B110](#sai-b110), [SAI-B125](#sai-b125), [SAI-B001](#sai-b001) |
| 55 | [SAI-B112](#sai-b112): Run a bounded incident exercise for worker outage and recovery | Pending | P2 | operations-recovery / operated-pilot | [SAI-B107](#sai-b107), [SAI-B108](#sai-b108), [SAI-B110](#sai-b110), [SAI-B111](#sai-b111), [SAI-B126](#sai-b126), [SAI-B001](#sai-b001) |
| 56 | [SAI-B041](#sai-b041): Record the single-provider hint pilot activation decision | Pending | P1 | AI activation governance / AI-1 controlled model hints | [SAI-B001](#sai-b001), [SAI-B002](#sai-b002), [SAI-B003](#sai-b003), [SAI-B026](#sai-b026) |
| 57 | [SAI-B042](#sai-b042): Bound and fingerprint the existing public-only hint context | Pending | P1 | Safe model context / AI-1 controlled model hints | [SAI-B041](#sai-b041), [SAI-B001](#sai-b001) |
| 58 | [SAI-B043](#sai-b043): Validate trusted provider destinations and secret configuration | Pending | P1 | Provider configuration / AI-1 controlled model hints | [SAI-B041](#sai-b041), [SAI-B006](#sai-b006), [SAI-B001](#sai-b001) |
| 59 | [SAI-B044](#sai-b044): Define an internal generation result and usage contract | Pending | P1 | Provider-neutral contracts / AI-1 controlled model hints | [SAI-B042](#sai-b042), [SAI-B001](#sai-b001) |
| 60 | [SAI-B045](#sai-b045): Version bounded hint prompts and spoiler policies | Pending | P1 | Tutoring prompts / AI-1 controlled model hints | [SAI-B042](#sai-b042), [SAI-B044](#sai-b044), [SAI-B001](#sai-b001) |
| 61 | [SAI-B046](#sai-b046): Reject malformed model hints before constructing learner responses | Pending | P1 | Model output contracts / AI-1 controlled model hints | [SAI-B044](#sai-b044), [SAI-B045](#sai-b045), [SAI-B001](#sai-b001) |
| 62 | [SAI-B047](#sai-b047): Add deterministic provider transport fixtures without external inference | Pending | P1 | Provider adapter verification / AI-1 controlled model hints | [SAI-B043](#sai-b043), [SAI-B044](#sai-b044), [SAI-B046](#sai-b046), [SAI-B001](#sai-b001) |
| 63 | [SAI-B048](#sai-b048): Implement one opt-in bounded asynchronous hint provider adapter | Pending | P1 | Real provider transport / AI-1 controlled model hints | [SAI-B043](#sai-b043), [SAI-B044](#sai-b044), [SAI-B046](#sai-b046), [SAI-B047](#sai-b047), [SAI-B001](#sai-b001) |
| 64 | [SAI-B049](#sai-b049): Enforce account-level entitlement before model-backed hints | Pending | P1 | AI admission policy / AI-1 controlled model hints | [SAI-B041](#sai-b041), [SAI-B044](#sai-b044), [SAI-B014](#sai-b014), [SAI-B016](#sai-b016), [SAI-B001](#sai-b001) |
| 65 | [SAI-B050](#sai-b050): Reserve and reconcile durable per-account hint budgets atomically | Pending | P1 | AI token and request quotas / AI-1 controlled model hints | [SAI-B044](#sai-b044), [SAI-B049](#sai-b049), [SAI-B013](#sai-b013), [SAI-B001](#sai-b001) |
| 66 | [SAI-B051](#sai-b051): Add process-wide provider concurrency and monetary admission ceilings | Pending | P1 | Global AI spend control / AI-1 controlled model hints | [SAI-B050](#sai-b050), [SAI-B001](#sai-b001) |
| 67 | [SAI-B052](#sai-b052): Deduplicate model hint retries with account-scoped idempotency | Pending | P1 | AI request reliability / AI-1 controlled model hints | [SAI-B050](#sai-b050), [SAI-B001](#sai-b001) |
| 68 | [SAI-B053](#sai-b053): Record redacted generation usage and failure telemetry | Pending | P1 | AI observability / AI-1 controlled model hints | [SAI-B044](#sai-b044), [SAI-B050](#sai-b050), [SAI-B020](#sai-b020), [SAI-B001](#sai-b001) |
| 69 | [SAI-B054](#sai-b054): Propagate total generation deadlines and explicit cancellation states | Pending | P1 | AI cancellation and deadlines / AI-1 controlled model hints | [SAI-B048](#sai-b048), [SAI-B050](#sai-b050), [SAI-B053](#sai-b053), [SAI-B001](#sai-b001) |
| 70 | [SAI-B055](#sai-b055): Bound provider retries and add outage admission state | Pending | P1 | AI failure policy / AI-1 controlled model hints | [SAI-B048](#sai-b048), [SAI-B051](#sai-b051), [SAI-B054](#sai-b054), [SAI-B001](#sai-b001) |
| 71 | [SAI-B056](#sai-b056): Require clear external-AI disclosure before opt-in hint requests | Pending | P1 | AI privacy UX / AI-1 controlled model hints | [SAI-B041](#sai-b041), [SAI-B049](#sai-b049), [SAI-B053](#sai-b053), [SAI-B001](#sai-b001) |
| 72 | [SAI-B057](#sai-b057): Provide a tested operator kill switch for model hint admission | Pending | P1 | AI operations / AI-1 controlled model hints | [SAI-B048](#sai-b048), [SAI-B049](#sai-b049), [SAI-B055](#sai-b055), [SAI-B056](#sai-b056), [SAI-B001](#sai-b001) |
| 73 | [SAI-B058](#sai-b058): Add shared golden fixtures for hint API and browser schema parity | Pending | P2 | Cross-runtime AI contracts / AI-1 controlled model hints | [SAI-B044](#sai-b044), [SAI-B046](#sai-b046), [SAI-B001](#sai-b001) |
| 74 | [SAI-B059](#sai-b059): Define and execute a small consented model-hint pilot acceptance gate | Pending | P1 | Hint quality pilot / AI-1 controlled model hints | [SAI-B045](#sai-b045), [SAI-B050](#sai-b050), [SAI-B051](#sai-b051), [SAI-B056](#sai-b056), [SAI-B057](#sai-b057), [SAI-B058](#sai-b058), [SAI-B124](#sai-b124), [SAI-B126](#sai-b126), [SAI-B001](#sai-b001) |
| 75 | [SAI-B113](#sai-b113): Provide learner-controlled progress summaries with assistance provenance | Pending | P2 | learning-analytics / learning-coaching | [SAI-B003](#sai-b003), [SAI-B022](#sai-b022), [SAI-B001](#sai-b001) |
| 76 | [SAI-B114](#sai-b114): Add editable practice plans and deterministic review reminders | Pending | P2 | learning-plans / learning-coaching | [SAI-B113](#sai-b113), [SAI-B001](#sai-b001) |
| 77 | [SAI-B115](#sai-b115): Implement opt-in coach cohorts with explicit sharing permissions | Pending | P2 | coaching / learning-coaching | [SAI-B113](#sai-b113), [SAI-B001](#sai-b001) |
| 78 | [SAI-B116](#sai-b116): Add permissioned assignments and human rubric feedback | Pending | P2 | coaching / learning-coaching | [SAI-B113](#sai-b113), [SAI-B115](#sai-b115), [SAI-B001](#sai-b001) |
| 79 | [SAI-B060](#sai-b060): Design a bounded tutoring interaction contract beyond hint levels | Pending | P2 | Tutor interaction design / AI-2 consented tutor and debugger | [SAI-B059](#sai-b059), [SAI-B001](#sai-b001) |
| 80 | [SAI-B061](#sai-b061): Implement account-owned expiring tutor conversation state | Pending | P2 | Tutor context lifecycle / AI-2 consented tutor and debugger | [SAI-B050](#sai-b050), [SAI-B053](#sai-b053), [SAI-B056](#sai-b056), [SAI-B060](#sai-b060), [SAI-B001](#sai-b001) |
| 81 | [SAI-B062](#sai-b062): Add a consented concept-check interaction with bounded feedback | Pending | P2 | Evidence-oriented tutoring / AI-2 consented tutor and debugger | [SAI-B060](#sai-b060), [SAI-B061](#sai-b061), [SAI-B001](#sai-b001) |
| 82 | [SAI-B063](#sai-b063): Collect minimal account-owned hint quality feedback | Pending | P2 | AI feedback and correction / AI-2 consented tutor and debugger | [SAI-B053](#sai-b053), [SAI-B059](#sai-b059), [SAI-B001](#sai-b001) |
| 83 | [SAI-B064](#sai-b064): Define explicit source-sharing consent and owned debugger input | Pending | P1 | Debugger privacy boundary / AI-2 consented tutor and debugger | [SAI-B042](#sai-b042), [SAI-B049](#sai-b049), [SAI-B056](#sai-b056), [SAI-B060](#sai-b060), [SAI-B001](#sai-b001) |
| 84 | [SAI-B065](#sai-b065): Build a public-only execution evidence projection for debugging | Pending | P1 | Safe debugger evidence / AI-2 consented tutor and debugger | [SAI-B044](#sai-b044), [SAI-B064](#sai-b064), [SAI-B001](#sai-b001) |
| 85 | [SAI-B066](#sai-b066): Return debugger hypotheses separately from observed failures | Pending | P2 | Evidence-backed debugging / AI-2 consented tutor and debugger | [SAI-B048](#sai-b048), [SAI-B050](#sai-b050), [SAI-B064](#sai-b064), [SAI-B065](#sai-b065), [SAI-B001](#sai-b001) |
| 86 | [SAI-B067](#sai-b067): Show a source-hash-bound debugger patch preview with explicit apply | Pending | P2 | Debugger editor UX / AI-2 consented tutor and debugger | [SAI-B064](#sai-b064), [SAI-B066](#sai-b066), [SAI-B001](#sai-b001) |
| 87 | [SAI-B068](#sai-b068): Version authorized solver problem specifications and evaluation modes | Pending | P1 | Solver input contracts / AI-3 bounded candidate solver | [SAI-B042](#sai-b042), [SAI-B049](#sai-b049), [SAI-B064](#sai-b064), [SAI-B027](#sai-b027), [SAI-B001](#sai-b001) |
| 88 | [SAI-B069](#sai-b069): Generate a bounded algorithm-plan record before candidate code | Pending | P2 | Candidate planning / AI-3 bounded candidate solver | [SAI-B045](#sai-b045), [SAI-B048](#sai-b048), [SAI-B050](#sai-b050), [SAI-B068](#sai-b068), [SAI-B001](#sai-b001) |
| 89 | [SAI-B070](#sai-b070): Normalize bounded source candidates without archive parser assumptions | Pending | P1 | Candidate generation / AI-3 bounded candidate solver | [SAI-B046](#sai-b046), [SAI-B068](#sai-b068), [SAI-B069](#sai-b069), [SAI-B001](#sai-b001) |
| 90 | [SAI-B071](#sai-b071): Route authorized AI candidates through the existing isolated judge boundary | Pending | P1 | Solver-to-judge integration / AI-3 bounded candidate solver | [SAI-B050](#sai-b050), [SAI-B051](#sai-b051), [SAI-B065](#sai-b065), [SAI-B068](#sai-b068), [SAI-B070](#sai-b070), [SAI-B121](#sai-b121), [SAI-B123](#sai-b123), [SAI-B125](#sai-b125), [SAI-B001](#sai-b001) |
| 91 | [SAI-B072](#sai-b072): Implement a finite repair state machine with one shared run budget | Pending | P1 | Bounded solver repair / AI-3 bounded candidate solver | [SAI-B054](#sai-b054), [SAI-B066](#sai-b066), [SAI-B069](#sai-b069), [SAI-B071](#sai-b071), [SAI-B001](#sai-b001) |
| 92 | [SAI-B073](#sai-b073): Rank candidates by explicit execution evidence with deterministic ties | Pending | P2 | Candidate ranking / AI-3 bounded candidate solver | [SAI-B070](#sai-b070), [SAI-B071](#sai-b071), [SAI-B072](#sai-b072), [SAI-B001](#sai-b001) |
| 93 | [SAI-B074](#sai-b074): Create a reproducible offline solver evaluation run manifest | Pending | P1 | Solver evaluation / AI-4 evaluation and research gates | [SAI-B053](#sai-b053), [SAI-B068](#sai-b068), [SAI-B072](#sai-b072), [SAI-B073](#sai-b073), [SAI-B001](#sai-b001) |
| 94 | [SAI-B075](#sai-b075): Admit only reviewed differential and metamorphic test specifications | Pending | P1 | Authorized test generation / AI-4 evaluation and research gates | [SAI-B068](#sai-b068), [SAI-B071](#sai-b071), [SAI-B074](#sai-b074), [SAI-B001](#sai-b001) |
| 95 | [SAI-B076](#sai-b076): Reduce consented public counterexamples under a finite execution budget | Pending | P2 | Counterexample debugging / AI-4 evaluation and research gates | [SAI-B064](#sai-b064), [SAI-B065](#sai-b065), [SAI-B071](#sai-b071), [SAI-B075](#sai-b075), [SAI-B001](#sai-b001) |
| 96 | [SAI-B081](#sai-b081): Implement contest lifecycle and authoritative event timing | Pending | P1 | contests / contest-foundation | [SAI-B003](#sai-b003), [SAI-B027](#sai-b027), [SAI-B001](#sai-b001) |
| 97 | [SAI-B082](#sai-b082): Add permissioned contest registration and eligibility checks | Pending | P1 | contests / contest-foundation | [SAI-B081](#sai-b081), [SAI-B001](#sai-b001) |
| 98 | [SAI-B083](#sai-b083): Freeze versioned problem sets for each contest | Pending | P1 | contests / contest-foundation | [SAI-B081](#sai-b081), [SAI-B027](#sai-b027), [SAI-B029](#sai-b029), [SAI-B001](#sai-b001) |
| 99 | [SAI-B084](#sai-b084): Implement deterministic ICPC scoring as a tested pure calculation | Pending | P1 | contests / contest-foundation | [SAI-B081](#sai-b081), [SAI-B083](#sai-b083), [SAI-B001](#sai-b001) |
| 100 | [SAI-B085](#sai-b085): Add participant and organizer scoreboard projections with freeze rules | Pending | P1 | contests / contest-foundation | [SAI-B084](#sai-b084), [SAI-B001](#sai-b001) |
| 101 | [SAI-B086](#sai-b086): Connect contest submissions to event eligibility and immutable attempt context | Pending | P1 | contests / contest-foundation | [SAI-B081](#sai-b081), [SAI-B082](#sai-b082), [SAI-B083](#sai-b083), [SAI-B084](#sai-b084), [SAI-B001](#sai-b001) |
| 102 | [SAI-B087](#sai-b087): Implement isolated virtual-contest sessions with personal start times | Pending | P2 | contests / contest-experience | [SAI-B081](#sai-b081), [SAI-B083](#sai-b083), [SAI-B084](#sai-b084), [SAI-B086](#sai-b086), [SAI-B001](#sai-b001) |
| 103 | [SAI-B088](#sai-b088): Add locked ICPC team rosters and event membership rules | Pending | P2 | teams / contest-experience | [SAI-B082](#sai-b082), [SAI-B001](#sai-b001) |
| 104 | [SAI-B089](#sai-b089): Scope contest attempts and source visibility to authorized team members | Pending | P2 | teams / contest-experience | [SAI-B086](#sai-b086), [SAI-B088](#sai-b088), [SAI-B001](#sai-b001) |
| 105 | [SAI-B090](#sai-b090): Enforce contest assistance policy across hint and submission routes | Pending | P1 | contest-integrity / contest-experience | [SAI-B081](#sai-b081), [SAI-B086](#sai-b086), [SAI-B089](#sai-b089), [SAI-B049](#sai-b049), [SAI-B001](#sai-b001) |
| 106 | [SAI-B091](#sai-b091): Build an organizer workflow for contest draft, preview and publication | Pending | P2 | contest-admin / contest-experience | [SAI-B081](#sai-b081), [SAI-B082](#sai-b082), [SAI-B083](#sai-b083), [SAI-B085](#sai-b085), [SAI-B001](#sai-b001) |
| 107 | [SAI-B092](#sai-b092): Implement audited contest rejudging with immutable verdict revisions | Pending | P1 | contest-admin / contest-corrections | [SAI-B085](#sai-b085), [SAI-B086](#sai-b086), [SAI-B091](#sai-b091), [SAI-B001](#sai-b001) |
| 108 | [SAI-B093](#sai-b093): Add contest clarification and appeal records with controlled disclosure | Pending | P2 | contest-admin / contest-corrections | [SAI-B091](#sai-b091), [SAI-B092](#sai-b092), [SAI-B001](#sai-b001) |
| 109 | [SAI-B094](#sai-b094): Deliver bounded scoreboard polling with consistent event revisions | Pending | P2 | leaderboards / contest-experience | [SAI-B085](#sai-b085), [SAI-B086](#sai-b086), [SAI-B088](#sai-b088), [SAI-B001](#sai-b001) |
| 110 | [SAI-B095](#sai-b095): Create a reproducible contest rehearsal and official standings export | Pending | P1 | contest-release / contest-corrections | [SAI-B090](#sai-b090), [SAI-B091](#sai-b091), [SAI-B092](#sai-b092), [SAI-B094](#sai-b094), [SAI-B001](#sai-b001) |
| 111 | [SAI-B096](#sai-b096): Version output-comparison policies without changing existing verdicts | Pending | P1 | judge-validators / judge-extensibility | [SAI-B027](#sai-b027), [SAI-B028](#sai-b028), [SAI-B001](#sai-b001) |
| 112 | [SAI-B097](#sai-b097): Add isolated versioned custom-checker support for authorized problems | Pending | P2 | judge-validators / judge-extensibility | [SAI-B096](#sai-b096), [SAI-B124](#sai-b124), [SAI-B125](#sai-b125), [SAI-B001](#sai-b001) |
| 113 | [SAI-B098](#sai-b098): Implement bounded floating-point answer validation | Pending | P2 | judge-validators / judge-extensibility | [SAI-B096](#sai-b096), [SAI-B001](#sai-b001) |
| 114 | [SAI-B099](#sai-b099): Introduce explicit subtask scoring for separately configured events | Pending | P3 | judge-validators / judge-extensibility | [SAI-B096](#sai-b096), [SAI-B097](#sai-b097), [SAI-B001](#sai-b001), [SAI-B013](#sai-b013), [SAI-B027](#sai-b027), [SAI-B084](#sai-b084) |
| 115 | [SAI-B100](#sai-b100): Add an audited C++20 runtime alongside existing C++17 | Pending | P2 | judge-languages / judge-extensibility | [SAI-B096](#sai-b096), [SAI-B125](#sai-b125), [SAI-B124](#sai-b124), [SAI-B001](#sai-b001) |
| 116 | [SAI-B101](#sai-b101): Add isolated Java support with explicit JVM resource semantics | Pending | P3 | judge-languages / judge-extensibility | [SAI-B096](#sai-b096), [SAI-B125](#sai-b125), [SAI-B124](#sai-b124), [SAI-B001](#sai-b001) |
| 117 | [SAI-B102](#sai-b102): Add isolated JavaScript support with denied network and bounded runtime | Pending | P3 | judge-languages / judge-extensibility | [SAI-B096](#sai-b096), [SAI-B125](#sai-b125), [SAI-B124](#sai-b124), [SAI-B001](#sai-b001) |
| 118 | [SAI-B103](#sai-b103): Add isolated Go compilation with offline standard-library execution | Pending | P3 | judge-languages / judge-extensibility | [SAI-B096](#sai-b096), [SAI-B125](#sai-b125), [SAI-B124](#sai-b124), [SAI-B001](#sai-b001) |
| 119 | [SAI-B104](#sai-b104): Add isolated Rust compilation with a fixed edition and no dependency fetch | Pending | P3 | judge-languages / judge-extensibility | [SAI-B096](#sai-b096), [SAI-B125](#sai-b125), [SAI-B124](#sai-b124), [SAI-B001](#sai-b001) |
| 120 | [SAI-B117](#sai-b117): Enforce institutional sponsorship and learner data-use boundaries | Pending | P1 | institutional-privacy / institutional-pilot | [SAI-B115](#sai-b115), [SAI-B116](#sai-b116), [SAI-B003](#sai-b003), [SAI-B018](#sai-b018), [SAI-B001](#sai-b001) |
| 121 | [SAI-B118](#sai-b118): Export institution-authorized assignment records with redaction tests | Pending | P2 | institutional-privacy / institutional-pilot | [SAI-B116](#sai-b116), [SAI-B117](#sai-b117), [SAI-B001](#sai-b001) |
| 122 | [SAI-B119](#sai-b119): Produce a redacted pilot cost ledger and resource-envelope report | Pending | P2 | business-operations / institutional-pilot | [SAI-B105](#sai-b105), [SAI-B109](#sai-b109), [SAI-B003](#sai-b003), [SAI-B021](#sai-b021), [SAI-B053](#sai-b053), [SAI-B001](#sai-b001) |
| 123 | [SAI-B120](#sai-b120): Extend existing pilot grants with expiring institutional scopes | Pending | P2 | business-release / institutional-pilot | [SAI-B110](#sai-b110), [SAI-B112](#sai-b112), [SAI-B117](#sai-b117), [SAI-B119](#sai-b119), [SAI-B049](#sai-b049), [SAI-B003](#sai-b003), [SAI-B001](#sai-b001), [SAI-B050](#sai-b050), [SAI-B051](#sai-b051) |
| 124 | [SAI-B077](#sai-b077): Separate evaluation splits and report archive contamination candidates | Pending | P1 | Evaluation integrity / AI-4 evaluation and research gates | [SAI-B068](#sai-b068), [SAI-B074](#sai-b074), [SAI-B026](#sai-b026), [SAI-B001](#sai-b001) |
| 125 | [SAI-B078](#sai-b078): Register dataset and model permissions separately from source licenses | Pending | P1 | Research provenance / AI-4 evaluation and research gates | [SAI-B041](#sai-b041), [SAI-B068](#sai-b068), [SAI-B077](#sai-b077), [SAI-B002](#sai-b002), [SAI-B026](#sai-b026), [SAI-B001](#sai-b001) |
| 126 | [SAI-B079](#sai-b079): Produce a resource-and-integrity feasibility decision for one self-hosted model | Pending | P2 | Model serving research gate / AI-4 evaluation and research gates | [SAI-B074](#sai-b074), [SAI-B078](#sai-b078), [SAI-B001](#sai-b001) |
| 127 | [SAI-B080](#sai-b080): Add an explicit admission gate for reproducible fine-tuning experiments | Pending | P1 | Fine-tuning research controls / AI-4 evaluation and research gates | [SAI-B074](#sai-b074), [SAI-B077](#sai-b077), [SAI-B078](#sai-b078), [SAI-B079](#sai-b079), [SAI-B001](#sai-b001) |
| 128 | [SAI-B128](#sai-b128): Implement a declared DSA coverage matrix and preregistered model release measurements | Pending | P1 | solver-readiness / ML-1 measured scope and baseline | [SAI-B001](#sai-b001), [SAI-B074](#sai-b074), [SAI-B077](#sai-b077), [SAI-B078](#sai-b078) |
| 129 | [SAI-B129](#sai-b129): Run an approved untuned checkpoint comparison and record a future selection | Pending | P1 | model-baseline / ML-1 measured scope and baseline | [SAI-B001](#sai-b001), [SAI-B074](#sai-b074), [SAI-B078](#sai-b078), [SAI-B079](#sai-b079), [SAI-B128](#sai-b128) |
| 130 | [SAI-B130](#sai-b130): Materialize a permitted validated training corpus with immutable split lineage | Pending | P1 | training-data / ML-2 approved data and training tooling | [SAI-B001](#sai-b001), [SAI-B077](#sai-b077), [SAI-B078](#sai-b078), [SAI-B128](#sai-b128) |
| 131 | [SAI-B131](#sai-b131): Create a separate locked training environment and reviewed artifact loader | Pending | P1 | training-infrastructure / ML-2 approved data and training tooling | [SAI-B001](#sai-b001), [SAI-B079](#sai-b079), [SAI-B080](#sai-b080), [SAI-B129](#sai-b129) |
| 132 | [SAI-B132](#sai-b132): Implement tokenizer-aware SFT examples and answer-only loss masking | Pending | P1 | training-preprocessing / ML-2 approved data and training tooling | [SAI-B001](#sai-b001), [SAI-B129](#sai-b129), [SAI-B130](#sai-b130), [SAI-B131](#sai-b131) |
| 133 | [SAI-B133](#sai-b133): Run an approved external LoRA smoke experiment with stop and resume evidence | Pending | P1 | training-smoke / ML-3 actual approved training | [SAI-B001](#sai-b001), [SAI-B080](#sai-b080), [SAI-B129](#sai-b129), [SAI-B130](#sai-b130), [SAI-B131](#sai-b131), [SAI-B132](#sai-b132) |
| 134 | [SAI-B134](#sai-b134): Execute the approved bounded SFT adapter training campaign | Pending | P1 | actual-fine-tuning / ML-3 actual approved training | [SAI-B001](#sai-b001), [SAI-B080](#sai-b080), [SAI-B129](#sai-b129), [SAI-B130](#sai-b130), [SAI-B131](#sai-b131), [SAI-B132](#sai-b132), [SAI-B133](#sai-b133) |
| 135 | [SAI-B135](#sai-b135): Publish immutable private model artifacts and complete adapter lineage | Pending | P1 | model-artifacts / ML-3 actual approved training | [SAI-B001](#sai-b001), [SAI-B078](#sai-b078), [SAI-B129](#sai-b129), [SAI-B130](#sai-b130), [SAI-B131](#sai-b131), [SAI-B134](#sai-b134) |
| 136 | [SAI-B136](#sai-b136): Evaluate tuned candidates against matched baselines and enforce category gates | Pending | P1 | model-promotion-evaluation / ML-4 evaluation and delivery | [SAI-B001](#sai-b001), [SAI-B074](#sai-b074), [SAI-B075](#sai-b075), [SAI-B077](#sai-b077), [SAI-B128](#sai-b128), [SAI-B129](#sai-b129), [SAI-B134](#sai-b134), [SAI-B135](#sai-b135) |
| 137 | [SAI-B137](#sai-b137): Qualify inference export and quantization at the deployed precision | Pending | P1 | inference-qualification / ML-4 evaluation and delivery | [SAI-B001](#sai-b001), [SAI-B079](#sai-b079), [SAI-B128](#sai-b128), [SAI-B135](#sai-b135), [SAI-B136](#sai-b136) |
| 138 | [SAI-B138](#sai-b138): Integrate the qualified trained artifact with bounded provider-neutral serving | Pending | P1 | trained-model-serving / ML-4 evaluation and delivery | [SAI-B001](#sai-b001), [SAI-B043](#sai-b043), [SAI-B044](#sai-b044), [SAI-B046](#sai-b046), [SAI-B050](#sai-b050), [SAI-B051](#sai-b051), [SAI-B054](#sai-b054), [SAI-B055](#sai-b055), [SAI-B057](#sai-b057), [SAI-B079](#sai-b079), [SAI-B135](#sai-b135), [SAI-B136](#sai-b136), [SAI-B137](#sai-b137) |
| 139 | [SAI-B139](#sai-b139): Promote a trained model through a limited pilot and rehearsed rollback | Pending | P1 | trained-model-release / ML-4 evaluation and delivery | [SAI-B001](#sai-b001), [SAI-B003](#sai-b003), [SAI-B057](#sai-b057), [SAI-B059](#sai-b059), [SAI-B110](#sai-b110), [SAI-B124](#sai-b124), [SAI-B126](#sai-b126), [SAI-B128](#sai-b128), [SAI-B135](#sai-b135), [SAI-B136](#sai-b136), [SAI-B137](#sai-b137), [SAI-B138](#sai-b138) |
| 140 | [SAI-B140](#sai-b140): Run a separately approved execution-reward preference or RL experiment | Pending | P2 | optional-model-research / ML-5 conditional improvement research | [SAI-B001](#sai-b001), [SAI-B075](#sai-b075), [SAI-B077](#sai-b077), [SAI-B078](#sai-b078), [SAI-B080](#sai-b080), [SAI-B128](#sai-b128), [SAI-B130](#sai-b130), [SAI-B131](#sai-b131), [SAI-B132](#sai-b132), [SAI-B133](#sai-b133), [SAI-B134](#sai-b134), [SAI-B135](#sai-b135), [SAI-B136](#sai-b136) |
| 141 | [SAI-B141](#sai-b141): Operate a consented failure-analysis and retraining improvement cycle | Pending | P2 | model-lifecycle / ML-5 conditional improvement research | [SAI-B001](#sai-b001), [SAI-B003](#sai-b003), [SAI-B063](#sai-b063), [SAI-B077](#sai-b077), [SAI-B078](#sai-b078), [SAI-B128](#sai-b128), [SAI-B130](#sai-b130), [SAI-B134](#sai-b134), [SAI-B135](#sai-b135), [SAI-B136](#sai-b136), [SAI-B139](#sai-b139) |

## Complete task specifications

All scope, acceptance, validation, exclusions and review risks from the canonical catalogue are included here. Expand a task to assign it. Target paths can name future files; they are ownership instructions rather than claims those files already exist. Owner roles suggest expertise, not actual assignees or granted permissions.

<a id="sai-b001"></a>
<details>
<summary>1. SAI-B001: Enforce an evidence contract for contributor pull requests [completed_locally]</summary>

**Priority:** P0 · **Phase:** 0-contribution-gates · **Area:** foundation.

**Suggested role:** repository maintainer and reviewer.

**Prerequisites:** None.

**Problem / missing behavior**

The requested multi-tool workflow needs PR submissions that the reviewing assistant can assess consistently. Instructions alone do not show whether a contributor mapped an issue, respected scope or actually ran a claimed check.

**Target paths / responsibility**

- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/workflows/ci.yml`
- `docs/engineering/CODEX_PLAYBOOK.md`
- `CONTRIBUTING.md`

**Implementation scope**

- Extend the PR evidence contract with stable backlog ID, before/after behavior, exact changed paths, dependency status, tests actually run with fail/skip/unrun states, security/data impact and rollback.
- Add a narrow pull-request metadata check that reports missing sections or an unknown/missing issue reference; keep implementation review and merge authorization with the designated reviewer.
- Require external AI tools to submit focused PRs and corrections rather than bypassing review; recognize explicit owner overrides for exceptional direct-main work.
- Apply the evidence gate to all contributor PRs; do not infer or classify authorship as AI/human from content.

**Acceptance criteria**

- A fixture PR with all required evidence passes the metadata check; fixtures with no issue ID or invented empty test evidence fail with an actionable explanation.
- An explicit not-run explanation is allowed when the owner forbids testing; the check never forces fabricated results.
- The workflow never executes arbitrary PR-body text and never grants write permission or auto-merges a PR.

**Validation required**

- Inspect the proposed PR template and run the metadata-check fixtures introduced by this issue.
- Inspect workflow permissions and fork-PR handling; do not run pull-request head code with write credentials.

**Out of scope**

- Automated code correctness judgment
- Automatically approving or merging all AI contributions
- Reimplementing the repository-wide instructions the owner is already updating

**Risk and review**

Untrusted PR text must remain data, and evidence completeness must not be presented as substantive review.

**Completion record (2026-11-17):** Implemented scripts/github/check_pr_evidence.py and read-only trusted-base PR workflow;37 scoped evidence cases and the complete50-case tooling suite passed. Source/contract reviewed for inert data, stale heads and malformed events. Hosted workflow execution and branch-rule enforcement remain unverified and separate from metadata completeness. The complete npm run test:all aggregate passed at source 33ed42f0b42b43e228c547cfc106c5c874bc61d1 with337 cases and exit0.

</details>

<a id="sai-b127"></a>
<details>
<summary>2. SAI-B127: Enforce owner-approved reviewed-merge rules for the main branch [pending]</summary>

**Priority:** P0 · **Phase:** 0-contribution-gates · **Area:** repository governance.

**Suggested role:** Repository owner and designated security reviewer.

**Prerequisites:** [SAI-B001](#sai-b001).

**Problem / missing behavior**

A written review-only workflow does not restrict credentials that can currently write main. The actual GitHub branch rules and reviewer identities must be verified before distributed contributors rely on enforced review.

**Target paths / responsibility**

- `.github/workflows/ci.yml`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `CONTRIBUTING.md`
- `AGENTS.md`

**Implementation scope**

- Have the repository owner name the actual reviewer identities and approve a narrow emergency-maintenance policy; do not invent an assistant GitHub account.
- Configure supported main-branch rules requiring PR review and the verified check contexts, protecting against forced updates/deletion and documenting any unavoidable owner bypass.
- Record the effective rules and hosting-plan limitations without exposing tokens; preserve access for the designated review/merge workflow.

**Acceptance criteria**

- An authorized read of effective branch rules confirms review/check requirements and protected history.
- The owner can identify which principals may merge and which emergency bypasses remain; the documentation does not claim an assistant monitors or approves work continuously.
- If permissions or hosting-plan capabilities block enforcement, the issue remains explicitly blocked with the exact prerequisite rather than claiming policy prose enforced it.

**Validation required**

- Read the effective GitHub rules/protection configuration using authorized API access and review the required check context names.
- Use a disposable authorized repository/rule fixture for any negative push experiments; never test forced updates or destructive changes on main.

**Out of scope**

- Creating or sharing new credentials in chat
- Automatically merging contributor PRs
- Changing repository visibility or purchasing a hosting plan

**Risk and review**

Incorrect rules can block maintainers or leave unreviewed writes possible. Owner authorization and verified actual identities are prerequisites.

</details>

<a id="sai-b002"></a>
<details>
<summary>3. SAI-B002: Record owner-approved original-code licensing and inbound contribution rights [pending]</summary>

**Priority:** P0 · **Phase:** 0-contribution-gates · **Area:** governance.

**Suggested role:** project owner with legal/IP reviewer.

**Prerequisites:** [SAI-B001](#sai-b001).

**Problem / missing behavior**

The original project has no selected outbound license or settled inbound IP policy. Inviting many AI-assisted contributors without an explicit rights decision leaves reuse and contribution expectations unclear.

**Target paths / responsibility**

- `docs/governance/OPEN_DECISIONS.md`
- `docs/governance/DATA_AND_LICENSES.md`
- `CONTRIBUTING.md`
- `AGENTS.md`

**Implementation scope**

- Prepare a short decision record comparing owner-selected licensing options and how external human/AI-assisted contributions are accepted.
- Obtain the actual owner decision, record its date and scope, and only then add or amend license/notice files and contributor declarations.
- Distinguish original application rights from preserved upstream MIT/Apache code, datasets, problems and model artifacts.

**Acceptance criteria**

- The owner-approved decision states exact rights for original code and the inbound contribution mechanism; undecided points remain explicitly blocked.
- Contributor instructions identify third-party attribution and provenance requirements without claiming ownership of upstream or user code.
- A PR containing this change includes the owner decision reference and reviewer evidence required by B001.

**Validation required**

- Statically review the decision, selected license text and contributor notice for consistency.
- Review the diff to ensure preserved upstream notices and archive hashes were not changed.

**Out of scope**

- Choosing a license without owner authority
- Re-licensing archived dependencies or datasets
- Legal certification

**Risk and review**

An assistant cannot invent licensing consent or assign rights it does not own.

</details>

<a id="sai-b003"></a>
<details>
<summary>4. SAI-B003: Approve a small pilot charter and data lifecycle contract [pending]</summary>

**Priority:** P0 · **Phase:** 0-contribution-gates · **Area:** product.

**Suggested role:** project owner and privacy/product reviewer.

**Prerequisites:** [SAI-B002](#sai-b002), [SAI-B001](#sai-b001).

**Problem / missing behavior**

The existing local app can support learning, but first audience, public-hosting responsibility, retention periods, deletion and provider-sharing consent remain unresolved. These decisions are prerequisites for handling real learner data.

**Target paths / responsibility**

- `docs/governance/OPEN_DECISIONS.md`
- `docs/governance/DATA_AND_LICENSES.md`
- `docs/product/PRODUCT_REQUIREMENTS.md`
- `docs/product/PROJECT_VISION.md`

**Implementation scope**

- Document a deliberately small first pilot audience and the existing practice/account/history features included.
- Have the owner specify retention and deletion rules for source, accounts, logs, exports and backups, including how in-flight jobs and legal exceptions are handled.
- Record who operates the pilot, its approved resource ceiling, incident contact and whether external model sharing is disabled; keep paid services off by default.

**Acceptance criteria**

- A decision table names each stored data class, purpose, owner, retention trigger and deletion/export behavior.
- No private submission is eligible for training or external provider transfer without explicit separately recorded consent.
- Pilot launch criteria distinguish local readiness, controlled pilot access and public production exposure; unapproved budget or hosting choices remain blocked.

**Validation required**

- Review the charter against current source locations and the technical-debt privacy/operations gates.
- Have the owner approve the decision record; no runtime or paid-service call is required.

**Out of scope**

- Implementing billing or an AI provider
- Claiming production readiness
- Inventing a retention period or hosting budget without owner approval

**Risk and review**

Policy choices affect irreversible deletion and public trust; engineering must follow recorded owner decisions.

</details>

<a id="sai-b004"></a>
<details>
<summary>5. SAI-B004: Pin CI actions to immutable reviewed commits [pending]</summary>

**Priority:** P1 · **Phase:** 1-safe-pilot · **Area:** supply-chain.

**Suggested role:** release engineer.

**Prerequisites:** [SAI-B001](#sai-b001).

**Problem / missing behavior**

CI currently references checkout, setup-node, setup-uv and upload-artifact by mutable major tags. Package locks do not pin the executable action implementations.

**Target paths / responsibility**

- `.github/workflows/ci.yml`
- `docs/engineering/CODEX_PLAYBOOK.md`

**Implementation scope**

- Resolve each currently used action to an official reviewed commit and record the readable release alongside the digest.
- Keep workflow permissions at the existing minimum and document a bounded update/review process.
- Preserve frozen installs and existing check coverage rather than replacing the workflow.

**Acceptance criteria**

- Every third-party uses entry is pinned to a full commit SHA from the official upstream.
- No new token write permission, unsafe pull_request_target execution or secret exposure is introduced.
- The workflow configuration still contains all existing required steps and explicit artifact retention.

**Validation required**

- Statically inspect all uses entries, source provenance and workflow permissions.
- When check execution is authorized, observe a normal fork-safe PR CI run at the exact commit and record its outcome.

**Out of scope**

- Changing application dependencies
- Running untrusted PR code with repository write credentials
- Claiming mutable tags prove compromise

**Risk and review**

Incorrect action provenance can install a malicious implementation; digest updates require review.

</details>

<a id="sai-b005"></a>
<details>
<summary>6. SAI-B005: Pin web and API container bases and align intended Python patch versions [pending]</summary>

**Priority:** P1 · **Phase:** 1-safe-pilot · **Area:** supply-chain.

**Suggested role:** release engineer.

**Prerequisites:** [SAI-B004](#sai-b004), [SAI-B001](#sai-b001).

**Problem / missing behavior**

The judge base is already digest-pinned, while web/API image tags remain mutable and the API Python pin is broader than the root patch pin. Rebuilding can silently select different toolchains.

**Target paths / responsibility**

- `apps/web/Dockerfile`
- `services/api/Dockerfile`
- `services/api/.python-version`
- `.python-version`
- `.node-version`
- `docs/onboarding/DEVELOPMENT.md`

**Implementation scope**

- Select supported official web/API base-image identities and pin immutable digests while preserving their current nonroot and read-only runtime assumptions.
- Reconcile the intended root and API Python patch policy with actual documented supported versions; do not silently widen dependency compatibility.
- Document how digest/patch updates are reviewed and refreshed.

**Acceptance criteria**

- Web/API base-image references include reviewed digests and readable versions.
- Root/API Python pins express one intentional policy and frozen dependency installation remains enabled.
- A later authorized build produces artifacts without runtime keys, databases or AnalyseFuture content; no TLS or checksum verification is disabled.

**Validation required**

- Statically review Docker stages, image origins and version pins.
- When builds are authorized: npm run build; docker build --secret id=proxy_ca,src=/etc/ssl/certs/ca-certificates.crt -t solver-ai-api:pin-check services/api.

**Out of scope**

- Replacing the sandbox runtime
- Automatic latest-version upgrades
- Installing GPU tooling

**Risk and review**

Image updates may change OS libraries or runtime behavior; preserve rollback digests and verify supported architecture.

</details>

<a id="sai-b006"></a>
<details>
<summary>7. SAI-B006: Reject plaintext external identity and worker transport configuration [pending]</summary>

**Priority:** P1 · **Phase:** 1-safe-pilot · **Area:** deployment-security.

**Suggested role:** backend security engineer.

**Prerequisites:** [SAI-B003](#sai-b003), [SAI-B001](#sai-b001).

**Problem / missing behavior**

AUTH_JWKS_URL currently permits HTTP for any hostname. Local loopback/Compose routes need support, but the same permissive configuration can be unsafe across an untrusted network.

**Target paths / responsibility**

- `services/api/solver_api/features/identity/verification.py`
- `services/api/solver_api/main.py`
- `services/judge/solver_judge/control/worker.py`
- `compose.yaml`
- `docs/onboarding/DEVELOPMENT.md`

**Implementation scope**

- Define an explicit local/trusted-private transport policy and reject external plaintext JWKS, issuer and worker API routes by default.
- Validate origins, credentials, fragments and configured destinations once at startup with safe error messages.
- Keep documented loopback and explicitly selected private Compose development routes usable without disabling TLS validation.

**Acceptance criteria**

- Configuration fixtures accept supported local routes and HTTPS external routes, and reject a public HTTP hostname, embedded credentials and malformed origins.
- A denied configuration fails startup before accepting authenticated traffic; no URL credentials appear in errors.
- Existing fixed-destination, no-redirect JWKS behavior and worker credential separation remain intact.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/identity/test_auth.py
- uv run --project services/api --frozen pytest services/judge/tests/control/test_worker.py

**Out of scope**

- Purchasing certificates or deploying publicly
- User-selected provider destinations
- Disabling proxy/CA trust

**Risk and review**

A broad private-network exception would recreate the gap; explicit development exemptions need owner-reviewed scope.

</details>

<a id="sai-b007"></a>
<details>
<summary>8. SAI-B007: Add a total JWKS fetch deadline with real transport fixtures [pending]</summary>

**Priority:** P1 · **Phase:** 1-safe-pilot · **Area:** identity.

**Suggested role:** backend identity engineer.

**Prerequisites:** [SAI-B006](#sai-b006), [SAI-B001](#sai-b001).

**Problem / missing behavior**

JWKS refresh uses HTTPX operation timeouts and a size cap but has no outer elapsed-time bound. A slow stream can hold authentication refresh longer than the nominal five-second timeout; most existing tests stub the fetch function.

**Target paths / responsibility**

- `services/api/solver_api/features/identity/verification.py`
- `services/api/tests/identity/test_auth.py`

**Implementation scope**

- Wrap the full JWKS transfer and decoding path in an explicit total deadline with a monotonic/async cancellation mechanism.
- Add HTTPX transport fixtures for slow chunks, redirects, oversized/incorrect Content-Length, invalid JSON and cancellation.
- Preserve refresh cooldown, cache locking, fixed algorithms and safe unavailable-versus-unauthorized responses.

**Acceptance criteria**

- A slow trickle terminates at the configured total deadline rather than extending on every chunk.
- Redirects and bodies above 65,536 bytes are rejected, including missing/false length headers.
- Concurrent refresh requests do not create unbounded fetches and valid cached-key behavior remains covered.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/identity/test_auth.py

**Out of scope**

- Changing JWT algorithms or trusting token-supplied key URLs
- Adding a second identity authority
- Live calls to arbitrary JWKS hosts in tests

**Risk and review**

Cancellation and cache-state changes can accidentally deny all users or accept stale keys; fixtures must exercise both failure and recovery.

</details>

<a id="sai-b008"></a>
<details>
<summary>9. SAI-B008: Describe protected endpoints with an accurate OpenAPI bearer scheme [pending]</summary>

**Priority:** P2 · **Phase:** 1-safe-pilot · **Area:** api-contract.

**Suggested role:** API engineer.

**Prerequisites:** [SAI-B007](#sai-b007), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Manual bearer parsing enforces authentication but does not expose a usable security scheme in interactive API docs. A docs-only scheme must not relax duplicate-header or strict signature checks.

**Target paths / responsibility**

- `services/api/solver_api/main.py`
- `services/api/solver_api/features/identity/verification.py`
- `services/api/tests/catalog/test_api.py`
- `services/api/tests/identity/test_auth.py`

**Implementation scope**

- Declare bearer security metadata for protected learner endpoints while retaining require_user as the authorization authority.
- Keep public catalog/health endpoints public and worker-only routes visibly separate from learner token authentication.
- Extend schema assertions to verify correct security declarations, not merely path presence.

**Acceptance criteria**

- OpenAPI contains one documented learner bearer scheme and protected submission/hint endpoints reference it.
- Public catalog endpoints do not advertise a mandatory bearer token.
- Duplicate authorization headers, wrong issuer/audience/algorithm and token-supplied URLs still fail exactly as before.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/catalog/test_api.py services/api/tests/identity/test_auth.py

**Out of scope**

- Changing authentication semantics
- Exposing worker credentials through Swagger
- Adding a new API-key login mechanism

**Risk and review**

Convenience helpers can mask duplicate headers or bypass the existing verifier; the security dependency must remain authoritative.

</details>

<a id="sai-b009"></a>
<details>
<summary>10. SAI-B009: Validate production worker credential strength before enabling internal routes [pending]</summary>

**Priority:** P1 · **Phase:** 1-safe-pilot · **Area:** worker-auth.

**Suggested role:** backend security engineer.

**Prerequisites:** [SAI-B006](#sai-b006), [SAI-B001](#sai-b001).

**Problem / missing behavior**

The native runner generates a strong local worker token, but the API accepts configured worker bearer material without an independent strength check. A manually supplied weak production value can define the whole controller trust domain.

**Target paths / responsibility**

- `services/api/solver_api/main.py`
- `scripts/development/local_config.py`
- `services/judge/solver_judge/control/worker.py`
- `services/api/tests/submissions/test_submissions.py`
- `docs/onboarding/DEVELOPMENT.md`

**Implementation scope**

- Centralize worker credential validation for configured internal-route enablement, with a documented minimum entropy/length policy and no public fallback key.
- Keep the existing secure local generation path and distinguish deliberately disabled judging from invalid configured credentials.
- Reject invalid credentials at configuration time without logging their value.

**Acceptance criteria**

- Empty/unset worker auth leaves execution unavailable as documented; a nonempty weak configured value fails clearly.
- Generated local tokens and a valid production-format fixture enable the existing authenticated control flow.
- Logs, API errors and diagnostics contain no token values or token-derived reversible representation.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/submissions/test_submissions.py
- uv run --project services/api --frozen pytest services/judge/tests/control/test_worker.py

**Out of scope**

- Implementing multi-worker certificate identities
- Changing sandbox isolation
- Printing or requesting real secret values

**Risk and review**

Overly broad validation could break deliberate no-judge development; disabled mode and invalid mode need distinct tests.

</details>

<a id="sai-b010"></a>
<details>
<summary>11. SAI-B010: Support bounded worker bearer rotation without an outage [pending]</summary>

**Priority:** P1 · **Phase:** 1-safe-pilot · **Area:** worker-auth.

**Suggested role:** backend engineer and deployment operator.

**Prerequisites:** [SAI-B009](#sai-b009), [SAI-B001](#sai-b001).

**Problem / missing behavior**

The controller trust domain relies on one configured bearer, with no tested handover protocol. Replacing it can abruptly stop heartbeat/lease/completion requests during active work.

**Target paths / responsibility**

- `services/api/solver_api/main.py`
- `services/judge/solver_judge/control/worker.py`
- `services/api/tests/submissions/test_submissions.py`
- `docs/onboarding/DEVELOPMENT.md`

**Implementation scope**

- Design a narrow current/previous credential handover with an explicit short overlap deadline and constant-time comparisons.
- Document update order and rollback for API and existing workers; prohibit permanent previous-token acceptance.
- Cover active completion during rotation and expiry without extending arbitrary job authorization.

**Acceptance criteria**

- During the bounded overlap both approved credentials work; after expiry the previous credential receives the existing unauthorized response.
- An active worker can complete only its valid lease and cannot cross worker/job ownership during rotation.
- Unknown credentials and expired overlap fail closed, and token material never enters logs or public capability responses.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/submissions/test_submissions.py
- uv run --project services/api --frozen pytest services/judge/tests/control/test_worker.py

**Out of scope**

- Rotating real deployment credentials in this issue without operator authorization
- Building a PKI
- Unbounded multi-token allowlists

**Risk and review**

A permissive grace window can preserve a compromised key; require operator-controlled expiry and revoke procedure.

</details>

<a id="sai-b011"></a>
<details>
<summary>12. SAI-B011: Introduce an explicit trusted-ingress identity throttle policy [pending]</summary>

**Priority:** P1 · **Phase:** 1-safe-pilot · **Area:** identity.

**Suggested role:** identity/platform engineer.

**Prerequisites:** [SAI-B003](#sai-b003), [SAI-B006](#sai-b006), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Local auth deliberately uses shared per-path buckets because no trusted ingress is configured. This prevents spoofed forwarding bypasses but is not suitable as a complete public per-client abuse policy.

**Target paths / responsibility**

- `apps/web/features/accounts/server.ts`
- `apps/web/tests/auth.test.mjs`
- `compose.yaml`
- `docs/onboarding/DEVELOPMENT.md`

**Implementation scope**

- Add a disabled-by-default trusted-proxy/header configuration tied to an explicit ingress deployment contract.
- Retain the current safe shared-bucket fallback for direct local access and reject ambiguous forwarding configurations.
- Exercise the same Better Auth sign-in/sign-up rules through trusted and untrusted request fixtures.

**Acceptance criteria**

- Spoofed X-Forwarded-For from an untrusted direct caller cannot obtain a new throttle identity.
- A request from the configured trusted ingress resolves only the reviewed client-address field and cannot append arbitrary hops.
- Independent legitimate clients do not all share the same public deployment throttle bucket, while local safe defaults remain unchanged.

**Validation required**

- node --test apps/web/tests/auth.test.mjs

**Out of scope**

- Assuming any forwarding header is trustworthy
- Changing password requirements
- Purchasing an ingress service

**Risk and review**

Trusting client-controlled IP headers weakens existing defenses; proxy provenance must be enforced, not inferred from a header name.

</details>

<a id="sai-b012"></a>
<details>
<summary>13. SAI-B012: Create a consistent private backup and restore procedure for both stores [pending]</summary>

**Priority:** P1 · **Phase:** 1-safe-pilot · **Area:** storage-operations.

**Suggested role:** storage/platform engineer.

**Prerequisites:** [SAI-B003](#sai-b003), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Local SQLite databases and the web signing/session secret must be preserved together, but no tested coordinated backup/restore procedure exists. Copying live WAL files casually can produce an unusable or inconsistent recovery.

**Target paths / responsibility**

- `apps/web/features/accounts/server.ts`
- `services/api/solver_api/features/submissions/store.py`
- `scripts/development`
- `docs/onboarding/DEVELOPMENT.md`
- `compose.yaml`

**Implementation scope**

- Implement a trusted operator helper using supported SQLite backup/quiescence semantics for auth and submissions plus required private key material.
- Write a manifest of revision/schema and checksums in a private archive outside Git, with restrictive modes and explicit destination handling.
- Document restore into a fresh temporary workspace and the policy for queued/in-flight work; require confirmation before replacing real state.

**Acceptance criteria**

- A temporary fixture backup restores account login/session-key consistency and owned submission history without copying unrelated files.
- A partial/corrupted/missing-key backup is rejected before overwriting destination state.
- Backup files are private, no credential values print, and generated archives remain excluded from Git and application packaging.

**Validation required**

- Run the new backup/restore helper only against temporary fixture databases and a fresh temporary destination.
- node --test apps/web/tests/auth.test.mjs
- uv run --project services/api --frozen pytest services/api/tests/submissions/test_submissions.py

**Out of scope**

- Backing up production data without operator authorization
- Choosing a paid backup vendor
- Claiming encryption-at-rest solely from chmod

**Risk and review**

Backups contain credentials and source; accidental publication or destructive restore is a high-impact failure.

</details>

<a id="sai-b013"></a>
<details>
<summary>14. SAI-B013: Introduce versioned transactional migrations for the submission database [pending]</summary>

**Priority:** P1 · **Phase:** 1-safe-pilot · **Area:** storage.

**Suggested role:** backend storage engineer.

**Prerequisites:** [SAI-B012](#sai-b012), [SAI-B001](#sai-b001).

**Problem / missing behavior**

The submission store initializes tables with CREATE IF NOT EXISTS but has no recorded schema version or tested forward migration path. Retention, provenance and deletion changes need safe evolution of existing user data.

**Target paths / responsibility**

- `services/api/solver_api/features/submissions/store.py`
- `services/api/tests/submissions/test_submissions.py`
- `scripts/development`
- `docs/onboarding/DEVELOPMENT.md`

**Implementation scope**

- Add a small schema-version registry and ordered transactional migrations for the existing SQLite store.
- Represent the current schema as the supported baseline and fail safely on unknown newer versions.
- Provide operator preflight/backup guidance and a failure rollback strategy without editing Better Auth-owned schema.

**Acceptance criteria**

- A fixture built with the current schema upgrades without losing IDs, ownership, source, idempotency or lease semantics.
- A failing migration leaves the prior valid schema/data intact; repeat startup does not reapply an already completed migration.
- A database with a future unknown schema is refused with a safe diagnostic instead of silently modified.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/submissions/test_submissions.py

**Out of scope**

- Migrating to PostgreSQL
- Writing custom migrations for Better Auth internal tables
- Running destructive downgrade on real data

**Risk and review**

Schema mistakes can corrupt private history; require backup and real old-schema fixtures, not only fresh-database tests.

</details>

<a id="sai-b014"></a>
<details>
<summary>15. SAI-B014: Add a testable email-verification delivery flow for pilot accounts [pending]</summary>

**Priority:** P1 · **Phase:** 1-safe-pilot · **Area:** identity.

**Suggested role:** identity engineer.

**Prerequisites:** [SAI-B003](#sai-b003), [SAI-B011](#sai-b011), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Local email/password accounts do not verify email ownership. A real-user pilot needs a deliberate verification policy before relying on an email address for identity or recovery.

**Target paths / responsibility**

- `apps/web/features/accounts/server.ts`
- `apps/web/features/accounts/account-form.tsx`
- `apps/web/tests/auth.test.mjs`
- `tests/e2e/submissions/submissions.spec.ts`
- `docs/onboarding/DEVELOPMENT.md`

**Implementation scope**

- Use Better Auth supported verification hooks with a delivery adapter and local deterministic outbox fixture.
- Implement pending, resend, expired-link and verified UI states without confirming whether arbitrary addresses are registered.
- Keep delivery disabled or local-only until the owner supplies an approved provider/configuration; no paid call by default.

**Acceptance criteria**

- A fresh token verifies only its intended address once; expired/reused/mismatched tokens fail safely.
- Resend is bounded and response wording does not enumerate accounts.
- Verified-email requirements follow the approved pilot policy and do not silently lock out existing local development users.

**Validation required**

- node --test apps/web/tests/auth.test.mjs
- PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e -- tests/e2e/submissions/submissions.spec.ts --workers=2

**Out of scope**

- Selecting or purchasing a mail provider without approval
- Implementing custom email-token cryptography
- Sending real verification messages during tests

**Risk and review**

Mail links and logs can leak account tokens; use fixture delivery and library-supported semantics.

</details>

<a id="sai-b015"></a>
<details>
<summary>16. SAI-B015: Implement password recovery with bounded single-use reset links [pending]</summary>

**Priority:** P1 · **Phase:** 1-safe-pilot · **Area:** identity.

**Suggested role:** identity engineer.

**Prerequisites:** [SAI-B014](#sai-b014), [SAI-B001](#sai-b001).

**Problem / missing behavior**

There is no delivered account recovery flow. Users who lose a password cannot safely recover a pilot account through the current interface.

**Target paths / responsibility**

- `apps/web/features/accounts/server.ts`
- `apps/web/features/accounts/account-form.tsx`
- `apps/web/tests/auth.test.mjs`
- `tests/e2e/submissions/submissions.spec.ts`

**Implementation scope**

- Use supported Better Auth reset hooks and the verified delivery abstraction from B014.
- Add request/reset views with neutral account-existence wording, resend limits and explicit expired-link behavior.
- Apply the approved session invalidation policy on reset and disclose the existing short-lived API-token window unless separately changed.

**Acceptance criteria**

- A valid reset link changes the intended account password once; used/expired links cannot be replayed.
- Reset requests for absent/present addresses have indistinguishable public response structure.
- The old password fails after reset; session behavior matches the documented policy, and no reset token is logged or persisted in browser storage.

**Validation required**

- node --test apps/web/tests/auth.test.mjs
- PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e -- tests/e2e/submissions/submissions.spec.ts --workers=2

**Out of scope**

- Custom password/token cryptography
- Guaranteeing immediate revocation of already issued stateless API JWTs without an explicit design
- Real email delivery in CI

**Risk and review**

Enumeration and reset-link leakage can turn recovery into account takeover; use official library flows and adversarial fixtures.

</details>

<a id="sai-b016"></a>
<details>
<summary>17. SAI-B016: Expose owned session listing and revoke-other-sessions controls [pending]</summary>

**Priority:** P2 · **Phase:** 1-safe-pilot · **Area:** identity.

**Suggested role:** identity/frontend engineer.

**Prerequisites:** [SAI-B015](#sai-b015), [SAI-B001](#sai-b001).

**Problem / missing behavior**

The account page provides sign-out but no way to inspect or revoke other active sessions. Users cannot react deliberately to an unfamiliar session after an access concern.

**Target paths / responsibility**

- `apps/web/features/accounts/server.ts`
- `apps/web/features/accounts/account-form.tsx`
- `apps/web/features/accounts/client.ts`
- `apps/web/tests/auth.test.mjs`
- `tests/e2e/submissions/submissions.spec.ts`

**Implementation scope**

- Use Better Auth supported session listing/revocation APIs and render a bounded owner-only session list.
- Require recent authentication for revoke-other-sessions and identify the current session without revealing raw session tokens.
- Show the documented limit that previously issued short-lived API tokens may remain usable for their remaining lifetime.

**Acceptance criteria**

- Account A cannot list or revoke Account B sessions by supplying another identifier.
- Revoking another session makes that cookie fail while the chosen current session remains usable.
- Session token values never appear in DOM, API snapshots, logs or exports, and stale list responses are cleared on account change.

**Validation required**

- node --test apps/web/tests/auth.test.mjs
- PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e -- tests/e2e/submissions/submissions.spec.ts --workers=2

**Out of scope**

- Fingerprint-based identity or precise location tracking
- Changing JWT revocation architecture
- Automatically rotating real credentials

**Risk and review**

Session metadata is sensitive, and stale browser state must not cross identities.

</details>

<a id="sai-b017"></a>
<details>
<summary>18. SAI-B017: Record privacy-safe account security events [pending]</summary>

**Priority:** P2 · **Phase:** 1-safe-pilot · **Area:** identity-observability.

**Suggested role:** identity engineer and privacy reviewer.

**Prerequisites:** [SAI-B003](#sai-b003), [SAI-B016](#sai-b016), [SAI-B001](#sai-b001).

**Problem / missing behavior**

The project has no owner-facing security activity history for password recovery, session revocation or account administration. Operators and users need limited evidence without storing credentials or excessive personal data.

**Target paths / responsibility**

- `apps/web/features/accounts/server.ts`
- `apps/web/features/accounts/account-form.tsx`
- `apps/web/tests/auth.test.mjs`
- `docs/governance/DATA_AND_LICENSES.md`

**Implementation scope**

- Define a small versioned security-event vocabulary and retention policy for completed recovery/session actions.
- Record only approved metadata and expose a bounded owner-only activity list through supported account hooks.
- Avoid raw token, password, mail-link, full IP or user-agent logging unless separately justified and approved.

**Acceptance criteria**

- Fixtures produce exactly the intended event for reset/revocation success and distinguish failure without storing secret input.
- A second user cannot query another account activity, and pagination/retention bounds are enforced.
- The privacy document names stored fields and retention; event ingestion cannot be used for arbitrary log injection.

**Validation required**

- node --test apps/web/tests/auth.test.mjs

**Out of scope**

- A general SIEM or analytics platform
- Indefinite IP/device tracking
- Claiming activity logs identify an attacker

**Risk and review**

Additional audit data creates privacy and storage obligations; collect the smallest useful record.

</details>

<a id="sai-b018"></a>
<details>
<summary>19. SAI-B018: Implement deliberate account deletion across auth and owned submission state [pending]</summary>

**Priority:** P1 · **Phase:** 1-safe-pilot · **Area:** privacy.

**Suggested role:** backend/identity engineer and privacy reviewer.

**Prerequisites:** [SAI-B003](#sai-b003), [SAI-B016](#sai-b016), [SAI-B013](#sai-b013), [SAI-B001](#sai-b001).

**Problem / missing behavior**

There is no end-to-end account deletion lifecycle. Removing only an auth row would strand private source/history, while deleting active work without coordination could break worker leases.

**Target paths / responsibility**

- `apps/web/features/accounts/server.ts`
- `apps/web/features/accounts/account-form.tsx`
- `services/api/solver_api/features/submissions/store.py`
- `services/api/solver_api/main.py`
- `services/api/tests/submissions/test_submissions.py`
- `apps/web/tests/auth.test.mjs`

**Implementation scope**

- Implement an explicitly confirmed, recently authenticated account deletion flow using supported identity hooks and owner-scoped API cleanup.
- Apply the approved in-flight-job, retention and backup policy; refuse or defer unsafe active deletion rather than orphaning work.
- Make retries idempotent and explain what is removed immediately versus retained temporarily by policy.

**Acceptance criteria**

- The requester cannot target a different account; forged identity, stale reauthentication and CSRF attempts fail.
- Deleting an eligible account removes or irreversibly anonymizes its approved live data classes without affecting another owner.
- Interrupted/retried deletion converges to one documented terminal state; active jobs follow the stated safe policy and credentials are invalidated as supported.

**Validation required**

- node --test apps/web/tests/auth.test.mjs
- uv run --project services/api --frozen pytest services/api/tests/submissions/test_submissions.py

**Out of scope**

- Deleting live user data during development validation
- Promising instant erasure from historical backups without policy support
- Bypassing Better Auth mutation hooks

**Risk and review**

Deletion is destructive and spans two stores; fixtures and failure recovery must prove ownership and partial-completion behavior.

</details>

<a id="sai-b019"></a>
<details>
<summary>20. SAI-B019: Bound general API admission and concurrent slow requests [pending]</summary>

**Priority:** P1 · **Phase:** 1-safe-pilot · **Area:** ingress-security.

**Suggested role:** API/platform engineer.

**Prerequisites:** [SAI-B003](#sai-b003), [SAI-B006](#sai-b006), [SAI-B001](#sai-b001).

**Problem / missing behavior**

The current 128 KiB body and per-operation deadline do not bound simultaneous callers or whole-process request admission. Submission quotas alone cannot prevent general ingress exhaustion.

**Target paths / responsibility**

- `services/api/solver_api/main.py`
- `services/api/solver_api/http/body_limit.py`
- `services/api/tests/catalog/test_api.py`
- `compose.yaml`
- `docs/security/JUDGE_SECURITY.md`

**Implementation scope**

- Add a configurable bounded admission/concurrency policy appropriate to the existing single-process pilot, with clear limitations for multiple replicas.
- Ensure slow bodies and slow auth requests release capacity on cancellation/timeouts.
- Use safe overload responses and explicit retry information; preserve separate internal-worker capacity or a documented isolation policy.

**Acceptance criteria**

- A deterministic concurrent-request fixture reaches the configured cap and receives bounded overload responses rather than unbounded work.
- Cancelled and timed-out requests release permits; the next legitimate request succeeds.
- Worker control traffic cannot be starved indefinitely by public catalog requests, and overload output includes no request body or credential.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/catalog/test_api.py services/api/tests/identity/test_auth.py

**Out of scope**

- A distributed DDoS service
- Changing sandbox limits
- Using caller-supplied identities as trusted rate-limit keys

**Risk and review**

An in-process cap is not a global multi-replica budget; document deployment scope and avoid self-deadlock on internal work.

</details>

<a id="sai-b020"></a>
<details>
<summary>21. SAI-B020: Add structured redacted request and failure logs [pending]</summary>

**Priority:** P1 · **Phase:** 1-safe-pilot · **Area:** operations.

**Suggested role:** platform engineer.

**Prerequisites:** [SAI-B003](#sai-b003), [SAI-B019](#sai-b019), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Request IDs and safe client errors exist, but there is no defined structured operational logging contract. Troubleshooting needs correlation and failure categories without exposing source, tokens or hidden cases.

**Target paths / responsibility**

- `services/api/solver_api/main.py`
- `services/api/solver_api/http/errors.py`
- `services/judge/solver_judge/control/worker.py`
- `docs/onboarding/DEVELOPMENT.md`

**Implementation scope**

- Define structured request/failure fields such as service, generated correlation ID, route template, duration and safe error category.
- Redact or exclude authorization/cookies, raw query values, source, grading inputs, provider context and account identifiers beyond approved pseudonymous correlation.
- Document output format and retention/collection assumptions without provisioning a paid logging service.

**Acceptance criteria**

- Fixtures containing marker secrets in headers/body/query produce no marker in log output or exception formatting.
- A failed request can be correlated with its safe response request ID and route template.
- Untrusted multiline input cannot forge a second log record; logging failure does not change a valid API result.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/catalog/test_api.py services/api/tests/submissions/test_submissions.py
- uv run --project services/api --frozen pytest services/judge/tests/control/test_worker.py

**Out of scope**

- Persisting all request/response bodies
- Installing a telemetry cluster
- Publishing private source or security diagnostics

**Risk and review**

Logs are another data export channel; redaction must be tested before deployment collection is enabled.

</details>

<a id="sai-b021"></a>
<details>
<summary>22. SAI-B021: Expose private bounded operational readiness and queue metrics [pending]</summary>

**Priority:** P2 · **Phase:** 1-safe-pilot · **Area:** operations.

**Suggested role:** platform/backend engineer.

**Prerequisites:** [SAI-B020](#sai-b020), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Public health only reports process liveness and capabilities report recent worker readiness. Operators lack a private bounded view of queue age, expired leases and storage pressure without inspecting user records.

**Target paths / responsibility**

- `services/api/solver_api/main.py`
- `services/api/solver_api/features/submissions/store.py`
- `services/api/tests/submissions/test_submissions.py`
- `services/judge/solver_judge/control/diagnostics.py`

**Implementation scope**

- Add an operator-only metrics/readiness surface that reuses trusted store state and does not return source, tests, bearer material or high-cardinality identifiers.
- Separate liveness, deployment readiness and worker execution availability so a missing optional local judge is not mislabeled an API crash.
- Document scrape/authentication and metric cardinality bounds; keep public responses minimal.

**Acceptance criteria**

- Anonymous/learner credentials cannot read private operational metrics.
- Seeded queued/running/expired fixtures yield exact aggregate counts and oldest-job age, with no source or user IDs.
- Metrics collection remains bounded and unavailable storage produces a safe readiness failure rather than a false healthy state.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/submissions/test_submissions.py services/api/tests/catalog/test_api.py

**Out of scope**

- A public admin dashboard
- Accurate aggregate sandbox peak-memory claims
- Installing Prometheus or paid monitoring by default

**Risk and review**

Operator endpoints can expose sensitive topology and state; require a separate credential/policy and low-cardinality output.

</details>

<a id="sai-b022"></a>
<details>
<summary>23. SAI-B022: Apply retention to terminal submission source with a dry-run purge [pending]</summary>

**Priority:** P1 · **Phase:** 1-safe-pilot · **Area:** privacy-storage.

**Suggested role:** backend engineer and privacy reviewer.

**Prerequisites:** [SAI-B003](#sai-b003), [SAI-B013](#sai-b013), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Terminal private source/history grows indefinitely. The store has no approved source retention lifecycle, even when account/request quotas are respected.

**Target paths / responsibility**

- `services/api/solver_api/features/submissions/store.py`
- `services/api/tests/submissions/test_submissions.py`
- `scripts/development`
- `docs/governance/DATA_AND_LICENSES.md`

**Implementation scope**

- Implement the owner-approved source/summary retention policy for terminal records with an explicit dry-run report and bounded batches.
- Preserve active jobs and any data classes the approved policy must retain; define idempotency behavior for purged source.
- Run purge only through an authorized operator path or scheduled process with safe counts and no source output.

**Acceptance criteria**

- Boundary-time fixtures purge only eligible terminal data and retain queued/running/other-owner records as specified.
- Dry-run performs no writes and reports only aggregate counts/bytes; repeat purge is idempotent.
- Detail/history endpoints handle a retained summary with expired source honestly instead of reconstructing or leaking content.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/submissions/test_submissions.py
- Exercise the purge dry-run and apply paths only on temporary fixture databases.

**Out of scope**

- Deleting real developer/user history during validation
- Choosing retention periods without B003
- Changing hidden grading data lifecycle

**Risk and review**

Retention is deliberate destruction; ensure policy, exclusions and backup behavior are explicit before enabling scheduled writes.

</details>

<a id="sai-b023"></a>
<details>
<summary>24. SAI-B023: Enforce cumulative owned-source storage budgets at submission admission [pending]</summary>

**Priority:** P1 · **Phase:** 1-safe-pilot · **Area:** storage-abuse.

**Suggested role:** backend storage engineer.

**Prerequisites:** [SAI-B003](#sai-b003), [SAI-B013](#sai-b013), [SAI-B022](#sai-b022), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Per-source size and request/concurrency quotas do not bound cumulative stored source. A valid account can accumulate completed submissions until the shared disk is exhausted.

**Target paths / responsibility**

- `services/api/solver_api/features/submissions/store.py`
- `services/api/tests/submissions/test_submissions.py`
- `services/api/solver_api/main.py`

**Implementation scope**

- Track or compute bounded per-owner retained-source usage transactionally and apply configured byte/record ceilings when accepting new submissions.
- Keep idempotent replay of an existing request stable and exclude already purged bytes consistently.
- Return an actionable safe quota error without revealing another account usage.

**Acceptance criteria**

- Concurrent writes near the limit cannot exceed the configured budget by racing.
- An idempotency-key replay returns the original record without double-charging usage; a conflicting replay retains its existing rejection.
- After eligible retention frees bytes, a new request can be accepted, and another owner budget is unaffected.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/submissions/test_submissions.py

**Out of scope**

- Paid storage plans
- A global filesystem quota implementation
- Weakening existing queue limits

**Risk and review**

Accounting races can bypass budgets or reject valid replay; enforce charging in the same transaction as creation.

</details>

<a id="sai-b024"></a>
<details>
<summary>25. SAI-B024: Avoid loading private source for submission summary pages [pending]</summary>

**Priority:** P2 · **Phase:** 2-useful-practice · **Area:** storage-performance.

**Suggested role:** backend engineer.

**Prerequisites:** [SAI-B013](#sai-b013), [SAI-B001](#sai-b001).

**Problem / missing behavior**

History listing uses SELECT * and constructs full details before discarding source. Large retained programs are unnecessarily read and materialized for summary-only pagination.

**Target paths / responsibility**

- `services/api/solver_api/features/submissions/store.py`
- `services/api/tests/submissions/test_submissions.py`

**Implementation scope**

- Select explicit summary columns in the list query and map summaries without building SubmissionDetail.
- Retain stable created_at/id ordering, owner filtering, total count and expiry semantics.
- Add a regression fixture with large source to distinguish summary projection from detail retrieval.

**Acceptance criteria**

- History responses are byte-for-byte contract-compatible and never include source_code.
- An instrumented query/row fixture shows list mapping does not request/read the source_code column, while owned detail still returns it.
- Pagination ties, empty pages and cross-owner access retain existing behavior.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/submissions/test_submissions.py

**Out of scope**

- A database rewrite or ORM migration
- Speculative caching layers
- Removing owned detail access

**Risk and review**

Summary optimization must not bypass expiry/ownership checks or change deterministic pagination.

</details>

<a id="sai-b025"></a>
<details>
<summary>26. SAI-B025: Export an authenticated user-owned submission history bundle [pending]</summary>

**Priority:** P2 · **Phase:** 2-useful-practice · **Area:** privacy-product.

**Suggested role:** backend/frontend engineer.

**Prerequisites:** [SAI-B003](#sai-b003), [SAI-B022](#sai-b022), [SAI-B024](#sai-b024), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Users can inspect individual owned attempts but cannot take a bounded portable export of their history. An export must honor retention and avoid becoming a cross-user or bulk-memory leak.

**Target paths / responsibility**

- `services/api/solver_api/main.py`
- `services/api/solver_api/features/submissions/store.py`
- `apps/web/features/submissions/api.ts`
- `apps/web/features/submissions/submission-history.tsx`
- `services/api/tests/submissions/test_submissions.py`

**Implementation scope**

- Define a versioned owner export schema with attempts and optional retained source; use bounded batches and an explicit maximum/export continuation policy.
- Add an authenticated download action and make expired-source omissions explicit.
- Exclude tokens, internal worker IDs/leases, private grading cases and raw auth database content.

**Acceptance criteria**

- Account A export contains only A records, even with supplied IDs or concurrent account changes.
- A dataset exceeding the batch size exports completely through the documented bounded mechanism without materializing arbitrary history in one response.
- Exported metadata identifies schema/time and omitted expired source; files contain no credentials or private test fields.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/submissions/test_submissions.py
- PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e -- tests/e2e/submissions/submissions.spec.ts --workers=2

**Out of scope**

- Exporting all users or auth secrets
- Cloud storage uploads
- An implicit backup/training-consent grant

**Risk and review**

Exports are private source artifacts; owner authorization, response limits and cache/download handling need explicit tests.

</details>

<a id="sai-b026"></a>
<details>
<summary>27. SAI-B026: Extend problem provenance with explicit permitted-use metadata [pending]</summary>

**Priority:** P1 · **Phase:** 2-useful-practice · **Area:** content.

**Suggested role:** content engineer and rights reviewer.

**Prerequisites:** [SAI-B002](#sai-b002), [SAI-B003](#sai-b003), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Problem provenance currently records only author/source text. More content needs a machine-readable distinction between original authorship, permission, redistribution and training rights.

**Target paths / responsibility**

- `services/api/solver_api/features/catalog/models.py`
- `services/api/solver_api/features/catalog/content.py`
- `apps/web/features/practice/api.ts`
- `apps/web/features/practice/workspace.tsx`
- `services/api/tests/catalog/test_api.py`

**Implementation scope**

- Define a bounded public provenance schema with stable content identity, author attribution and approved permitted-use fields; keep private evidence references out of public responses.
- Populate truthful metadata for the three original seed exercises without importing third-party banks.
- Render concise attribution/rights information and validate it in the typed browser contract.

**Acceptance criteria**

- Every current seed validates with explicit provenance; unknown/unapproved reuse states cannot silently become approved.
- Public responses expose no private license documents or contributor personal contact data.
- Malformed/oversized metadata is rejected and existing problem rendering/tests remain contract-compatible through an intentional schema change.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/catalog/test_api.py
- PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e -- tests/e2e/practice/practice.spec.ts --workers=2

**Out of scope**

- Approving archived datasets
- Inventing legal permission for public websites
- Training any model

**Risk and review**

Rights metadata is a recorded authorization, not automatic legal clearance; owner/content review is required.

</details>

<a id="sai-b027"></a>
<details>
<summary>28. SAI-B027: Version problem and grader identity on every new submission [pending]</summary>

**Priority:** P1 · **Phase:** 2-useful-practice · **Area:** content-contract.

**Suggested role:** backend/content engineer.

**Prerequisites:** [SAI-B013](#sai-b013), [SAI-B026](#sai-b026), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Submissions retain problem slug/title but not an immutable public specification and grading revision. Future content changes could make an old verdict appear to refer to a different problem/test contract.

**Target paths / responsibility**

- `services/api/solver_api/features/catalog/models.py`
- `services/api/solver_api/features/catalog/content.py`
- `services/api/solver_api/features/submissions/store.py`
- `services/judge/solver_judge/grading/cases.py`
- `services/api/tests/submissions/test_submissions.py`

**Implementation scope**

- Introduce explicit problem revision and grader-manifest identity at creation/lease time without exposing private cases.
- Persist these identities in new submissions via a tested migration and define how legacy records are labeled unknown/legacy.
- Require the worker to reject unsupported revision combinations safely rather than grade with the nearest current slug.

**Acceptance criteria**

- Changing current problem content does not relabel the revision recorded on an existing attempt.
- A worker cannot complete an unsupported revision as AC; the job receives a safe explicit system outcome.
- Owned history/detail and exports show revision metadata, while private grading content remains outside public API/model context.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/submissions/test_submissions.py services/api/tests/catalog/test_api.py
- uv run --project services/api --frozen pytest services/judge/tests/grading/test_cases.py services/judge/tests/control/test_worker.py

**Out of scope**

- Building a full contest/version administration platform
- Returning hidden test data or expected answers
- Rejudging historical submissions automatically

**Risk and review**

Revision mismatches can silently invalidate verdicts; worker/API identity must be checked before execution and preserved in records.

</details>

<a id="sai-b028"></a>
<details>
<summary>29. SAI-B028: Detect public-sample drift between catalog and judge deployments [pending]</summary>

**Priority:** P1 · **Phase:** 2-useful-practice · **Area:** content-quality.

**Suggested role:** content/backend engineer.

**Prerequisites:** [SAI-B027](#sai-b027), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Public samples are represented across independent API/judge deployments. Current examples can drift so Run samples checks a different input/output from the problem page.

**Target paths / responsibility**

- `services/api/solver_api/features/catalog/content.py`
- `services/judge/solver_judge/grading/cases.py`
- `services/api/tests/catalog/test_api.py`
- `services/judge/tests/grading/test_cases.py`
- `scripts/verification`

**Implementation scope**

- Add a deterministic public-only sample manifest or cross-component contract fixture keyed by problem revision.
- Compare exact sample inputs/outputs and supported language starter interfaces without coupling API imports to private judge test data.
- Document how an author updates both deployments and how mismatch blocks release.

**Acceptance criteria**

- All three current problems have identical public sample contracts across API and judge.
- Changing one sample fixture on either side causes a targeted consistency failure with problem/revision identification.
- The shared/public fixture contains no generated private grading cases or oracle answers beyond public samples.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/catalog/test_api.py services/judge/tests/grading/test_cases.py

**Out of scope**

- Merging trusted private grading data into the API package
- Executing arbitrary author code on the API host
- A full data-ingestion pipeline

**Risk and review**

A shared manifest must not accidentally package private tests into web/API artifacts.

</details>

<a id="sai-b029"></a>
<details>
<summary>30. SAI-B029: Validate trusted problem authoring inputs before catalog publication [pending]</summary>

**Priority:** P2 · **Phase:** 2-useful-practice · **Area:** content-tooling.

**Suggested role:** content tooling engineer.

**Prerequisites:** [SAI-B026](#sai-b026), [SAI-B027](#sai-b027), [SAI-B028](#sai-b028), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Catalog exercises are hand-authored in Python source. Adding content lacks a focused author preflight for duplicate IDs/slugs, incomplete constraints, bad samples, missing provenance or revision mismatch.

**Target paths / responsibility**

- `scripts/verification`
- `services/api/solver_api/features/catalog/models.py`
- `services/api/solver_api/features/catalog/content.py`
- `services/judge/solver_judge/grading/cases.py`
- `docs/onboarding/DEVELOPMENT.md`

**Implementation scope**

- Create an offline trusted-author validation command for the existing content format or a deliberately small versioned input format.
- Check identifier uniqueness, required statements/formats/constraints, sample shape, starter languages, hint levels, provenance and public/grader revision linkage.
- Report path/field errors without executing arbitrary uploaded scripts or ingesting external archives.

**Acceptance criteria**

- The current seeds pass all documented checks, while fixtures for duplicate slug, missing rights, invalid sample and revision mismatch fail precisely.
- The command leaves input files unchanged and never imports a user-selected executable module.
- An author can follow one documented workflow to prepare a reviewed content PR with B001 evidence.

**Validation required**

- Run the new authoring command only on trusted committed seeds and intentionally invalid temporary data fixtures.
- uv run --project services/api --frozen pytest services/api/tests/catalog/test_api.py services/judge/tests/grading/test_cases.py

**Out of scope**

- Web-based public problem uploads
- Bulk competitor dataset ingestion
- A generic plugin execution system

**Risk and review**

An authoring validator must validate data rather than become an unrestricted code loader.

</details>

<a id="sai-b030"></a>
<details>
<summary>31. SAI-B030: Add one original prefix-sum range-query teaching exercise [pending]</summary>

**Priority:** P2 · **Phase:** 2-useful-practice · **Area:** content.

**Suggested role:** problem author and judge reviewer.

**Prerequisites:** [SAI-B029](#sai-b029), [SAI-B001](#sai-b001).

**Problem / missing behavior**

The three current seeds cover summation, contiguous growth and sliding windows. There is no original exercise teaching preprocessing with repeated range queries.

**Target paths / responsibility**

- `services/api/solver_api/features/catalog/content.py`
- `services/judge/solver_judge/grading/cases.py`
- `services/judge/tests/grading/test_cases.py`
- `services/judge/tests/sandbox/test_sandbox.py`
- `tests/e2e/practice/practice.spec.ts`

**Implementation scope**

- Author one original statement, constraints, two informative public samples, Python/C++17 starter code and three progressive authored hints.
- Add a small independent reference oracle and generated boundary cases for one-based/zero-based endpoints, full-range queries, negatives and 64-bit totals.
- Use the provenance, revision and authoring gates already introduced; keep expected private cases in the trusted judge.

**Acceptance criteria**

- A correct Python and C++17 solution receive AC on the authorized finite tests; off-by-one and repeated-linear-scan fixtures demonstrate the intended failure limits.
- Both public samples agree with the independent oracle and the rendered statement.
- The content has explicit original authorship and no copied third-party problem text; explanation states O(n+q) reasoning without a universal-correctness claim.

**Validation required**

- uv run --project services/api --frozen pytest services/judge/tests/grading/test_cases.py services/api/tests/catalog/test_api.py
- In a supported isolated runtime: npm run test:judge:integration
- PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e -- tests/e2e/practice/practice.spec.ts --workers=2

**Out of scope**

- Adding a bulk problem bank
- Changing language runtime support
- Claiming finite grading proves all-input correctness

**Risk and review**

Poor constraints/oracles can invalidate teaching and verdicts; require independent content review.

</details>

<a id="sai-b031"></a>
<details>
<summary>32. SAI-B031: Use bounded server-side pagination for the expanding problem catalog [pending]</summary>

**Priority:** P2 · **Phase:** 2-useful-practice · **Area:** catalog.

**Suggested role:** frontend/API engineer.

**Prerequisites:** [SAI-B029](#sai-b029), [SAI-B001](#sai-b001).

**Problem / missing behavior**

The UI currently fetches limit=100 once and filters that page locally. Once the catalog exceeds the first page, learners could miss matching problems while totals imply a larger searchable collection.

**Target paths / responsibility**

- `apps/web/features/practice/catalog.tsx`
- `apps/web/features/practice/api.ts`
- `services/api/solver_api/main.py`
- `services/api/tests/catalog/test_api.py`
- `tests/e2e/practice/practice.spec.ts`

**Implementation scope**

- Drive bounded q/difficulty/tag/limit/offset requests through the existing catalog API instead of pretending the first 100 entries are the whole library.
- Add deliberate pagination/loading/empty states, cancel stale searches and reset offset when filters change.
- Retain the simple existing API store and avoid adding search infrastructure.

**Acceptance criteria**

- A fixture with more than 100 problems finds a matching item beyond the original first page.
- Rapid filter changes cannot render stale results or retain an out-of-range offset.
- Displayed totals, page boundaries and empty results match API semantics; keyboard access and existing retry behavior remain usable.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/catalog/test_api.py
- PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e -- tests/e2e/practice/practice.spec.ts tests/e2e/practice/resilience.spec.ts --workers=2

**Out of scope**

- Meilisearch or a database migration
- Unbounded client fetching of the entire catalog
- Personalized recommendations

**Risk and review**

Stale network responses and partial-page filtering can create misleading results; retain strict schemas and cancellation.

</details>

<a id="sai-b032"></a>
<details>
<summary>33. SAI-B032: Make catalog filters and page position shareable through the URL [pending]</summary>

**Priority:** P2 · **Phase:** 2-useful-practice · **Area:** catalog-ux.

**Suggested role:** frontend engineer.

**Prerequisites:** [SAI-B031](#sai-b031), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Search, difficulty and topic exist only in component state. Refresh, browser navigation and shared links lose the chosen practice view.

**Target paths / responsibility**

- `apps/web/features/practice/catalog.tsx`
- `apps/web/app/page.tsx`
- `tests/e2e/practice/practice.spec.ts`

**Implementation scope**

- Map supported filter/page values to validated query parameters and restore them on initial navigation.
- Update browser history intentionally without placing sensitive data in the URL.
- Normalize unknown/overlong values and provide an accessible clear-filters action that resets the URL and pagination together.

**Acceptance criteria**

- A copied filtered URL restores the same API query and visible result set after reload.
- Back/forward navigation restores the previous valid filter state without duplicate stale fetches.
- Invalid or overlong parameters are normalized safely, and no source, token or account ID enters the URL.

**Validation required**

- PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e -- tests/e2e/practice/practice.spec.ts --workers=2

**Out of scope**

- Saving private learner profiles
- A new routing framework
- Analytics tracking parameters

**Risk and review**

URL state must be bounded and must not introduce navigation loops or expose private drafts.

</details>

<a id="sai-b033"></a>
<details>
<summary>34. SAI-B033: Add explicit local draft export and bounded import [pending]</summary>

**Priority:** P2 · **Phase:** 2-useful-practice · **Area:** editor.

**Suggested role:** frontend editor engineer.

**Prerequisites:** [SAI-B003](#sai-b003), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Drafts are best-effort browser storage and learners are told to copy their code, but there is no deliberate portable download/import path when storage fails or a browser is replaced.

**Target paths / responsibility**

- `apps/web/features/practice/code-pane.tsx`
- `apps/web/features/practice/workspace.tsx`
- `tests/e2e/practice/practice.spec.ts`

**Implementation scope**

- Add user-initiated source download with clear problem/language file naming.
- Add a bounded plain-text import flow with preview and explicit replace confirmation; do not execute or upload imported content.
- Preserve the current Monaco/simple-editor and storage-failure behavior.

**Acceptance criteria**

- Exported UTF-8 bytes match the selected draft exactly, including non-ASCII text and trailing newline.
- An oversized or unsupported import is rejected before changing the draft; cancel preserves the original bytes.
- Import/export work in the simple-editor fallback and cause no submission, model request or external network call.

**Validation required**

- PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e -- tests/e2e/practice/practice.spec.ts --workers=2

**Out of scope**

- Cloud draft sync
- Archive extraction in the browser
- Automatic code execution after import

**Risk and review**

Import is a destructive edit and export may contain private source; require explicit user intent and bounded text handling.

</details>

<a id="sai-b034"></a>
<details>
<summary>35. SAI-B034: Offer explicit draft ownership and clear-on-shared-device controls [pending]</summary>

**Priority:** P2 · **Phase:** 2-useful-practice · **Area:** editor-privacy.

**Suggested role:** frontend engineer and privacy reviewer.

**Prerequisites:** [SAI-B003](#sai-b003), [SAI-B033](#sai-b033), [SAI-B001](#sai-b001).

**Problem / missing behavior**

The current draft key is scoped by browser/problem/language, not by signed-in account. The disclosure is honest, but shared-device users have no deliberate account-scoping or local-clear workflow.

**Target paths / responsibility**

- `apps/web/features/practice/code-pane.tsx`
- `apps/web/features/accounts/account-form.tsx`
- `apps/web/features/practice/workspace.tsx`
- `tests/e2e/practice/practice.spec.ts`
- `tests/e2e/submissions/submissions.spec.ts`

**Implementation scope**

- Define separate guest and signed-in local namespaces without treating localStorage as encrypted account backup.
- Offer explicit export/keep/move choices for existing guest drafts and a bounded clear-local-drafts control.
- Never silently upload drafts or erase another browser identity on sign-out; explain shared-device behavior.

**Acceptance criteria**

- Switching A to B cannot silently display A private draft under B namespace.
- Existing v1 guest drafts remain recoverable until the user chooses migration or deletion; cancelled prompts preserve bytes.
- Clear-local-drafts affects only the selected namespace and explicit confirmation; no server source is deleted or uploaded.

**Validation required**

- PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e -- tests/e2e/practice/practice.spec.ts tests/e2e/submissions/submissions.spec.ts --workers=2

**Out of scope**

- Claiming browser storage is encrypted or secure against local device access
- Automatic cloud synchronization
- Silent deletion on logout

**Risk and review**

Local identity migration can lose code or cross account boundaries; migration must be reversible through explicit export.

</details>

<a id="sai-b035"></a>
<details>
<summary>36. SAI-B035: Detect cross-tab draft conflicts before overwriting newer code [pending]</summary>

**Priority:** P2 · **Phase:** 2-useful-practice · **Area:** editor-reliability.

**Suggested role:** frontend editor engineer.

**Prerequisites:** [SAI-B034](#sai-b034), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Two tabs editing the same local draft overwrite one storage key without revision metadata or a conflict warning. A stale tab can silently replace more recent code.

**Target paths / responsibility**

- `apps/web/features/practice/code-pane.tsx`
- `tests/e2e/practice/practice.spec.ts`

**Implementation scope**

- Record a small local draft revision/timestamp envelope with a migration path for plain v1 text.
- Observe storage events for the active namespace and show a non-destructive conflict choice when another tab changes the saved revision.
- Keep each unsaved in-memory value available for copying/export before choosing one version.

**Acceptance criteria**

- Two-tab fixtures trigger a conflict notice instead of silently overwriting a newer saved revision.
- Choosing keep-local, load-other or cancel has deterministic storage/editor outcomes and preserves an exportable losing version until explicit resolution.
- Different problem/language/account namespaces do not trigger conflicts, and storage-unavailable fallback still permits editing.

**Validation required**

- PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e -- tests/e2e/practice/practice.spec.ts --workers=2

**Out of scope**

- Real-time collaboration or CRDT infrastructure
- Server draft persistence
- Pretending timestamps provide distributed conflict-free correctness

**Risk and review**

Migration must not mistake existing source text for malformed metadata or discard unsaved code.

</details>

<a id="sai-b036"></a>
<details>
<summary>37. SAI-B036: Add persistent editor display and accessibility preferences [pending]</summary>

**Priority:** P3 · **Phase:** 2-useful-practice · **Area:** editor-ux.

**Suggested role:** frontend editor engineer.

**Prerequisites:** [SAI-B033](#sai-b033), [SAI-B001](#sai-b001).

**Problem / missing behavior**

The editor exposes basic mode/reset controls but no deliberate learner control over font size, wrapping or preferred simple-editor mode. These choices affect readability and keyboard accessibility.

**Target paths / responsibility**

- `apps/web/features/practice/code-pane.tsx`
- `apps/web/features/practice/workspace.tsx`
- `apps/web/app/globals.css`
- `tests/e2e/practice/practice.spec.ts`

**Implementation scope**

- Add a small bounded preference model for font size, wrapping and editor mode using local non-sensitive storage.
- Apply compatible behavior to Monaco and the simple editor, with a reset-to-default action.
- Keep preferences separate from source drafts and handle unavailable/malformed storage safely.

**Acceptance criteria**

- Preferences survive reload and apply consistently without changing source bytes or submission language.
- Out-of-range/malformed saved preferences fall back to supported defaults.
- Controls have accessible names, keyboard operation and usable focus; choosing simple mode does not repeatedly force Monaco back.

**Validation required**

- PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e -- tests/e2e/practice/practice.spec.ts --workers=2

**Out of scope**

- A full design-system replacement
- Cloud preference profiles
- Changing compiler/runtime settings

**Risk and review**

Preference initialization can race draft hydration; source must remain unchanged.

</details>

<a id="sai-b037"></a>
<details>
<summary>38. SAI-B037: Complete keyboard navigation for the practice and submission workflow [pending]</summary>

**Priority:** P1 · **Phase:** 2-useful-practice · **Area:** accessibility.

**Suggested role:** accessibility/frontend engineer.

**Prerequisites:** [SAI-B001](#sai-b001).

**Problem / missing behavior**

Basic keyboard support exists, but there is no complete documented keyboard-only path through navigation, problem reading, editor entry/exit, language selection, hints and deliberate submission.

**Target paths / responsibility**

- `apps/web/components/shell.tsx`
- `apps/web/features/practice/workspace.tsx`
- `apps/web/features/practice/code-pane.tsx`
- `apps/web/features/submissions/submission-panel.tsx`
- `tests/e2e/practice/practice.spec.ts`

**Implementation scope**

- Audit the existing flow with a keyboard and repair concrete focus-order, editor-escape and visible-focus gaps.
- Add a skip-to-main/editor guidance path without trapping Tab inside Monaco or inventing mandatory shortcuts.
- Document supported editor behavior and add focused browser assertions for repaired gaps.

**Acceptance criteria**

- A keyboard-only fixture reaches and operates catalog, problem, editor, language and Run/Submit controls without pointer input.
- Users can leave both Monaco and simple editor through a documented accessible mechanism; focus is never trapped.
- Disabled/loading/retry controls expose state and visible focus remains discernible in supported themes.

**Validation required**

- PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e -- tests/e2e/practice/practice.spec.ts tests/e2e/submissions/submissions.spec.ts --workers=2
- Record a manual keyboard pass for the exact changed workflow; do not claim full WCAG conformance.

**Out of scope**

- Replacing Monaco solely for aesthetics
- A full accessibility certification
- Changing judging or authentication rules

**Risk and review**

Automation cannot establish all editor assistive-technology behavior; include an actual manual pass and limitations.

</details>

<a id="sai-b038"></a>
<details>
<summary>39. SAI-B038: Improve screen-reader announcements and focus for asynchronous results [pending]</summary>

**Priority:** P1 · **Phase:** 2-useful-practice · **Area:** accessibility.

**Suggested role:** accessibility/frontend engineer.

**Prerequisites:** [SAI-B037](#sai-b037), [SAI-B001](#sai-b001).

**Problem / missing behavior**

The app uses role=status/alert in places, but there is no reviewed announcement/focus contract across account errors, hint retry, polled verdicts and opened history details. Repeated polling can be noisy or updates can be missed.

**Target paths / responsibility**

- `apps/web/features/accounts/account-form.tsx`
- `apps/web/features/hints/account-hint.tsx`
- `apps/web/features/submissions/submission-panel.tsx`
- `apps/web/features/submissions/submission-history.tsx`
- `tests/e2e/hints/hints.spec.ts`
- `tests/e2e/submissions/submissions.spec.ts`

**Implementation scope**

- Define concise live-region announcements for meaningful state changes, with stable labels and error associations.
- Preserve logical focus after retries, modal/confirmation actions and detail opening; avoid shifting focus on every poll.
- Add targeted assertions and a manual screen-reader walkthrough for repaired cases.

**Acceptance criteria**

- One transition to a final verdict announces once; unchanged polls do not repeat the same message indefinitely.
- Account field/error relationships and hint result provenance are programmatically exposed.
- After retry/detail close or account change, focus remains on a meaningful visible control and stale private result text is removed.

**Validation required**

- PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e -- tests/e2e/hints/hints.spec.ts tests/e2e/submissions/submissions.spec.ts --workers=2
- Record manual screen-reader/keyboard findings for the affected states, including the tool/version used.

**Out of scope**

- Synthesized voice tutoring
- Changing source provenance semantics
- Claiming automated checks replace assistive-technology review

**Risk and review**

Over-announcement and forced focus can make a technically labeled UI unusable; test real interaction timing.

</details>

<a id="sai-b039"></a>
<details>
<summary>40. SAI-B039: Repair contrast, reduced-motion and zoom reflow gaps [pending]</summary>

**Priority:** P2 · **Phase:** 2-useful-practice · **Area:** accessibility.

**Suggested role:** accessibility/UI engineer.

**Prerequisites:** [SAI-B037](#sai-b037), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Responsive styles exist, but the repository has no demonstrated review of text/control contrast, reduced-motion behavior and high-zoom reflow. Decorative motion and narrow result surfaces can block access.

**Target paths / responsibility**

- `apps/web/app/globals.css`
- `apps/web/components/shell.tsx`
- `apps/web/features/practice/catalog.tsx`
- `apps/web/features/practice/workspace.tsx`
- `tests/e2e/practice/practice.spec.ts`

**Implementation scope**

- Measure contrast of actual text/control/focus states and repair specific failures without redesigning the product.
- Respect prefers-reduced-motion for decorative animation and smooth scrolling.
- Check 200%/400% zoom and a narrow viewport for catalog, problem/editor controls and result text; preserve necessary code scrolling without page-wide loss of controls.

**Acceptance criteria**

- Changed text/control combinations meet the chosen documented WCAG AA contrast criterion with recorded measurements.
- Reduced-motion emulation removes nonessential animation while all controls remain usable.
- At reviewed zoom/viewports, content and actions are reachable with no clipped critical labels or horizontal page scrolling caused by layout controls.

**Validation required**

- PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e -- tests/e2e/practice/practice.spec.ts --workers=2
- Record manual contrast and zoom findings for changed states and limitations.

**Out of scope**

- A new brand/theme system
- Marketing a complete accessibility certification
- Reformatting user code to eliminate editor horizontal scrolling

**Risk and review**

Visual fixes can hide controls or alter editor sizing; preserve responsive behavior and clear focus states.

</details>

<a id="sai-b040"></a>
<details>
<summary>41. SAI-B040: Add a focused automated accessibility regression gate [pending]</summary>

**Priority:** P2 · **Phase:** 2-useful-practice · **Area:** accessibility-quality.

**Suggested role:** accessibility/test engineer.

**Prerequisites:** [SAI-B037](#sai-b037), [SAI-B038](#sai-b038), [SAI-B039](#sai-b039), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Accessibility repairs need a repeatable regression signal. Existing functional Playwright assertions do not provide a dedicated scan of representative guest, signed-in, loading, error and result states.

**Target paths / responsibility**

- `apps/web/package.json`
- `package-lock.json`
- `tests/e2e/practice/practice.spec.ts`
- `tests/e2e/submissions/submissions.spec.ts`
- `tests/e2e/hints/hints.spec.ts`
- `.github/workflows/ci.yml`
- `docs/onboarding/DEVELOPMENT.md`

**Implementation scope**

- Review and pin a browser accessibility scanner as a development-only dependency, retaining its license and lockfile integrity.
- Scan a small representative set of stable app states and fail on agreed actionable violations; keep explicit, justified exceptions narrow.
- Document which manual keyboard/screen-reader checks remain necessary and attach evidence to AI-authored PRs.

**Acceptance criteria**

- A deliberate missing-label or contrast fixture is detected by the new gate and a clean repaired state passes.
- The gate covers guest practice, account form, authored hint result and owned submission result without scanning private production data.
- Exceptions identify a specific rule/node, reason and owner rather than globally disabling categories; scan output does not claim full conformance.

**Validation required**

- Run the scoped Playwright accessibility cases added to the existing practice/hints/submissions suites.
- When CI execution is authorized, observe the dedicated accessibility job/step on the exact PR commit.

**Out of scope**

- Replacing manual accessibility review
- Adding a paid audit service by default
- Globally suppressing violations to obtain a green check

**Risk and review**

Scanner version changes and noisy exceptions can erode trust; pin the tool and review exceptions like code.

</details>

<a id="sai-b121"></a>
<details>
<summary>42. SAI-B121: Persist owned sandbox records and reconcile crash-orphaned containers [pending]</summary>

**Priority:** P0 · **Phase:** 1-safe-pilot · **Area:** judge-recovery.

**Suggested role:** Judge maintainer and recovery reviewer.

**Prerequisites:** [SAI-B003](#sai-b003), [SAI-B001](#sai-b001).

**Problem / missing behavior**

The corrected runner retains failed cleanup names in _active and stops readiness, but that set disappears if the worker process crashes. A restart cannot distinguish its leftover sandboxes from unrelated containers, and the existing incident exercise does not implement recovery authority.

**Target paths / responsibility**

- `services/judge/solver_judge/control/runner.py`
- `services/judge/solver_judge/control/diagnostics.py`
- `services/judge/tests/control/test_runner.py`
- `docs/security/JUDGE_SECURITY.md`
- `docs/onboarding/DEVELOPMENT.md`

**Implementation scope**

- Introduce a minimal private, atomically persisted sandbox-ownership journal written before container creation and cleared only after confirmed absence. Store generated container identity, approved image identity and lifecycle generation; never store source, test input, account identifiers or bearer material.
- Label newly created sandboxes with the same trusted ownership generation. On startup, perform one bounded reconciliation pass that validates both journal and actual container labels/image before removing an owned orphan.
- Treat malformed journal data, mismatched ownership, unreachable Docker and unresolved cleanup as unavailable readiness with sanitized diagnostics; preserve the record for an explicit operator retry.

**Acceptance criteria**

- A simulated crash after create and before normal cleanup leaves a recoverable record; a fresh runner instance removes only the matching owned sandbox before becoming ready.
- An unrelated container or a journal entry with a mismatched ownership label/image is never removed automatically and cannot grant readiness.
- Journal permissions, atomic replacement, bounded size and redacted failure output are exercised; duplicate reconciliation is safe and no host execution fallback exists.

**Validation required**

- uv run --project services/api --frozen pytest services/judge/tests/control/test_runner.py
- On an explicitly approved isolated gVisor test host, run a finite one-container crash/restart fixture and record cleanup plus unchanged unrelated-container identity.

**Out of scope**

- Sweeping every Docker container or deleting unknown state
- Persisting private program data or worker secrets
- A general distributed container orchestrator

**Risk and review**

Automatic orphan cleanup is destructive unless ownership is established independently of an untrusted filename or container name; refuse ambiguous recovery.

</details>

<a id="sai-b122"></a>
<details>
<summary>43. SAI-B122: Bind controller credentials to registered worker identities [pending]</summary>

**Priority:** P0 · **Phase:** 1-safe-pilot · **Area:** worker-auth.

**Suggested role:** Backend security engineer and judge maintainer.

**Prerequisites:** [SAI-B009](#sai-b009), [SAI-B010](#sai-b010), [SAI-B013](#sai-b013), [SAI-B001](#sai-b001).

**Problem / missing behavior**

require_worker currently authenticates one shared bearer, while heartbeat, lease and completion accept a caller-supplied worker_id. Any holder belongs to the entire controller trust domain and can register or impersonate another worker; token-strength and rotation tasks do not establish separate principals.

**Target paths / responsibility**

- `services/api/solver_api/main.py`
- `services/api/solver_api/features/submissions/store.py`
- `services/judge/solver_judge/control/worker.py`
- `services/api/tests/submissions/test_submissions.py`
- `services/judge/tests/control/test_worker.py`
- `docs/onboarding/DEVELOPMENT.md`

**Implementation scope**

- Resolve an authenticated controller credential to one owner-registered stable worker principal and bind every internal route payload to that principal rather than trusting worker_id alone.
- Retain a bounded per-principal current/previous credential overlap using the rotation mechanism from B010; provide an explicit single-worker development configuration rather than an implicit production shared-key fallback.
- Reject unknown identities and cross-principal heartbeat, lease and completion operations with closed safe errors; document credential provisioning and revocation without writing actual secrets into Git.

**Acceptance criteria**

- Two configured worker fixtures can operate only under their registered identities; the credential for A cannot register, renew, lease as or complete a lease belonging to B.
- Rotating or revoking A leaves B unaffected and preserves only the deliberately allowed bounded overlap for A.
- The normal configured single-worker local workflow remains supported, while production mode refuses an unbound shared credential; no secret appears in logs or capability output.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/submissions/test_submissions.py
- uv run --project services/api --frozen pytest services/judge/tests/control/test_worker.py

**Out of scope**

- Building a certificate authority or automatic worker registration service
- Rotating real deployment credentials without operator approval
- Treating per-worker identity as protection against a malicious trusted Docker host

**Risk and review**

An identity migration can lock out valid workers or accidentally widen completion rights; use explicit compatibility and cross-principal denial fixtures.

</details>

<a id="sai-b123"></a>
<details>
<summary>44. SAI-B123: Enforce an atomic active-lease allowance per worker principal [pending]</summary>

**Priority:** P0 · **Phase:** 1-safe-pilot · **Area:** judge-admission.

**Suggested role:** Backend queue engineer.

**Prerequisites:** [SAI-B122](#sai-b122), [SAI-B013](#sai-b013), [SAI-B001](#sai-b001).

**Problem / missing behavior**

The current worker implementation runs serially, but the API lease transaction has no check for an existing RUNNING lease belonging to the worker. Repeated or concurrent authenticated lease requests can reserve many jobs, so the client convention is not an enforceable execution allowance.

**Target paths / responsibility**

- `services/api/solver_api/features/submissions/store.py`
- `services/api/solver_api/main.py`
- `services/api/tests/submissions/test_submissions.py`
- `services/judge/solver_judge/control/worker.py`
- `services/judge/tests/control/test_worker.py`

**Implementation scope**

- Inside the existing atomic lease transaction, enforce a configured active-lease allowance for the authenticated worker principal; begin with the current one-job-per-worker contract.
- Return a documented busy/no-new-lease outcome without claiming another job, and release allowance only after the authoritative completion or expiry transition.
- Keep idempotent retry and cross-worker ownership semantics explicit; integrate with registered identities from B122 so inventing another worker_id cannot evade the allowance.

**Acceptance criteria**

- Two concurrent lease calls for the same principal cannot create more RUNNING jobs than its configured allowance.
- A busy worker does not consume another queued job; a second independently authorized worker can lease its own job.
- Completion and lease expiry each release exactly the intended allowance, while stale completion and forged identity do not release or consume another worker slot.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/submissions/test_submissions.py
- uv run --project services/api --frozen pytest services/judge/tests/control/test_worker.py

**Out of scope**

- Distributed host-capacity scheduling
- Changing learner submission quotas or provider budgets
- Assuming a lease count measures actual CPU or aggregate memory

**Risk and review**

A nontransactional count-and-lease check can race; a stranded lease must expire without allowing cross-worker or double completion.

</details>

<a id="sai-b125"></a>
<details>
<summary>45. SAI-B125: Gate production readiness on an approved supported runtime identity [pending]</summary>

**Priority:** P0 · **Phase:** 1-safe-pilot · **Area:** runtime-maintenance.

**Suggested role:** Judge operator, security reviewer and project owner.

**Prerequisites:** [SAI-B003](#sai-b003), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Preflight establishes that runsc exists, rootless Docker is selected and finite probes pass. It does not enforce a maintained approved runtime identity or support window. The historical review explicitly records an outdated installed runtime; B111 qualifies candidates later but does not establish this prerequisite policy.

**Target paths / responsibility**

- `services/judge/UPSTREAM_REVIEW.md`
- `services/judge/solver_judge/control/runner.py`
- `services/judge/solver_judge/control/diagnostics.py`
- `services/judge/tests/control/test_runner.py`
- `docs/security/JUDGE_SECURITY.md`
- `docs/onboarding/DEVELOPMENT.md`

**Implementation scope**

- Record an owner/operator-approved production runtime support policy: trusted deployment inventory source, approved runtime/image identities, review owner, review deadline and rollback identity.
- Require production startup/diagnostics to validate the current daemon runtime identity against that approved inventory. An unverifiable identity or expired review must prevent readiness rather than infer patch status from the word runsc.
- Keep operator deployment/update actions separate from application configuration. Feed the approved policy into the existing B111 canary qualification work instead of creating another upgrade rehearsal.

**Acceptance criteria**

- Fixtures for approved, unapproved, unverifiable and expired-review identities produce explicit safe readiness outcomes.
- Diagnostics distinguish declared identity, independently available runtime evidence and unknown provenance; hashing a local binary is not mislabeled proof of a remote daemon runtime.
- No host package is installed or runtime replaced by application startup, and documented development-only use of an older managed runtime cannot be described as production patched.

**Validation required**

- uv run --project services/api --frozen pytest services/judge/tests/control/test_runner.py
- Statically review the operator-approved runtime policy and inventory provenance; a real production approval cannot be invented by a coding agent.

**Out of scope**

- Automatic host runtime upgrades
- A second canary implementation duplicating B111
- Independent sandbox certification or guaranteed freedom from vulnerabilities

**Risk and review**

A self-asserted or stale inventory can create false confidence; policy approval and actual deployment evidence must have a named operator and expiry.

</details>

<a id="sai-b124"></a>
<details>
<summary>46. SAI-B124: Require a verified aggregate resource envelope for a production judge host [pending]</summary>

**Priority:** P0 · **Phase:** 1-safe-pilot · **Area:** judge-isolation.

**Suggested role:** Judge infrastructure engineer and security reviewer.

**Prerequisites:** [SAI-B003](#sai-b003), [SAI-B121](#sai-b121), [SAI-B123](#sai-b123), [SAI-B125](#sai-b125), [SAI-B001](#sai-b001).

**Problem / missing behavior**

The present managed rootless runtime lacks aggregate cgroup memory/PID accounting. Per-process rlimits and per-container tmpfs caps are real finite controls, but adding workers can exceed host-wide CPU, memory, process or temporary-storage budgets. B109 measures capacity; it does not enforce these limits.

**Target paths / responsibility**

- `services/judge/solver_judge/control/runner.py`
- `services/judge/solver_judge/control/diagnostics.py`
- `services/judge/tests/control/test_runner.py`
- `services/judge/tests/sandbox`
- `docs/security/JUDGE_SECURITY.md`
- `docs/onboarding/DEVELOPMENT.md`

**Implementation scope**

- Define one explicit operator-provisioned dedicated-host production resource envelope, including aggregate CPU, memory, PID, running-sandbox and temporary-storage ceilings; preserve the current bounded development mode as a clearly separate mode.
- Add production preflight that verifies supported aggregate controls and the selected host/cgroup assignment before advertising readiness. Pass only reviewed fixed resource arguments to Docker and retain existing per-process, no-network and output controls.
- Fail production readiness when accounting/enforcement cannot be verified or owned orphan usage exceeds the declared envelope. Do not install or reconfigure the managed daemon or claim that a CLI flag alone proves enforcement.

**Acceptance criteria**

- Mocked unsupported/missing/mismatched aggregate-control states refuse production readiness and cannot silently select the development policy.
- On an approved dedicated test host, finite original multi-process/concurrent sandbox fixtures demonstrate the declared aggregate caps and controlled recovery; report which resource dimensions were actually measured.
- The supported development configuration retains its explicit limitations, and no new accurate-MLE or sandbox-certification claim is made without trustworthy evidence.

**Validation required**

- uv run --project services/api --frozen pytest services/judge/tests/control/test_runner.py
- Run only the new explicitly enabled, finite aggregate-budget fixtures on an operator-approved dedicated gVisor host; mark them blocked rather than passed on the current unsupported managed runtime.

**Out of scope**

- Provisioning paid hosts or changing the cloud daemon automatically
- A multi-host scheduler or unlimited stress testing
- Claiming protection from --memory or --pids-limit when the daemon reports no enforcement

**Risk and review**

Resource flags can be ignored by unsupported runtimes; readiness must depend on observed controls, not desired configuration. Host provisioning remains an external operator prerequisite.

</details>

<a id="sai-b126"></a>
<details>
<summary>47. SAI-B126: Withdraw worker readiness and reconcile its current lease on retirement [pending]</summary>

**Priority:** P1 · **Phase:** 1-safe-pilot · **Area:** judge-lifecycle.

**Suggested role:** Backend queue engineer and judge maintainer.

**Prerequisites:** [SAI-B013](#sai-b013), [SAI-B121](#sai-b121), [SAI-B122](#sai-b122), [SAI-B123](#sai-b123), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Cleanup failure now stops further claims and heartbeat renewal, but the API can continue advertising the last worker heartbeat for 60 seconds. Process/transport failure also leaves lease retirement to expiry. There is no explicit generation-bound withdrawal protocol connecting shutdown, cleanup outcome and the authoritative lease state.

**Target paths / responsibility**

- `services/api/solver_api/features/submissions/store.py`
- `services/api/solver_api/main.py`
- `services/judge/solver_judge/control/worker.py`
- `services/judge/tests/control/test_worker.py`
- `services/api/tests/submissions/test_submissions.py`
- `docs/onboarding/DEVELOPMENT.md`

**Implementation scope**

- Add one authenticated principal-and-instance-bound retirement operation using a closed reason vocabulary. Atomically withdraw only that worker instance from availability and prevent further lease grants.
- Have graceful shutdown or revoked runtime readiness attempt this operation with a short fixed deadline while still preserving controlled in-flight completion and orphan records. A transport failure retains the existing expiry fallback.
- Specify an idempotent authoritative disposition for its current lease: retain an already committed terminal result; otherwise record only a safe SYSTEM_ERROR when retirement is authorized, and never auto-requeue code whose cleanup is unconfirmed.

**Acceptance criteria**

- Successful retirement removes the affected worker from capabilities immediately while other ready workers remain available.
- A late heartbeat/retirement from a previous process generation cannot revive or retire its registered replacement, and another worker principal cannot affect the lease.
- Shutdown versus completion races yield exactly one documented terminal state with no private diagnostics, no second execution and no hung shutdown; unavailable retirement transport falls back to the documented finite heartbeat/lease expiry behavior.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/submissions/test_submissions.py
- uv run --project services/api --frozen pytest services/judge/tests/control/test_worker.py

**Out of scope**

- General learner-facing cancellation UX
- Automatically rerunning uncertain jobs
- Assuming API retirement proves a container was removed

**Risk and review**

Retiring a shared identity or releasing an uncertain lease incorrectly can invalidate a healthy replacement or double-execute code; principal, process generation and lease transitions must be checked transactionally.

</details>

<a id="sai-b105"></a>
<details>
<summary>48. SAI-B105: Add a bounded metrics exporter consuming the existing private operational surface [pending]</summary>

**Priority:** P1 · **Phase:** operated-pilot · **Area:** operations-observability.

**Suggested role:** Backend engineer and operator.

**Prerequisites:** [SAI-B021](#sai-b021), [SAI-B020](#sai-b020), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Once B021 supplies canonical private queue/readiness measurements, operators need a stable low-cardinality exporter/report adapter without a second metrics authority.

**Target paths / responsibility**

- `services/api/solver_api/main.py`
- `services/api/solver_api/features/submissions/store.py`
- `services/judge/solver_judge/control/worker.py`
- `services/api/tests`

**Implementation scope**

- Consume B021 aggregate measurements through its existing authenticated operator boundary; do not create another queue/readiness endpoint.
- Add a versioned bounded export adapter for outcome/latency histograms and worker health, with an explicitly reviewed scrape/rotation policy.
- Reuse B020 redaction and cardinality rules; keep user/source/token data out of metrics.

**Acceptance criteria**

- Exporter fixtures match B021 canonical counters and handle unhealthy/stale input honestly.
- No second metrics endpoint, competing source of truth or unbounded identity labels are introduced.
- Unauthorized scrapes and unavailable source state fail safely without exposing underlying data.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/operations/test_metrics.py
- uv run --project services/api --frozen pytest services/judge/tests/control/test_worker.py

**Out of scope**

- Provisioning paid telemetry vendors
- Logging full submissions

**Risk and review**

Metrics labels and endpoints can leak private activity or overload storage.

</details>

<a id="sai-b106"></a>
<details>
<summary>49. SAI-B106: Propagate redacted correlation identifiers across accepted jobs [pending]</summary>

**Priority:** P2 · **Phase:** operated-pilot · **Area:** operations-observability.

**Suggested role:** Backend engineer.

**Prerequisites:** [SAI-B105](#sai-b105), [SAI-B001](#sai-b001), [SAI-B020](#sai-b020), [SAI-B027](#sai-b027).

**Problem / missing behavior**

Request-level diagnostics are difficult to connect to leased jobs and worker completion safely.

**Target paths / responsibility**

- `services/api/solver_api/main.py`
- `services/api/solver_api/features/submissions/store.py`
- `services/judge/solver_judge/control/worker.py`
- `services/api/tests`

**Implementation scope**

- Carry B020 existing server-generated request correlation ID into accepted job, worker lease and sanitized completion lineage.
- Validate length/format and use bounded diagnostics; identifiers remain telemetry and cannot grant ownership or select hidden tests.
- Reuse the existing log/telemetry schema instead of creating another request-ID authority.

**Acceptance criteria**

- A request/job/worker fixture can be followed by one correlation identifier without including source or credentials.
- Malformed and oversized supplied identifiers cannot inject log lines or labels.
- Lease retries retain the intended job lineage while attempts remain distinguishable.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/operations/test_correlation.py
- uv run --project services/api --frozen pytest services/judge/tests/control/test_worker.py

**Out of scope**

- A distributed tracing vendor deployment
- Publishing internal identifiers in unrestricted public analytics

**Risk and review**

Improper correlation data can become an injection or cross-user tracking vector.

</details>

<a id="sai-b107"></a>
<details>
<summary>50. SAI-B107: Define measurable service objectives and test operator alert rules [pending]</summary>

**Priority:** P1 · **Phase:** operated-pilot · **Area:** operations-observability.

**Suggested role:** Site reliability engineer and service owner.

**Prerequisites:** [SAI-B105](#sai-b105), [SAI-B106](#sai-b106), [SAI-B003](#sai-b003), [SAI-B001](#sai-b001).

**Problem / missing behavior**

A working local service does not define when operators should treat a deployment as degraded.

**Target paths / responsibility**

- `docs/onboarding/DEVELOPMENT.md`
- `docs/security/JUDGE_SECURITY.md`
- `scripts/verification`
- `services/api/tests`

**Implementation scope**

- Add proposed configuration/runbook rules for queue delay, stale workers, job-control failures and API error rate.
- Create deterministic metric fixtures to exercise alert activation and recovery, with owner-selected thresholds.

**Acceptance criteria**

- Each rule has an owner, observation window and tested firing/recovery fixture.
- Expected learner WA/CE/RE outcomes do not count as application incidents.
- A worker-readiness failure prevents an operator from declaring execution healthy.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/operations/test_alert_rules.py
- python3 scripts/verification/repository_inventory.py --help

**Out of scope**

- Invented production uptime claims
- Unapproved external paging or paid monitoring

**Risk and review**

Noisy alerts can hide actual incidents; broad thresholds can miss failures.

</details>

<a id="sai-b108"></a>
<details>
<summary>51. SAI-B108: Rehearse a timed full-stack disaster restore using the approved backup helper [pending]</summary>

**Priority:** P1 · **Phase:** operated-pilot · **Area:** operations-recovery.

**Suggested role:** Site reliability engineer with privacy reviewer.

**Prerequisites:** [SAI-B012](#sai-b012), [SAI-B013](#sai-b013), [SAI-B003](#sai-b003), [SAI-B001](#sai-b001).

**Problem / missing behavior**

B012 provides the backup/restore implementation; operations still need an isolated full-service recovery rehearsal with measured completeness and timing.

**Target paths / responsibility**

- `scripts/verification`
- `docs/onboarding/DEVELOPMENT.md`
- `compose.yaml`
- `apps/web/features/accounts/server.ts`
- `services/api/solver_api/features/submissions/store.py`

**Implementation scope**

- Invoke B012 backup/restore tooling and manifest format in fresh disposable service volumes; do not create another backup format or restore implementation.
- Restart web/API against restored data and verify auth/key continuity, ownership and job-recovery policy without changing live developer state.
- Produce a redacted RPO/RTO rehearsal report against B003 targets, including interrupted/missing-generation cases.

**Acceptance criteria**

- A seeded account can authenticate and read only its restored attempts after the drill restart.
- Missing key material, corrupt backup and mismatched database generation cause a clear failure.
- The report records measured restore duration and completeness, and proves original state was untouched.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/operations/test_restore_drill.py
- node --test apps/web/tests/auth.test.mjs

**Out of scope**

- Designing the foundational backup storage/encryption system
- Uploading backups to a new paid service

**Risk and review**

A partial restoration can lose accounts, invalidate sessions or mismatch ownership.

</details>

<a id="sai-b109"></a>
<details>
<summary>52. SAI-B109: Measure bounded capacity and overload behavior using original fixtures [pending]</summary>

**Priority:** P1 · **Phase:** operated-pilot · **Area:** operations-capacity.

**Suggested role:** Performance engineer and operator.

**Prerequisites:** [SAI-B105](#sai-b105), [SAI-B107](#sai-b107), [SAI-B124](#sai-b124), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Queue limits need an empirical operating envelope before opening a pilot.

**Target paths / responsibility**

- `scripts/verification`
- `services/api/tests/submissions`
- `services/judge/tests/control`
- `docs/onboarding/DEVELOPMENT.md`

**Implementation scope**

- Add a proposed opt-in load rehearsal with explicit concurrency/job/time ceilings and only original harmless programs.
- Measure queue latency, rejection behavior, cancellations and recovery under the configured local/dedicated test environment.

**Acceptance criteria**

- The run refuses to start without an explicit finite budget.
- Over-capacity requests receive the documented bounded response and the queue drains after load stops.
- A reproducible report records environment/revision and distinguishes measured limits from production guarantees.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/operations/test_load_budget.py
- uv run --project services/api --frozen pytest services/api/tests/submissions/test_submissions.py -k queue

**Out of scope**

- Unbounded stress loops
- Paid load infrastructure or testing third-party endpoints

**Risk and review**

A careless load test can exhaust the shared development machine.

</details>

<a id="sai-b110"></a>
<details>
<summary>53. SAI-B110: Implement a revisioned deployment smoke and rollback rehearsal [pending]</summary>

**Priority:** P1 · **Phase:** operated-pilot · **Area:** operations-release.

**Suggested role:** Release engineer and service owner.

**Prerequisites:** [SAI-B107](#sai-b107), [SAI-B108](#sai-b108), [SAI-B109](#sai-b109), [SAI-B005](#sai-b005), [SAI-B013](#sai-b013), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Local builds alone do not prove a deployable revision can be promoted or rolled back safely.

**Target paths / responsibility**

- `compose.yaml`
- `compose.cloud.yaml`
- `apps/web/Dockerfile`
- `services/api/Dockerfile`
- `scripts/verification`
- `docs/onboarding/DEVELOPMENT.md`

**Implementation scope**

- Add a proposed operator-invoked release rehearsal using immutable built artifact identifiers and isolated state.
- Verify health, account/session continuity, owned history and compatibility before recording a promotion decision.

**Acceptance criteria**

- A healthy candidate and a deliberately unhealthy candidate exercise promotion and rollback paths.
- Rollback preserves seeded account/submission state and records the exact application/artifact revisions.
- The helper never publishes externally or modifies the running environment without an explicit operator invocation.

**Validation required**

- docker compose config --quiet
- npx playwright test tests/e2e/operations/release-smoke.spec.ts --workers=1

**Out of scope**

- Automatic production deployment
- Provisioning a hosting account or paid infrastructure

**Risk and review**

Rollback across incompatible state versions can corrupt user data.

</details>

<a id="sai-b111"></a>
<details>
<summary>54. SAI-B111: Create a canary qualification gate for judge runtime upgrades [pending]</summary>

**Priority:** P1 · **Phase:** operated-pilot · **Area:** operations-release.

**Suggested role:** Judge maintainer and security reviewer.

**Prerequisites:** [SAI-B110](#sai-b110), [SAI-B125](#sai-b125), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Maintaining isolation requires a repeatable way to evaluate a runtime/toolchain update before broad rollout.

**Target paths / responsibility**

- `services/judge/UPSTREAM_REVIEW.md`
- `services/judge/Dockerfile`
- `services/judge/tests/sandbox`
- `services/judge/solver_judge/control/diagnostics.py`
- `scripts/verification`

**Implementation scope**

- Add a proposed comparison runbook/report for an operator-provided approved candidate runtime or image.
- Run existing hostile-program, cleanup and language fixtures on the candidate before allowing a canary decision.

**Acceptance criteria**

- Reports name old/new runtime and image identifiers and every executed/skipped check.
- A failed isolation/cleanup probe blocks qualification even when correct solutions pass.
- The process does not replace the managed host daemon or silently fall back to ordinary containers.

**Validation required**

- npm run test:judge:integration
- uv run --project services/api --frozen pytest services/judge/tests/control/test_runner.py

**Out of scope**

- Installing host runtimes automatically
- Claiming independent security certification

**Risk and review**

A toolchain update can weaken isolation or alter resource semantics.

</details>

<a id="sai-b112"></a>
<details>
<summary>55. SAI-B112: Run a bounded incident exercise for worker outage and recovery [pending]</summary>

**Priority:** P2 · **Phase:** operated-pilot · **Area:** operations-recovery.

**Suggested role:** Site reliability engineer and service owner.

**Prerequisites:** [SAI-B107](#sai-b107), [SAI-B108](#sai-b108), [SAI-B110](#sai-b110), [SAI-B111](#sai-b111), [SAI-B126](#sai-b126), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Operators need evidence that readiness, job reconciliation and user messaging work during failures.

**Target paths / responsibility**

- `docs/security/JUDGE_SECURITY.md`
- `docs/onboarding/DEVELOPMENT.md`
- `scripts/verification`
- `services/judge/tests/control`
- `services/api/tests`

**Implementation scope**

- Add a proposed isolated exercise covering lost worker heartbeat, interrupted control service and restored service.
- Record detection, containment, queued-job reconciliation and owner communication steps without sending external messages automatically.

**Acceptance criteria**

- The exercise demonstrates unavailable execution while probes fail and safe recovery after reconciliation.
- No attempt is attributed to another account or completed twice.
- A post-exercise report names observed times, unresolved gaps and a responsible owner; live databases remain untouched.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/operations/test_incident_rehearsal.py
- uv run --project services/api --frozen pytest services/judge/tests/control/test_worker.py

**Out of scope**

- Simulated credential theft against real accounts
- Automatic incident messaging or account-admin changes

**Risk and review**

An exercise that touches live state can create the incident it is meant to test.

</details>

<a id="sai-b041"></a>
<details>
<summary>56. SAI-B041: Record the single-provider hint pilot activation decision [pending]</summary>

**Priority:** P1 · **Phase:** AI-1 controlled model hints · **Area:** AI activation governance.

**Suggested role:** Project owner with privacy and AI engineering reviewers.

**Prerequisites:** [SAI-B001](#sai-b001), [SAI-B002](#sai-b002), [SAI-B003](#sai-b003), [SAI-B026](#sai-b026).

**Problem / missing behavior**

Authored hints and their UI work, but no provider, data-processing terms, spend owner or activation authority has been selected for real inference.

**Target paths / responsibility**

- `docs/product/AI_SOLVER.md`
- `docs/governance/OPEN_DECISIONS.md`
- `docs/governance/DATA_AND_LICENSES.md`

**Implementation scope**

- Document one bounded hint pilot and its permitted public-only context.
- Record provider-selection criteria, credential destinations, pricing assumptions, responsible owner and rollback authority.
- Make activation conditional on privacy, admission and transport issues below.

**Acceptance criteria**

- Decision separates authored service, optional model pilot and unapproved debugging/training.
- Every unresolved credential, rights or spending prerequisite has an owner and blocks activation.
- No default configuration begins paid inference.

**Validation required**

- Document review against docs/status/PROJECT_STATUS.md and the existing HintBackend implementation; no provider calls.

**Out of scope**

- Provisioning a paid account or GPU
- Replacing existing authored hints

**Risk and review**

A written provider name must not be mistaken for permission to send user data or spend money.

</details>

<a id="sai-b042"></a>
<details>
<summary>57. SAI-B042: Bound and fingerprint the existing public-only hint context [pending]</summary>

**Priority:** P1 · **Phase:** AI-1 controlled model hints · **Area:** Safe model context.

**Suggested role:** Backend engineer.

**Prerequisites:** [SAI-B041](#sai-b041), [SAI-B001](#sai-b001).

**Problem / missing behavior**

PublicHintContext already excludes private tests and identity, but future inference needs explicit per-field and aggregate bounds and a stable content fingerprint.

**Target paths / responsibility**

- `services/api/solver_api/features/hints/service.py`
- `services/api/solver_api/features/catalog/models.py`
- `services/api/tests/hints/test_hints.py`

**Implementation scope**

- Add validated context-size limits and deterministic canonical fingerprinting without introducing private grading fields.
- Define overflow rejection or documented deterministic truncation for each public field.
- Keep authored lookup behavior and the public HTTP v1 response compatible.

**Acceptance criteria**

- Private test/source/credential sentinels never enter serialized model context.
- Identical authorized catalog content produces the same fingerprint; changed samples change it.
- Boundary and one-byte-over-limit inputs have deterministic outcomes.

**Validation required**

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q

**Out of scope**

- Reading owned submission source
- Sending a model request

**Risk and review**

Silent truncation could remove a constraint and produce misleading hints.

</details>

<a id="sai-b043"></a>
<details>
<summary>58. SAI-B043: Validate trusted provider destinations and secret configuration [pending]</summary>

**Priority:** P1 · **Phase:** AI-1 controlled model hints · **Area:** Provider configuration.

**Suggested role:** Backend security engineer.

**Prerequisites:** [SAI-B041](#sai-b041), [SAI-B006](#sai-b006), [SAI-B001](#sai-b001).

**Problem / missing behavior**

The authored-only selector intentionally fails closed. A future provider must not inherit archive adapters that accept arbitrary endpoints or ambiguous environment state.

**Target paths / responsibility**

- `services/api/solver_api/features/hints/service.py`
- `services/api/tests/hints/test_hints.py`
- `docs/onboarding/DEVELOPMENT.md`

**Implementation scope**

- Define administrator-controlled HTTPS destination/model settings with strict URL parsing and an explicit local-development exception policy.
- Reject URL userinfo, unexpected redirects and request-supplied endpoint overrides.
- Validate credential presence without logging values; keep authored as the default.

**Acceptance criteria**

- Malformed, unapproved and insecure external destinations fail before transport.
- Missing credentials produce a sanitized configuration failure.
- No browser bundle, OpenAPI example or log contains credential values.

**Validation required**

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q

**Out of scope**

- Collecting credentials in chat
- Changing network policy automatically

**Risk and review**

Provider configuration can become an SSRF or credential-forwarding boundary if endpoint control leaks to callers.

</details>

<a id="sai-b044"></a>
<details>
<summary>59. SAI-B044: Define an internal generation result and usage contract [pending]</summary>

**Priority:** P1 · **Phase:** AI-1 controlled model hints · **Area:** Provider-neutral contracts.

**Suggested role:** Backend and AI interface engineer.

**Prerequisites:** [SAI-B042](#sai-b042), [SAI-B001](#sai-b001).

**Problem / missing behavior**

HintBackend returns bounded HintContent today; real inference also needs trusted model identity, usage, finish reason and request metadata without exposing provider payloads.

**Target paths / responsibility**

- `services/api/solver_api/features/hints/service.py`
- `services/api/tests/hints/test_hints.py`
- `docs/product/AI_SOLVER.md`

**Implementation scope**

- Introduce an internal provider-neutral result separating display content from operational metadata.
- Represent missing usage, partial completion and unknown billing explicitly.
- Adapt authored generation to the internal interface while preserving its truthful source/provider fields.

**Acceptance criteria**

- Existing HTTP v1 authored responses remain compatible.
- Operational metadata cannot serialize into the learner response accidentally.
- Invalid provenance and contradictory usage/finish data are rejected by named contract rules.

**Validation required**

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q

**Out of scope**

- Implementing multiple providers
- Changing account JWT claims

**Risk and review**

Treating absent provider usage as zero would undercount spend.

</details>

<a id="sai-b045"></a>
<details>
<summary>60. SAI-B045: Version bounded hint prompts and spoiler policies [pending]</summary>

**Priority:** P1 · **Phase:** AI-1 controlled model hints · **Area:** Tutoring prompts.

**Suggested role:** AI engineer and teaching reviewer.

**Prerequisites:** [SAI-B042](#sai-b042), [SAI-B044](#sai-b044), [SAI-B001](#sai-b001).

**Problem / missing behavior**

The three authored levels have clear meaning; a model integration needs repeatable templates that preserve that progression instead of exposing full solutions by default.

**Target paths / responsibility**

- `services/api/solver_api/features/hints/service.py`
- `docs/product/AI_SOLVER.md`
- `services/api/tests/hints/test_hints.py`

**Implementation scope**

- Define versioned concept/observation/plan templates and a minimal response format.
- Treat problem text as quoted task data with no authority over permissions or tools.
- Record prompt version with internal run metadata without requesting or storing hidden chain-of-thought.

**Acceptance criteria**

- Each level has a reviewed allowed-content rubric and output limit.
- Prompt-injection fixtures cannot add tools, destinations or private context.
- Template changes alter a recorded version/fingerprint and keep authored content untouched.

**Validation required**

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q; human review of level rubrics.

**Out of scope**

- Claiming prompts guarantee compliance
- Copying archive prompts wholesale

**Risk and review**

A model may still overshare; prompt instructions require output review and product policy.

</details>

<a id="sai-b046"></a>
<details>
<summary>61. SAI-B046: Reject malformed model hints before constructing learner responses [pending]</summary>

**Priority:** P1 · **Phase:** AI-1 controlled model hints · **Area:** Model output contracts.

**Suggested role:** Backend engineer.

**Prerequisites:** [SAI-B044](#sai-b044), [SAI-B045](#sai-b045), [SAI-B001](#sai-b001).

**Problem / missing behavior**

HintContent already bounds and labels authored/mock/model output, but raw provider responses need a separate defensive normalization boundary.

**Target paths / responsibility**

- `services/api/solver_api/features/hints/service.py`
- `services/api/tests/hints/test_hints.py`
- `apps/web/features/hints/api.ts`

**Implementation scope**

- Validate selected provider message content, completion status and text size before HintContent construction.
- Reject empty, oversized, unexpected multimodal/tool-call and incomplete responses with stable sanitized errors.
- Keep raw model text out of exception messages and logs.

**Acceptance criteria**

- Every malformed-response fixture produces a stable failure rather than partial success.
- Accepted model hints always have source=model, ai_generated=true and a configured provider identifier.
- Existing frontend provenance/schema checks remain strict.

**Validation required**

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q; npm run typecheck

**Out of scope**

- Rendering provider HTML
- Adding unconstrained chat messages

**Risk and review**

String cleanup must not silently convert a refusal or truncated answer into a normal hint.

</details>

<a id="sai-b047"></a>
<details>
<summary>62. SAI-B047: Add deterministic provider transport fixtures without external inference [pending]</summary>

**Priority:** P1 · **Phase:** AI-1 controlled model hints · **Area:** Provider adapter verification.

**Suggested role:** AI integration engineer.

**Prerequisites:** [SAI-B043](#sai-b043), [SAI-B044](#sai-b044), [SAI-B046](#sai-b046), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Real transport behavior cannot be validated by relabeling an authored hint or by requiring paid calls in routine checks.

**Target paths / responsibility**

- `services/api/tests/hints/test_hints.py`
- `services/api/solver_api/features/hints/service.py`

**Implementation scope**

- Create deterministic HTTP transport fixtures for success, refusal, malformed data, rate limiting and disconnects.
- Assert exact outgoing field allowlists and absence of account JWTs, worker tokens, private tests and source.
- Separate fixture provenance from actual model-backed production responses.

**Acceptance criteria**

- Fixtures run with all outbound network access denied.
- Tests fail when an extra credential/context field is injected.
- No fixture result is presented as evidence of model quality or paid-provider access.

**Validation required**

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q

**Out of scope**

- Live provider benchmarks
- Adding a public mock backend as a completed AI feature

**Risk and review**

A fixture may drift from the selected provider schema; record the reviewed API version.

</details>

<a id="sai-b048"></a>
<details>
<summary>63. SAI-B048: Implement one opt-in bounded asynchronous hint provider adapter [pending]</summary>

**Priority:** P1 · **Phase:** AI-1 controlled model hints · **Area:** Real provider transport.

**Suggested role:** AI backend engineer.

**Prerequisites:** [SAI-B043](#sai-b043), [SAI-B044](#sai-b044), [SAI-B046](#sai-b046), [SAI-B047](#sai-b047), [SAI-B001](#sai-b001).

**Problem / missing behavior**

select_hint_backend deliberately supports authored only. The first real adapter needs bounded async transport rather than archived sync clients with missing timeouts.

**Target paths / responsibility**

- `services/api/solver_api/features/hints/service.py`
- `services/api/pyproject.toml`
- `services/api/tests/hints/test_hints.py`

**Implementation scope**

- Implement the single provider selected in B041 using an existing suitable HTTP dependency where possible.
- Set request/response byte caps, completion-token cap, explicit transport timeouts and destination restrictions.
- Keep registration disabled unless the later entitlement, budget and privacy gates are satisfied.

**Acceptance criteria**

- Adapter passes deterministic transport fixtures without real network access.
- Oversized or endless responses terminate within documented limits.
- Default startup and authored hints do not require provider credentials or make external calls.

**Validation required**

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q; uv run --project services/api --frozen ruff check services/api

**Out of scope**

- Automatic activation or spend
- Installing archive requirements or adding a second provider

**Risk and review**

Transport completion does not establish content quality, privacy compliance or production readiness.

</details>

<a id="sai-b049"></a>
<details>
<summary>64. SAI-B049: Enforce account-level entitlement before model-backed hints [pending]</summary>

**Priority:** P1 · **Phase:** AI-1 controlled model hints · **Area:** AI admission policy.

**Suggested role:** Backend authorization engineer.

**Prerequisites:** [SAI-B041](#sai-b041), [SAI-B044](#sai-b044), [SAI-B014](#sai-b014), [SAI-B016](#sai-b016), [SAI-B001](#sai-b001).

**Problem / missing behavior**

The hints route authenticates but discards its user ID because authored lookup does not need a model entitlement. Real inference must authorize an account before transport.

**Target paths / responsibility**

- `services/api/solver_api/main.py`
- `services/api/solver_api/features/hints/service.py`
- `services/api/solver_api/features/identity/verification.py`
- `services/api/tests/hints/test_hints.py`

**Implementation scope**

- Carry the verified internal account identifier into an admission layer, never into model context.
- Define a local pilot allowlist/entitlement source and explicit denied/disabled states.
- Keep public authored hints and existing signed-in authored behavior available.

**Acceptance criteria**

- Unauthenticated, unentitled and disabled-account requests make zero provider calls.
- Caller-supplied user IDs and forwarding headers cannot change entitlement.
- Allowed/denied decisions are testable independently of transport.

**Validation required**

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints services/api/tests/identity -q

**Out of scope**

- Billing plans
- Changing existing JWT ownership boundaries

**Risk and review**

Authentication alone is insufficient authority to consume external resources.

</details>

<a id="sai-b050"></a>
<details>
<summary>65. SAI-B050: Reserve and reconcile durable per-account hint budgets atomically [pending]</summary>

**Priority:** P1 · **Phase:** AI-1 controlled model hints · **Area:** AI token and request quotas.

**Suggested role:** Backend persistence engineer.

**Prerequisites:** [SAI-B044](#sai-b044), [SAI-B049](#sai-b049), [SAI-B013](#sai-b013), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Submission quotas exist for execution jobs, but no durable reservation mechanism currently limits model tokens or model request count.

**Target paths / responsibility**

- `services/api/solver_api/features/hints/service.py`
- `services/api/solver_api/features/submissions/store.py`
- `services/api/tests/hints/test_hints.py`
- `docs/onboarding/DEVELOPMENT.md`

**Implementation scope**

- Add a separate model-usage ledger with atomic request/token reservation and idempotent reconciliation.
- Reserve the configured upper bound before transport; conservatively handle unknown usage and interrupted runs.
- Document additive local schema migration and keep submission quota responsibility separate.

**Acceptance criteria**

- Concurrent requests cannot reserve beyond an account limit.
- Restart/repeated settlement cannot erase consumption or charge one reservation twice.
- Exhausted budget returns a stable 429 without a provider request.

**Validation required**

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints services/api/tests/submissions -q

**Out of scope**

- Payment collection
- Treating missing usage as free

**Risk and review**

Ledger races and ambiguous completion can bypass caps or unfairly consume allowance.

</details>

<a id="sai-b051"></a>
<details>
<summary>66. SAI-B051: Add process-wide provider concurrency and monetary admission ceilings [pending]</summary>

**Priority:** P1 · **Phase:** AI-1 controlled model hints · **Area:** Global AI spend control.

**Suggested role:** Backend platform engineer.

**Prerequisites:** [SAI-B050](#sai-b050), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Per-account allowance cannot prevent many accounts from exhausting provider concurrency or a project-wide spending ceiling.

**Target paths / responsibility**

- `services/api/solver_api/features/hints/service.py`
- `services/api/tests/hints/test_hints.py`
- `docs/onboarding/DEVELOPMENT.md`

**Implementation scope**

- Define bounded global in-flight admission and an explicitly versioned token-price estimate.
- Reject requests whose maximum reserved cost exceeds a configured project ceiling.
- Fail closed for invalid pricing/ceiling configuration; distinguish estimated from billed cost.

**Acceptance criteria**

- An N+1 concurrent request is denied or boundedly queued under an N-slot configuration.
- Worst-case reservations never exceed the configured monetary ceiling.
- Restart semantics and single-process versus multi-process limits are documented honestly.

**Validation required**

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q

**Out of scope**

- Distributed quota infrastructure without a deployment need
- Automatic model upgrades

**Risk and review**

A process-local semaphore is not a distributed project-wide spending guarantee.

</details>

<a id="sai-b052"></a>
<details>
<summary>67. SAI-B052: Deduplicate model hint retries with account-scoped idempotency [pending]</summary>

**Priority:** P1 · **Phase:** AI-1 controlled model hints · **Area:** AI request reliability.

**Suggested role:** Backend engineer.

**Prerequisites:** [SAI-B050](#sai-b050), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Browser retries or lost responses could trigger duplicate paid generation even when the learner intended one hint request.

**Target paths / responsibility**

- `services/api/solver_api/main.py`
- `services/api/solver_api/features/hints/service.py`
- `apps/web/features/hints/api.ts`
- `services/api/tests/hints/test_hints.py`

**Implementation scope**

- Add optional account-scoped idempotency keyed by canonical request/context/backend version.
- Define replay, in-progress and same-key/different-payload outcomes.
- Reuse the same reservation/result for matching retries with bounded retention.

**Acceptance criteria**

- Two matching concurrent retries result in at most one provider invocation.
- Different accounts cannot retrieve each other's cached hint.
- A reused key with changed problem/level/context receives a stable conflict.

**Validation required**

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q; npm run typecheck

**Out of scope**

- Global shared personalized-answer cache
- Changing submission idempotency behavior

**Risk and review**

An underspecified cache key can leak responses or replay stale prompt policy.

</details>

<a id="sai-b053"></a>
<details>
<summary>68. SAI-B053: Record redacted generation usage and failure telemetry [pending]</summary>

**Priority:** P1 · **Phase:** AI-1 controlled model hints · **Area:** AI observability.

**Suggested role:** Backend observability engineer.

**Prerequisites:** [SAI-B044](#sai-b044), [SAI-B050](#sai-b050), [SAI-B020](#sai-b020), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Archive adapters log prompts/responses and simple CSV usage; production troubleshooting needs operational evidence without copying learner content or secrets.

**Target paths / responsibility**

- `services/api/solver_api/features/hints/service.py`
- `services/api/solver_api/http/errors.py`
- `services/api/tests/hints/test_hints.py`
- `docs/governance/DATA_AND_LICENSES.md`

**Implementation scope**

- Define allowlisted run ID, model/version, context fingerprint, latency, capped usage and termination metadata.
- Redact authorization, provider payloads, source and problem text by construction.
- Set bounded retention and document aggregation versus account-level access.

**Acceptance criteria**

- Sentinel credentials/source/private tests never appear in captured logs on success or failure.
- Unknown usage and provider-timeout categories remain distinguishable.
- A learner-visible correlation ID maps to one operational event without revealing another account.

**Validation required**

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q

**Out of scope**

- Collecting full prompts by default
- Claiming estimated token counts equal invoices

**Risk and review**

Verbose error logging can defeat an otherwise safe context boundary.

</details>

<a id="sai-b054"></a>
<details>
<summary>69. SAI-B054: Propagate total generation deadlines and explicit cancellation states [pending]</summary>

**Priority:** P1 · **Phase:** AI-1 controlled model hints · **Area:** AI cancellation and deadlines.

**Suggested role:** Full-stack AI integration engineer.

**Prerequisites:** [SAI-B048](#sai-b048), [SAI-B050](#sai-b050), [SAI-B053](#sai-b053), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Authored hints use a three-second server bound and the client already cancels requests, but real provider transport and quota settlement need a total lifecycle contract.

**Target paths / responsibility**

- `services/api/solver_api/features/hints/service.py`
- `apps/web/features/hints/api.ts`
- `apps/web/features/hints/account-hint.tsx`
- `services/api/tests/hints/test_hints.py`
- `tests/e2e/hints/hints.spec.ts`

**Implementation scope**

- Define bounded server generation, transport cleanup and caller-abandonment states.
- Propagate cancellation to async transport and reconcile reservations conservatively.
- Preserve the existing UI cancellation/stale-result protection; avoid claiming upstream billing stopped without evidence.

**Acceptance criteria**

- Slow-chunk fixtures cannot exceed the total configured deadline.
- Cancel/level-change/account-change never renders a stale result.
- Interrupted requests have exactly one documented settlement outcome.

**Validation required**

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q; npm run test:e2e -- tests/e2e/hints/hints.spec.ts --workers=1

**Out of scope**

- Unlimited timeout increases
- Guaranteeing remote provider cancellation

**Risk and review**

Local cancellation and remote resource consumption can diverge.

</details>

<a id="sai-b055"></a>
<details>
<summary>70. SAI-B055: Bound provider retries and add outage admission state [pending]</summary>

**Priority:** P1 · **Phase:** AI-1 controlled model hints · **Area:** AI failure policy.

**Suggested role:** Backend reliability engineer.

**Prerequisites:** [SAI-B048](#sai-b048), [SAI-B051](#sai-b051), [SAI-B054](#sai-b054), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Archived clients retry up to twenty times or wait many minutes. A paid hint endpoint needs predictable bounded failures and must not amplify outages.

**Target paths / responsibility**

- `services/api/solver_api/features/hints/service.py`
- `services/api/tests/hints/test_hints.py`
- `apps/web/features/hints/api.ts`

**Implementation scope**

- Classify retryable transport/429 failures separately from invalid output/authentication/refusal.
- Cap attempts within the original deadline and reserve the possible retry cost.
- Add a small observable outage/cooldown admission policy with explicit recovery behavior.

**Acceptance criteria**

- Nonretryable fixture errors make exactly one attempt.
- Retryable fixtures never exceed configured attempts, deadline or reserved spend.
- Outage responses preserve stable public errors and keep authored practice usable.

**Validation required**

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q

**Out of scope**

- Automatic fallback to a more expensive provider
- Infinite background retries

**Risk and review**

Retries can multiply both latency and charges even after the browser gives up.

</details>

<a id="sai-b056"></a>
<details>
<summary>71. SAI-B056: Require clear external-AI disclosure before opt-in hint requests [pending]</summary>

**Priority:** P1 · **Phase:** AI-1 controlled model hints · **Area:** AI privacy UX.

**Suggested role:** Product privacy and frontend engineer.

**Prerequisites:** [SAI-B041](#sai-b041), [SAI-B049](#sai-b049), [SAI-B053](#sai-b053), [SAI-B001](#sai-b001).

**Problem / missing behavior**

The completed UI accurately advertises authored hints. Introducing external generation changes where context is processed and requires an honest, explicit choice.

**Target paths / responsibility**

- `apps/web/features/hints/account-hint.tsx`
- `apps/web/features/hints/api.ts`
- `services/api/solver_api/features/hints/service.py`
- `docs/governance/DATA_AND_LICENSES.md`
- `tests/e2e/hints/hints.spec.ts`

**Implementation scope**

- Expose trusted capability/disclosure information without provider credentials or editable destinations.
- Explain the exact public context sent, retention policy and optional nature of model help.
- Record the accepted disclosure version for model admission while leaving authored hints accessible.

**Acceptance criteria**

- No external generation occurs before the required explicit choice.
- Switching back to authored mode removes model provenance claims.
- UI and API agree on the disclosure version; stale/absent consent blocks model requests.

**Validation required**

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q; npm run test:e2e -- tests/e2e/hints/hints.spec.ts --workers=1

**Out of scope**

- Consent to training on private submissions
- Uploading editor drafts

**Risk and review**

A blanket consent checkbox cannot authorize unspecified future source sharing.

</details>

<a id="sai-b057"></a>
<details>
<summary>72. SAI-B057: Provide a tested operator kill switch for model hint admission [pending]</summary>

**Priority:** P1 · **Phase:** AI-1 controlled model hints · **Area:** AI operations.

**Suggested role:** Backend operations engineer.

**Prerequisites:** [SAI-B048](#sai-b048), [SAI-B049](#sai-b049), [SAI-B055](#sai-b055), [SAI-B056](#sai-b056), [SAI-B001](#sai-b001).

**Problem / missing behavior**

A provider incident or budget concern must disable future external work without breaking the already completed local authored workflow.

**Target paths / responsibility**

- `services/api/solver_api/features/hints/service.py`
- `services/api/tests/hints/test_hints.py`
- `apps/web/features/hints/account-hint.tsx`
- `docs/onboarding/DEVELOPMENT.md`

**Implementation scope**

- Define trusted enabled/disabled/draining states and bounded in-flight treatment.
- Make the UI display the effective source/capability rather than a hard-coded model promise.
- Document disable, verify-no-egress and restore procedures.

**Acceptance criteria**

- Disabling admission prevents new external calls immediately at the admission boundary.
- In-flight reservation handling follows one documented policy.
- Authored hints, catalog and submissions retain their existing behavior.

**Validation required**

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q; npm run test:e2e -- tests/e2e/hints/hints.spec.ts --workers=1

**Out of scope**

- Disabling account security checks
- Silently labeling fallback text as model output

**Risk and review**

A UI-only toggle cannot stop API callers or already admitted upstream work.

</details>

<a id="sai-b058"></a>
<details>
<summary>73. SAI-B058: Add shared golden fixtures for hint API and browser schema parity [pending]</summary>

**Priority:** P2 · **Phase:** AI-1 controlled model hints · **Area:** Cross-runtime AI contracts.

**Suggested role:** Full-stack contract engineer.

**Prerequisites:** [SAI-B044](#sai-b044), [SAI-B046](#sai-b046), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Pydantic and Zod intentionally validate the same bounded contract independently; future provider fields could drift between implementations.

**Target paths / responsibility**

- `services/api/solver_api/features/hints/service.py`
- `apps/web/features/hints/api.ts`
- `services/api/tests/hints/test_hints.py`
- `tests/e2e/hints/hints.spec.ts`

**Implementation scope**

- Define public golden authored/model/mock/error fixtures and explicit incompatible examples.
- Exercise both validators against provenance, level, slug, length and response-correlation cases.
- Document additive internal metadata versus HTTP schema version changes.

**Acceptance criteria**

- Both runtimes accept every valid golden fixture and reject every invalid one.
- A changed provider/source/ai_generated combination cannot bypass either validator.
- Fixtures contain no credentials, private cases or account identifiers.

**Validation required**

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q; npm run test:e2e -- tests/e2e/hints/hints.spec.ts --workers=1

**Out of scope**

- Replacing runtime validation with TypeScript types only
- Changing public API v1 unnecessarily

**Risk and review**

Generated types alone do not validate hostile network payloads.

</details>

<a id="sai-b059"></a>
<details>
<summary>74. SAI-B059: Define and execute a small consented model-hint pilot acceptance gate [pending]</summary>

**Priority:** P1 · **Phase:** AI-1 controlled model hints · **Area:** Hint quality pilot.

**Suggested role:** Teaching evaluator with project owner.

**Prerequisites:** [SAI-B045](#sai-b045), [SAI-B050](#sai-b050), [SAI-B051](#sai-b051), [SAI-B056](#sai-b056), [SAI-B057](#sai-b057), [SAI-B058](#sai-b058), [SAI-B124](#sai-b124), [SAI-B126](#sai-b126), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Passing adapter fixtures demonstrates integration behavior, not whether generated hints are correct, useful or appropriately limited in spoilers.

**Target paths / responsibility**

- `docs/product/AI_SOLVER.md`
- `docs/status/PROJECT_STATUS.md`
- `docs/research/MODEL_DATA_EVALUATION.md`
- `services/api/tests/hints/test_hints.py`

**Implementation scope**

- Choose a small original/permissioned task set with human-reviewed level rubrics.
- Record an explicit owner-approved call/spend ceiling before any live pilot.
- Report usefulness, factual mistakes, spoilers, refusal/outage outcomes and negative results separately.

**Acceptance criteria**

- Every evaluated hint records task/context/prompt/model versions and its rubric outcome.
- Pilot costs stay inside the approved cap; no live calls run without that approval.
- Activation recommendation cites failures and sample size rather than claiming general learning improvement.

**Validation required**

- Future authorized evaluation: run the documented bounded pilot only after owner approval; review fixture suite and publish a redacted result manifest.

**Out of scope**

- Unbounded benchmark sweeps
- Claims of causal educational benefit from a small observational pilot

**Risk and review**

A provider working on three seed problems is not evidence of broad tutoring quality.

</details>

<a id="sai-b113"></a>
<details>
<summary>75. SAI-B113: Provide learner-controlled progress summaries with assistance provenance [pending]</summary>

**Priority:** P2 · **Phase:** learning-coaching · **Area:** learning-analytics.

**Suggested role:** Backend engineer with learning researcher.

**Prerequisites:** [SAI-B003](#sai-b003), [SAI-B022](#sai-b022), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Owned attempt history does not yet offer a careful summary of independent versus assisted practice.

**Target paths / responsibility**

- `services/api/solver_api/features/submissions/store.py`
- `services/api/solver_api/main.py`
- `apps/web/features/submissions`
- `services/api/tests`

**Implementation scope**

- Add a proposed summary of completed practice by topic, observed attempts and explicitly recorded assistance state.
- Show the source/limits of each metric and exclude contest results when event policy requires it.

**Acceptance criteria**

- Hand-seeded histories produce exact counts with no cross-account rows.
- Unknown assistance remains unknown rather than being labeled independent.
- The interface does not claim learning improvement or skill diagnosis from accepted-answer totals alone.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/learning/test_progress_summaries.py
- npx playwright test tests/e2e/learning/progress.spec.ts --workers=2

**Out of scope**

- AI skill prediction
- Public ranking of personal learning data

**Risk and review**

Misleading or leaking progress metrics can harm learner trust.

</details>

<a id="sai-b114"></a>
<details>
<summary>76. SAI-B114: Add editable practice plans and deterministic review reminders [pending]</summary>

**Priority:** P2 · **Phase:** learning-coaching · **Area:** learning-plans.

**Suggested role:** Full-stack engineer and learning designer.

**Prerequisites:** [SAI-B113](#sai-b113), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Learners need a plan they can control without an opaque personalization model.

**Target paths / responsibility**

- `apps/web/app`
- `apps/web/features/practice`
- `services/api/solver_api/main.py`
- `services/api/tests`

**Implementation scope**

- Add a proposed user-owned plan with selected topics/problems, due dates and in-app review prompts.
- Support snooze, reschedule and disabling prompts; use a documented deterministic review rule.

**Acceptance criteria**

- Only the owner can read or modify a plan.
- A completed/repeated problem updates the expected next review date under fixed-clock fixtures.
- Disabled reminders stop appearing and do not trigger email or external notifications.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/learning/test_practice_plans.py
- npx playwright test tests/e2e/learning/plans.spec.ts --workers=2

**Out of scope**

- Model-based adaptation
- Unrequested email/push notifications

**Risk and review**

Incorrect scheduling or intrusive reminders can undermine user control.

</details>

<a id="sai-b115"></a>
<details>
<summary>77. SAI-B115: Implement opt-in coach cohorts with explicit sharing permissions [pending]</summary>

**Priority:** P2 · **Phase:** learning-coaching · **Area:** coaching.

**Suggested role:** Backend engineer and privacy reviewer.

**Prerequisites:** [SAI-B113](#sai-b113), [SAI-B001](#sai-b001).

**Problem / missing behavior**

A coach must not gain access to a learner’s private practice simply because both have accounts.

**Target paths / responsibility**

- `services/api/solver_api/features/identity`
- `services/api/solver_api/main.py`
- `apps/web/app`
- `services/api/tests`

**Implementation scope**

- Add a proposed cohort invitation/acceptance workflow with bounded coach membership and learner-controlled sharing scopes.
- Keep ordinary private history inaccessible unless a specific cohort permission covers it.

**Acceptance criteria**

- Joining requires the invited learner’s explicit action and shows exactly which data becomes visible.
- A coach outside the cohort and a removed coach cannot query cohort-only data.
- Leaving/revoking sharing changes subsequent access according to a tested policy.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/coaching/test_cohorts.py
- npx playwright test tests/e2e/coaching/invitations.spec.ts --workers=2

**Out of scope**

- Automatic contact imports
- Giving coaches general account-administrator access

**Risk and review**

Broad sharing scopes could expose unrelated private attempts.

</details>

<a id="sai-b116"></a>
<details>
<summary>78. SAI-B116: Add permissioned assignments and human rubric feedback [pending]</summary>

**Priority:** P2 · **Phase:** learning-coaching · **Area:** coaching.

**Suggested role:** Full-stack engineer and educator reviewer.

**Prerequisites:** [SAI-B113](#sai-b113), [SAI-B115](#sai-b115), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Coaching needs an assignment boundary and visible human feedback rather than ad hoc access to all submissions.

**Target paths / responsibility**

- `services/api/solver_api/features/catalog`
- `services/api/solver_api/main.py`
- `apps/web/app`
- `apps/web/features`
- `services/api/tests`

**Implementation scope**

- Add proposed cohort assignments using authorized problem versions and explicit deadlines.
- Support a bounded human rubric/comment record attached only to submitted assignment work.

**Acceptance criteria**

- A learner sees only assigned work and feedback allowed for that cohort.
- A coach cannot attach feedback to an unrelated private practice attempt.
- Rubric edits retain attribution/revision and render as safe text in browser tests.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/coaching/test_assignments.py
- npx playwright test tests/e2e/coaching/assignments.spec.ts --workers=2

**Out of scope**

- Automatic AI grading of educational ability
- Live classroom video or plagiarism accusations

**Risk and review**

Feedback permissions and immutable problem references must remain consistent.

</details>

<a id="sai-b060"></a>
<details>
<summary>79. SAI-B060: Design a bounded tutoring interaction contract beyond hint levels [pending]</summary>

**Priority:** P2 · **Phase:** AI-2 consented tutor and debugger · **Area:** Tutor interaction design.

**Suggested role:** Product and AI interface designer.

**Prerequisites:** [SAI-B059](#sai-b059), [SAI-B001](#sai-b001).

**Problem / missing behavior**

The completed hint ladder handles one level at a time; conceptual questions and learner reasoning require a deliberately scoped interaction rather than an unlimited chat box.

**Target paths / responsibility**

- `docs/product/AI_SOLVER.md`
- `services/api/solver_api/features/hints/service.py`
- `apps/web/features/hints/account-hint.tsx`

**Implementation scope**

- Specify allowed interaction types, role boundaries, spoiler level, maximum turns and public-only task context.
- Separate concise pedagogical explanations from hidden model reasoning.
- Record compatibility with the existing hint endpoint before adding a new contract.

**Acceptance criteria**

- Contract includes exact bounds, account ownership and allowed-context rules.
- Each interaction has a measurable completion/refusal/stop outcome.
- The design does not silently turn hint requests into source review or full-solution generation.

**Validation required**

- Static contract review against existing API/UI and the approved pilot findings; no model calls for this design issue.

**Out of scope**

- Unrestricted general-purpose chat
- Replacing authored hints

**Risk and review**

An open-ended conversation broadens privacy and cost exposure beyond the successful pilot.

</details>

<a id="sai-b061"></a>
<details>
<summary>80. SAI-B061: Implement account-owned expiring tutor conversation state [pending]</summary>

**Priority:** P2 · **Phase:** AI-2 consented tutor and debugger · **Area:** Tutor context lifecycle.

**Suggested role:** Backend privacy engineer.

**Prerequisites:** [SAI-B050](#sai-b050), [SAI-B053](#sai-b053), [SAI-B056](#sai-b056), [SAI-B060](#sai-b060), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Multiple tutoring turns must not reuse another account's context, grow without bound or persist private discussion indefinitely.

**Target paths / responsibility**

- `services/api/solver_api/features/hints/service.py`
- `services/api/solver_api/main.py`
- `apps/web/features/hints/api.ts`
- `services/api/tests/hints/test_hints.py`

**Implementation scope**

- Implement the approved turn contract with account/problem/version ownership, expiration and deletion.
- Apply per-turn and aggregate context/token limits before each model request.
- Invalidate client state on account/problem changes using the existing cancellation pattern.

**Acceptance criteria**

- A second account cannot read, append or delete another conversation.
- Expired or maximum-turn conversations stop without external work.
- No hidden tests or worker credentials can be represented in stored turns.

**Validation required**

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q; npm run typecheck

**Out of scope**

- Cross-problem permanent memory
- Training from conversation content

**Risk and review**

Conversation history can become an uncontrolled source of retained personal data.

</details>

<a id="sai-b062"></a>
<details>
<summary>81. SAI-B062: Add a consented concept-check interaction with bounded feedback [pending]</summary>

**Priority:** P2 · **Phase:** AI-2 consented tutor and debugger · **Area:** Evidence-oriented tutoring.

**Suggested role:** Teaching product engineer.

**Prerequisites:** [SAI-B060](#sai-b060), [SAI-B061](#sai-b061), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Receiving a hint does not show that a learner understands the concept; a small follow-up can collect observable reasoning without assigning unsupported ability labels.

**Target paths / responsibility**

- `apps/web/features/hints/account-hint.tsx`
- `apps/web/features/hints/api.ts`
- `services/api/solver_api/features/hints/service.py`
- `tests/e2e/hints/hints.spec.ts`

**Implementation scope**

- Offer an optional single concept question tied to the selected public problem and hint level.
- Accept a bounded learner explanation and return rubric-linked feedback with uncertainty.
- Allow skip/stop and preserve authored practice when the service is unavailable.

**Acceptance criteria**

- No answer is submitted without an explicit learner action.
- Feedback distinguishes a rubric observation from a diagnosis of learner ability.
- Question, answer and feedback obey the existing conversation/usage limits.

**Validation required**

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q; npm run test:e2e -- tests/e2e/hints/hints.spec.ts --workers=1

**Out of scope**

- Automated grading of overall intelligence
- Forced quizzes before submissions

**Risk and review**

A model-generated rubric may be wrong; reviewed questions and appeal/skip behavior are necessary.

</details>

<a id="sai-b063"></a>
<details>
<summary>82. SAI-B063: Collect minimal account-owned hint quality feedback [pending]</summary>

**Priority:** P2 · **Phase:** AI-2 consented tutor and debugger · **Area:** AI feedback and correction.

**Suggested role:** Full-stack product engineer.

**Prerequisites:** [SAI-B053](#sai-b053), [SAI-B059](#sai-b059), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Pilot quality reports need a way to identify confusing, incorrect or spoiler-heavy hints without collecting unrelated source or inventing learning metrics.

**Target paths / responsibility**

- `apps/web/features/hints/account-hint.tsx`
- `services/api/solver_api/features/hints/service.py`
- `services/api/solver_api/main.py`
- `docs/governance/DATA_AND_LICENSES.md`

**Implementation scope**

- Add bounded helpful/incorrect/spoiler feedback keyed to an owned generation ID.
- Deduplicate submissions, constrain optional text and define correction/retention ownership.
- Expose aggregate review counts separately from model correctness or learning claims.

**Acceptance criteria**

- Feedback cannot reference another account's private run.
- One account/run/action cannot inflate aggregate counts through retries.
- Logs and exports omit account tokens and editor source.

**Validation required**

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q; npm run typecheck

**Out of scope**

- Training automatically from feedback
- Public account rankings

**Risk and review**

Self-selected ratings are product feedback, not a controlled educational study.

</details>

<a id="sai-b064"></a>
<details>
<summary>83. SAI-B064: Define explicit source-sharing consent and owned debugger input [pending]</summary>

**Priority:** P1 · **Phase:** AI-2 consented tutor and debugger · **Area:** Debugger privacy boundary.

**Suggested role:** Privacy and backend authorization engineer.

**Prerequisites:** [SAI-B042](#sai-b042), [SAI-B049](#sai-b049), [SAI-B056](#sai-b056), [SAI-B060](#sai-b060), [SAI-B001](#sai-b001).

**Problem / missing behavior**

The current public-only hint contract intentionally excludes source. A debugger needs a separate deliberate source-sharing boundary rather than reading drafts or stored submissions implicitly.

**Target paths / responsibility**

- `services/api/solver_api/features/submissions/store.py`
- `services/api/solver_api/features/hints/service.py`
- `apps/web/features/practice/code-pane.tsx`
- `docs/governance/DATA_AND_LICENSES.md`

**Implementation scope**

- Specify bounded language/source/public-evidence input with a distinct disclosure and explicit user action.
- Resolve stored source only through existing owned-submission checks.
- Record exact source hash and consent version; prohibit background keystroke upload.

**Acceptance criteria**

- Foreign submission IDs and forged ownership fields are rejected before model admission.
- No source leaves the browser/API without the debugger-specific action and consent.
- Oversized/unsupported-language input has a stable failure with zero model calls.

**Validation required**

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints services/api/tests/submissions -q; npm run typecheck

**Out of scope**

- Implicit training consent
- Reading other users' solutions or private grading tests

**Risk and review**

Source can contain personal information or secrets; the product must disclose this additional processing.

</details>

<a id="sai-b065"></a>
<details>
<summary>84. SAI-B065: Build a public-only execution evidence projection for debugging [pending]</summary>

**Priority:** P1 · **Phase:** AI-2 consented tutor and debugger · **Area:** Safe debugger evidence.

**Suggested role:** Judge/API security engineer.

**Prerequisites:** [SAI-B044](#sai-b044), [SAI-B064](#sai-b064), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Worker/API summaries already protect private grading details. Model debugging needs a separately allowlisted evidence projection that cannot accidentally export hidden inputs or raw diagnostics.

**Target paths / responsibility**

- `services/api/solver_api/features/submissions/store.py`
- `services/judge/solver_judge/control/worker.py`
- `services/judge/solver_judge/grading/cases.py`
- `services/api/tests/submissions/test_submissions.py`

**Implementation scope**

- Define structured evidence for owned public sample runs and capped compiler/runtime categories.
- Preserve independent worker and API sanitization; reject private-test manifests and opaque raw logs.
- Associate evidence with source/problem/runtime hashes.

**Acceptance criteria**

- Hidden input/output and credential sentinels never enter model evidence.
- Evidence with a mismatched source/problem hash is refused.
- Output limits apply before storage and provider serialization.

**Validation required**

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/submissions services/judge/tests/control -q

**Out of scope**

- Exporting private failing tests
- Weakening current safe_summary controls

**Risk and review**

An error message can contain hostile program-written text and must remain untrusted.

</details>

<a id="sai-b066"></a>
<details>
<summary>85. SAI-B066: Return debugger hypotheses separately from observed failures [pending]</summary>

**Priority:** P2 · **Phase:** AI-2 consented tutor and debugger · **Area:** Evidence-backed debugging.

**Suggested role:** AI debugging engineer.

**Prerequisites:** [SAI-B048](#sai-b048), [SAI-B050](#sai-b050), [SAI-B064](#sai-b064), [SAI-B065](#sai-b065), [SAI-B001](#sai-b001).

**Problem / missing behavior**

A wrong-answer verdict alone does not reveal its cause, and generated explanations can invent failure evidence or overstate a proposed correction.

**Target paths / responsibility**

- `services/api/solver_api/features/hints/service.py`
- `services/api/solver_api/main.py`
- `docs/product/AI_SOLVER.md`
- `services/api/tests/hints/test_hints.py`

**Implementation scope**

- Implement a bounded debug response with observed evidence references, hypotheses, suggested correction and unverified claims.
- Validate cited evidence IDs and treat unmatched claims as hypotheses or reject them.
- Reuse admission, privacy, token and timeout controls rather than adding an independent unbounded loop.

**Acceptance criteria**

- No response can cite evidence not supplied to that run.
- A correction is never labeled tested before the isolated runner has returned matching evidence.
- Provider outage produces a stable failure and leaves source/history intact.

**Validation required**

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q

**Out of scope**

- Guaranteed root-cause detection
- Executing suggested code in API processes

**Risk and review**

Well-written model explanations can sound more certain than the supplied evidence allows.

</details>

<a id="sai-b067"></a>
<details>
<summary>86. SAI-B067: Show a source-hash-bound debugger patch preview with explicit apply [pending]</summary>

**Priority:** P2 · **Phase:** AI-2 consented tutor and debugger · **Area:** Debugger editor UX.

**Suggested role:** Frontend editor engineer.

**Prerequisites:** [SAI-B064](#sai-b064), [SAI-B066](#sai-b066), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Model suggestions must not overwrite a learner's newer draft or silently change another problem/language after an asynchronous request.

**Target paths / responsibility**

- `apps/web/features/practice/code-pane.tsx`
- `apps/web/features/practice/workspace.tsx`
- `apps/web/features/hints/api.ts`
- `tests/e2e/practice/practice.spec.ts`

**Implementation scope**

- Display an inert before/after patch tied to the exact requested source hash.
- Require explicit apply/copy and refuse automatic application if the current draft changed.
- Preserve undo behavior and existing per-problem/language draft isolation.

**Acceptance criteria**

- Editing while a request runs causes a visible stale-patch state rather than overwrite.
- Switching account/problem/language cannot apply a prior suggestion.
- Dismiss/apply/copy actions never execute code or submit a job implicitly.

**Validation required**

- Future authorized check: npm run typecheck; npm run test:e2e -- tests/e2e/practice/practice.spec.ts --workers=1

**Out of scope**

- Autonomous editing agents
- Automatic submission of generated code

**Risk and review**

Applying a correct-looking diff can still introduce a bug; retain original source and label evidence limits.

</details>

<a id="sai-b068"></a>
<details>
<summary>87. SAI-B068: Version authorized solver problem specifications and evaluation modes [pending]</summary>

**Priority:** P1 · **Phase:** AI-3 bounded candidate solver · **Area:** Solver input contracts.

**Suggested role:** Backend contract engineer.

**Prerequisites:** [SAI-B042](#sai-b042), [SAI-B049](#sai-b049), [SAI-B064](#sai-b064), [SAI-B027](#sai-b027), [SAI-B001](#sai-b001).

**Problem / missing behavior**

A candidate solver needs immutable problem/context identity and explicit allowed evaluation modes; a slug alone cannot describe changed constraints or permissions.

**Target paths / responsibility**

- `services/api/solver_api/features/catalog/models.py`
- `services/api/solver_api/features/catalog/content.py`
- `services/api/solver_api/features/hints/service.py`
- `docs/product/AI_SOLVER.md`

**Implementation scope**

- Project B027 canonical immutable problem/grader revision into a bounded public ProblemSpec with context fingerprint, requested runtime and rights/assistance scope; do not create a competing content-version authority.
- Keep private grading manifests outside model serialization.
- Document how current seed catalog records produce this specification without changing public catalog semantics.

**Acceptance criteria**

- Changed public task content creates a different immutable specification ID.
- Unsupported runtime or unauthorized evaluation mode is rejected before generation.
- Serialized specifications contain no private cases or account credentials.

**Validation required**

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/catalog services/api/tests/hints -q

**Out of scope**

- Bulk import of archive benchmarks
- Inventing permission metadata for existing third-party data

**Risk and review**

Version labels without immutable content and rights metadata are not reproducible inputs.

</details>

<a id="sai-b069"></a>
<details>
<summary>88. SAI-B069: Generate a bounded algorithm-plan record before candidate code [pending]</summary>

**Priority:** P2 · **Phase:** AI-3 bounded candidate solver · **Area:** Candidate planning.

**Suggested role:** AI solver engineer.

**Prerequisites:** [SAI-B045](#sai-b045), [SAI-B048](#sai-b048), [SAI-B050](#sai-b050), [SAI-B068](#sai-b068), [SAI-B001](#sai-b001).

**Problem / missing behavior**

CodeSIM provides useful planning/simulation ideas, but its archived framework mixes provider calls and unsafe evaluation. Solver AI needs a small original typed plan stage.

**Target paths / responsibility**

- `services/api/solver_api/features/hints/service.py`
- `docs/product/AI_SOLVER.md`
- `AnalyseFuture/extracted/CodeGenerator-master/src/promptings/CodeSIM.py`

**Implementation scope**

- Define concise algorithm summary, assumptions, invariant and claimed complexity fields with strict bounds.
- Record model/prompt/problem identity and consume the shared run budget.
- Treat simulation text as a model claim rather than execution or proof.

**Acceptance criteria**

- Malformed/oversized plans fail before candidate generation.
- Every plan is attributable to an immutable specification and prompt version.
- No prompt requests hidden chain-of-thought or claims that simulated samples prove correctness.

**Validation required**

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q; static comparison to the archived design without executing it.

**Out of scope**

- Modifying the immutable archive
- Formal verification of arbitrary algorithms

**Risk and review**

A convincing plan may be wrong and must not bypass isolated tests.

</details>

<a id="sai-b070"></a>
<details>
<summary>89. SAI-B070: Normalize bounded source candidates without archive parser assumptions [pending]</summary>

**Priority:** P1 · **Phase:** AI-3 bounded candidate solver · **Area:** Candidate generation.

**Suggested role:** AI/backend engineer.

**Prerequisites:** [SAI-B046](#sai-b046), [SAI-B068](#sai-b068), [SAI-B069](#sai-b069), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Archived fenced-code parsers assume matching blocks and can index an empty result. Candidate source must have a deterministic language, byte cap and provenance before execution.

**Target paths / responsibility**

- `services/api/solver_api/features/hints/service.py`
- `services/api/solver_api/features/submissions/store.py`
- `AnalyseFuture/extracted/CodeGenerator-master/src/utils/parse.py`
- `services/api/tests/hints/test_hints.py`

**Implementation scope**

- Define a candidate artifact schema with exact source bytes/hash and supported runtime identity.
- Accept one reviewed response form; reject ambiguous multiple blocks, missing source and excess bytes.
- Count rejected generation against the run's recorded attempts/usage without executing it.

**Acceptance criteria**

- Empty, mismatched-fence, multiple-code and oversized fixtures have deterministic outcomes.
- Source hash is stable over the exact bytes later sent to the judge.
- Unsupported languages never reach the execution queue.

**Validation required**

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints services/api/tests/submissions -q

**Out of scope**

- Running source during extraction
- Repairing archived parsers in place

**Risk and review**

Aggressive source cleanup can silently alter the program the learner thinks was tested.

</details>

<a id="sai-b071"></a>
<details>
<summary>90. SAI-B071: Route authorized AI candidates through the existing isolated judge boundary [pending]</summary>

**Priority:** P1 · **Phase:** AI-3 bounded candidate solver · **Area:** Solver-to-judge integration.

**Suggested role:** Judge and backend integration engineer.

**Prerequisites:** [SAI-B050](#sai-b050), [SAI-B051](#sai-b051), [SAI-B065](#sai-b065), [SAI-B068](#sai-b068), [SAI-B070](#sai-b070), [SAI-B121](#sai-b121), [SAI-B123](#sai-b123), [SAI-B125](#sai-b125), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Generated candidates currently have no active execution integration. Archive host evaluators cannot be imported safely, and model runs must not masquerade as learner submissions.

**Target paths / responsibility**

- `services/api/solver_api/features/submissions/store.py`
- `services/api/solver_api/main.py`
- `services/judge/solver_judge/control/worker.py`
- `services/judge/solver_judge/control/runner.py`

**Implementation scope**

- Define explicit candidate-job ownership/attribution while reusing queue leases, runtime readiness, limits and cleanup.
- Allow only the evaluation modes approved by ProblemSpec and charge test jobs to a shared run budget.
- Return the public-only evidence projection; preserve normal learner history semantics.

**Acceptance criteria**

- Missing isolation/readiness refuses candidate jobs with no host fallback.
- One account cannot poll or cancel another account's candidate run.
- Matching source/runtime hashes connect each result to one candidate; private test data never reaches model context.

**Validation required**

- Future authorized check: npm run test:judge:integration; uv run --project services/api --frozen pytest services/api/tests/submissions services/api/tests/hints -q

**Out of scope**

- Executing programs in the API
- Bypassing worker budgets for research users

**Risk and review**

Generated code is equally untrusted as learner code and may target the result protocol.

</details>

<a id="sai-b072"></a>
<details>
<summary>91. SAI-B072: Implement a finite repair state machine with one shared run budget [pending]</summary>

**Priority:** P1 · **Phase:** AI-3 bounded candidate solver · **Area:** Bounded solver repair.

**Suggested role:** Backend workflow engineer.

**Prerequisites:** [SAI-B054](#sai-b054), [SAI-B066](#sai-b066), [SAI-B069](#sai-b069), [SAI-B071](#sai-b071), [SAI-B001](#sai-b001).

**Problem / missing behavior**

A plan/generate/test/repair loop can consume unlimited calls and execution jobs unless state transitions and aggregate stop conditions are explicit.

**Target paths / responsibility**

- `services/api/solver_api/features/hints/service.py`
- `services/api/solver_api/features/submissions/store.py`
- `docs/product/AI_SOLVER.md`
- `services/api/tests/hints/test_hints.py`

**Implementation scope**

- Model generation, queued/running evaluation, repair, cancellation and terminal states explicitly.
- Limit total candidates, repair attempts, tokens, test jobs, elapsed time and reserved spend across the complete run.
- Feed back only approved public evidence and preserve every attempted candidate hash.

**Acceptance criteria**

- Every transition is covered by a deterministic state-machine fixture.
- Exhausting any limit stops new provider and judge work.
- Restart/retry/cancel cannot restart a terminal run or duplicate reserved work.

**Validation required**

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints services/api/tests/submissions -q

**Out of scope**

- Unlimited autonomous repair
- Leaking private failing cases as feedback

**Risk and review**

Per-step limits are insufficient when aggregate attempts can still grow.

</details>

<a id="sai-b073"></a>
<details>
<summary>92. SAI-B073: Rank candidates by explicit execution evidence with deterministic ties [pending]</summary>

**Priority:** P2 · **Phase:** AI-3 bounded candidate solver · **Area:** Candidate ranking.

**Suggested role:** AI evaluation engineer.

**Prerequisites:** [SAI-B070](#sai-b070), [SAI-B071](#sai-b071), [SAI-B072](#sai-b072), [SAI-B001](#sai-b001).

**Problem / missing behavior**

phi-code ranks sample passes and embedding similarity, but similarity is not correctness and zero or incomparable test sets must not produce an acceptance claim.

**Target paths / responsibility**

- `services/api/solver_api/features/hints/service.py`
- `docs/product/AI_SOLVER.md`
- `AnalyseFuture/extracted/phi-code-main/solver/terminal.py`

**Implementation scope**

- Define versioned comparable-evidence requirements and deterministic ranking/tie rules.
- Label untested, failed and finite-check-passed candidates separately.
- Keep embedding or model-confidence scores optional research signals outside correctness claims.

**Acceptance criteria**

- Ranking is stable across repeated ordering of identical records.
- Candidates with different test manifests are not compared as equivalent evidence.
- Zero-test candidates cannot be labeled accepted or preferred on correctness grounds.

**Validation required**

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints -q; review adversarial ranking fixtures.

**Out of scope**

- Claiming mathematical verification
- Loading the archived ranker model

**Risk and review**

Optimizing public tests can overfit them; show exactly which finite checks informed selection.

</details>

<a id="sai-b074"></a>
<details>
<summary>93. SAI-B074: Create a reproducible offline solver evaluation run manifest [pending]</summary>

**Priority:** P1 · **Phase:** AI-4 evaluation and research gates · **Area:** Solver evaluation.

**Suggested role:** Research evaluation engineer.

**Prerequisites:** [SAI-B053](#sai-b053), [SAI-B068](#sai-b068), [SAI-B072](#sai-b072), [SAI-B073](#sai-b073), [SAI-B001](#sai-b001).

**Problem / missing behavior**

The repository has historical upstream claims but no current model evaluation harness that pins tasks, prompts, runtime and budgets for fair strategy comparisons.

**Target paths / responsibility**

- `docs/research/MODEL_DATA_EVALUATION.md`
- `docs/product/AI_SOLVER.md`
- `services/api/solver_api/features/hints/service.py`
- `AnalyseFuture/repository-inventory/FEATURE_INVENTORY.txt`

**Implementation scope**

- Define an offline manifest and bounded harness using only approved tasks and existing isolated execution.
- Compare single-candidate, planning and repair/ranking variants under explicitly comparable budgets.
- Record model/prompt/runtime/task versions, seeds, usage, latency, failures and termination reasons.

**Acceptance criteria**

- A deterministic fake-provider run can be replayed without external calls.
- Reports separate completed, failed, skipped and unexecuted tasks.
- pass@1/pass@k include the stated sampling procedure, eligible sample counts and uncertainty; no gains are invented.

**Validation required**

- Future authorized check: targeted harness tests added beside services/api/tests/hints; any live evaluation requires a separately approved manifest and spend cap.

**Out of scope**

- Downloading large benchmark corpora by default
- Claiming the upstream scores were reproduced

**Risk and review**

Unequal inference budgets or contaminated tasks can make a comparison misleading.

</details>

<a id="sai-b075"></a>
<details>
<summary>94. SAI-B075: Admit only reviewed differential and metamorphic test specifications [pending]</summary>

**Priority:** P1 · **Phase:** AI-4 evaluation and research gates · **Area:** Authorized test generation.

**Suggested role:** Problem author and judge evaluation engineer.

**Prerequisites:** [SAI-B068](#sai-b068), [SAI-B071](#sai-b071), [SAI-B074](#sai-b074), [SAI-B001](#sai-b001).

**Problem / missing behavior**

More generated inputs do not establish correctness when the reference oracle or metamorphic relationship is wrong; model-produced expectations may share the candidate's error.

**Target paths / responsibility**

- `services/judge/solver_judge/grading/cases.py`
- `services/judge/solver_judge/sandbox/harness.py`
- `docs/research/MODEL_DATA_EVALUATION.md`
- `services/judge/tests/grading/test_cases.py`

**Implementation scope**

- Define versioned reviewed oracle/relation manifests tied to original or permissioned tasks.
- Bound generated case counts, seed space and execution resources.
- Keep expected answers outside learner containers and forbid model assertions from becoming trusted oracles automatically.

**Acceptance criteria**

- Invalid relation/oracle versions are refused before candidate scoring.
- Reference fixtures independently expose a deliberately wrong candidate.
- Run reports distinguish reviewed generated cases from public samples and private grading.

**Validation required**

- Future authorized check: uv run --project services/api --frozen pytest services/judge/tests/grading -q; approved isolated oracle integration fixtures.

**Out of scope**

- Universal test adequacy guarantees
- Publishing private grader answers

**Risk and review**

A faulty oracle can confidently reject correct programs or accept incorrect ones.

</details>

<a id="sai-b076"></a>
<details>
<summary>95. SAI-B076: Reduce consented public counterexamples under a finite execution budget [pending]</summary>

**Priority:** P2 · **Phase:** AI-4 evaluation and research gates · **Area:** Counterexample debugging.

**Suggested role:** Judge tooling engineer.

**Prerequisites:** [SAI-B064](#sai-b064), [SAI-B065](#sai-b065), [SAI-B071](#sai-b071), [SAI-B075](#sai-b075), [SAI-B001](#sai-b001).

**Problem / missing behavior**

A large permitted failing input can be hard to explain; reduction is useful only if it preserves task validity and the observed failure without exposing private cases.

**Target paths / responsibility**

- `services/judge/solver_judge/grading/cases.py`
- `services/api/solver_api/features/hints/service.py`
- `apps/web/features/practice/workspace.tsx`
- `docs/product/AI_SOLVER.md`

**Implementation scope**

- Implement one reviewed task-specific reducer with explicit validity checks and execution ceiling.
- Accept only user-supplied or approved public/generated inputs with a trustworthy failure predicate.
- Label the result as a smaller observed counterexample, not a globally minimal one.

**Acceptance criteria**

- Every returned input remains valid and reproduces the same selected failure.
- Exhausted budgets return the best observed input with a clear stop reason.
- Private test IDs/manifests are rejected at intake.

**Validation required**

- Future authorized check: task-scoped grading fixtures in services/judge/tests/grading and debugger contract fixtures in services/api/tests/hints.

**Out of scope**

- General-purpose automatic minimization for every problem
- Recovering hidden tests

**Risk and review**

Naive reduction can leave the input domain or change the failure being explained.

</details>

<a id="sai-b081"></a>
<details>
<summary>96. SAI-B081: Implement contest lifecycle and authoritative event timing [pending]</summary>

**Priority:** P1 · **Phase:** contest-foundation · **Area:** contests.

**Suggested role:** Backend engineer with contest product owner.

**Prerequisites:** [SAI-B003](#sai-b003), [SAI-B027](#sai-b027), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Contests are proposed but no active event lifecycle or authoritative clock exists.

**Target paths / responsibility**

- `services/api/solver_api/main.py`
- `services/api/solver_api/features`
- `services/api/tests`
- `docs/product/PRODUCT_REQUIREMENTS.md`

**Implementation scope**

- Add a proposed contests feature module with draft, scheduled, running, frozen and finished transitions.
- Specify UTC storage, inclusive/exclusive start/end boundaries and organizer-only transition rules before adding routes.

**Acceptance criteria**

- A transition table rejects every invalid state change.
- Boundary tests cover one instant before, at and after start/end; browser time cannot extend an event.
- Practice submissions remain unaffected when no contest is selected.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/contests/test_lifecycle.py
- uv run --project services/api --frozen ruff check services/api

**Out of scope**

- Rated public events
- External clock services or paid infrastructure

**Risk and review**

Ambiguous deadlines can accept late work or invalidate legitimate attempts.

</details>

<a id="sai-b082"></a>
<details>
<summary>97. SAI-B082: Add permissioned contest registration and eligibility checks [pending]</summary>

**Priority:** P1 · **Phase:** contest-foundation · **Area:** contests.

**Suggested role:** Backend engineer.

**Prerequisites:** [SAI-B081](#sai-b081), [SAI-B001](#sai-b001).

**Problem / missing behavior**

An event needs explicit participant eligibility separate from ordinary account access.

**Target paths / responsibility**

- `services/api/solver_api/features/identity`
- `services/api/solver_api/main.py`
- `services/api/tests`

**Implementation scope**

- Add proposed contest registration records and join/withdraw endpoints using the existing verified identity boundary.
- Enforce event visibility, registration windows and organizer/participant permissions server-side.

**Acceptance criteria**

- An unauthenticated user receives 401 and an ineligible authenticated user receives 403.
- Duplicate registration is idempotent; withdrawal after a locked roster follows the documented policy.
- One user cannot alter another registration or enumerate a private participant list.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/contests/test_registration.py
- npm run test:auth

**Out of scope**

- New identity provider
- Payment-based qualification or automatic real-world identity verification

**Risk and review**

Registration leakage or weak checks could expose private events.

</details>

<a id="sai-b083"></a>
<details>
<summary>98. SAI-B083: Freeze versioned problem sets for each contest [pending]</summary>

**Priority:** P1 · **Phase:** contest-foundation · **Area:** contests.

**Suggested role:** Backend engineer and problem curator.

**Prerequisites:** [SAI-B081](#sai-b081), [SAI-B027](#sai-b027), [SAI-B029](#sai-b029), [SAI-B001](#sai-b001).

**Problem / missing behavior**

A contest must not silently change when the practice catalog or grading cases are updated.

**Target paths / responsibility**

- `services/api/solver_api/features/catalog`
- `services/api/solver_api/main.py`
- `services/api/tests`
- `services/judge/solver_judge/grading`

**Implementation scope**

- Add a proposed immutable contest problem-set reference with ordered problem/version identifiers.
- Reject set edits after the documented publication lock and record the permitted correction process.

**Acceptance criteria**

- A scheduled event resolves every configured problem version before it opens.
- Changing the active practice problem does not alter an already locked event.
- Participants cannot read unreleased statements or private grading metadata through contest endpoints.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/contests/test_problem_sets.py
- uv run --project services/api --frozen pytest services/judge/tests/grading/test_cases.py

**Out of scope**

- Bulk competitor content import
- Interactive problem types

**Risk and review**

Incorrect version linkage changes fairness and reproducibility.

</details>

<a id="sai-b084"></a>
<details>
<summary>99. SAI-B084: Implement deterministic ICPC scoring as a tested pure calculation [pending]</summary>

**Priority:** P1 · **Phase:** contest-foundation · **Area:** contests.

**Suggested role:** Backend engineer with experienced contest reviewer.

**Prerequisites:** [SAI-B081](#sai-b081), [SAI-B083](#sai-b083), [SAI-B001](#sai-b001).

**Problem / missing behavior**

The repository has verdicts but no ICPC score or penalty semantics.

**Target paths / responsibility**

- `services/api/solver_api/features`
- `services/api/tests`
- `docs/product/PRODUCT_REQUIREMENTS.md`

**Implementation scope**

- Add a proposed scoring module with solved-count priority, configurable wrong-attempt penalty and explicit tie ordering.
- Define how pending, canceled, compiler-error and rejudged attempts affect each problem.

**Acceptance criteria**

- Hand-calculated fixtures cover tied solved counts, multiple wrong attempts, first acceptance and submissions after acceptance.
- The same event ledger always yields identical standings independent of input row order.
- Pending/untrusted worker messages cannot create an accepted score.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/contests/test_icpc_scoring.py

**Out of scope**

- Global user rating
- IOI partial scoring

**Risk and review**

A small scoring rule mistake can change winners.

</details>

<a id="sai-b085"></a>
<details>
<summary>100. SAI-B085: Add participant and organizer scoreboard projections with freeze rules [pending]</summary>

**Priority:** P1 · **Phase:** contest-foundation · **Area:** contests.

**Suggested role:** Backend engineer.

**Prerequisites:** [SAI-B084](#sai-b084), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Contest standings need different visibility during a scoreboard freeze.

**Target paths / responsibility**

- `services/api/solver_api/main.py`
- `services/api/solver_api/features`
- `services/api/tests`

**Implementation scope**

- Build proposed public/participant and organizer projections from the scored event ledger.
- Apply freeze/unfreeze rules before serialization; do not send hidden verdicts for the browser to hide.

**Acceptance criteria**

- A participant response contains no post-freeze verdict, timestamp detail or score that reveals the hidden result.
- Authorized organizers see the complete projection and unauthorized users receive 403.
- Unfreezing produces the same final standings as an unfrozen full replay.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/contests/test_scoreboard_projection.py

**Out of scope**

- WebSockets
- Public rating formulas

**Risk and review**

Aggregate fields can accidentally leak frozen results.

</details>

<a id="sai-b086"></a>
<details>
<summary>101. SAI-B086: Connect contest submissions to event eligibility and immutable attempt context [pending]</summary>

**Priority:** P1 · **Phase:** contest-foundation · **Area:** contests.

**Suggested role:** Backend engineer.

**Prerequisites:** [SAI-B081](#sai-b081), [SAI-B082](#sai-b082), [SAI-B083](#sai-b083), [SAI-B084](#sai-b084), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Existing owned attempts cannot yet prove which contest, problem version or event window they belong to.

**Target paths / responsibility**

- `services/api/solver_api/features/submissions/store.py`
- `services/api/solver_api/main.py`
- `services/api/tests/submissions`
- `services/judge/solver_judge/control/worker.py`

**Implementation scope**

- Add a proposed optional contest context without changing ordinary practice behavior.
- Bind event eligibility, authoritative receipt time, problem version and scoring identity atomically when accepting a request.

**Acceptance criteria**

- Early, late, unregistered and mismatched-problem attempts are rejected before queuing.
- Idempotent retries preserve one receipt time and one scored attempt.
- Queued work finishing after the deadline is handled by the documented receipt-time policy; practice regression tests pass.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/contests/test_contest_submissions.py services/api/tests/submissions/test_submissions.py
- uv run --project services/api --frozen pytest services/judge/tests/control/test_worker.py

**Out of scope**

- Changing the worker trust boundary
- Multi-database distributed transactions

**Risk and review**

Race conditions between registration, deadline and enqueue could create unfair attempts.

</details>

<a id="sai-b087"></a>
<details>
<summary>102. SAI-B087: Implement isolated virtual-contest sessions with personal start times [pending]</summary>

**Priority:** P2 · **Phase:** contest-experience · **Area:** contests.

**Suggested role:** Full-stack engineer.

**Prerequisites:** [SAI-B081](#sai-b081), [SAI-B083](#sai-b083), [SAI-B084](#sai-b084), [SAI-B086](#sai-b086), [SAI-B001](#sai-b001).

**Problem / missing behavior**

A learner cannot replay a contest under a personal timer without changing the shared event.

**Target paths / responsibility**

- `services/api/solver_api/main.py`
- `services/api/solver_api/features`
- `services/api/tests`
- `apps/web/app`

**Implementation scope**

- Add proposed virtual-session state referencing an immutable published problem set and duration.
- Keep personal timing/scoring separate from official standings and provide a recoverable resume view.

**Acceptance criteria**

- Two learners starting at different times receive independent deadlines and standings.
- Reloading or opening a second tab cannot reset or extend a started session.
- Virtual attempts never appear in official rankings.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/contests/test_virtual_sessions.py
- npx playwright test tests/e2e/contests/virtual.spec.ts --workers=2

**Out of scope**

- Anti-cheat guarantees for self-directed practice
- Paid virtual events

**Risk and review**

Shared identifiers could mix personal and official attempts.

</details>

<a id="sai-b088"></a>
<details>
<summary>103. SAI-B088: Add locked ICPC team rosters and event membership rules [pending]</summary>

**Priority:** P2 · **Phase:** contest-experience · **Area:** teams.

**Suggested role:** Backend engineer.

**Prerequisites:** [SAI-B082](#sai-b082), [SAI-B001](#sai-b001).

**Problem / missing behavior**

ICPC-style participation needs explicit team identity rather than caller-supplied teammate IDs.

**Target paths / responsibility**

- `services/api/solver_api/features/identity`
- `services/api/solver_api/main.py`
- `services/api/tests`

**Implementation scope**

- Implement proposed invitation, acceptance, captain and roster-lock rules for a contest team.
- Enforce team-size limits and the policy for one user joining multiple teams in the same event.

**Acceptance criteria**

- Only an invited account can accept its own invitation.
- A locked roster rejects membership changes except the documented organizer correction.
- Concurrent acceptance cannot exceed the configured team-size or single-team limit.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/contests/test_team_rosters.py

**Out of scope**

- Organization-wide employee directories
- Voice/video collaboration

**Risk and review**

Membership races or invitation leakage could grant unintended team access.

</details>

<a id="sai-b089"></a>
<details>
<summary>104. SAI-B089: Scope contest attempts and source visibility to authorized team members [pending]</summary>

**Priority:** P2 · **Phase:** contest-experience · **Area:** teams.

**Suggested role:** Backend engineer with privacy reviewer.

**Prerequisites:** [SAI-B086](#sai-b086), [SAI-B088](#sai-b088), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Existing submissions are individual-owned; team sharing must be deliberate and event-bounded.

**Target paths / responsibility**

- `services/api/solver_api/features/submissions/store.py`
- `services/api/solver_api/main.py`
- `apps/web/features/submissions`
- `services/api/tests`

**Implementation scope**

- Add proposed team-scoring attribution and explicit source/history visibility rules for event members.
- Preserve personal practice ownership and define access after roster correction or event completion.

**Acceptance criteria**

- Eligible teammates can view only the event attempts allowed by policy.
- A member of another team and a former unauthorized member cannot fetch source through detail/list endpoints.
- The event scoreboard attributes retries and idempotent attempts to exactly one team.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/contests/test_team_attempts.py services/api/tests/submissions/test_submissions.py
- npx playwright test tests/e2e/contests/team-history.spec.ts --workers=2

**Out of scope**

- Shared live code editing
- Global sharing of private submissions

**Risk and review**

Expanding ownership from a user to a team can leak private code.

</details>

<a id="sai-b090"></a>
<details>
<summary>105. SAI-B090: Enforce contest assistance policy across hint and submission routes [pending]</summary>

**Priority:** P1 · **Phase:** contest-experience · **Area:** contest-integrity.

**Suggested role:** Backend engineer and contest policy owner.

**Prerequisites:** [SAI-B081](#sai-b081), [SAI-B086](#sai-b086), [SAI-B089](#sai-b089), [SAI-B049](#sai-b049), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Contest rules require server-enforced assistance restrictions; hiding the hint panel is insufficient.

**Target paths / responsibility**

- `services/api/solver_api/features/hints/service.py`
- `services/api/solver_api/main.py`
- `apps/web/features/hints`
- `services/api/tests/hints`
- `apps/web/features/practice/workspace.tsx`

**Implementation scope**

- Add proposed explicit event assistance modes and policy evaluation shared by relevant API entrypoints.
- Show the effective policy in the workspace and permit post-event review only when event rules allow it.

**Acceptance criteria**

- Direct authenticated requests cannot obtain disallowed assistance during a restricted event.
- Allowed practice and post-event modes retain correct authored/model provenance.
- Policy changes are audited and cannot silently weaken an already active event.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/contests/test_assistance_policy.py services/api/tests/hints/test_hints.py
- npx playwright test tests/e2e/contests/assistance-policy.spec.ts --workers=2

**Out of scope**

- Detecting all off-platform AI use
- Changing model-provider budgets

**Risk and review**

Inconsistent checks across endpoints could bypass event policy.

</details>

<a id="sai-b091"></a>
<details>
<summary>106. SAI-B091: Build an organizer workflow for contest draft, preview and publication [pending]</summary>

**Priority:** P2 · **Phase:** contest-experience · **Area:** contest-admin.

**Suggested role:** Full-stack engineer.

**Prerequisites:** [SAI-B081](#sai-b081), [SAI-B082](#sai-b082), [SAI-B083](#sai-b083), [SAI-B085](#sai-b085), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Organizers have no supported interface to prepare a validated contest.

**Target paths / responsibility**

- `apps/web/app`
- `apps/web/features`
- `services/api/solver_api/main.py`
- `tests/e2e`

**Implementation scope**

- Create a proposed organizer feature with draft editing, problem ordering, timing and assistance-policy preview.
- Require explicit publication confirmation showing the final immutable rules and validation errors.

**Acceptance criteria**

- A participant cannot access organizer mutations even by calling their API directly.
- A draft with missing problem versions or invalid times cannot publish.
- A complete original-problem event can be prepared, previewed and published in an end-to-end test.

**Validation required**

- npx playwright test tests/e2e/contests/organizer.spec.ts --workers=2
- npm run typecheck

**Out of scope**

- New design system
- Bulk third-party problem ingestion

**Risk and review**

Administrative forms can expose mutation permissions or conceal critical rules.

</details>

<a id="sai-b092"></a>
<details>
<summary>107. SAI-B092: Implement audited contest rejudging with immutable verdict revisions [pending]</summary>

**Priority:** P1 · **Phase:** contest-corrections · **Area:** contest-admin.

**Suggested role:** Backend engineer and judge maintainer.

**Prerequisites:** [SAI-B085](#sai-b085), [SAI-B086](#sai-b086), [SAI-B091](#sai-b091), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Organizers need to correct grading errors without overwriting the evidence behind earlier standings.

**Target paths / responsibility**

- `services/api/solver_api/features/submissions/store.py`
- `services/api/solver_api/main.py`
- `services/judge/solver_judge/control/worker.py`
- `services/api/tests`

**Implementation scope**

- Add proposed authorized rejudge requests with reason, selected grading version and append-only result revision.
- Recompute affected standings from the chosen official revision while retaining prior visible audit history.

**Acceptance criteria**

- Repeated identical rejudge requests enqueue no duplicate active job.
- Unapproved/failed rejudges leave official standings unchanged.
- A completed approved rejudge changes the expected score and records actor, reason and prior revision reference.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/contests/test_rejudge.py
- uv run --project services/api --frozen pytest services/judge/tests/control/test_worker.py

**Out of scope**

- Deleting original verdicts
- User-controlled executable graders

**Risk and review**

A faulty correction can retroactively invalidate many results.

</details>

<a id="sai-b093"></a>
<details>
<summary>108. SAI-B093: Add contest clarification and appeal records with controlled disclosure [pending]</summary>

**Priority:** P2 · **Phase:** contest-corrections · **Area:** contest-admin.

**Suggested role:** Full-stack engineer and contest moderator.

**Prerequisites:** [SAI-B091](#sai-b091), [SAI-B092](#sai-b092), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Participants need a traceable correction channel that does not reveal another team’s private work.

**Target paths / responsibility**

- `services/api/solver_api/main.py`
- `apps/web/app`
- `apps/web/features`
- `services/api/tests`

**Implementation scope**

- Add proposed private participant questions, organizer responses and separately approved public clarifications.
- Link a grading appeal to an attempt/rejudge decision with bounded text and a visible state history.

**Acceptance criteria**

- A private clarification is visible only to its participant/team and authorized organizers.
- Publishing a clarification requires explicit organizer action and does not auto-copy private source.
- Appeal resolution links to the official result revision without modifying the original report.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/contests/test_clarifications.py
- npx playwright test tests/e2e/contests/clarifications.spec.ts --workers=2

**Out of scope**

- Unmoderated public chat
- Automatic AI adjudication

**Risk and review**

Support discussions can leak hidden cases or identifiable submissions.

</details>

<a id="sai-b094"></a>
<details>
<summary>109. SAI-B094: Deliver bounded scoreboard polling with consistent event revisions [pending]</summary>

**Priority:** P2 · **Phase:** contest-experience · **Area:** leaderboards.

**Suggested role:** Frontend engineer.

**Prerequisites:** [SAI-B085](#sai-b085), [SAI-B086](#sai-b086), [SAI-B088](#sai-b088), [SAI-B001](#sai-b001).

**Problem / missing behavior**

A leaderboard must refresh reliably without exposing frozen results or creating an unbounded request loop.

**Target paths / responsibility**

- `apps/web/app`
- `apps/web/features`
- `services/api/solver_api/main.py`
- `services/api/tests`
- `tests/e2e`

**Implementation scope**

- Add a proposed scoreboard view using bounded polling, conditional/versioned responses and explicit stale/error states.
- Render ties, team names and freeze state from server projections; cancel requests on navigation.

**Acceptance criteria**

- A response from an older event revision cannot overwrite a newer display.
- Polling stops on navigation and backs off after failures under fake-clock tests.
- Narrow-screen and keyboard flows expose the same frozen/public data as the API.

**Validation required**

- npx playwright test tests/e2e/contests/scoreboard.spec.ts --workers=2
- uv run --project services/api --frozen pytest services/api/tests/contests/test_scoreboard_projection.py

**Out of scope**

- WebSocket infrastructure
- Global rating or follower systems

**Risk and review**

Out-of-order updates and aggressive polling can harm fairness or availability.

</details>

<a id="sai-b095"></a>
<details>
<summary>110. SAI-B095: Create a reproducible contest rehearsal and official standings export [pending]</summary>

**Priority:** P1 · **Phase:** contest-corrections · **Area:** contest-release.

**Suggested role:** QA engineer and contest operator.

**Prerequisites:** [SAI-B090](#sai-b090), [SAI-B091](#sai-b091), [SAI-B092](#sai-b092), [SAI-B094](#sai-b094), [SAI-B001](#sai-b001).

**Problem / missing behavior**

A contest feature set needs an end-to-end operational gate rather than separate passing screens.

**Target paths / responsibility**

- `tests/e2e`
- `services/api/tests`
- `scripts/verification`
- `docs/onboarding/DEVELOPMENT.md`

**Implementation scope**

- Add a proposed deterministic rehearsal using only original fixtures: register, submit AC/WA, freeze, clarify, rejudge and finish.
- Export versioned official standings with event/rules identifiers and exclude private source and grading inputs.

**Acceptance criteria**

- The exported standings match a hand-checked expected fixture and replay to identical ordering.
- The rehearsal covers an unauthorized participant, pending job at deadline and a failed rejudge.
- Each export records its event revision; no real learner database is modified by the rehearsal.

**Validation required**

- npx playwright test tests/e2e/contests/rehearsal.spec.ts --workers=2
- uv run --project services/api --frozen pytest services/api/tests/contests/test_standings_export.py

**Out of scope**

- Running a public rated contest
- Publishing participant personal information

**Risk and review**

An incomplete rehearsal can hide event-wide correctness failures.

</details>

<a id="sai-b096"></a>
<details>
<summary>111. SAI-B096: Version output-comparison policies without changing existing verdicts [pending]</summary>

**Priority:** P1 · **Phase:** judge-extensibility · **Area:** judge-validators.

**Suggested role:** Judge engineer.

**Prerequisites:** [SAI-B027](#sai-b027), [SAI-B028](#sai-b028), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Existing grading needs an explicit comparison-policy boundary before supporting richer problem types.

**Target paths / responsibility**

- `services/judge/solver_judge/grading/cases.py`
- `services/judge/solver_judge/control/worker.py`
- `services/judge/tests/grading`
- `services/api/solver_api/features/catalog`

**Implementation scope**

- Add a proposed trusted comparison-policy registry with exact and documented whitespace/token policies.
- Bind a policy version to a problem/grading version and retain current seed-problem semantics.

**Acceptance criteria**

- Current seed solutions keep their previous verdicts.
- Fixtures distinguish trailing newline, extra tokens, encoding errors and output-size bounds.
- Unknown comparator IDs fail closed rather than selecting a permissive default.

**Validation required**

- uv run --project services/api --frozen pytest services/judge/tests/grading/test_comparators.py services/judge/tests/grading/test_cases.py
- npm run test:judge:integration

**Out of scope**

- Running arbitrary checker scripts on the host
- Changing public API verdict names

**Risk and review**

A permissive comparator can accept incorrect programs.

</details>

<a id="sai-b097"></a>
<details>
<summary>112. SAI-B097: Add isolated versioned custom-checker support for authorized problems [pending]</summary>

**Priority:** P2 · **Phase:** judge-extensibility · **Area:** judge-validators.

**Suggested role:** Judge engineer with security reviewer.

**Prerequisites:** [SAI-B096](#sai-b096), [SAI-B124](#sai-b124), [SAI-B125](#sai-b125), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Some original problems need custom validation, but checker code cannot gain host execution privileges.

**Target paths / responsibility**

- `services/judge/solver_judge/control/runner.py`
- `services/judge/solver_judge/control/worker.py`
- `services/judge/solver_judge/sandbox/harness.py`
- `services/judge/tests/sandbox`

**Implementation scope**

- Design a proposed bounded checker protocol and execute approved checker artifacts through the isolated runtime.
- Separate checker/runtime failure from learner wrong answer and limit feedback to permitted summaries.

**Acceptance criteria**

- A valid alternative output is accepted and an invalid witness is rejected by maintained fixtures.
- Checker timeout, malformed result and attempted network/host-file access fail closed with cleanup.
- Private expected data and checker diagnostics never appear in participant responses.

**Validation required**

- uv run --project services/api --frozen pytest services/judge/tests/grading/test_custom_checkers.py
- SOLVER_JUDGE_INTEGRATION=1 uv run --project services/api --frozen pytest services/judge/tests/sandbox/test_checker_isolation.py

**Out of scope**

- User-uploaded arbitrary checkers
- Production approval of an unaudited execution engine

**Risk and review**

Checker privileges and diagnostic leakage expand the execution trust boundary.

</details>

<a id="sai-b098"></a>
<details>
<summary>113. SAI-B098: Implement bounded floating-point answer validation [pending]</summary>

**Priority:** P2 · **Phase:** judge-extensibility · **Area:** judge-validators.

**Suggested role:** Judge engineer and numerical-problem author.

**Prerequisites:** [SAI-B096](#sai-b096), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Numerical problems require explicit tolerance semantics rather than ad hoc string conversion.

**Target paths / responsibility**

- `services/judge/solver_judge/grading`
- `services/judge/tests/grading`
- `services/api/solver_api/features/catalog`

**Implementation scope**

- Add a proposed versioned comparator with approved absolute/relative tolerance and token-count rules.
- Reject malformed numbers, non-finite values and unsupported locale formats deterministically.

**Acceptance criteria**

- Boundary fixtures cover both tolerance limits, signed zero, scientific notation and extreme finite magnitudes.
- NaN/infinity/extra-token outputs cannot bypass validation.
- Problem metadata cannot choose unbounded or negative tolerances.

**Validation required**

- uv run --project services/api --frozen pytest services/judge/tests/grading/test_float_comparator.py

**Out of scope**

- Arbitrary precision symbolic proofs
- Changing existing integer-problem grading

**Risk and review**

Floating-point edge cases can produce false acceptance or rejection.

</details>

<a id="sai-b099"></a>
<details>
<summary>114. SAI-B099: Introduce explicit subtask scoring for separately configured events [pending]</summary>

**Priority:** P3 · **Phase:** judge-extensibility · **Area:** judge-validators.

**Suggested role:** Judge engineer and contest product owner.

**Prerequisites:** [SAI-B096](#sai-b096), [SAI-B097](#sai-b097), [SAI-B001](#sai-b001), [SAI-B013](#sai-b013), [SAI-B027](#sai-b027), [SAI-B084](#sai-b084).

**Problem / missing behavior**

Future partial-score tasks need a contract that does not silently reinterpret ICPC AC/WA scoring.

**Target paths / responsibility**

- `services/judge/solver_judge/grading`
- `services/judge/solver_judge/control/worker.py`
- `services/api/solver_api/features/submissions/store.py`
- `services/api/tests`

**Implementation scope**

- Add a proposed problem-version subtask/weight contract with bounded aggregate score reporting.
- Keep partial-score events distinct from ICPC scoring and withhold private case details.

**Acceptance criteria**

- Weights and dependencies validate before a task is released.
- Hand-calculated pass/fail fixtures yield exact deterministic subtask totals.
- ICPC and ordinary practice results remain byte-compatible in their existing public fields.

**Validation required**

- uv run --project services/api --frozen pytest services/judge/tests/grading/test_subtask_scoring.py
- uv run --project services/api --frozen pytest services/api/tests/contests/test_partial_scoring.py

**Out of scope**

- Changing every existing contest to IOI rules
- Interactive grading

**Risk and review**

Mixing score models can silently change rankings.

</details>

<a id="sai-b100"></a>
<details>
<summary>115. SAI-B100: Add an audited C++20 runtime alongside existing C++17 [pending]</summary>

**Priority:** P2 · **Phase:** judge-extensibility · **Area:** judge-languages.

**Suggested role:** Judge engineer.

**Prerequisites:** [SAI-B096](#sai-b096), [SAI-B125](#sai-b125), [SAI-B124](#sai-b124), [SAI-B001](#sai-b001).

**Problem / missing behavior**

C++20 is a roadmap language, but the current supported contract is C++17.

**Target paths / responsibility**

- `services/judge/Dockerfile`
- `services/judge/solver_judge/sandbox/harness.py`
- `services/judge/solver_judge/control/runner.py`
- `apps/web/features/practice/code-pane.tsx`
- `services/judge/tests/sandbox`

**Implementation scope**

- Add a proposed explicit C++20 language ID/compiler mode while retaining C++17.
- Advertise the runtime only after compiler/version and isolation probes succeed; update editor/submission validation together.

**Acceptance criteria**

- A C++20-only original fixture compiles and passes while the existing C++17 suite remains green.
- Compiler errors, time/output limits and cleanup execute through the same isolation boundary.
- A missing compiler mode does not appear as an available language.

**Validation required**

- npm run test:judge:integration
- npx playwright test tests/e2e/submissions/languages.spec.ts --grep Cpp20 --workers=2

**Out of scope**

- Claiming all C++20 library features across compilers
- Upgrading the managed host runtime without approval

**Risk and review**

Compiler-mode drift can make editor and judge capabilities disagree.

</details>

<a id="sai-b101"></a>
<details>
<summary>116. SAI-B101: Add isolated Java support with explicit JVM resource semantics [pending]</summary>

**Priority:** P3 · **Phase:** judge-extensibility · **Area:** judge-languages.

**Suggested role:** Judge engineer with runtime reviewer.

**Prerequisites:** [SAI-B096](#sai-b096), [SAI-B125](#sai-b125), [SAI-B124](#sai-b124), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Java support requires JVM-aware startup and limits, not only a language dropdown.

**Target paths / responsibility**

- `services/judge/Dockerfile`
- `services/judge/solver_judge/sandbox/harness.py`
- `services/judge/solver_judge/control/runner.py`
- `services/api/solver_api/features/submissions/store.py`
- `apps/web/features/practice/code-pane.tsx`

**Implementation scope**

- Add a proposed pinned JDK toolchain, class/main contract and versioned compilation/run command.
- Document runtime overhead and supported resource accounting before enabling the capability.

**Acceptance criteria**

- Original fixtures cover successful execution, compilation failure, uncaught exception and deadline/output limits.
- JVM startup overhead is included in the documented total deadline; host process execution is never used.
- Capability remains unavailable if preflight or resource enforcement fails.

**Validation required**

- SOLVER_JUDGE_INTEGRATION=1 uv run --project services/api --frozen pytest services/judge/tests/sandbox/test_java_runtime.py
- npx playwright test tests/e2e/submissions/languages.spec.ts --grep Java --workers=2

**Out of scope**

- Multiple arbitrary JDK versions
- Claiming aggregate memory measurement without runtime support

**Risk and review**

JVM memory reservations can conflict with existing per-process limits.

</details>

<a id="sai-b102"></a>
<details>
<summary>117. SAI-B102: Add isolated JavaScript support with denied network and bounded runtime [pending]</summary>

**Priority:** P3 · **Phase:** judge-extensibility · **Area:** judge-languages.

**Suggested role:** Judge engineer.

**Prerequisites:** [SAI-B096](#sai-b096), [SAI-B125](#sai-b125), [SAI-B124](#sai-b124), [SAI-B001](#sai-b001).

**Problem / missing behavior**

JavaScript submissions need an independent untrusted-code runtime, not the application Node process.

**Target paths / responsibility**

- `services/judge/Dockerfile`
- `services/judge/solver_judge/sandbox/harness.py`
- `services/judge/solver_judge/control/runner.py`
- `apps/web/features/practice/code-pane.tsx`
- `services/judge/tests/sandbox`

**Implementation scope**

- Add a proposed pinned sandbox Node runtime and a documented stdin/stdout/module contract.
- Disable package installation and retain sandbox network, process, filesystem and output restrictions.

**Acceptance criteria**

- Original success, syntax-error, rejected-network, process-spawn and infinite-loop fixtures produce documented results.
- Learner code cannot read application state or inherit provider/worker credentials.
- The browser and API reject JavaScript submissions when its preflight is not ready.

**Validation required**

- SOLVER_JUDGE_INTEGRATION=1 uv run --project services/api --frozen pytest services/judge/tests/sandbox/test_javascript_runtime.py
- npx playwright test tests/e2e/submissions/languages.spec.ts --grep JavaScript --workers=2

**Out of scope**

- npm packages in learner submissions
- Browser DOM execution

**Risk and review**

Reusing the application runtime would collapse the isolation boundary.

</details>

<a id="sai-b103"></a>
<details>
<summary>118. SAI-B103: Add isolated Go compilation with offline standard-library execution [pending]</summary>

**Priority:** P3 · **Phase:** judge-extensibility · **Area:** judge-languages.

**Suggested role:** Judge engineer.

**Prerequisites:** [SAI-B096](#sai-b096), [SAI-B125](#sai-b125), [SAI-B124](#sai-b124), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Go is feasible only with a reproducible offline compiler and bounded compilation/runtime behavior.

**Target paths / responsibility**

- `services/judge/Dockerfile`
- `services/judge/solver_judge/sandbox/harness.py`
- `services/judge/solver_judge/control/runner.py`
- `apps/web/features/practice/code-pane.tsx`
- `services/judge/tests/sandbox`

**Implementation scope**

- Add a proposed pinned Go toolchain and standard-library-only submission contract.
- Set deterministic compilation environment and forbid module downloads inside jobs.

**Acceptance criteria**

- Success, compile-error, excessive goroutine/output and timeout fixtures remain bounded and cleaned up.
- An attempted remote module import cannot cause outbound fetch.
- Existing Python/C++ grading remains unchanged and capabilities reflect actual Go readiness.

**Validation required**

- SOLVER_JUDGE_INTEGRATION=1 uv run --project services/api --frozen pytest services/judge/tests/sandbox/test_go_runtime.py
- npx playwright test tests/e2e/submissions/languages.spec.ts --grep Go --workers=2

**Out of scope**

- Arbitrary Go modules
- Paid compilation services

**Risk and review**

Compiler caches, network resolution and concurrent goroutines need bounded policy.

</details>

<a id="sai-b104"></a>
<details>
<summary>119. SAI-B104: Add isolated Rust compilation with a fixed edition and no dependency fetch [pending]</summary>

**Priority:** P3 · **Phase:** judge-extensibility · **Area:** judge-languages.

**Suggested role:** Judge engineer.

**Prerequisites:** [SAI-B096](#sai-b096), [SAI-B125](#sai-b125), [SAI-B124](#sai-b124), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Rust submissions require a toolchain/edition contract and compile budgets separate from application builds.

**Target paths / responsibility**

- `services/judge/Dockerfile`
- `services/judge/solver_judge/sandbox/harness.py`
- `services/judge/solver_judge/control/runner.py`
- `apps/web/features/practice/code-pane.tsx`
- `services/judge/tests/sandbox`

**Implementation scope**

- Add a proposed pinned rustc toolchain and standard-library-only edition contract.
- Bound compilation and program execution independently; reject Cargo dependency retrieval.

**Acceptance criteria**

- Original success, borrow/type-error, panic, output-limit and compile-timeout fixtures produce documented results.
- No job downloads crates or modifies a shared writable compiler cache.
- Unavailable toolchain/preflight prevents advertising Rust support.

**Validation required**

- SOLVER_JUDGE_INTEGRATION=1 uv run --project services/api --frozen pytest services/judge/tests/sandbox/test_rust_runtime.py
- npx playwright test tests/e2e/submissions/languages.spec.ts --grep Rust --workers=2

**Out of scope**

- Arbitrary Cargo packages
- Nightly or user-selected toolchains

**Risk and review**

Long compilation or shared cache mutation can exhaust capacity or contaminate jobs.

</details>

<a id="sai-b117"></a>
<details>
<summary>120. SAI-B117: Enforce institutional sponsorship and learner data-use boundaries [pending]</summary>

**Priority:** P1 · **Phase:** institutional-pilot · **Area:** institutional-privacy.

**Suggested role:** Backend engineer with policy/privacy owner.

**Prerequisites:** [SAI-B115](#sai-b115), [SAI-B116](#sai-b116), [SAI-B003](#sai-b003), [SAI-B018](#sai-b018), [SAI-B001](#sai-b001).

**Problem / missing behavior**

An institutional pilot needs explicit limits on what an organization controls versus the learner’s personal account.

**Target paths / responsibility**

- `services/api/solver_api/features/identity`
- `services/api/solver_api/main.py`
- `apps/web/features/accounts`
- `docs/governance/DATA_AND_LICENSES.md`
- `services/api/tests`

**Implementation scope**

- Add a proposed institution/cohort sponsorship policy record with accepted terms version and permitted data scopes.
- Ensure institutional administrators can manage sponsored assignments without inheriting personal practice/source access.

**Acceptance criteria**

- An institutional administrator is denied unrelated personal history and source detail routes.
- Terms/scope changes require the documented acknowledgement path and an audit record.
- Pilot enrollment fails clearly when the organization’s required policy configuration is missing.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/institutions/test_data_boundaries.py
- npx playwright test tests/e2e/institutions/policy.spec.ts --workers=2

**Out of scope**

- Claiming legal compliance certification
- Redesigning the foundational account deletion/retention system

**Risk and review**

Institutional roles can unintentionally override personal privacy.

</details>

<a id="sai-b118"></a>
<details>
<summary>121. SAI-B118: Export institution-authorized assignment records with redaction tests [pending]</summary>

**Priority:** P2 · **Phase:** institutional-pilot · **Area:** institutional-privacy.

**Suggested role:** Backend engineer and privacy reviewer.

**Prerequisites:** [SAI-B116](#sai-b116), [SAI-B117](#sai-b117), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Institutions need a narrow portable assignment record without receiving unrelated private learner data.

**Target paths / responsibility**

- `services/api/solver_api/main.py`
- `services/api/solver_api/features/submissions/store.py`
- `scripts/verification`
- `services/api/tests`

**Implementation scope**

- Add a proposed versioned export for authorized cohorts/assignments and an explicit field allowlist.
- Default to summary/rubric records; include source only when the assignment consent/policy explicitly permits it.

**Acceptance criteria**

- A seeded mixed personal/cohort history exports only the requested institution’s allowed assignment rows.
- Private grading data, tokens, account keys and unrelated identifiers never appear.
- Expired/revoked institution permissions cannot generate or retrieve a fresh export.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/institutions/test_assignment_export.py

**Out of scope**

- General database dumps
- Exporting user code for training

**Risk and review**

Portable exports can turn a narrow permission mistake into a durable data leak.

</details>

<a id="sai-b119"></a>
<details>
<summary>122. SAI-B119: Produce a redacted pilot cost ledger and resource-envelope report [pending]</summary>

**Priority:** P2 · **Phase:** institutional-pilot · **Area:** business-operations.

**Suggested role:** Operations engineer and project owner.

**Prerequisites:** [SAI-B105](#sai-b105), [SAI-B109](#sai-b109), [SAI-B003](#sai-b003), [SAI-B021](#sai-b021), [SAI-B053](#sai-b053), [SAI-B001](#sai-b001).

**Problem / missing behavior**

A sustainable pilot needs measured usage and declared prices rather than assumptions that self-hosting or AI is free.

**Target paths / responsibility**

- `scripts/verification`
- `services/api/solver_api/main.py`
- `docs/product/ROADMAP.md`
- `services/api/tests`

**Implementation scope**

- Add a proposed offline report combining bounded usage aggregates with operator-supplied nonsecret unit prices.
- Separate measured consumption, estimated allocation and unpriced items; never infer a paid purchase from report generation.
- Consume B021/B053 measurements and the B003 approved envelope; never create another online token/budget reservation ledger.

**Acceptance criteria**

- Known usage/price fixtures produce exact totals and missing prices remain explicitly unknown.
- The report excludes source, personal identifiers and provider credentials.
- A budget scenario exceeding its approved resource envelope is flagged with the contributing categories.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/operations/test_cost_ledger.py

**Out of scope**

- Buying infrastructure or model credits
- Live invoicing, payment processing or guaranteed profitability

**Risk and review**

False precision can hide unpriced support, capacity or provider costs.

</details>

<a id="sai-b120"></a>
<details>
<summary>123. SAI-B120: Extend existing pilot grants with expiring institutional scopes [pending]</summary>

**Priority:** P2 · **Phase:** institutional-pilot · **Area:** business-release.

**Suggested role:** Backend engineer and project owner.

**Prerequisites:** [SAI-B110](#sai-b110), [SAI-B112](#sai-b112), [SAI-B117](#sai-b117), [SAI-B119](#sai-b119), [SAI-B049](#sai-b049), [SAI-B003](#sai-b003), [SAI-B001](#sai-b001), [SAI-B050](#sai-b050), [SAI-B051](#sai-b051).

**Problem / missing behavior**

A limited pilot needs enforceable access grants and a recorded go/no-go decision before any commercial expansion.

**Target paths / responsibility**

- `services/api/solver_api/features/identity`
- `services/api/solver_api/main.py`
- `apps/web/features/accounts`
- `docs/product/ROADMAP.md`
- `services/api/tests`

**Implementation scope**

- Extend B049 admission authority with owner-approved institutional scope, expiry and revocation; do not add a parallel entitlement or budget ledger.
- Use B117 sponsorship/data-use boundaries and B119 resource reports to decide an explicitly approved pilot envelope.
- Make revocation stop new admission while documenting bounded treatment of in-flight authorized jobs.
- Reuse B050/B051 reservations and spend limits for institutional grants; no parallel accounting store.

**Acceptance criteria**

- Expired/revoked grants cannot access the gated workflow; existing ordinary practice remains available.
- A grant cannot override contest assistance rules, ownership boundaries or hard execution/model budgets.
- The release record lists the tested revision, approved audience/capacity, unresolved risks and accountable owner.

**Validation required**

- uv run --project services/api --frozen pytest services/api/tests/institutions/test_pilot_entitlements.py
- npx playwright test tests/e2e/institutions/pilot-access.spec.ts --workers=2

**Out of scope**

- Automatic charging or creating paid subscriptions
- Declaring public production readiness from the existence of a grant

**Risk and review**

A commercial access flag must not become a bypass for safety or privacy policy.

</details>

<a id="sai-b077"></a>
<details>
<summary>124. SAI-B077: Separate evaluation splits and report archive contamination candidates [pending]</summary>

**Priority:** P1 · **Phase:** AI-4 evaluation and research gates · **Area:** Evaluation integrity.

**Suggested role:** Data evaluation engineer.

**Prerequisites:** [SAI-B068](#sai-b068), [SAI-B074](#sai-b074), [SAI-B026](#sai-b026), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Archived benchmark variants contain overlapping tasks, and public model training history is incomplete. Reusing them naively can contaminate training/evaluation comparisons.

**Target paths / responsibility**

- `docs/research/MODEL_DATA_EVALUATION.md`
- `AnalyseFuture/manifest.json`
- `AnalyseFuture/extracted/CodeGenerator-master/data/HumanEval/HumanEval.jsonl`
- `AnalyseFuture/extracted/CodeGenerator-master/data/HumanEval/HumanEvalET.jsonl`

**Implementation scope**

- Define immutable split manifests by problem/source/date lineage rather than file name alone.
- Compute permitted exact/normalized overlap fingerprints and flag near-duplicate candidates for review.
- Record unknown model-training exposure as uncertainty rather than claiming a clean benchmark.

**Acceptance criteria**

- The same task cannot enter training and evaluation splits under different variant filenames.
- Every exclusion/override records its reason and owner.
- Original archives stay byte-identical; analysis outputs contain hashes/metadata rather than copied benchmark bodies.

**Validation required**

- Future authorized check: deterministic synthetic overlap fixtures; static manifest review before any real-data analysis.

**Out of scope**

- Claiming zero contamination for closed models
- Training on archived benchmark solutions

**Risk and review**

Approximate deduplication needs human review and cannot establish unseen model pretraining data.

</details>

<a id="sai-b078"></a>
<details>
<summary>125. SAI-B078: Register dataset and model permissions separately from source licenses [pending]</summary>

**Priority:** P1 · **Phase:** AI-4 evaluation and research gates · **Area:** Research provenance.

**Suggested role:** Data stewardship and project owner.

**Prerequisites:** [SAI-B041](#sai-b041), [SAI-B068](#sai-b068), [SAI-B077](#sai-b077), [SAI-B002](#sai-b002), [SAI-B026](#sai-b026), [SAI-B001](#sai-b001).

**Problem / missing behavior**

MIT/Apache source notices do not authorize benchmark redistribution, training, commercial use or model-weight deployment; five archived datasets are only pointers.

**Target paths / responsibility**

- `docs/governance/DATA_AND_LICENSES.md`
- `docs/research/MODEL_DATA_EVALUATION.md`
- `AnalyseFuture/repository-inventory/ARCHIVED_FILES_MANIFEST.txt`
- `AnalyseFuture/extracted/phi-code-main/datasets/atcoder.jsonl`

**Implementation scope**

- Define machine-readable provenance with source, owner, version/hash, permitted uses, evidence and unresolved status.
- Require separate flags for evaluate/train/redistribute/commercial/model-serving permissions.
- Represent missing LFS objects explicitly and block activation until content and rights are available.

**Acceptance criteria**

- Unknown or absent permission never defaults to allowed.
- A source-code license cannot satisfy an unrelated dataset/model permission field.
- Each approved experiment references complete immutable inputs and review evidence.

**Validation required**

- Future authorized check: schema fixtures using synthetic rights records; owner review of actual permission evidence without bulk downloads.

**Out of scope**

- Legal conclusions without review
- Fetching all missing LFS datasets automatically

**Risk and review**

Permission metadata can be incomplete or expire; record review date and responsible owner.

</details>

<a id="sai-b079"></a>
<details>
<summary>126. SAI-B079: Produce a resource-and-integrity feasibility decision for one self-hosted model [pending]</summary>

**Priority:** P2 · **Phase:** AI-4 evaluation and research gates · **Area:** Model serving research gate.

**Suggested role:** ML infrastructure researcher.

**Prerequisites:** [SAI-B074](#sai-b074), [SAI-B078](#sai-b078), [SAI-B001](#sai-b001).

**Problem / missing behavior**

Archived ranker/solver code permits remote model code and names consumer-hardware models, but current hardware, artifact integrity, licensing and serving economics are unverified.

**Target paths / responsibility**

- `docs/research/MODEL_DATA_EVALUATION.md`
- `docs/governance/OPEN_DECISIONS.md`
- `AnalyseFuture/extracted/phi-code-main/solver/main.py`
- `AnalyseFuture/planning/TECHNICAL_DEBT.txt`

**Implementation scope**

- Compare one pinned checkpoint/quantization against the approved provider baseline using documented memory, concurrency and maintenance requirements.
- Review model code/license/artifact hashes and reject arbitrary trust_remote_code loading as a default.
- Specify the separate approval, isolated environment and fixed budget needed for an empirical serving experiment.

**Acceptance criteria**

- Decision names an exact artifact/revision and states unknown measurements honestly.
- No weight download, remote-code execution or GPU purchase occurs during the feasibility issue.
- Recommendation includes a measurable evaluation plan and a do-not-proceed outcome when resources are inadequate.

**Validation required**

- Static artifact/terms/hardware review and comparison table; optional empirical commands remain unexecuted until separately approved.

**Out of scope**

- Provisioning inference infrastructure
- Assuming self-hosting is automatically cheaper

**Risk and review**

Published memory or benchmark claims may not hold under this project's concurrency and isolation requirements.

</details>

<a id="sai-b080"></a>
<details>
<summary>127. SAI-B080: Add an explicit admission gate for reproducible fine-tuning experiments [pending]</summary>

**Priority:** P1 · **Phase:** AI-4 evaluation and research gates · **Area:** Fine-tuning research controls.

**Suggested role:** ML evaluation lead with project owner.

**Prerequisites:** [SAI-B074](#sai-b074), [SAI-B077](#sai-b077), [SAI-B078](#sai-b078), [SAI-B079](#sai-b079), [SAI-B001](#sai-b001).

**Problem / missing behavior**

The archived trainer can start expensive, nondeterministic work, while Solver AI has no proven baseline, approved complete dataset or production training workflow.

**Target paths / responsibility**

- `docs/research/MODEL_DATA_EVALUATION.md`
- `docs/governance/OPEN_DECISIONS.md`
- `AnalyseFuture/extracted/phi-code-main/ranker/train.py`
- `AnalyseFuture/planning/PROJECT_VISION_AND_FUTURE_ROADMAP.txt`

**Implementation scope**

- Define and validate an experiment manifest covering rights-approved disjoint data, base artifact, seed, hyperparameters, external compute, spend ceiling and owner approval.
- Require a matched untuned baseline and an evaluation/negative-result publication plan.
- Reject manifests that request training inside the application workspace or omit rollback/artifact-retention rules.

**Acceptance criteria**

- Missing approval, dataset/model permission, budget or disjoint evaluation split prevents experiment admission.
- Manifest validation performs no training, cloud provisioning or model loading.
- Promotion criteria compare quality, cost and regressions; failure to improve is a valid recorded outcome.

**Validation required**

- Future authorized check: synthetic manifest validation fixtures and owner review; any actual training is a separate approved execution task.

**Out of scope**

- Running LoRA/QLoRA/GRPO in this issue
- Promising that tuning improves solver correctness

**Risk and review**

Training can memorize evaluation tasks or consume substantial resources without improving product value.

</details>

<a id="sai-b128"></a>
<details>
<summary>128. SAI-B128: Implement a declared DSA coverage matrix and preregistered model release measurements [pending]</summary>

**Priority:** P1 · **Phase:** ML-1 measured scope and baseline · **Area:** solver-readiness.

**Suggested role:** ML evaluation lead and product owner.

**Prerequisites:** [SAI-B001](#sai-b001), [SAI-B074](#sai-b074), [SAI-B077](#sai-b077), [SAI-B078](#sai-b078).

**Problem / missing behavior**

The readiness document can describe broad ambitions, but training and release need a machine-readable support policy and measurable category coverage. Neither attempting a prompt nor passing a small benchmark demonstrates support for every DSA problem.

**Target paths / responsibility**

- `docs/product/DSA_SOLVER_READINESS.md`
- `docs/product/AI_SOLVER.md`
- `docs/research/MODEL_DATA_EVALUATION.md`
- `scripts/verification`
- `tests/tooling`

**Implementation scope**

- Create a versioned coverage manifest under a new ml/evaluation/ implementation, keyed by algorithm topic/subtopic, problem format, difficulty band, supported language/runtime, constraint range and evaluation budget. Reuse B068 problem identities and B074 run records instead of creating another identity authority.
- Bind rights-approved held-out task manifests and independent graders to declared cells; represent missing evidence, out-of-distribution inputs and unsupported formats explicitly.
- Record owner-reviewed per-category quality, reliability, latency/cost and regression thresholds before tuned results are inspected. Define attemptable, measured-supported and unsupported states, including safe refusal/abstention.

**Acceptance criteria**

- Synthetic fixtures distinguish an untested category from a measured pass, a failed category and an unsupported input; no empty cell counts as success.
- Release aggregation records eligible task counts, pass@1/pass@k sampling policy, uncertainty and execution failures for each declared category without hiding weak categories in an overall score.
- A model cannot receive a universal any-DSA label, an untested language/interactive format cannot be advertised as supported, and threshold changes retain dated review provenance.

**Validation required**

- Future authorized checks: deterministic manifest/report fixtures introduced under tests/tooling; no weights, model calls or GPU access are needed for these schema checks.
- Review the coverage manifest and preregistration against DSA_SOLVER_READINESS.md with the evaluation lead and owner.

**Out of scope**

- Selecting a checkpoint now
- Claiming formal correctness from finite tests
- Implementing a general natural-language problem parser or replacing B074 evaluation orchestration

**Risk and review**

Coverage can be gamed by easy tasks or thresholds chosen after results; preserve category counts, lineage, uncertainty and preregistration.

</details>

<a id="sai-b129"></a>
<details>
<summary>129. SAI-B129: Run an approved untuned checkpoint comparison and record a future selection [pending]</summary>

**Priority:** P1 · **Phase:** ML-1 measured scope and baseline · **Area:** model-baseline.

**Suggested role:** ML evaluation engineer with project owner.

**Prerequisites:** [SAI-B001](#sai-b001), [SAI-B074](#sai-b074), [SAI-B078](#sai-b078), [SAI-B079](#sai-b079), [SAI-B128](#sai-b128).

**Problem / missing behavior**

The research catalogue names future candidates but no model has been selected, downloaded or benchmarked here. A fine-tuning choice needs measured task fit, actual resource behavior and license compatibility rather than a nominal parameter count or advertised score.

**Target paths / responsibility**

- `docs/research/FINETUNING_MODEL_RESEARCH.md`
- `docs/research/MODEL_DATA_EVALUATION.md`
- `docs/governance/OPEN_DECISIONS.md`
- `scripts/verification`
- `tests/tooling`

**Implementation scope**

- After separate owner authorization for artifacts, hardware and a fixed experiment budget, compare at least two eligible open-weight checkpoints or explicitly justify why only one is eligible. Do not assume any family or size wins.
- Reuse B074 evaluation and B128 coverage on a model-selection/validation split disjoint from training and the sealed final release test; fix prompts/templates, decoding, context limits, candidate/test budgets and exact model revisions. Run single-candidate untuned baselines before adding repair or tuning.
- Measure peak training/inference feasibility separately where authorized, report unknowns and record a reviewed selection or do-not-proceed outcome. Hosted/API models may be optional approved reference baselines, not assumed downloadable LoRA bases.

**Acceptance criteria**

- The report includes exact checkpoint/revision, license/usage evidence, tokenizer/template, hardware/software, precision, per-category results, latency, memory, cost and failures.
- All compared scores state task eligibility and comparable budgets; no task used for later held-out evaluation is silently moved into training.
- No checkpoint is selected merely by writing this issue. Actual execution requires recorded artifact/compute permission; absent resources produce an explicit blocked decision without substituting invented measurements.
- Checkpoint selection never inspects the sealed final release-test results; record a separate selection split and freeze the chosen model/criteria before final evaluation.

**Validation required**

- Future approved execution: use the B074 harness to replay the recorded untuned manifests on the allowed isolated inference host and retain result hashes.
- Reproduce one small manifest twice and investigate nondeterministic/failed outcomes; any paid API baseline requires its own existing approval and cap.

**Out of scope**

- Choosing a specific model in this planning update
- Training adapters
- Reproducing every published model benchmark or buying hardware by default

**Risk and review**

Model training exposure is often unknown and published hardware figures may not match this workload; report contamination and feasibility uncertainty.

</details>

<a id="sai-b130"></a>
<details>
<summary>130. SAI-B130: Materialize a permitted validated training corpus with immutable split lineage [pending]</summary>

**Priority:** P1 · **Phase:** ML-2 approved data and training tooling · **Area:** training-data.

**Suggested role:** Data engineer and rights/evaluation reviewer.

**Prerequisites:** [SAI-B001](#sai-b001), [SAI-B077](#sai-b077), [SAI-B078](#sai-b078), [SAI-B128](#sai-b128).

**Problem / missing behavior**

B077 and B078 define split/permission records, but no approved corpus has been normalized, validated and materialized for actual training. The archives include incomplete LFS entries and overlapping benchmark variants that cannot be treated as a ready dataset.

**Target paths / responsibility**

- `docs/governance/DATA_AND_LICENSES.md`
- `docs/research/MODEL_DATA_EVALUATION.md`
- `services/judge/solver_judge/grading/cases.py`
- `scripts/verification`
- `tests/tooling`

**Implementation scope**

- Implement a data-only pipeline under new ml/data/ modules that reads only explicitly approved complete inputs and emits immutable train/validation manifests outside Git. Reuse the permission/split registries rather than infer rights from repository licenses.
- Normalize task/solution/language/provenance records, quarantine malformed or duplicate entries and verify solution correctness through authorized independent grading before including solution targets.
- Reserve the held-out release set; record exact and reviewed near-duplicate exclusions, source lineage, content hashes, accepted/rejected counts and a reproducible materialization recipe.

**Acceptance criteria**

- Every emitted training record points to complete approved source and a valid immutable task identity; missing LFS objects, unknown training permission and private unconsented submissions are rejected.
- A synthetic variant of a held-out task is excluded even when its file name or wording changes, with reviewable reason/override records.
- The manifest can be rebuilt to matching hashes from the same approved inputs; logs contain metadata/counts rather than raw private code or benchmark bodies.

**Validation required**

- Future authorized checks: synthetic malformed/rights/duplicate/split fixtures for the new data pipeline.
- Future approved data execution: run the fixed corpus materialization manifest, independently inspect a stratified sample and verify solution targets in the existing isolated judge.

**Out of scope**

- Bulk importing all archived datasets
- Using model-created answers as trusted ground truth without independent validation
- Redistributing datasets or downloading missing objects without permission

**Risk and review**

Bad solutions, silent rights assumptions and leakage can invalidate both training and evaluation; quarantine uncertain inputs rather than filling gaps automatically.

</details>

<a id="sai-b131"></a>
<details>
<summary>131. SAI-B131: Create a separate locked training environment and reviewed artifact loader [pending]</summary>

**Priority:** P1 · **Phase:** ML-2 approved data and training tooling · **Area:** training-infrastructure.

**Suggested role:** ML infrastructure engineer.

**Prerequisites:** [SAI-B001](#sai-b001), [SAI-B079](#sai-b079), [SAI-B080](#sai-b080), [SAI-B129](#sai-b129).

**Problem / missing behavior**

The active API environment deliberately has no ML training stack. Actual training requires a reproducible separate environment, compatible accelerator libraries and safe artifact loading without importing archived requirements or model remote code into app services.

**Target paths / responsibility**

- `docs/research/MODEL_DATA_EVALUATION.md`
- `docs/onboarding/DEVELOPMENT.md`
- `scripts/verification`
- `tests/tooling`

**Implementation scope**

- Create ml/training/ with its own pinned project/lock, supported Python/CUDA/toolchain matrix and noninteractive setup/preflight entry point; retain independent API/web lockfiles.
- Implement an artifact loader tied to the future selected revision and B078/B080 records, verifying approved artifact identities, tokenizer/config files and allowed local paths. Default to no arbitrary trust_remote_code and safe tensor formats.
- Implement dry-run configuration and resource preflight that report required resources, supported precision/adapter modes, environment versions and hard stop conditions without automatically provisioning compute.

**Acceptance criteria**

- Installing or importing training tooling does not add ML dependencies to services/api or start a download/training job.
- Synthetic unapproved revision, hash mismatch, path escape and remote-code-required cases fail before loading; trusted artifact handling preserves TLS/checksum verification.
- The exact training environment can be reconstructed and its preflight distinguishes unsupported hardware, missing approved artifact and ready state without pretending a memory estimate is an actual measurement.

**Validation required**

- Future authorized checks: the new loader/config fixtures run on CPU with tiny local synthetic tensors/configurations and no external requests.
- On separately approved external hardware, run only the documented training preflight and record the actual environment/artifact hashes before a training job.

**Out of scope**

- Installing GPU drivers in the application environment
- Copying archive requirements or enabling unreviewed remote code
- Provisioning paid GPUs or running the actual smoke/train job

**Risk and review**

Artifact deserialization and accelerator dependencies expand the supply chain; isolate them from app credentials and preserve immutable versions.

</details>

<a id="sai-b132"></a>
<details>
<summary>132. SAI-B132: Implement tokenizer-aware SFT examples and answer-only loss masking [pending]</summary>

**Priority:** P1 · **Phase:** ML-2 approved data and training tooling · **Area:** training-preprocessing.

**Suggested role:** ML data/training engineer.

**Prerequisites:** [SAI-B001](#sai-b001), [SAI-B129](#sai-b129), [SAI-B130](#sai-b130), [SAI-B131](#sai-b131).

**Problem / missing behavior**

A clean text corpus is insufficient for SFT: the chosen tokenizer/chat template, truncation, special tokens and labels determine what the model actually learns. Incorrect masking can train on user/system text or cut away the solution.

**Target paths / responsibility**

- `docs/research/MODEL_DATA_EVALUATION.md`
- `docs/product/DSA_SOLVER_READINESS.md`
- `tests/tooling`

**Implementation scope**

- Implement preprocessing under ml/training/ using the selected artifact tokenizer/template and materialized corpus lineage, with versioned formatting and no fabricated private chain-of-thought targets.
- Define explicit maximum lengths, special-token handling, sample packing/attention policy and assistant-target loss masking; reject or separately report examples that cannot fit validly.
- Produce an immutable tokenization manifest containing tokenizer/template/config hashes, retained/dropped counts and non-sensitive inspection summaries.

**Acceptance criteria**

- Synthetic multi-turn, empty-answer, Unicode, long-source and boundary-token examples have exact expected masks; prompt/system/user tokens and padding do not receive unintended loss.
- No included example silently loses its required answer or crosses split boundaries through packing.
- Reprocessing the same corpus/tokenizer/config reproduces the manifest; inspection summaries do not publish full private examples.

**Validation required**

- Future authorized checks: deterministic tokenizer/masking/packing fixtures with a tiny local tokenizer under the separate training environment.
- After artifact approval, manually inspect a small stratified token/label sample and record truncation/drop rates before smoke training.

**Out of scope**

- An actual optimization run
- Automatic generation of reasoning traces from private model internals
- Silently changing the corpus or selected tokenizer to make examples fit

**Risk and review**

Loss-mask/template errors can create a seemingly successful training curve while teaching the wrong objective; inspect labels, not just batch shapes.

</details>

<a id="sai-b133"></a>
<details>
<summary>133. SAI-B133: Run an approved external LoRA smoke experiment with stop and resume evidence [pending]</summary>

**Priority:** P1 · **Phase:** ML-3 actual approved training · **Area:** training-smoke.

**Suggested role:** ML training engineer and authorized compute operator.

**Prerequisites:** [SAI-B001](#sai-b001), [SAI-B080](#sai-b080), [SAI-B129](#sai-b129), [SAI-B130](#sai-b130), [SAI-B131](#sai-b131), [SAI-B132](#sai-b132).

**Problem / missing behavior**

Admission validation and CPU fixtures do not demonstrate that the selected base, tokenizer, adapter configuration and accelerator stack can train safely. A finite external smoke experiment must precede a larger job.

**Target paths / responsibility**

- `docs/research/MODEL_DATA_EVALUATION.md`
- `docs/product/DSA_SOLVER_READINESS.md`
- `docs/governance/OPEN_DECISIONS.md`
- `tests/tooling`

**Implementation scope**

- Implement a bounded LoRA/QLoRA-compatible training command under ml/training/ consuming the accepted B080 manifest and fixed tiny approved corpus slice; choose only a supported precision/method for the future selected model.
- Execute the smoke only on separately authorized external hardware with a recorded low step/time/spend ceiling, cancellation and OOM behavior.
- Save a checkpoint, deliberately stop within the fixture budget, resume under the same configuration and evaluate a small allowed sanity set without using held-out release results for tuning.

**Acceptance criteria**

- Evidence records a real approved run: optimizer updates occurred, losses/gradients are finite, intended adapter parameters changed and frozen base parameters remained unchanged.
- Checkpoint resume restores the documented optimizer/scheduler/RNG state or explicitly reports nondeterministic limits; cancellation and budget exhaustion stop the job and leave a usable manifest.
- Memory/time/cost measurements and failed/OOM outcomes are recorded honestly; a dry-run or five-minute demonstration is not marked as a completed full training campaign.

**Validation required**

- Future approved execution: run the new smoke command with the accepted manifest on the authorized external host, then run its bounded stop/resume scenario.
- Verify checkpoint/base/tokenizer/data hashes and run only the declared finite sanity evaluation; do not load model-generated programs on the host.

**Out of scope**

- Selecting a model now
- Training inside Codex/application services
- Launching an unconstrained full corpus job or assuming successful smoke establishes quality

**Risk and review**

Even smoke runs incur compute and artifact risk; enforce hard limits in the runner and stop on invalid gradients, loss or artifact state.

</details>

<a id="sai-b134"></a>
<details>
<summary>134. SAI-B134: Execute the approved bounded SFT adapter training campaign [pending]</summary>

**Priority:** P1 · **Phase:** ML-3 actual approved training · **Area:** actual-fine-tuning.

**Suggested role:** ML training lead and compute operator.

**Prerequisites:** [SAI-B001](#sai-b001), [SAI-B080](#sai-b080), [SAI-B129](#sai-b129), [SAI-B130](#sai-b130), [SAI-B131](#sai-b131), [SAI-B132](#sai-b132), [SAI-B133](#sai-b133).

**Problem / missing behavior**

B080 explicitly excludes actual LoRA/QLoRA/GRPO execution. Without this separate task the roadmap can finish admission tooling and still produce no fine-tuned model.

**Target paths / responsibility**

- `docs/research/MODEL_DATA_EVALUATION.md`
- `docs/product/DSA_SOLVER_READINESS.md`
- `docs/governance/OPEN_DECISIONS.md`

**Implementation scope**

- Execute the approved SFT campaign through the separate ml/training/ runner using the fixed base, allowed adapter method, training/validation corpus, seed, effective batch, schedule and bounded hyperparameter plan from the accepted manifest.
- Use validation data for the preregistered checkpoint/stopping policy, record every attempted run including failed/aborted ones and enforce external compute/time/spend ceilings.
- Produce retained candidate adapters and a complete run report with environment/data/code lineage, losses, step counts, resource measurements and termination reason; keep weights and private data out of Git.

**Acceptance criteria**

- At least one actual optimization campaign reaches its declared completion or a clearly recorded failure/early-stop state; documentation completion cannot substitute for execution.
- The saved candidate loads with the exact base/tokenizer and has verified tensor/checkpoint identities; no held-out release task was used to select hyperparameters or checkpoints.
- The report states actual cost/resources and all runs, including negative outcomes. Training completion alone neither promotes the artifact nor asserts improved DSA performance.

**Validation required**

- Future separately approved execution: run the training command against the signed-off B080 manifest on the approved external host; verify recorded steps, cancellation and spend stops.
- Reconstruct the selected checkpoint from the report and run the declared validation-only evaluation before handing the candidate to B136.

**Out of scope**

- Defaulting to a named checkpoint in this planning update
- Unlimited hyperparameter search
- A foundation-model pretraining project or guaranteed performance gain

**Risk and review**

Training can overfit, leak evaluation data or exhaust resources; frozen manifests and independent review of run evidence are required.

</details>

<a id="sai-b135"></a>
<details>
<summary>135. SAI-B135: Publish immutable private model artifacts and complete adapter lineage [pending]</summary>

**Priority:** P1 · **Phase:** ML-3 actual approved training · **Area:** model-artifacts.

**Suggested role:** ML platform engineer and data/model steward.

**Prerequisites:** [SAI-B001](#sai-b001), [SAI-B078](#sai-b078), [SAI-B129](#sai-b129), [SAI-B130](#sai-b130), [SAI-B131](#sai-b131), [SAI-B134](#sai-b134).

**Problem / missing behavior**

A training checkpoint directory is not a reproducible deliverable. Consumers need to know which base/tokenizer/license/data/run produced an adapter and must not accidentally load a mismatched or modified artifact.

**Target paths / responsibility**

- `docs/research/MODEL_DATA_EVALUATION.md`
- `docs/governance/DATA_AND_LICENSES.md`
- `docs/product/DSA_SOLVER_READINESS.md`
- `scripts/verification`
- `tests/tooling`

**Implementation scope**

- Implement an immutable artifact manifest/registry interface under ml/ for base, tokenizer, adapter/config, training run and intended compatible inference precisions, storing approved large artifacts outside Git.
- Record hashes, size, code/environment versions, data/split lineage, license/NOTICE/redistribution restrictions and retention/access policy; do not publish private training examples.
- Provide a fetch/verify/reconstruct command that requires exact identities, rejects unauthorized artifacts and records a retained last-known-good candidate for rollback.

**Acceptance criteria**

- Reconstruction with the correct authorized base/tokenizer/adapter succeeds to matching identities; mismatched bases, altered tensors and missing required files fail before serving.
- Registry entries are immutable/versioned, contain every required provenance link and distinguish unpublished/private from approved redistributable artifacts.
- No weight, credential, private corpus or raw learner code enters the application repository or public model-card evidence.

**Validation required**

- Future authorized checks: synthetic registry/manifest/hash/access fixtures in the separate ML tooling.
- For the trained candidate, fetch only the approved artifacts into an isolated temporary inference workspace and verify the complete reconstruction record.

**Out of scope**

- Making weights public without permission
- Buying an artifact-store service by default
- Silently merging an adapter into an unidentified base

**Risk and review**

Ambiguous lineage or unrestricted artifact publication can violate licenses and make rollback impossible; retain exact reconstructible identities.

</details>

<a id="sai-b136"></a>
<details>
<summary>136. SAI-B136: Evaluate tuned candidates against matched baselines and enforce category gates [pending]</summary>

**Priority:** P1 · **Phase:** ML-4 evaluation and delivery · **Area:** model-promotion-evaluation.

**Suggested role:** Independent ML evaluation reviewer.

**Prerequisites:** [SAI-B001](#sai-b001), [SAI-B074](#sai-b074), [SAI-B075](#sai-b075), [SAI-B077](#sai-b077), [SAI-B128](#sai-b128), [SAI-B129](#sai-b129), [SAI-B134](#sai-b134), [SAI-B135](#sai-b135).

**Problem / missing behavior**

A decreasing SFT loss or successful adapter load does not show better solving, teaching or cost. Promotion requires independent held-out comparison against the untuned baseline and the declared support matrix.

**Target paths / responsibility**

- `docs/research/MODEL_DATA_EVALUATION.md`
- `docs/product/DSA_SOLVER_READINESS.md`
- `docs/product/AI_SOLVER.md`
- `services/judge/solver_judge/grading/cases.py`

**Implementation scope**

- Run the frozen immutable candidate and matched untuned base through the existing B074 harness on a sealed final release set disjoint from training and model-selection/validation, using preregistered B128 measurements, equal budgets and approved independent graders.
- Report per-topic/difficulty/language/input-format coverage, compile/runtime/system failures, pass@1/pass@k protocol, uncertainty, cost/latency and relevant hint quality/safety regressions.
- Produce a reviewed promote/reject/limited-scope decision; quarantine contaminated or invalid tasks and invalidate affected claims instead of repairing the score by omission.

**Acceptance criteria**

- A deterministic synthetic worse candidate fails promotion, and missing category evidence yields unmeasured/unsupported status rather than a pass.
- The actual trained candidate receives a complete held-out report including weak categories and failures; no improvement claim is made unless supported by the preregistered comparison.
- A rejected or inconclusive run remains documented and the untuned/previous qualified artifact remains usable; no public activation occurs in this issue.
- Repeated model/hyperparameter selection cannot query the same sealed final test for feedback; any exposed set is labeled and replaced with a newly rights-approved untouched release set for later claims.

**Validation required**

- Future separately approved execution: replay the locked held-out evaluation manifests for base and candidate with the authorized isolated judge and inference budget.
- Independently review a sample of predictions, grading validity and report aggregation; retain hashes and exact eligible sample counts.

**Out of scope**

- Using release-set failures as another training batch before preserving an independent holdout
- Claiming all-DSA correctness
- Changing success thresholds after seeing candidate results

**Risk and review**

Contamination, faulty oracles and unequal budgets can manufacture gains; evaluator independence and complete negative reporting are essential.

</details>

<a id="sai-b137"></a>
<details>
<summary>137. SAI-B137: Qualify inference export and quantization at the deployed precision [pending]</summary>

**Priority:** P1 · **Phase:** ML-4 evaluation and delivery · **Area:** inference-qualification.

**Suggested role:** ML inference engineer.

**Prerequisites:** [SAI-B001](#sai-b001), [SAI-B079](#sai-b079), [SAI-B128](#sai-b128), [SAI-B135](#sai-b135), [SAI-B136](#sai-b136).

**Problem / missing behavior**

The trained adapter and the intended serving artifact may differ through merging, quantization, tokenizer handling or engine support. A training-precision score cannot be assumed to survive the deployment format.

**Target paths / responsibility**

- `docs/research/MODEL_DATA_EVALUATION.md`
- `docs/product/DSA_SOLVER_READINESS.md`
- `docs/architecture/ARCHITECTURE.md`
- `tests/tooling`

**Implementation scope**

- Implement a reproducible export recipe for one approved serving engine/precision with exact base/adapter/tokenizer/config identities and safe serialization.
- Compare the exported artifact with the qualified training/reference representation using bounded tokenization/generation parity fixtures and the preregistered regression subset.
- Measure supported context, throughput/latency, actual peak memory and constrained concurrency on approved hardware; document unsupported operations and fallback to the retained qualified artifact.

**Acceptance criteria**

- Export artifacts carry reconstructible lineage and cannot load with an incompatible tokenizer or unapproved remote-code path.
- Actual inference-precision evaluation meets B128 thresholds or produces an explicit narrower/rejected decision; no assumption of lossless quantization substitutes for measurement.
- A repeat export from the recorded recipe yields the stated deterministic identities or documented tool nondeterminism, and resources stay inside the approved envelope.

**Validation required**

- Future approved execution: run the exact export/qualification recipe on the authorized inference host and replay token/template plus held-out regression checks.
- Verify malformed/mismatched export manifests fail in the CPU synthetic tooling fixtures.

**Out of scope**

- Quantizing every available format
- Assuming a specific model/engine is selected now
- Public deployment or unrestricted benchmark tuning

**Risk and review**

Merging/quantization can silently degrade quality or exceed memory; qualify the artifact actually deployed, not only its training checkpoint.

</details>

<a id="sai-b138"></a>
<details>
<summary>138. SAI-B138: Integrate the qualified trained artifact with bounded provider-neutral serving [pending]</summary>

**Priority:** P1 · **Phase:** ML-4 evaluation and delivery · **Area:** trained-model-serving.

**Suggested role:** ML serving engineer and backend security reviewer.

**Prerequisites:** [SAI-B001](#sai-b001), [SAI-B043](#sai-b043), [SAI-B044](#sai-b044), [SAI-B046](#sai-b046), [SAI-B050](#sai-b050), [SAI-B051](#sai-b051), [SAI-B054](#sai-b054), [SAI-B055](#sai-b055), [SAI-B057](#sai-b057), [SAI-B079](#sai-b079), [SAI-B135](#sai-b135), [SAI-B136](#sai-b136), [SAI-B137](#sai-b137).

**Problem / missing behavior**

The project has no trained-model inference service. An artifact registry and model score do not connect a qualified checkpoint to authenticated tutor/solver requests with enforceable budget and failure behavior.

**Target paths / responsibility**

- `services/api/solver_api/features/hints/service.py`
- `docs/architecture/ARCHITECTURE.md`
- `docs/onboarding/DEVELOPMENT.md`
- `docs/product/DSA_SOLVER_READINESS.md`
- `tests/tooling`

**Implementation scope**

- Deploy one separately operated approved inference endpoint for the exact qualified artifact and wire it through the existing provider-neutral result/usage contracts; do not load GPU weights in web/API processes.
- Reuse existing destination/secret, output-validation, entitlement, concurrency/budget, deadline/retry and kill-switch controls rather than implement a competing authorization or quota stack.
- Add explicit model/artifact/revision provenance, bounded health/readiness and operator-only diagnostics; support the approved offline/local-model route without requiring a paid external provider.

**Acceptance criteria**

- A permitted request reaches only the configured qualified artifact and returns correct provenance; unauthorized/over-budget/oversized/out-of-scope inputs fail before inference as specified.
- Endpoint timeout/crash/malformed output triggers bounded safe behavior and visibly authored fallback only under the existing policy; no fake model output is shown.
- Admission caps hold at the declared serving concurrency, no provider/worker secrets or private tests reach generation context, and a kill switch stops new model work without breaking ordinary practice.

**Validation required**

- Future authorized checks: deterministic fake-endpoint contract/security/timeout/quota fixtures through the existing provider test harness.
- On the approved isolated inference environment, run a small capped end-to-end request/overload/failure smoke using the exact exported artifact and no private learner data.

**Out of scope**

- Choosing or buying serving hardware now
- Replacing B048 transport/entitlement/budget work
- Public activation before the pilot/release gates

**Risk and review**

Model-serving isolation and endpoint configuration can bypass established policy if treated as a new shortcut; reuse existing trusted admission controls.

</details>

<a id="sai-b139"></a>
<details>
<summary>139. SAI-B139: Promote a trained model through a limited pilot and rehearsed rollback [pending]</summary>

**Priority:** P1 · **Phase:** ML-4 evaluation and delivery · **Area:** trained-model-release.

**Suggested role:** Release owner, ML evaluation lead and deployment operator.

**Prerequisites:** [SAI-B001](#sai-b001), [SAI-B003](#sai-b003), [SAI-B057](#sai-b057), [SAI-B059](#sai-b059), [SAI-B110](#sai-b110), [SAI-B124](#sai-b124), [SAI-B126](#sai-b126), [SAI-B128](#sai-b128), [SAI-B135](#sai-b135), [SAI-B136](#sai-b136), [SAI-B137](#sai-b137), [SAI-B138](#sai-b138).

**Problem / missing behavior**

A working endpoint is not a release. The trained artifact needs an accountable go/no-go decision, clear supported scope and a real rollback rehearsal before wider learners rely on it.

**Target paths / responsibility**

- `docs/product/DSA_SOLVER_READINESS.md`
- `docs/status/PROJECT_STATUS.md`
- `docs/onboarding/DEVELOPMENT.md`
- `docs/governance/OPEN_DECISIONS.md`
- `apps/web/features/hints/account-hint.tsx`
- `services/api/solver_api/features/hints/service.py`

**Implementation scope**

- Run an explicitly approved small consented pilot for the trained artifact with fixed audience, duration, traffic/cost ceilings and the B128 declared coverage.
- Present artifact provenance, assistance mode, limitations, unsupported inputs and finite-evidence wording to users; preserve private data/contest rules and ordinary authored practice.
- Rehearse switching to the last qualified artifact or authored-only mode during in-flight work, then record the actual measured pilot outcomes and owner promotion/rejection decision.

**Acceptance criteria**

- The release record binds exact artifact/application revisions, coverage matrix, evaluation evidence, audience/capacity and owner/operator approval.
- Rollback/kill-switch drill stops new model admissions and handles in-flight jobs within their recorded budgets without cross-user results or loss of ordinary practice.
- All preregistered quality/security/resource gates are passed or the pilot remains blocked/rejected; no universal any-DSA or independent security certification claim appears.

**Validation required**

- Future explicitly approved execution: finite end-to-end pilot and rollback rehearsal on the operated test/pilot deployment; record observed outcomes and unrun checks separately.
- Review UI disclosures and release artifacts against the exact served model identity and held-out report.

**Out of scope**

- Unattended permanent public launch
- Automatic model promotion from a training script
- Treating user activity alone as proof of learning improvement

**Risk and review**

Promotion changes real-user behavior and recurring spend; require accountable operations, consent, capacity and a tested fallback.

</details>

<a id="sai-b140"></a>
<details>
<summary>140. SAI-B140: Run a separately approved execution-reward preference or RL experiment [pending]</summary>

**Priority:** P2 · **Phase:** ML-5 conditional improvement research · **Area:** optional-model-research.

**Suggested role:** ML researcher, independent grader reviewer and compute owner.

**Prerequisites:** [SAI-B001](#sai-b001), [SAI-B075](#sai-b075), [SAI-B077](#sai-b077), [SAI-B078](#sai-b078), [SAI-B080](#sai-b080), [SAI-B128](#sai-b128), [SAI-B130](#sai-b130), [SAI-B131](#sai-b131), [SAI-B132](#sai-b132), [SAI-B133](#sai-b133), [SAI-B134](#sai-b134), [SAI-B135](#sai-b135), [SAI-B136](#sai-b136).

**Problem / missing behavior**

SFT may leave systematic failures, but preference tuning or GRPO/RL can reward test exploitation and spend significant compute. The existing roadmap only mentions later research; it implements and runs no RL training stage.

**Target paths / responsibility**

- `docs/research/MODEL_DATA_EVALUATION.md`
- `docs/product/DSA_SOLVER_READINESS.md`
- `services/judge/solver_judge/grading/cases.py`
- `services/judge/solver_judge/sandbox/harness.py`
- `tests/tooling`

**Implementation scope**

- First record a falsifiable hypothesis and a separately approved method/reward/data/compute manifest comparing one narrow preference or execution-reward method against the retained SFT baseline and equal-budget inference alternatives.
- Reuse approved data/artifact tooling; build audited reward checks around independently reviewed finite execution evidence, with bounded generation/judge budgets and anti-reward-hacking fixtures.
- Execute a tiny approved reward/training smoke, then only if valid execute the specifically approved bounded experiment; preserve actual checkpoints, costs, failed runs and independent held-out results.

**Acceptance criteria**

- Synthetic exploit candidates that print forged success, exploit grader assumptions or consume unbounded resources do not earn a valid success reward.
- The actual approved experiment records optimizer updates and full resource/termination evidence; missing approval/valid reward prevents any job, and no improvement is a valid outcome.
- Independent evaluation reports quality, regressions and total cost versus SFT and inference-only alternatives; the candidate is not promoted automatically.

**Validation required**

- Future authorized checks: deterministic reward/manifest fixtures with original finite sandbox cases and no live training.
- Only after separate approval, run the recorded external smoke/experiment and replay the untouched held-out comparison under its fixed budget.

**Out of scope**

- Making RL a prerequisite for releasing a useful SFT/tutor product
- Unlimited GRPO rollouts or unknown reward oracles
- Claiming finite rewards prove general reasoning or correctness

**Risk and review**

Reward hacking, data leakage and resource amplification can produce misleading gains; this optional issue requires an explicit stop/no-go outcome.

</details>

<a id="sai-b141"></a>
<details>
<summary>141. SAI-B141: Operate a consented failure-analysis and retraining improvement cycle [pending]</summary>

**Priority:** P2 · **Phase:** ML-5 conditional improvement research · **Area:** model-lifecycle.

**Suggested role:** ML lifecycle owner and privacy/evaluation reviewers.

**Prerequisites:** [SAI-B001](#sai-b001), [SAI-B003](#sai-b003), [SAI-B063](#sai-b063), [SAI-B077](#sai-b077), [SAI-B078](#sai-b078), [SAI-B128](#sai-b128), [SAI-B130](#sai-b130), [SAI-B134](#sai-b134), [SAI-B135](#sai-b135), [SAI-B136](#sai-b136), [SAI-B139](#sai-b139).

**Problem / missing behavior**

After release, failures and user feedback need a controlled correction path. Automatically training on reported code or repeatedly optimizing against the same holdout would violate consent and undermine future evidence.

**Target paths / responsibility**

- `docs/research/MODEL_DATA_EVALUATION.md`
- `docs/product/DSA_SOLVER_READINESS.md`
- `docs/governance/DATA_AND_LICENSES.md`
- `docs/status/PROJECT_STATUS.md`
- `services/api/solver_api/features/hints/service.py`

**Implementation scope**

- Define bounded operator review of consented/redacted failure categories, with separate source/problem rights checks and no automatic collection of raw private submissions.
- Turn reviewed failures into correction candidates only through the approved corpus pipeline; quarantine any previously exposed evaluation task and preserve a genuinely independent future release set.
- For a justified improvement, create a new approved training/evaluation manifest and execute the existing bounded cycle, comparing to the last released artifact before any owner-authorized rollout. Record no-change/rejected outcomes as well.

**Acceptance criteria**

- Opt-out/deleted/private inputs cannot enter a training batch; approved additions retain immutable provenance, consent and split lineage.
- A failure that came from release evaluation cannot silently become both training data and a claimed unseen success in the next report.
- Each actually attempted improvement has distinct run/artifact IDs, before/after category/regression/cost evidence and a tested rollback link; collecting feedback does not by itself trigger training or deployment.

**Validation required**

- Future authorized checks: synthetic consent/deletion/split-lineage/lifecycle fixtures in ML tooling.
- For a separately approved iteration, replay the retained baseline and candidate manifests and record the actual training, independent evaluation and rollout decision; do not silently reuse old successes as new proof.

**Out of scope**

- Continuous autonomous training on user activity
- Default upload of learner code to models or datasets
- A guarantee that every failure can be corrected or every DSA task solved

**Risk and review**

Feedback loops can turn private data into training material and destroy holdout independence; keep human/owner review and repeatable negative outcomes.

</details>

## PR review and merge process

Other tools implement one scoped task and submit a PR. Bring its URL or number
into an active assistant session. Review covers the exact head diff, task and
dependency fit, contracts/imports, ownership/auth, sandbox boundaries, dependency
and data changes, observed checks, docs and rollback. Requested corrections get
reviewed again at the new head before an owner-authorized merge. Preserve Git
history and never force-push `main`.

The implemented evidence metadata gate checks a structured PR record using
trusted base code with read-only permissions. It does not prove tests ran, approve
code or authorize a merge. Hosted execution of this gate and effective GitHub
branch protection remain unverified. SAI-B127 records the separate enforcement
work; do not treat policy prose as enforced permissions or invent an assistant
GitHub identity.

The assistant can review PRs during active sessions. It cannot continue monitoring
or merging after a session ends. Continuous monitoring would require separately
implemented, approved automation. No unattended monitor or auto-merger is enabled.
See the [full contribution workflow](docs/engineering/AI_CONTRIBUTION_WORKFLOW.md)
and [PR evidence contract](docs/engineering/PR_EVIDENCE.md).

## Keeping this handoff current

Sources: `docs/engineering/backlog/issues.json` owns task detail and completion;
`AnalyseFuture/repository-inventory/features.json` owns feature evidence/gaps;
review annotations under `AnalyseFuture/repository-inventory/reviews/` describe
file purposes; `docs/engineering/handoff-directories.json` describes folder
responsibilities. `PROJECT_STRUCTURE.md` is the shorter layout guide. Earlier
review annotations can describe baseline findings; the dated status/validation
ledgers establish later fixes and executed results.

Stage intended source/documentation first: the static inventory reads Git-index
blobs. Add annotations for new files and descriptions for new folders. Regenerate
task cards, then the root handoff, then the hash inventory after staging the
generated handoff. No application or archive code is executed by these generators.

```sh
python3 scripts/github/build_backlog.py --write
git add <the-specific-intended-files>
python3 -W ignore::SyntaxWarning scripts/verification/project_handoff.py --write
git add PROJECT_HANDOFF.md
python3 -W ignore::SyntaxWarning scripts/verification/repository_inventory.py --write
git add AnalyseFuture/repository-inventory/current-files.json AnalyseFuture/repository-inventory/COMPLETE_FILE_INVENTORY.txt
python3 scripts/github/build_backlog.py --check
python3 -W ignore::SyntaxWarning scripts/verification/project_handoff.py --check
python3 -W ignore::SyntaxWarning scripts/verification/repository_inventory.py --check
python3 scripts/verification/verify_preserved_archives.py --git-index
```

The full runtime gate for implementation changes is `npm run test:all` with the
required supported gVisor environment and browser dependencies. Use the
development guide for setup; never report a skipped integration run as a real
sandbox pass. Documentation-only maintenance uses its relevant static consistency
checks and clearly retains the revision of prior runtime evidence.

When issue API access is available, `python3 scripts/github/publish_issues.py
--publish` reconciles and publishes missing tasks using authorized existing
authentication. It records confirmed results and stops on ambiguous writes.
Regenerate task cards and this handoff after the receipt changes. Never paste
credentials into documentation, chat, issues or commits.
