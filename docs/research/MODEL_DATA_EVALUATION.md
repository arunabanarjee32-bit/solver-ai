# Model selection, data strategy, fine-tuning and evaluation

**Status: proposed research and delivery plan. No model currently selected,
trained or benchmarked in this repository.**

The owner explicitly requests a future model comparison before selection.
Use [Fine-tuning model research](FINETUNING_MODEL_RESEARCH.md) for the broad
candidate catalogue and unresolved checkpoint/license/hardware questions.
Use [DSA solver readiness](../product/DSA_SOLVER_READINESS.md) for the complete
coverage, training, evaluation and release checklist. A model that attempts
supported problems cannot be promised to solve every possible DSA problem.

## Model selection

Compare code-specialized and reasoning-oriented open-weight candidates from
multiple families against an authorized provider baseline on the same disjoint
tasks and budgets. The research catalogue includes small/dense models, larger
models and MoE alternatives. No named family is the assumed winner. Choose the
exact checkpoint, revision, license, template and hardware only after empirical
comparison and the resource decision. API-only models may be baselines but are
not downloadable checkpoints for local LoRA. Model size, total/active parameter
counts, memory requirements and license are not interchangeable.

## Data pipeline

1. Collect *permitted* training tasks, official/original examples and solution artifacts with source URL and rights metadata.
2. Normalize statements, constraints, input/output, difficulty, language, editorial/solution provenance.
3. Validate compilations, outputs, constraints and grader/reference quality.
4. Deduplicate near-identical problems and submissions across train/validation/test.
5. Split by problem and contest/source/date as appropriate; prevent leakage from benchmark or evaluation sets.
6. Train via SFT/LoRA/QLoRA on external CUDA infrastructure; record hardware, seed, code commit, data manifest, hyperparameters and compute cost.
7. Report accuracy before and after; discard a trained checkpoint if it does not outperform baseline.

Candidate resources for **rights/quality review**: [TACO](https://huggingface.co/datasets/BAAI/TACO), [DeepMind CodeContests](https://github.com/google-deepmind/code_contests), [LiveCodeBench](https://livecodebench.github.io/). They are not automatically approved for redistribution or commercial training. Original source-site rights and model/dataset terms apply.

## Evaluation

Track compile-success, pass@1, pass@k with stated sampling procedure, TLE/MLE rates, tests-per-solution, median and tail latency, model tokens, serving costs, breakdown by algorithm family/difficulty/language, explanation quality and error types.

- Keep held-out evaluation problems and test cases separate from training.
- Pin compiler versions, CPU/memory limits, prompt templates, decoding and candidate budget.
- Maintain exact-match and sandbox-execution checks as applicable; do not rely on static code matching.
- Evaluate baseline (no tools), tools without tuning, and tools plus tuning separately.
- Report statistical uncertainty, sample sizes, failing categories and reproducible logs.
- LiveCodeBench and other benchmarks must follow their specific license and evaluation policies.
- A passing finite test suite does not prove algorithm correctness.

## Reinforcement learning / GRPO (later)

Only after dependable verifiable feedback. Reward must be resistant to test exploitation, benchmark leakage and shallow compile-only heuristics. Record GPU spend and compare against increased test-time inference/candidate generation costs.

## Deployment

Serving via provider abstraction: remote model API or separate vLLM GPU service; rate limits, authentication, logging/redaction and version pinning. Never store model weights, large training corpora or credentials in Git; use artifact storage and checksums.

## Exit criteria for training milestone

Licensed/provenanced dataset manifest + reproducible baseline + held-out eval + documented GPU/training run + quantifiable gain or honest failure. Avoid declaring 'ICPC-level AI' based on anecdotal demos.

## Delivery beyond training admission

SAI-B080 validates an experiment admission manifest and explicitly does not train
a model. The appended training-delivery cards in the
[canonical backlog](../engineering/backlog/README.md) cover the missing work:

1. Define supported DSA coverage and pre-registered release measurements.
2. Compare checkpoint candidates empirically; record a future owner selection.
3. Materialize permitted, validated, deduplicated train/validation data without
   contaminating the separate held-out evaluation set.
4. Implement pinned tokenization/loss masking and reproducible SFT/LoRA/QLoRA
   tooling outside application dependencies.
5. Run an explicitly approved external smoke experiment, then the approved real
   bounded training run, with memory/cost/stop/resume evidence.
6. Preserve adapter/base/tokenizer/data lineage and evaluate the deployed
   precision against matched untuned baselines, regressions and category targets.
7. Qualify provider-neutral serving, a model card, a limited pilot, kill switch
   and rollback before promotion.
8. Improve from consented failure analysis; optional preference/RL experiments
   remain separately approved research with reliable execution rewards.

Documentation completion is not training completion. No model weights, datasets,
ML dependencies, external inference requests or paid compute are activated by
this planning update.
