# Two primary AI solver research repositories — selected 2026-11-16

**Exactly two primary research references; neither is a dependency.** Current HEAD and code were reread via GitHub on 2026-11-16. This decision retains the 2026-11-15 selection. We will independently implement patterns compatible with our FastAPI and gVisor, not transplant code.

## 1. CodeSIM / MapCoder — planning and simulation

- Upstream: https://github.com/kagnlp/CodeGenerator; default branch `master`; HEAD `9cf09ee6c788bfda3b7e1524e88be3447098eb24`.
- Inspected: `src/promptings/CodeSIM.py` (plan generation, simulation, bounded retry and debug), `src/models/ModelFactory.py` (provider selection), `src/evaluations/func_evaluate.py` and `src/evaluations/api_comm.py` (evaluation path from prior audit).
- Adopt *ideas*: explicit plan artifact, constraint-aware algorithm proposal, simulate public samples and revise discrepancies, bounded debug attempts, reproducible step and model counts.
- Upstream research defaults `max_plan_try=5` and `max_debug_try=5` are **not** sensible automatic commercial budgets. Begin with 1 plan, 1–2 candidates, zero or one repair in an explicitly authorized later solver experiment.
- **Do not copy:** untrusted host `exec`, raw test logs containing hidden cases, imported prompts or dataset content, direct execution adapter or authors' advertised benchmark figures as facts. Finite checks do not prove correctness.
- License: MIT text verified in upstream `LICENSE`; preserve copyright/notice if code ever reused. Our plan is independent implementation. Research head is from 2025 and maintenance should be rechecked before using modules in production.
- Estimated effort: M for a narrow planner/simulator adapter; H for an entire agent framework. Present value: design only; no extra dependency/model cost.

## 2. phi-code — candidate diversity and evidence-based ranking

- Upstream: https://github.com/Nan-Do/phi-code; default branch `main`; HEAD `b3ca73d7dcc37aed6809eb7789281465a7a04d22`.
- Inspected: `solver/terminal.py` (multiple candidates, sample-test score then embedding tie-break), `solver/main.py` (llama.cpp-style model and sentence-transformer integration), `solver/leetcode.py` (`exec` within child process), plus `ranker/train.py` documented in prior audit.
- Adopt *ideas*: track candidate language/source/plan/provider/budget separately, sandbox each candidate, sort by verified evidence first then deterministic explicit tie-breaks; report number of executed tests and uncertainty.
- **Do not copy:** `exec`/host subprocess for adversarial code, scraping platform problem statements, benchmark datasets, full local ranker or self-hosted inference requirements. Semantic similarity to text is not correctness. Test scores on unseen benchmark data were not reproduced.
- License: Apache-2.0 text verified in upstream `LICENSE`. Attribution/NOTICE may apply to code reuse; problem content rights are independent. Research head is from 2025; project authors' contest result claims are not validation.
- Estimated effort: M for bounded candidate ranker and result schema, H for sentence-transformer training/GPU service. Present value: design only.

## Combined original Solver AI design

1. Authorized public `ProblemSpec` with statement, samples, language and limits; private tests remain in trusted judge.
2. Explicit constraint extraction + algorithm-family tags + 1 bounded planning attempt (CodeSIM idea).
3. 1–2 independently sampled candidate plans/code records (phi-code idea) under per-user model quota.
4. Stage-specific provenance: provider/model ID, prompt template version, seed, token/time budget, number of candidate attempts.
5. Optional public-only reasoning/simulation check; mark as *hypothesis*, never execution proof.
6. Compile/run generated code only via preexisting authorized gVisor worker and no-network isolation. No `exec`, `eval` or arbitrary host subprocess.
7. Rank candidates by explicitly permitted executable evidence first: compilation, fixed samples, independent edge/metamorphic checks with valid oracle, then complexity plausibility, deterministic tie-break. Never feed hidden expected outputs or case text to models.
8. Permit at most one budgeted repair in the initial experiment; prefer failure summaries without private data. Surface evidence, resource usage and uncertainty.
9. Evaluate against a single-candidate/no-repair baseline on held-out rights-approved tasks. Report pass@1/pass@k methodology, runtime, spend, failure types and contamination precautions.
10. Kill switch defaults all model/solver features off until provider threat model, quotas and entitlement checks have shipped and been tested.

## Acceptance gates for adopting these ideas

- No new model loop before authenticated tutor works and explicit budget approval exists.
- Deterministic fixtures prove candidate count, zero unbounded retries, cancellation and token caps, zero model access to private judge cases or user tokens.
- Real gVisor integration reproduces failure isolation before executing any model-generated source.
- Per-candidate evidence includes actual test count and results; invalid oracle/missing tests produce *unverified*, not *correct*.
- Rights-approved held-out evaluation compares cost/latency/accuracy to baseline; no claimed improvement without measurement.
- No upstream source or model assets imported for this research task. Rollback is feature-flag off / revert adapter.

This research choice does not replace the existing judge. See [architecture plan](AI_ARCHITECTURE_PLAN.md), [audit](REPOSITORY_AUDIT.md) and [model evaluation](MODEL_DATA_EVALUATION.md).
