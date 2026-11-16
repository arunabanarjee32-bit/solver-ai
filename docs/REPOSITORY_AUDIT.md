# Repository audit — 2026-11-16

**Source of truth:** GitHub `main` at `9952f8b5fa74f6900d57d1b48e3a26f3e962a358`. The 135-entry recursive Git tree, source files listed below, tests, prior audit, and 20 upstream default-branch refs were inspected through the connected GitHub API. GitHub permissions permit a separate feature branch. Open PRs at audit start: zero. A local `git ls-remote` failed because this environment cannot resolve github.com. Do not construe earlier local validation as re-run here. [Previous detailed audit](AUDIT_AND_AI_PLAN_2026-11-15.md) records original evidence and history.

## Actual monorepo inventory

| Layer / source path | Implementation evidence | Assessment / next priority |
| --- | --- | --- |
| `apps/web/app/`; `components/catalog.tsx` | Next.js 16 routes, public three-original-problem library, filtering | Implemented local MVP; maintain API schema and accessibility |
| `apps/web/components/workspace.tsx`, `code-pane.tsx`, `app/globals.css` | Monaco Python/C++17, browser-only drafts and authored public hint ladder | Implemented; do not upload drafts to hints or mislabel authored content |
| `apps/web/lib/auth.ts`, `auth-client.ts`, `app/api/auth/[...all]/route.ts` | Better Auth sessions, local SQLite, EdDSA API JWT | Implemented local identity; P0 production recovery/verification and retention decisions |
| `apps/web/lib/submissions.ts`, `submission-panel.tsx`, `submission-history.tsx` | Authenticated bearer requests; owned submission and polling UI | Implemented; preserve cancellation, ownership and failure behavior |
| `apps/web/lib/api.ts`, `next.config.ts` | Zod response guard, local same-origin rewrite to FastAPI | Implemented; explicit schema opt-in for new routes |
| `services/api/solver_api/main.py`, `catalog.py`, `models.py` | Public catalog; versioned API, stable error codes | Implemented; catalogue is three original seeds, not competitor content |
| `services/api/solver_api/auth.py` | Fixed-JWKS EdDSA signature, issuer/audience/subject verification | Implemented; fail closed on invalid credentials |
| `services/api/solver_api/submissions.py` | Owned SQLite history, idempotency, quota, durable leases | Implemented locally; P0 production persistence/backup policy remains open |
| `services/api/solver_api/hints.py`, `services/api/tests/test_hints.py` | Signed `POST /api/v1/hints`, levels 1–3, authored source, provider Protocol | **Already on main**; no paid provider. This is not an unmerged backend feature |
| `services/judge/solver_judge/{worker,runner,cases,harness,bounded}.py` | Worker-token control plane, original grading, gVisor-only Docker sandbox with preflight | Implemented local isolated runner; production exposure blocked on independent review |
| `services/api/tests/`, `services/judge/tests/`, `tests/e2e/` | Auth, API, queue, hostile-program, browser regressions | Present; hosted CI can run standard suites but not real gVisor tests |
| `scripts/`, `compose.yaml`, `compose.cloud.yaml`, `.github/workflows/ci.yml` | Local startup, isolated-worker setup, CI/frozen installs | Present; no public production deployment established |

**Real data path:** Browser obtains signed short-lived token through Better Auth; API verifies immutable user subject against configured JWKS. Public catalog and authored hints are served directly. User source goes to owned SQLite queue only after explicit Run/Submit; worker-only secret leases job to a trusted controller; controller uses gVisor for execution and returns sanitized verdict; API checks ownership on results. Public hint context contains no submitted source or private judge tests. Never run model code in browser/API/host Python.

## Risks and incomplete work

- P0: original project outbound LICENSE and inbound contributor-IP policy are undecided (`docs/OPEN_DECISIONS.md`); no automatic relicensing.
- P0: public multi-tenant judge is **not certified**; absent aggregate cgroup accounting, isolated runtime maintenance and incident controls remain deployment blockers.
- P0: local account recovery/email verification, retention/deletion, backup and JWT logout-delay policies remain undecided.
- P1: backend hints exist but on `main` lack frontend calling code. SAI-011 integrates that path on a feature branch with explicit provenance; no genuine generated tutor yet.
- P2: solver, debugger, fair ICPC contests, analytics, training and production observability remain unimplemented. A prior audit's statement that the hint endpoint was missing is stale for current `main`.

## Full 20-repository study inventory

**Method:** Default branch and HEAD below refreshed from GitHub branches on 2026-11-16. License indication and architectural top-level tree were inspected in the 2026-11-15 source audit except CodeSIM and phi-code licenses/source independently reread on 2026-11-16. Exact release condition, transitive CVEs and deployment compatibility were **not** audited for all 20. HEAD changes are not release or quality guarantees. Complexity/value are relative: L/M/H and low/medium/high benefit to our present milestone. No upstream code was copied.

