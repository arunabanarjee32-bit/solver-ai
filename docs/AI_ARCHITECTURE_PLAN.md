# Incremental AI architecture — 2026-11-16

## Actual foundation and trust boundary

`Next.js + Monaco -> Better Auth session -> short-lived EdDSA solver-api JWT -> FastAPI`. FastAPI exposes a public original problem catalog, authenticated offline hints, owned submission queue and worker-only judge routes. `apps/web/lib/submissions.ts` is the reference for authenticated browser requests; `solver_api/auth.py` verifies JWTs; `solver_api/hints.py` exposes a bounded `HintBackend` protocol and public-only context. The trusted judge control worker manages private generated grading cases and delegates execution to gVisor; neither frontend nor API executes arbitrary source.

The new `apps/web/lib/hints.ts` and `components/account-hint.tsx` (SAI-011 branch, awaiting hosted validation) use the same JWT/session boundary. They intentionally **do not** submit editor code, use a paid model or claim AI inference. Existing guest-authored hint ladder is untouched.

## Progressive stages and contracts

**Stage A: authenticated offline tutor (current).** POST `/api/v1/hints` with versioned schema `{problem_slug, level:1|2|3}`; successful response `{schema_version:"1",problem_slug,level,hint,source:"authored"|"mock"|"model",provider,ai_generated}`. Invariant: authored has null provider, mock/model have provider; `ai_generated` iff source=model. Zod in browser and Pydantic in API reject invalid/wrong-level responses and never echo provider internals. Token is request-scoped; 10-second browser timeout; 3-second backend timeout; cancellation on navigation/sign-out/level change. Author hints remain public and independent.

**Stage B: real provider (P1, not started).** Define `Provider.generate(public_context, level, budget, cancellation)` and return a provider-owned answer with provenance validated *at trusted orchestration*. Context can contain only public catalog fields from `public_hint_context`. Fixed allowlisted origin/HTTPS, no model-selected URL, no user secrets, no source code by default, no private grading data, no free-form system prompt assembly from external text, bounded input/output/tokens/time, concurrency and per-user cost quotas. Disable in restricted contests. Explicit feature flag defaults offline; budget exhaustion/unavailability falls back to visibly authored hints, not silent mock text. Add deterministic fake-provider tests, secret-redaction tests and cost accounting before real API calls. A separate ADR and cost approval gate are required.

**Stage C: code debugger (P2).** User explicitly consents to share selected draft/own attempt; authorize ownership via signed user; cap code length and redact logs. Compilation/runtime evidence is obtained only through existing isolated judge paths. Never send private case text or expected outputs to provider. Give minimal fix and reproduce only on public/authorized inputs. Feature-disabled during restricted contests.

**Stage D: verified solver (P2).** Convert `ProblemSpec` (original metadata/constraints/samples) into bounded `AlgorithmPlan` then 1–2 `Candidate` records. Simulation from CodeSIM is untrusted reasoning; phi-code-style testing/ranking uses real sandbox evidence first. Each `SolverRun` records model/provider version, attempts, token cost, `ExecutionResult`, termination reason and uncertainty. No dynamic host execution. Further repairs require explicit bounded budget. Finite AC means checks passed, not a proof. Real judge integration tests and rights-approved held-out evaluation are acceptance gates.

**Stage E: progress, ICPC contests (P3).** Derive learner progress only from owned attempts; provide topic mastery and next practice step. Add versioned contest/team/registration/scoring policy later with integrity constraints, scoreboard freeze and audit logs. AI disabled for events prohibiting assistance. Do not build a contest system now.

**Stage F: scale/model training (P4).** Only after deployment/retention decisions and measured demand: evaluate PostgreSQL/queue migration, low-risk instrumentation, rate limits and backup/recovery. Only benchmark open-weight vs API systems on rights-approved held-out tasks before proposing Transformers/PEFT/TRL/Unsloth/vLLM and approved GPUs. Avoid a default solver microservice, Redis cluster, search service or GPU while local workflows suffice.

## Security and rollback

- Identity: immutable verified JWT subject; browser never persists bearer; automatic cancellation when session identity changes.
- Execution: gVisor required, no host exec/eval fallback, no Docker socket in web/API, separate worker credential, limited outputs; original expected answers remain in trusted controller.
- AI: model responses always untrusted; JSON and provenance validate on both sides; no prompt/token/source/case logging or uncontrolled egress.
- Cost: single offline provider until explicit approval; future per-user token/spend/attempt ceilings and global kill switch, instrument cost independently of coding-agent credits.
- Rollback: remove UI entry without touching public hints; `SOLVER_HINT_BACKEND=authored` disables any future provider; new solver/debugger routes must be feature-gated.

See [backlog](IMPLEMENTATION_BACKLOG.md), [primary references](PRIMARY_RESEARCH_REPOS.md), and [threat model](JUDGE_SECURITY.md).
