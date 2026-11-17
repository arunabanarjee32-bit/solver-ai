# DSA solver readiness: from the current application to a trained solver

Updated: 2026-11-17 (Asia/Kolkata).

**Main goal:** build a solver that can attempt a broad range of previously unseen
data-structure and algorithm problems, explain a proposed algorithm, generate
supported code, and report execution evidence and remaining uncertainty.
Expand measured coverage over time. No model or finite benchmark establishes
correctness for every possible DSA problem.

**Current state:** the practice application, account ownership, authored hints,
submission history and finite gVisor judge are implemented locally. Live model
inference, the generated solver, training pipelines, trained artifacts and this
readiness process are future work. No model has been selected for fine-tuning.
See the [model research catalogue](../research/FINETUNING_MODEL_RESEARCH.md) before
making a future selection; it compares candidates rather than choosing one.

## What “ready” must mean

Separate four claims and require evidence for each:

| Claim | Required evidence |
| --- | --- |
| Can attempt a supported problem | Validated statement, constraints, format and language; a bounded attempt or an explicit unsupported/insufficient-information result |
| Solved an evaluated problem | An actual accepted result against the authorized, versioned evaluator, with resource limits and model/run provenance |
| Useful across DSA categories | Disjoint held-out evaluation, per-category and difficulty results, uncertainty, latency/cost and known failures |
| Ready for an operated release | The preceding evidence plus identity/privacy, sandbox, capacity, model/data rights, rollback, budget and operator acceptance |

“Passed samples”, “model is confident”, “fine-tuning finished” and “all repository
tasks are closed” do not establish those four claims. A proof sketch is an
explanation unless separately checked by an appropriate proof system. Formal
verification is optional research and would need explicit specifications and
tool support; it does not give a general automatic solution to arbitrary tasks.

## Complete capability and work checklist

The canonical [ordered tasks](../engineering/backlog/README.md) define ownership,
dependencies and acceptance. Existing B041–B080 cover provider controls, tutoring,
debugging, bounded solving, evaluation, data rights and training admission.
The appended training-delivery tasks extend that plan through actual approved
training, model artifacts, release qualification and subsequent improvement.

### 1. Define the supported problem contract and coverage matrix

- Accept a complete statement, input/output contract, constraints, examples,
  requested language/runtime and assistance/rights scope. Validate missing or
  contradictory information before generation. Distinguish a new authorized
  problem from the current three seed catalog problems.
- Start with standard input/output Python and C++17. Function/class methods,
  custom checkers, interactive/output-only tasks, additional languages and
  tool-dependent problems need separate adapters and qualification. Mark formats
  unsupported until their evaluator and isolation contract exist.
- Version a topic matrix: arrays/strings; hashing; sorting/search; prefix sums;
  two pointers/sliding windows; stacks/queues; linked structures; trees/BSTs;
  heaps; tries; disjoint sets; Fenwick/segment trees; graph traversal; shortest
  paths; spanning trees; topological order/SCCs; flow/matching; greedy methods;
  dynamic programming including tree/digit/bitmask variants; backtracking;
  bit operations; number theory; combinatorics; geometry; advanced string
  algorithms; and advanced polynomial/randomized techniques where supported.
- Track easy/medium/hard labels, constraint scale, adversarial cases and language
  separately. A topic list is a coverage plan, not an implementation claim.

### 2. Finish reliable execution and evaluation foundations

- Complete the security, ownership, worker identity, crash-recovery, aggregate
  resource and runtime lifecycle gates. Keep learner/model-generated code in
  gVisor. Never execute imported archive helpers that use host `exec`/subprocesses.
- Create authorized versioned evaluators, independently reviewed reference
  solutions and valid input generators. Add differential/metamorphic checks only
  when their assumptions hold. Detect bad tests/references instead of training
  the model to match them.
- Separate public reasoning/debug evidence from private grading data. The model
  and repair loop must not observe the private held-out evaluator or its answers.
  Evaluation uses separate permissioned execution and reports permitted results.

### 3. Research and select an existing model empirically

- Maintain the model research catalogue. Include dense and mixture-of-experts
  models, code and reasoning variants, manageable experimental sizes and larger
  comparison models. API-only models can supply inference baselines but are not
  downloadable open-weight fine-tuning checkpoints.
- Compare a small feasible shortlist under the same problem splits, languages,
  output/test/token/time budgets and evaluator. Include an untuned baseline.
- Record exact model revision, tokenizer/chat template, context/output behavior,
  license/use restrictions, training/inference compatibility, hardware estimate
  and measured peak memory. Active MoE parameters are not total stored parameters.
- Select only after the comparison and owner resource decision. There is no
  universally best model independent of accuracy, hardware, latency and terms.

### 4. Build a lawful, validated training corpus

- Record source, permissions, redistribution/training terms and consent for each
  problem, solution and teacher-generated artifact. Source-code license alone
  does not establish dataset rights. Do not scrape private/unauthorized submissions.
- Normalize statement/constraints, algorithm summary, complexity discussion,
  verified source, language and provenance. Check correctness with authorized
  evaluators. Remove unsafe, inconsistent, low-quality and near-duplicate examples.
- Split by problem/contest/source/time before training; keep near-duplicates and
  translated versions together. Separate training, model-selection/validation and
  a sealed final release test. Quarantine ambiguous overlaps and contamination.
- Never put held-out benchmark solutions, private grading tests, credentials or
  personal account data in the training corpus. Archive LFS pointer files are
  missing data, not a usable training set.
