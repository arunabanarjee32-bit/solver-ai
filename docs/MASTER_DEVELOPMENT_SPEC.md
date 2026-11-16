# SOLVER AI — MASTER DEVELOPMENT SPECIFICATION

**Preserved user-development instructions from the 2026-11-16 project conversation.**

This is a **structured restatement** of the long user-submitted *"MASTER DEVELOPMENT PROMPT — SOLVER AI"*, not a guaranteed word-for-word reproduction. It captures the project's complete task definitions and non-negotiable rules so future coding sessions can resume without the original conversation. The source of truth for implementation remains the live repository.

**Repository:** https://github.com/arunabanarjee32-bit/solver-ai

## Mission and roles

Build an original, independently owned, commercial-quality AI-native system for competitive programming, DSA learning, practice and ICPC preparation. Product/workflow benchmarks include LeetCode, Codeforces, AtCoder, HackerRank and AI coding assistants. **Do not copy proprietary competitor code, statements, editorials or hidden tests.**

The AI coding agent should act as principal software architect, senior engineer, ML/AI researcher, competitive-programming specialist, security engineer, reviewer and Codex developer. Audit before coding. Work autonomously within available limits. Deep research is useful when it produces decisions and tested code; do not spend time, credits or paid resources for appearances. If execution is constrained, write findings, implement and test the smallest safe change, commit to authorized feature branch and give a precise resume path. Never fabricate inspections, CI results or deployments.

## Task 1 — Complete existing-repository audit

Inspect latest `main` HEAD/commit, repository status and PRs. Read `README.md`, `AGENTS.md`, `docs/INDEX.md`, `PROJECT_VISION.md`, `PRODUCT_REQUIREMENTS.md`, `ARCHITECTURE.md`, `ROADMAP.md`, `PROJECT_STATUS.md`, `CODEX_PLAYBOOK.md`, `OPEN_SOURCE_STRATEGY.md`, `OPEN_DECISIONS.md`, `AI_SOLVER.md`, `JUDGE_SECURITY.md`, `MODEL_DATA_EVALUATION.md`, `AUDIT_AND_AI_PLAN_2026-11-15.md`, `PUBLIC_REPOSITORIES_AND_RESOURCES.txt` and relevant ADRs.

Inspect `apps/web/` including components and libs; `services/api/solver_api/`, `services/judge/solver_judge/`, API/judge tests, `tests/e2e/`, scripts, CI, Compose and dependency lockfiles. Identify implemented/partial/documented-only/broken, redundant modules, identity and ownership boundaries, judge submission routing, API contracts, reuse opportunities and risks. Maintain a source-path/evidence-based architecture inventory.

**Known verified finding:** On `main`, the signed `POST /api/v1/hints` backend and `services/api/solver_api/hints.py` and `services/api/tests/test_hints.py` already exist. Do not recreate or describe them as unmerged. The frontend gap was addressed in PR #5; check whether merged before editing.

## Task 2 — Analyze all twenty public study repositories

Treat `docs/PUBLIC_REPOSITORIES_AND_RESOURCES.txt` as the master inventory. Evaluate upstream URLs, default branches, relevant commit SHAs, primary architecture, maintenance/release condition, license/commercial obligations, security, compatibility with current code, safe dependencies vs concepts to reimplement, complexity and practical value. Verify important facts from upstream original README, source, manifests, tests, LICENSE and docs. Distinguish evidence from assumptions. **Never automatically clone or import all 20.**

## Task 3 — Select exactly two AI problem-solving research references

Previous selection: **CodeSIM / MapCoder** at https://github.com/kagnlp/CodeGenerator (planning, simulation and bounded refinement) plus **phi-code** at https://github.com/Nan-Do/phi-code (diverse candidates and tests-first ranking). Verify they remain best; change only if strongly justified. Record source modules, algorithms, synergy, integration plan, non-reusable code, security/license restrictions, complexity and measurable acceptance. Piston, DMOJ, MOJ and QingdaoU remain judge/contest references, not primary AI solvers. No unsupported benchmark claims.

## Task 4 — Design the full incremental architecture

- **Frontend:** professional accessible responsive Next.js; Monaco Python/C++, problem detail/samples, public authored hints, signed-in AI (when real), debugging, history, progress and eventual contests.
- **Backend:** preserve FastAPI and Better Auth/JWT ownership, queue and judge APIs; use narrow typed/versioned contracts, bounded inference orchestration; postpone DB/queue migration until measured.
- **Tutor:** explain algorithms from beginner to advanced, progressive non-spoiler hints, explain code/complexity, review solutions, analyze likely logic errors, track authorized learning progress, and label output `authored` / `mock` / `model` honestly.
- **Debugger:** reproduce only in authorized isolated execution, explain CE/RE/WA, show minimal fixes, use real evidence, redact hidden tests and privileged data.
- **Verified solver:** parse constraints, classify algorithm families, plan approaches, generate multiple bounded candidates, simulate/reason, compile and test in gVisor, rank by evidence, cap retries, explain proof ideas/complexity and uncertainty, track cost/latency/accuracy. Do not `exec`/`eval`/host subprocess arbitrary code; finite passed tests are not universal correctness proof.
- **ICPC/contests:** later registrations, teams, scoring/penalties, freeze, rating/analytics, administration, contest-integrity AI restrictions; not before essential learning/solver gates.
- **Models:** provider-neutral offline mode, deterministic tests first; compare API and open-weight models separately; train/serve with Transformers/TRL/PEFT/Unsloth/vLLM only when legal data, benchmarks, economics, GPUs and approval justify it.

