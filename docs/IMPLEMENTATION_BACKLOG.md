# Ordered engineering backlog and acceptance gates — 2026-11-16

**Rules:** One focused PR per independently testable gate; code/paths below refer to existing files unless prefixed NEW. Complexity S/M/L relative. Costs: 0=offline, low=normal development only, controlled=explicit model spend, high=provisioned GPU/operations. Revert feature branch/flag only; preserve local judge, auth and owned-history foundations. Status reflects `main` unless otherwise marked. See [progress](IMPLEMENTATION_PROGRESS.md) for SAI-011 branch.

## P0 — safety and reliability before public release

| Task / status | User value; existing paths and implementation | Dependencies; acceptance and verification | Security, cost, rollback |
| --- | --- | --- | --- |
| SAI-P0-01 **blocked** | Agree original-code outbound license and inbound contribution IP. `OPEN_DECISIONS.md`, `CONTRIBUTING.md`; owner-approved LICENSE/CLA policy only | Maintainer review; public docs state exact granted rights; check notices | Legal/IP risk; S/0; revert policy text only with owner decision |
| SAI-P0-02 **planned** | Production-grade judge isolation review and dedicated deployment. `services/judge/solver_judge/{runner,worker,bounded}.py`, `services/judge/tests/test_sandbox.py`, `compose.yaml`; address aggregate resource accounting, runtime update, worker compromise/abuse budgets | Existing gVisor local integration; deliberate hostile-code integration, verified cleanup, network/FS/fork limits and independent review. Never expose public judge before pass | Critical RCE/multi-tenant; L/controlled infra; disable judge availability and roll back image, never host fallback |
| SAI-P0-03 **planned** | Account recovery, data lifecycle, backups and logout-token policy. `apps/web/lib/auth.ts`, `services/api/solver_api/{auth,submissions}.py`, `tests/e2e/submissions.spec.ts`; write privacy/retention decisions before code | D-13 owner approval; auth ownership/cross-user tests, restore tests, revoked/expired JWT behavior | Privacy/auth; L/low; disable new recovery path, restore backed-up state per policy |
| SAI-P0-04 **maintain** | Keep authenticated owned submissions reliable. `apps/web/lib/submissions.ts`, `services/api/solver_api/submissions.py`, `services/api/tests/test_submissions.py`; fix only demonstrated P0 regressions | Existing code; tests for forged identity, job lease replay/idempotency, quota, timeout and no hidden-case leak | P0 ownership; M/0; revert narrow fix after security review |

## P1 — usable honest tutoring foundation

| Task / status | User value; reuse and exact change | Dependencies; acceptance/tests | Security, cost, rollback |
| --- | --- | --- | --- |
| SAI-010 **on main** | Versioned offline authored `POST /api/v1/hints` and backend tests, `solver_api/{main,hints}.py` and `tests/test_hints.py` | 29 hint tests in historic successful hosted CI; signed token, levels 1–3, provenance, safe 503/timeout; existing API tests remain | Public context only, no model; S/0; route can be disabled without judge changes |
| SAI-011 **feature branch** | Account hints on problem page; reuse Better Auth JWT and public authored ladder. NEW `apps/web/lib/hints.ts`, NEW `components/account-hint.tsx`, `components/workspace.tsx`, `app/globals.css`, NEW `tests/e2e/hints.spec.ts` | SAI-010; signed UI request, validated response, authored/mock/model labels, guest ladder, failure/cancel/retry; typecheck + Playwright + standard CI pass required before merge | No source upload, session JWT only, S/0; revert UI integration/client/tests |
| SAI-P1-03 **planned** | Real tutor provider only after threat-model/cost ADR; reuse `solver_api/hints.py` Protocol. NEW `docs/adr/0003-tutor-provider.md`; future provider adapter and focused API tests | SAI-011 + explicit budget/model/privacy decision. Verify fixed egress, limits, secret redaction, per-user quota, cancellation, versioned mock/live provenance, no private cases. Never fake AI | Prompt/SSRF/abuse; M/controlled model; set backend to `authored` and remove provider flag |