- Explainable summaries can be curated without assuming access to a provider's
  private reasoning trace. Review teacher-output terms before distillation.

### 5. Implement a reproducible supervised fine-tuning pipeline

- Choose a pinned, compatible training stack after model research. Keep training
  tools separate from application dependencies and the learner sandbox image.
- Support reviewed dataset manifests, deterministic formatting/tokenization,
  answer-only loss masking, padding/packing validation, length limits, seeds,
  optimizer settings, checkpoint/resume and cancellation.
- Compare LoRA/QLoRA with the unchanged baseline before considering full-parameter
  training. A 4-bit weight-size estimate excludes activation, optimizer, temporary
  buffer and context memory; qualify the actual GPU configuration with a smoke run.
- Validate labels, chat template and any reasoning delimiters so training does
  not silently learn the wrong output format or erase useful existing ability.

### 6. Run approved smoke training and the first real experiment

- B080 is the admission gate; it does not run training. Require its approved
  experiment manifest, permitted data and an external compute/spending decision.
- Run a tiny approved smoke experiment first. Prove real loss/gradient flow,
  checkpoint save/resume, memory bounds and a loadable adapter. Stop on invalid
  loss, unexpected data access or capacity failures.
- Then run the approved bounded SFT experiment on the training split. Record
  exact code/base/data revisions, seed, hardware, hyperparameters, steps, cost,
  failures and artifacts. Resume only from a compatible verified checkpoint.
- Store weights/adapters in approved artifact storage, with hashes and provenance,
  rather than Git. Label an unsuccessful or interrupted run honestly.

### 7. Qualify improvements on unseen problems

- Freeze the candidate and selection criteria before opening the separate final
  release test. Repeated model selection uses validation data, not that final set.
- Compare the unchanged model, tuned model, and the same bounded tool-assisted
  workflows. Use matched budgets and disclose sampling. Include pass@1 and pass@k,
  compile success, wrong answers, TLE/MLE, abstentions, repairs, latency and cost.
- Break down performance by topic, difficulty, constraint scale and language.
  Report sample counts and uncertainty; do not hide a failing category behind
  aggregate accuracy or cherry-picked demos.
- Pre-register numeric release thresholds on validation data before final held-out
  evaluation. Record who approves them. Thresholds and representative sample sizes
  are pending decisions, not current results. Require no disqualifying privacy,
  sandbox or data-integrity failure regardless of accuracy.
- Evaluate regression in explanation quality, instruction following, unsupported
  task handling and safe stopping. Retain the untuned model if tuning provides no
  justified improvement. Do not keep selecting checkpoints on the final test set.

### 8. Complete the bounded solver product

- Produce an algorithm plan, complexity estimate and a limited candidate set.
  Generate supported source, compile/run authorized public tests, examine safe
  failure feedback and make a fixed number of repairs under one shared budget.
- Rank by observed evidence with deterministic ties. Add valid counterexample
  search where permitted; similarity and confidence are supplementary signals.
- Return the chosen source/explanation, exact observed validation, model version,
  budget/termination reason and limits. Return “not solved”, “unsupported” or
  “more information needed” when appropriate instead of a false success.
- Keep tutoring, direct solution generation, debugging and restricted-contest
  policies distinct. A trained model alone does not implement these workflows.

### 9. Package and release a qualified model safely

- Link the adapter to its exact base/tokenizer/template; verify hashes and
  dependencies. Evaluate the actual deployment precision/quantization, not only
  the pre-export research checkpoint.
- Serve the qualified artifact behind the provider-neutral interface with
  authentication, context/output limits, cancellation, admission budgets,
  redacted telemetry, a kill switch and a tested previous-version rollback.
- Require model/data rights and a model card stating evaluated capabilities,
  unsupported formats, dataset lineage, limitations and actual run evidence.
- Use a small approved pilot before expansion. Meet the operating/privacy/judge
  gates independently of the model's benchmark score.

### 10. Improve using controlled failure analysis

- Maintain a failure taxonomy: parsing, algorithm choice, invariant/proof gap,
  implementation bug, complexity failure, invalid test, unsupported format and
  environmental error. Choose work from observed weaknesses.
- Add original/authorized new training examples without moving held-out failures
  directly into the same benchmark's training set. Establish new untouched test
  sets when adapting to previously held-out material; disclose benchmark turnover.
- Re-run category/regression/budget gates for each data, adapter, runtime or model
  change. Retire regressions and preserve reproducibility.
- Consider DPO or execution-reward RL/GRPO only as separate approved experiments
  after reliable feedback, anti-reward-hacking checks and matched-budget baselines
  exist. Neither is required before the first useful SFT solver, and neither
  guarantees correctness on every DSA problem.

## Model selection and progress record

| Question | Current answer |
| --- | --- |
| Which checkpoint will we fine-tune? | Unselected; future research and matched evaluation decide |
| Are we training now? | No |
| Has a Solver AI model been benchmarked or promoted? | No |
| Does the project currently generate AI solutions? | No; current hints are authored |
| What comes after the earlier training admission task? | Implement pipeline/data tooling, run approved smoke and real SFT, evaluate, package, qualify serving and improve from measured failures |
| Can completion guarantee solving any imaginable DSA task? | No; release claims must name evaluated scope and limitations |

Use [the complete handoff](../../PROJECT_HANDOFF.md) and the canonical task cards
to assign implementation. This document authorizes no compute purchase, training
run, dataset acquisition or provider activation by itself.
