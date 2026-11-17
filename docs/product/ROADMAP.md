# Roadmap: incremental path to a competitive product

Status: planned; dates and timelines deliberately not committed. Advance by acceptance gates, not promises.

The main solver/training delivery checklist is
[DSA solver readiness](DSA_SOLVER_READINESS.md). The
[fine-tuning model catalogue](../research/FINETUNING_MODEL_RESEARCH.md) supports
future research; no model is selected. Broad, measured DSA competence is the
goal, with explicit supported formats and failure reporting rather than a
guarantee for every problem. The detailed training cards supplement B080's
admission gate with actual future training and delivery.

## Phase 0 — foundation and decisions

- Agree on code license, contributor policy, first users, stack owners and initial judge security baseline.
- Review candidate dependencies; maintain a build-vs-reuse matrix.
- Scaffold web/API, typing/contracts, formatting, tests, CI, local Docker and example environment variables.
- Gate: fresh checkout follows README instructions and passes a smoke test.

## Phase 1 — minimal practice vertical slice (first meaningful software)

- Add a few originally authored or permissioned seed problems with versioned test cases.
- Build problem list/detail, Monaco editor, run and submit endpoints.
- Implement isolated C++17/Python execution and structured real verdicts.
- Persist submissions; add dev/demo authentication versus release-ready accounts clearly.
- Gate: a new contributor can submit correct and incorrect examples, observe reliable AC/WA/CE/TLE and run automated tests.

## Phase 2 — AI tutor and debugger

- Add model provider interface, safe prompt construction, graded hints and code feedback.
- Support model unavailability without breaking judge; make mock mode visually explicit.
- Add baseline regression tests and token/execution budgets.
- Gate: AI feedback is helpful and verifiably linked to an authorized problem; no hidden tests leak.

## Phase 3 — verified solver

- Algorithm plan, candidate generation, compile/test, differential tests where possible, bounded retry and explanation.
- Compare against fixed base model and no-repair baseline; record pass@1, pass@k, cost and latency.
- Gate: measurable gain on held-out tasks without test contamination.

## Phase 4 — practice intelligence and competitions

- Topic mastery, curated learning paths, search, virtual contests and ICPC team modes.
- Admin problem authoring, scoring, scoreboard freeze, integrity policy, post-contest coaching.
- Gate: end-to-end seeded contest works with fair judging and correct scoring.

## Phase 5 — model training and deployment

- Dataset provenance, deduplication, rights review, evaluation splits and inference harness.
- SFT/QLoRA experiment on external GPU, compare to original base with reproducible logs.
- Compare candidate model families before selection; pin model/tokenizer/license
  and materialize validated, disjoint, rights-approved training data.
- Implement the training pipeline; run approved smoke and real SFT experiments,
  verify checkpoint/resume and record complete adapter/base/data lineage.
- Qualify the deployed precision on per-topic/difficulty/language evaluation;
  publish a model card and rehearse bounded serving, pilot and rollback.
- Deploy model via versioned provider interface if accuracy/cost improves.
- Gate: reproducible benchmark report with honest failures and compute cost.

## Phase 6 — scale and business

- Moderation, incident response, payments where appropriate, usage quotas, analytics, mobile accessibility and reliability.
- Pilot with real learners and adjust positioning based on retention and outcomes.
- Gate: operational metrics and an acceptable abuse/security posture.

## Implementation discipline

Every milestone gets an issue, PR, tests, docs update, rollback path and owner review. Reuse established libraries where possible. Don't launch multiple workstreams before the first vertical slice runs.