## Task 5 — Prioritize a real backlog

P0 = security/correctness/ownership/reliability; P1 = essential working tutor/integration; P2 = evidence-first solver/debugging; P3 = contest/personalized learning; P4 = production scale/advanced ML.

Every task needs unique ID, goal/user behavior, existing reused code, exact paths, implementation outline, dependencies, acceptance/test cases, security/privacy implications, relative complexity, infrastructure/model expense and rollback. Distinguish MVP from later production features; do not create speculative services just to appear advanced.

## Task 6 — Implement the smallest missing high-value change

Original first milestone: **Integrate the already implemented signed hint endpoint in the frontend** while reusing Better Auth JWT, strict Zod request/response, preserving guest authored ladder, optional separate account request, accurate source provenance, robust unauthenticated/timeout/cancellation/error/retry/responsive/accessible states and API/browser regression tests. No paid model, no user-source upload in hint request, no changed judge/auth boundary. This was implemented/tested on [PR #5](https://github.com/arunabanarjee32-bit/solver-ai/pull/5); do not duplicate after merge.

After that, independently propose a threat-modeled provider adapter with fixed egress and token/user/spend budgets; do not implement a paid provider without maintainer approval.

## Task 7 — Verify for real

Run the actual supported commands: `npm ci`; `uv sync --project services/api --frozen`; `npm run test:api`; `npm run test:auth`; `npm run test:judge`; `uv run --project services/api --frozen ruff check services/api services/judge scripts`; `npm run typecheck`; `npm run build`; `npm run test:e2e`. For judge changes run real gVisor integration tests in supported isolated environment. Record exact pass/fail/skip/environment, regressions and fixes. Never weaken isolation or invent CI results.

## Task 8 — Preserve all research and context

Create or update `docs/REPOSITORY_AUDIT.md`, `PRIMARY_RESEARCH_REPOS.md`, `AI_ARCHITECTURE_PLAN.md`, `IMPLEMENTATION_BACKLOG.md`, `IMPLEMENTATION_PROGRESS.md` and synchronize `PROJECT_STATUS.md`, `INDEX.md` and `PUBLIC_REPOSITORIES_AND_RESOURCES.txt`. Write decisions, code paths, diagrams, verified tests, links and next action. GitHub alone should be sufficient for new contributors and agents.

**Additional continuity requirement from follow-up:** Keep `docs/PROJECT_MEMORY.md`, `docs/CHAT_CONTINUITY_LOG.md` and `docs/RESUME_PROMPT.md` current so long ChatGPT history is not a prerequisite. This is a summary/archive of accessible project messages, not a claim of complete verbatim private-chat export.

## Task 9 — Safe Git/contribution workflow

Check branch state and PRs before editing, avoid overwriting others, prefer focused feature branch/PR, no force push or unjustified deletion, no automatic unreviewed merge to main. Commit real verified changes when authorized. If unable to write, provide the full patch. Owner retains authority over original-code license and contributor-IP policy.

## Task 10 — Required final engineering report

Report current implemented/partial/missing/blocked status, actual source tree and flows, twenty study candidates, exactly two primary references, architecture/integration choices, full backlog/acceptance, files changed/user behavior, real tests and skips, security/license issues, cost optimization, GitHub branch/commits/PR and one next action. Do not report future work as shipped.

## Non-negotiables

1. Do not restart existing code or replace tested components without evidence.
2. Do not import all 20 repos or copy restricted problem content.
3. Select exactly two primary solver research repositories.
4. Do not misrepresent authored/mock hints as actual AI inference.
5. Do not violate user-data ownership, worker credential separation or sandbox isolation.
6. Do not run generated/untrusted programs in web/API/host; never expose private judge cases.
7. No paid models/GPU/infrastructure or unbounded model loops without explicit approval.
8. No inflated completion, unsupported accuracy comparisons, invented security tests or fabricated verification.
9. Prefer small reversible tested patches, complete docs and safe PR reviews.
10. In every new session, re-verify *current* GitHub state because prior chat reports become stale.

**Source:** The user's long development instruction in the current project conversation, 2026-11-16, reformatted for an enduring developer-facing document.