## P2 — evidence-first AI solving and debugging

| Task / status | User value; reuse and exact change | Dependencies; acceptance/tests | Security, cost, rollback |
| --- | --- | --- | --- |
| SAI-P2-01 **planned** | Debug user's explicitly shared code with a minimal fix; reuse `solver_api/submissions.py`, `services/judge/solver_judge/runner.py` and signed auth. NEW narrowly bounded debugger endpoint/client and tests | Provider gate + user consent + judge interface authorization; deterministic CE/RE cases, cross-user isolation and redacted private tests verified, including real sandbox as execution changes | User-source privacy, case secrecy; L/controlled; disable debugger flag |
| SAI-P2-02 **planned** | Candidate planning/simulation and test-evidence-first ranking. Build original bounded Python module behind API, not copied repos. Reuse `solver_api/hints.py` provider boundary and judge/queue only after reviewed authorization | SAI-P1-03 + real judge safety + evaluation harness; bounded 1–2 candidates, 0–1 repairs, explicit provenance, finite tests/unverified distinction, no host execution; fixtures + sandbox tests | RCE/hidden-case/prompt risks; L/controlled; solver feature flag off |
| SAI-P2-03 **planned** | Reproducible held-out solver comparison. `docs/MODEL_DATA_EVALUATION.md`; NEW `ml/evaluation/` only when actual code needed | Rights-approved tasks + P2 solver; pass@1/pass@k, sample count, seed, baseline, latency, token and run costs; contamination checks and failures published | Dataset copyright/leakage; L/controlled; withdraw invalid claims/model experiments |

## P3 — learning and ICPC practice (after tutor/judge quality)

| Task / status | User value; reuse and exact change | Dependencies; acceptance/tests | Security, cost, rollback |
| --- | --- | --- | --- |
| SAI-P3-01 **planned** | Personalized DSA progress and recommended practice using owned history; reuse `submissions.py`, `submission-history.tsx`, public catalog. NEW scoped progress endpoint and UI | Owned history + privacy decisions; deterministic topic summaries, no cross-user reads, no fabricated mastery and browser tests | Sensitive learner data; M/low; hide recommendation UI |
| SAI-P3-02 **planned** | Virtual contest/ICPC teams, registration, penalty/freeze scoreboard and post-contest review. NEW separate contest domain added only after approved rules | Secure judge + owner decisions D-12; tests for scores, freeze, team membership, AI disabled in restricted contests, concurrency | Integrity/copyright/abuse; L/low-medium infrastructure; disable contest registration/event feature |

## P4 — measured operations and optional ML

| Task / status | User value; reuse and exact change | Dependencies; acceptance/tests | Security, cost, rollback |
| --- | --- | --- | --- |
| SAI-P4-01 **planned** | Production database/queue migration, backups, telemetry and deployment reliability only when load justifies; reuse `compose.yaml` and `solver_api/submissions.py`; NEW migrations and runbooks | Retention and P0 decisions, measured usage; dual-path migration/restore tests and privacy-preserving observability | Ops/data loss; L/controlled infrastructure; rollback to last safe schema/backups |
| SAI-P4-02 **planned** | Evaluate licensed model training vs paid API. `docs/MODEL_DATA_EVALUATION.md`, optional external Transformers/PEFT/TRL/Unsloth/vLLM | Rights-approved, reproducible held-out benchmark and explicit GPU budget; only ship tuned model if measurable cost/quality win | Licensing/compute/contamination; L/high ONLY after approval; disable model adapter/revert checkpoint |

**Dependency order:** P0 safety policies operate in parallel with local SAI-011, but must precede public launch. SAI-010 → SAI-011 → provider threat model → measured tutor → debugger and/or verified solver → formal evaluation → progress/contests → production scale/ML. Do not confuse an offline hint with AI tutoring. Each PR must document real test commands and rollback. Costs of Codex agent sessions are separate from model-serving expenses.
