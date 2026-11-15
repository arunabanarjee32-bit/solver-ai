# Repository audit and AI implementation plan — 2026-11-15

**Baseline:** `main` at `b6f9fe90a05046dfc8adf879d09f91cd2fd5c32a`, examined through the connected GitHub source API. **Scope:** repository tree (132 entries), project handbook, main FastAPI/auth/catalog/submission code, targeted frontend and judge modules, tests and CI, all 20 listed upstream repository metadata records, and source in the two selected research references. The original reference inventory is `docs/PUBLIC_REPOSITORIES_AND_RESOURCES.txt`.

**Evidence rules:** VERIFIED = inspected source/API metadata; DOCUMENTED, NOT REPRODUCED = prior project ledger; INFERRED = a reasoned design implication; UNKNOWN = not independently established. A local clone could not be downloaded in this research environment (DNS to GitHub unavailable). The initial source audit did not run a local clone/test environment. **Subsequent hosted GitHub Actions validation was observed and inspected for the SAI-010 PR**: [run 43737836616](https://github.com/arunabanarjee32-bit/solver-ai/actions/runs/43737836616) passed at `9df915a422c2a45d93d967b66a6cd30a228e6914`, including 137 API passes (29 new hint tests), auth, 91 judge-unit passes (15 gated integration skips), Ruff, TypeScript, build and 17 Playwright passes (1 gated full-judge skip). The historical local sandbox evidence remains separate. No deployment or production security certification is claimed.

## A. Executive assessment

**VERIFIED:** Solver AI is an existing modular monorepo with original three-problem catalog, authored hint ladders, Next.js/Monaco editor, Better Auth-to-FastAPI JWT verification, submission persistence and a separate isolated-judge architecture. **DOCUMENTED, NOT REPRODUCED:** prior local end-to-end sandbox and browser tests passed; see PROJECT_STATUS for counts and limitations.

**VERIFIED missing on inspected baseline:** No model API, generated hints, solver orchestration, solver benchmarks, adaptive learning or contests. An AI chat widget alone would not make these real.

**Decision:** Preserve the existing practice and judge foundation. Implement **SAI-010** first: authenticated, bounded, honestly labeled offline hint contract and a narrow provider boundary. Only later add a real provider under quotas, egress policy, and evaluations.

## B. Modules, architecture and trust boundaries

| Area | Current responsibility / evidence | Assessment |
| --- | --- | --- |
| `apps/web/app/` | Next.js pages, auth route, problem/account/history routes | VERIFIED from file tree and targeted components |
| `apps/web/components/` | `workspace.tsx` public authored hints and practice; `code-pane.tsx` browser drafts/Monaco; `submission-panel.tsx` run/submit and polling | VERIFIED |
| `apps/web/lib/api.ts` | Zod validation of public problem data | VERIFIED |
| `apps/web/lib/submissions.ts` | Per-request Better Auth API token, 15-second network timeout, response parsing | VERIFIED |
| `apps/web/lib/auth.ts` | Better Auth web identity authority | DOCUMENTED, NOT FULLY TRACED |
| `services/api/solver_api/main.py` | Public catalog, signed-account submission APIs, worker-only internal routes; stable public errors and request IDs | VERIFIED |
| `services/api/solver_api/auth.py` | Fixed-origin EdDSA JWKS lookup, validated issuer/audience/subject, token expiry | VERIFIED |
| `services/api/solver_api/catalog.py`, `models.py` | Three original public problems, samples, three authored hints each; no private grading cases | VERIFIED |
| `services/api/solver_api/submissions.py` | SQLite ownership, idempotency, quotas, leases, safe result summaries | VERIFIED targeted functions |
| `services/api/solver_api/body_limit.py` | 128 KiB maximum inbound HTTP body | VERIFIED |
| `services/judge/solver_judge/worker.py` | Dedicated worker credential, heartbeat/leases, cancellation, runner invocation | VERIFIED targeted functions |
| `services/judge/solver_judge/runner.py` | gVisor-only `runsc` Docker boundary; no-network, nonroot, capped input/output, cleanup | VERIFIED targeted functions; runtime enforcement not reproduced |
| `services/judge/solver_judge/cases.py`, `harness.py`, `bounded.py` | Original generated grading, supervisor and finite budgets | DOCUMENTED, NOT FULLY TRACED |
| `tests/e2e/`, `services/api/tests/`, `services/judge/tests/` | Browser, auth, API, hostile-program and worker regressions | VERIFIED files exist; executions not reproduced |
| `.github/workflows/ci.yml` | Configured API/auth/judge tests, lint, typecheck, build, browser | VERIFIED config; hosted outcomes UNKNOWN |

### Existing request flow

```text
Browser / Monaco draft [untrusted code stays in browser]
    |  Better Auth session cookie -> short-lived signed API token
    v
Next.js auth endpoint ----public JWKS----> FastAPI (EdDSA, issuer/audience/subject)
    |                                        |                  |
    |                                 public catalog    owned submission SQLite
    |                                        |                  |
    |                                  authored hints    authenticated queue
    |                                                           |
    |                                                 worker-token lease
    |                                                           v
    |                                              trusted judge controller
    |                                                           |
    |                                         gVisor sandbox (no network)
    |                                                           |
    +<----------------------- sanitized verdict / user-owned history --------+
```

**Trust boundary:** Client-supplied JWTs are verified in `auth.require_user`; clients cannot claim an identity via `X-User-ID`. User source enters `SubmissionStore.create` but the API does not execute it; an authenticated worker fetches it and runs it in the gVisor boundary. Only owned submission records are returned; expected answers are in the trusted worker. **No AI provider should receive worker credentials or private grading cases.** The proposed tutor route has a distinct public-only context and never accepts executable code.

### Present versus missing

| Feature | Baseline | Next gate |
| --- | --- | --- |
| Catalog/editor/auth/history | Implemented, locally documented | Preserve regressions |
| C++17/Python isolated judging | Local implementation | Independent deployment review |
| Authored hint ladder | Implemented | Preserve without sign-in requirement on problem page |
| Versioned authenticated hint API | Missing | SAI-010 |
| Generated tutor / debugger | Missing | Configure provider and safe data flow |
| Multi-candidate verified solver | Missing | Provider plus judge authorization, budgets and evaluations |
| Contests, teams, adaptive practice | Missing | Later separate features |
| Model training and serving | Missing | After rights-approved held-out evaluations |

### Prioritized risk register

| Priority | Evidence | Risk and action |
| --- | --- | --- |
| P0 | VERIFIED `OPEN_DECISIONS.md` | No original-code outbound license or contributor IP policy: **maintainer decision required**, do not invent one |
| P0 | DOCUMENTED, NOT REPRODUCED `PROJECT_STATUS.md` | Local gVisor environment lacks aggregate cgroup accounting; obtain external isolation review before exposing public judge |
| P0 | VERIFIED `auth.py`, `submissions.py` | Identity/owned submission security is valuable existing work: maintain replay, cross-user, quota and lease tests |
| P1 | VERIFIED `catalog.py`, `models.py` | Authored hints and future AI must not be conflated; add explicit provenance |
| P1 | INFERRED | Future provider needs per-user AI quota/cost budget, controlled egress/endpoint selection, prompt-injection defenses, bounded outputs and fail-safe shutdown |
| P1 | VERIFIED config; UNKNOWN hosted status | CI configured but no hosted result verified at audit time; observe PR workflow |
| P2 | VERIFIED targeted frontend components | New hint API needs typed browser client, clear offline label and accessibility regression before UI integration |
| P2 | DOCUMENTED `PROJECT_STATUS.md` | SQLite retention/deletion/backups and account recovery not production-ready |
| P2 | UNKNOWN | Full code accessibility audit, live contest abuse controls, production latency and external model quality |

## C. All 20 public study repositories

Repository metadata and default-branch SHA were fetched on **2026-11-15**. The abbreviated SHA identifies the exact inspected HEAD; maintenance dates indicate activity, not security assurance. License IDs are from GitHub metadata except MOJ (explicit upstream README); NOASSERTION means **check actual license documents before reuse**. This is a **triage-level review** for the 18 non-primary candidates, not an audit of all their source trees or dependencies.

| # | Repository / head | License indication | Purpose / integration decision |
| --- | --- | --- | --- |
| 01 | [Nan-Do/phi-code](https://github.com/Nan-Do/phi-code) `b3ca73d7dcc3` | Apache-2.0 | **PRIMARY REFERENCE**: test/rank multiple code candidates; unsafe local execution must not transfer |
| 02 | [kagnlp/CodeGenerator](https://github.com/kagnlp/CodeGenerator) `9cf09ee6c788` | MIT | **PRIMARY REFERENCE**: bounded planning, simulation and debugging; no copied executor |
| 03 | [0xmetaschool/dsa-gpt-tutor](https://github.com/0xmetaschool/dsa-gpt-tutor) `e000b82487d7` | MIT | DSA tutor UX only; older research prototype, not a judge |
| 04 | [QingdaoU/OnlineJudge](https://github.com/QingdaoU/OnlineJudge) `df873278ab1b` | MIT | Problem admin/contest comparison; full server replacement deferred, latest code 2024 |
| 05 | [MonashAPS/MOJ](https://github.com/MonashAPS/MOJ) `2d5ca19bc298` | AGPL-3.0-or-later, README | Current ICPC/contest workflows reference; network copyleft and stack integration need review |
| 06 | [DMOJ/online-judge](https://github.com/DMOJ/online-judge) `6aaddea6aaea` | AGPL-3.0 | Mature judge site and contest patterns; defer integration |
| 07 | [DMOJ/judge-server](https://github.com/DMOJ/judge-server) `1245dc4158db` | AGPL-3.0 | Interactive tasks/runners; study isolation only when requirements grow |
| 08 | [engineer-man/piston](https://github.com/engineer-man/piston) `de2b365ac759` | MIT wrapper; bundled runtime caveats | Already reviewed/deferred by ADR 0002, not a default sandbox replacement |
| 09 | [microsoft/monaco-editor](https://github.com/microsoft/monaco-editor) `85549d055d7a` | MIT | Existing editor dependency; keep |
| 10 | [shadcn-ui/ui](https://github.com/shadcn-ui/ui) `e62c9435fff7` | MIT | UI components on demand; avoid redesign for its own sake |
| 11 | [better-auth/better-auth](https://github.com/better-auth/better-auth) `8382ce613f04` | MIT | Existing identity dependency; preserve tested integration |
| 12 | [fastapi/fastapi](https://github.com/fastapi/fastapi) `a3260d49e97b` | MIT | Existing API framework; keep |
| 13 | [huggingface/transformers](https://github.com/huggingface/transformers) `3a134bc37f7c` | Apache-2.0 | Optional external-GPU model research; defer |
| 14 | [huggingface/peft](https://github.com/huggingface/peft) `3e8f605975c5` | Apache-2.0 | LoRA tooling; defer until baseline and rights |
| 15 | [huggingface/trl](https://github.com/huggingface/trl) `8ad18ec1b649` | Apache-2.0 | SFT/preference optimization; defer |
| 16 | [unslothai/unsloth](https://github.com/unslothai/unsloth) `57d9d1ded53e` | Apache-2.0 core | Optional efficient tuning, optional-component terms vary; defer |
| 17 | [vllm-project/vllm](https://github.com/vllm-project/vllm) `dadf740edf4e` | Apache-2.0 | External GPU serving if justified; defer |
| 18 | [meilisearch/meilisearch](https://github.com/meilisearch/meilisearch) `1b782653f25c` | Metadata NOASSERTION | Optional search; simple catalog now, edition terms to review |
| 19 | [open-telemetry/opentelemetry-js](https://github.com/open-telemetry/opentelemetry-js) `5a78e6aef1fc` | Apache-2.0 | Telemetry when justified; redact code/session data |
| 20 | [google-deepmind/code_contests](https://github.com/google-deepmind/code_contests) `fa7a4f8139aa` | Apache-2.0 code; separate data rights | Archived 2024; evaluation reference only; upstream README warns third-party data rights |

**Unverified for 18 non-primary candidates:** exact transitive dependency exposure, full architecture, production threat models and compatibility tests. No external project source is incorporated in this branch.

### Source-tree triage: 18 additional candidates

Beyond the two deep AI references, GitHub README and top-level tree were inspected for the other 18 candidates. This verifies project structure and stated purpose, but **not full dependency trees, runnable integration or security**. No such code was imported.

| Candidate | Observed upstream directories / workflow | Compatibility, limits and action |
| --- | --- | --- |
| dsa-gpt-tutor | Next.js `src/`, application config and package manifest | AI chat and guided-question UX could inspire a future tutor UI. No demonstrated isolated CP judge; maintain separate ownership and no copied content |
| QingdaoU OnlineJudge | Django services `account/`, `contest/`, `judge/`, `problem/`, `submission/` | Educational contest admin design; old default-branch head (2024-10). Whole Python/Vue platform would duplicate auth/API and expand deployment/security surface |
| MOJ | `apps/`, `packages/`, `convex/`, `infra/`, `actions/`, `docs/`; describes live verdicts and ICPC/IOI contest formats | Valuable contest model, but Convex/TS platform does not replace current Python judge. **LICENSE inspected:** AGPL-3.0-or-later, requiring deliberate legal review of network-use and distributed modifications |
| DMOJ online-judge | Django `judge/`, `websocket/`, `templates/`, `dmoj/`, `requirements.txt` | Extensive contest and verdict workflows; integrating wholesale conflicts with existing auth + FastAPI. AGPL-3.0 and operational dependency review necessary |
| DMOJ judge-server | `dmoj/`, `testsuite/`, `contrib/`, Python `pyproject.toml` plus runtime support docs | Interactive grading and custom validators worth studying if product needs them. Host OS and security assumptions need assessment; no direct substitution for gVisor, AGPL-3.0 |
| Piston | `api/`, `builder/`, `cli/`, `packages/`, `piston/`, lowercase `readme.md` | General execution framework; documented stock deployment/runtime restrictions in ADR 0002. Wrapper MIT, bundled isolation dependency obligations and privileged operation require separate assessment. Existing controlled runner preferred |
| Monaco Editor | `src/`, `webpack-plugin/`, `samples/`, `test/`, `ThirdPartyNotices.txt` | Bundled editor in existing web app. Keep tested version and notices; upstream latest is not automatically the release currently installed |
| shadcn/ui | `apps/`, `packages/`, `templates/`, `skills/`, pnpm monorepo | Incremental components only, while keeping existing accessible workflow; importing whole design system creates churn without direct learner value |
| Better Auth | `packages/`, `docs/`, `test/`, `e2e/`, `SECURITY.md` | Existing signed auth authority. Scope future upgrade to pin/version and run real auth regression suite; avoid creating second identity service |
| FastAPI | `fastapi/`, `docs_src/`, `tests/`, `pyproject.toml` | Existing Pydantic/FastAPI system; reuse the current API. Avoid replacing it with another upstream backend |
| Transformers | `src/`, `tests/`, `examples/`, `benchmark_v2/` | Model training/inference framework on adequately provisioned hardware. Not required for API-based tutoring; checkpoints have separate model terms |
| PEFT | `src/`, `method_comparison/`, `examples/`, `tests/` | Low-rank fine-tuning only after rights-approved dataset, reproducible baselines and external GPU budget |
| TRL | `trl/`, `examples/`, `tests/`, `MIGRATION.md` | Training algorithms such as SFT/GRPO; environment and reward correctness costs unjustified before verified judge/evals |
| Unsloth | `unsloth/`, `studio/`, `docker/`, `tests/` | Optional efficient training and desktop tools; GPU and optional-component license checks needed; no immediate integration |
| vLLM | `vllm/`, `csrc/`, `rust/`, `docker/`, `benchmarks/` | High-throughput GPU inference service; only add if own throughput and economics exceed simpler provider API. Separate service/resource isolation |
| Meilisearch | Rust `crates/`, `workloads/`, `Cargo.toml`, `LICENSE`, `LICENSE-MIT`, `LICENSE-EE` | Current 3-problem catalog needs no standalone search. **LICENSE inspected:** MIT **and** BUSL-1.1 (enterprise sections); evaluate exact edition on adoption |
| OpenTelemetry JS | `api/`, `packages/`, `experimental/`, `integration-tests/`, `e2e-tests/` | Trace/metrics instrumentation when live operations require it; never emit source, model prompts, tokens or hidden tests |
| DeepMind CodeContests | `contest_problem.proto`, `execution/`, `third_party/`, `WORKSPACE`; repository archived | Useful dataset schema and baseline reference, not a blanket import. **LICENSE/README inspected:** Apache-2.0 for code, CC BY 4.0 claimed for non-code; source platform/problem rights still require legal review before usage/training |

**Maintenance snapshot:** Head commits and licenses in the matrix above were retrieved on 2026-11-15. Most popular frameworks and model libraries had commits during October–November 2026; CodeSIM's reference head dates June 2025, phi-code's December 2025, QingdaoU's October 2024, and DeepMind CodeContests' latest default head dates January 2023. Repository star counts and GitHub `updated_at` are not proof of active code maintenance. Model weights, training accelerators and licensed data are **not installed** in Solver AI. Copying code, running bulk dataset ingestion, or provisioning external GPUs would require later approval.

## D. Exactly TWO selected primary research repositories

### 1. CodeSIM / MapCoder (`kagnlp/CodeGenerator`, `9cf09ee6c788bfda3b7e1524e88be3447098eb24`)

**VERIFIED modules:** `src/promptings/CodeSIM.py` implements bounded outer plan attempts, model-driven simulation/plan adjustment, code generation and bounded debug attempts; `src/models/Base.py` and `ModelFactory.py` abstract providers; `src/evaluations/api_comm.py` bridges to an external execution API. The default strategy parameters in inspected code include `max_plan_try=5` and `max_debug_try=5`—these are **research defaults, not recommended budgets**.

**Learn/reimplement independently:** explicit stages, measured model calls, limited repair budget and a consistent versioned candidate record. **Do NOT copy:** the external judge protocol, use of Python `exec` in `src/evaluations/func_evaluate.py`, free-form test-log feedback containing private cases, upstream prompts or claims about benchmark gains. **License:** repository MIT as reported upstream; verify notices if copying any code (none copied). **Maintenance:** last default-branch commit June 2025 as of audit; benchmark claims not reproduced. **Complexity:** moderate to adapt concepts to the existing FastAPI and authorized judge; expensive/high-risk to transplant the whole pipeline.

### 2. phi-code (`Nan-Do/phi-code`, `b3ca73d7dcc37aed6809eb7789281465a7a04d22`)

**VERIFIED modules:** `solver/main.py` configures a llama.cpp-compatible model endpoint and a sentence-transformer ranker; `solver/terminal.py` generates multiple Python candidates, scores sample passes and embedding similarity, then ranks by tests passed first; `solver/utils.py` performs completion requests; `ranker/train.py` contains optional representation/ranker training. Its `solver/leetcode.py` executes generated Python via `exec` inside an OS multiprocessing child; `solver/atcoder.py` and `solver/codeforces.py` run generated scripts via host Python subprocesses. These are **not** Solver AI's secure multi-tenant execution boundary.

**Learn/reimplement independently:** candidate diversity, transparent test-evidence-first selection and reproducible ranking. **Do NOT copy:** host-side execution, site-specific content scrapers, corpus files, or assume sentence similarity equals functional correctness. **License:** repository Apache-2.0; problem-content permissions are separate. **Maintenance:** last default-branch commit December 2025; contest anecdote is not a benchmark on unseen tasks. **Complexity:** moderate for a bounded candidate ranking interface, high for training/self-hosted embedding models.

**Why these two:** CodeSIM explains *how to develop, challenge and refine a plan*; phi-code explains *how to compare multiple attempts*. Together they target the future solver, while the existing gVisor judge remains the authority on executed evidence. We explicitly select **no third primary repository**. Verify improvement using a held-out, rights-approved task set with fixed model, prompt, seed, execution budgets and pass@1/pass@k, latency and cost; compare no-repair/single-candidate baselines. Do not claim general correctness from finite tests.

## E. Provider-neutral incremental design

```text
Authorized problem + signed learner token
     |            (future contest policy gate)
     v
FastAPI POST /api/v1/hints
     |
strict slug + level + max body size
     |
public catalog context only (no source or private tests)
     |
HintBackend interface
     |-- AuthoredHintBackend [implemented in SAI-010; no AI cost]
     |-- Future bounded real model adapter [NOT implemented]
     |
bounded timeout + validated response + explicit provenance
     v
typed accessible browser hint presentation [future UI integration]
```

The **next** real provider must enforce: controlled provider URL (no user-selected SSRF), configuration only through deployment secrets, strict maximum token usage, user quotas and budget, no raw prompts/responses in logs, safe unavailable/timeout handling, validated response shape, no model-selected trust labels, and contest-specific entitlement. Real generated code must use existing authorized submission/judge pathways, never API/web `exec` or subprocess. Proposed four modes: tutor (progressive non-spoiler), debugger (bounded user code and authorized evidence), solver/research (multi-candidate evidence), contest (disable assistance if forbidden). Only tutor's **offline contract** is part of this change.

**Build vs reuse:** Build original tutor/solver request orchestration, rights-aware datasets, budget logic and learning UI. Reuse existing Monaco, Better Auth, FastAPI and gVisor with tests. Study CodeSIM/phi-code conceptually. Defer a solver microservice, heavyweight search stack, AGPL contest import, GPU training and paid provider until justified.

## F. Ordered roadmap and rollback gates

| Gate | Value, dependencies, files and acceptance | Tests / risks / rollback |
| --- | --- | --- |
| A. Audit | Inventory existing tests and trust boundaries; `docs/`, CI; choose two references | Human review, no behavior change; revert doc if inaccurate |
| B. SAI-010 offline hint contract | Add `solver_api/hints.py`, `main.py` route, `tests/test_hints.py`; signed user gets a level 1–3 authored hint with explicit `ai_generated=false` | Invalid/unauthorized/timeout/malformed/prompt-injection/size/provenance tests; no new dependency; revert route/module |
| C. Real tutor provider | B and policy/budget approval; add one provider adapter and typed browser UI | Network mock tests, cost/token cap, auth/contest restrictions, safe errors; disable via `SOLVER_HINT_BACKEND=authored` |
| D. AI debugger | C, authorized code/evidence and privacy rules; API + frontend | Redaction, limited input, regression tests; feature flag off |
| E. Verified solver | D and judge entitlement/budget; original planner/candidates/ranker, no new service without evidence | Deterministic gVisor tests, timeout/cost/repair caps, no private-answer leak; disable solver feature |
| F. Reproducible evaluation | E and rights-approved held-out set; `ml/evaluation/` only when implemented | Baseline comparisons, provenance, uncertainty; roll back poor model |
| G. Learning/contests | Foundation stable; topic paths and ICPC rules separately | Integrity, scoring and authorization integration; disable events |
| H. Scale/training | Validated usage and explicit infrastructure approval | Model/license/retention/cost checks; revert deployment/provider independently |

No delivery dates or benchmark improvements are promised. C–H have no existing funded provider and are not marked as implemented.

## G. First patch and verification boundary

**Proposed branch:** `feat/sai-010-authored-hint-contract`.
**Targeted files:** `services/api/solver_api/hints.py` (new), `services/api/solver_api/main.py` (one authenticated route), `services/api/tests/test_hints.py` (new), and this audit note. Existing public problem hints remain available without auth through `GET /api/v1/problems/{slug}`. Unconfigured alternate backends fail safely. The offline path makes no model call, reads no submissions, and executes no code.

**Commands verified by hosted GitHub Actions** (the real gVisor integration suites require the separate local runner):
```sh
npm run test:api
npm run test:auth
npm run test:judge
uv run --project services/api --frozen ruff check services/api services/judge scripts
npm run typecheck
npm run build
npm run test:e2e
```
The sandbox integration is only required if its execution boundary changes; it does not in SAI-010. Observe hosted CI separately and annotate actual outcomes; a green CI is not a production security certification. No fresh local gVisor sandbox runs were conducted; the hosted CI passed the standard non-gVisor tests, build and browser checks.

## H. Next three independently testable tasks

1. **SAI-010 review and integration:** run the full API/auth suite against this PR and observe GitHub Actions; review `solver_api/hints.py` for provenance, strict level parsing and all failure cases. Merge only with maintainer approval.
2. **Typed frontend hint client:** add Zod contract to `apps/web/lib/`, an authenticated, clearly marked authored/AI hint control to `apps/web/components/workspace.tsx`, and Playwright auth/offline/retry/a11y coverage. Preserve the currently accessible unauthenticated authored hint ladder.
3. **Provider/cost threat model ADR:** specify a real provider interface in `docs/adr/` including fixed destination, output/token caps, per-user budgets, error behavior, logout window, approved public context, contest restrictions and rollback; only then implement one provider behind an explicit opt-in flag.

**Owner decisions not made here:** outbound license, contributor IP terms, public hosting budget, production identity/retention policy and choice of commercial AI provider. No paid infrastructure, external code, model weights or datasets were added.
