# AI solver, tutor, debugger — design proposal

Goal: high-quality algorithmic help with *measured correctness* and a learning-oriented interface.

## Distinct user experiences

- Tutor: progressively reveal concept -> insight -> pseudocode -> code review; default to hints, not spoilers.
- Solver/research: produce algorithm, complexity, proof sketch, code and explicit validation report.
- Debugger: read user code/error, reproduce failure, identify root cause, suggest minimal correction.
- Post-contest: replay attempts, discuss alternatives and failure cases.
- Live contest: enforce competition-specific rules and disable forbidden AI assistance.

## Candidate solver workflow

1. Parse problem statement, input/output, constraints, sample tests; validate completeness.
2. Classify algorithm families and difficulty; retrieve only authorized educational references.
3. Produce candidate reasoning approaches and select bounded proposals.
4. Generate code in the requested language; ensure language/version contract.
5. Compile in separate sandbox and run public samples.
6. Run generated edge cases, oracle-based differential tests or metamorphic tests **where valid**.
7. Rank candidates with verifiable feedback; allow limited, budgeted repair.
8. Return explanation, proof idea, complexity, code, observed test results and remaining uncertainty.
9. Log model/provider version, usage, execution settings and failure data with privacy safeguards.

Do not expose private hidden test outputs to model or user. Passing samples or random tests is not proof of universal correctness. A flawed reference solution can invalidate differential testing.

## Architecture interfaces (conceptual)

`ProblemSpec`: statement, provenance, language, constraints, examples, allowed evaluation modes.
`SolutionCandidate`: language, algorithm_summary, source_code, explanation, model provenance.
`ExecutionRequest`: artifact, test manifest ID, resource limits, compilation flags.
`ExecutionResult`: status, stdout/stderr redacted/capped, time/memory, testcase summary.
`SolverRun`: attempts, tested candidates, verdict evidence, total tokens/cost, budget, termination reason.
`HintRequest`: user, problem ID/version, existing attempt, hint level; enforce access policy.

## Safety & performance

Per-user quotas; strict token and test budgets; input bounds; rate limits; adversarial/problem-prompt injection defense; sandbox untrusted code; strip secrets from logs. No arbitrary internet access from execution workers. Feature flag AI assistance in competitions.

## Model strategy

Start with interchangeable API and open-weight model adapters; baseline on an unseen benchmark before LoRA. Fine-tuning is a separate research experiment and not a shortcut around judge correctness. See MODEL_DATA_EVALUATION.md.

## First implementation after the judge

Basic provider abstraction + single hint endpoint + stub implementation clearly marked mock + test fixtures. Add candidate loops only when test harness and cost monitoring exist.