| # | Candidate / default HEAD (12 chars) | License indication | Useful architecture / security and compatibility | Adopt? Complexity / value |
| --- | --- | --- | --- | --- |
| 01 | [phi-code](https://github.com/Nan-Do/phi-code) main `b3ca73d7dcc3` | Apache-2.0 confirmed | `solver/terminal.py` multi-sample test/rank, `ranker/train.py`; unsafe `exec`/host execution, Python-only reference | **Primary research**; M / high later |
| 02 | [CodeGenerator](https://github.com/kagnlp/CodeGenerator) master `9cf09ee6c788` | MIT confirmed | `src/promptings/CodeSIM.py` simulation/repair, provider abstraction; avoid its direct evaluator and unbounded copies | **Primary research**; M / high later |
| 03 | [dsa-gpt-tutor](https://github.com/0xmetaschool/dsa-gpt-tutor) main `e000b82487d7` | MIT (prior audit) | Next.js tutoring UX, not a proven CP solver or sandbox | UX-only; L / medium |
| 04 | [QingdaoU OnlineJudge](https://github.com/QingdaoU/OnlineJudge) master `df873278ab1b` | MIT (prior audit) | Django account/contest/admin; older reference, adds duplicate auth/judge | Reference; H / low now |
| 05 | [MOJ](https://github.com/MonashAPS/MOJ) main `2d5ca19bc298` | AGPL-3.0-or-later | TypeScript/Convex ICPC/IOI scoreboards; network-copyleft and stack changes | Contest reference; H / medium later |
| 06 | [DMOJ online-judge](https://github.com/DMOJ/online-judge) master `6aaddea6aaea` | AGPL-3.0 | Django contest site, separate full-stack ecosystem | Reference; H / medium later |
| 07 | [DMOJ judge-server](https://github.com/DMOJ/judge-server) master `1245dc4158db` | AGPL-3.0 | Interactive/custom graders; host security model would need new review | Judge reference; H / medium later |
| 08 | [Piston](https://github.com/engineer-man/piston) master `de2b365ac759` | MIT wrapper; transitive caveats | General code execution; stock privilege/runtime choices differ from existing gVisor | Defer; H / low now |
| 09 | [Monaco](https://github.com/microsoft/monaco-editor) main `85549d055d7a` | MIT | Existing pinned local browser editor and sanitizer build guard | **Already dependency**; L / high |
| 10 | [shadcn/ui](https://github.com/shadcn-ui/ui) main `e62c9435fff7` | MIT | Optional accessible components; importing entire UI wastes effort | Selective only; L / low now |
| 11 | [Better Auth](https://github.com/better-auth/better-auth) main `8382ce613f04` | MIT | Already used web identity/JWT; upgrade only with regression evidence | **Already dependency**; M / high |
| 12 | [FastAPI](https://github.com/fastapi/fastapi) master `25584a5bc84c` | MIT | Existing validated REST backend; do not replace | **Already dependency**; L / high |
| 13 | [Transformers](https://github.com/huggingface/transformers) main `696c46bacf29` | Apache-2.0 | Open-weight model tooling; GPU + separate model license | Defer; H / low now |
| 14 | [PEFT](https://github.com/huggingface/peft) main `3e8f605975c5` | Apache-2.0 | LoRA when baselines and rights exist | Defer; H / low now |
| 15 | [TRL](https://github.com/huggingface/trl) main `add89358503a` | Apache-2.0 | SFT/RL/GRPO requires sound reward/evaluation | Defer; H / low now |
| 16 | [Unsloth](https://github.com/unslothai/unsloth) main `43898738c0d9` | Apache-2.0 core; optional terms | Training acceleration; optional licenses/GPUs need review | Defer; H / low now |
| 17 | [vLLM](https://github.com/vllm-project/vllm) main `c4182020b39a` | Apache-2.0 | Separate GPU inference only if throughput economics justify it | Defer; H / low now |
| 18 | [Meilisearch](https://github.com/meilisearch/meilisearch) main `1b782653f25` | Community MIT / enterprise BUSL caveat | Rust search; three-problem catalog does not justify service | Defer; M / low now |
| 19 | [OpenTelemetry JS](https://github.com/open-telemetry/opentelemetry-js) main `5a78e6aef1fc` | Apache-2.0 | Node traces when ops require; redact prompts/tokens/source | Defer; M / medium later |
| 20 | [DeepMind code_contests](https://github.com/google-deepmind/code_contests) main `fa7a4f8139aa` | Apache code; separate dataset rights | Archived benchmark/data schema; source-site rights must be checked | Reference only; M / medium later |

**Separate issues before dependency adoption:** exact commit or version pin, upstream license/NOTICE, included dependencies, known advisories, integration tests, and intellectual property rights to problems/datasets. Read [primary research](PRIMARY_RESEARCH_REPOS.md), [strategy](OPEN_SOURCE_STRATEGY.md) and the [2026-11-15 detailed audit](AUDIT_AND_AI_PLAN_2026-11-15.md).

**Verified vs assumed:** GitHub tree/branches and inspected files above are direct evidence. Earlier test counts in PROJECT_STATUS are historical; this audit's first CI evidence must be recorded separately after a completed run. Security posture and benchmark performance are not inferred from GitHub star counts, advertised results, or successful unit tests.
