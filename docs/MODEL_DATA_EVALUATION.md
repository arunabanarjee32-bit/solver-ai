# Model selection, data strategy, fine-tuning and evaluation

**Status: proposed research plan. No model currently trained or benchmarked in this repository.**

## Model selection

Compare at least one coding-focused open-weight base model and one reasoning-oriented base model against a provider API baseline on the same held-out tasks. Candidate families discussed include Qwen coding and thinking models; exact checkpoint/version/terms/hardware to be chosen later. Model size, memory requirements and license are not interchangeable.

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
