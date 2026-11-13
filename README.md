# Solver AI

**An open-development project aiming to build an AI-native platform for DSA, competitive programming and ICPC preparation.**

> **Current status:** Planning and documentation. The repository does **not** yet contain a working web application, online judge, trained model or public deployment. See [Project status](docs/PROJECT_STATUS.md).

## The idea

Build an independently controllable competitive-programming product inspired by the *types of workflows* users value on LeetCode, Codeforces, AtCoder and ICPC platforms, but with our own interface, authorized problem content and an AI tutor/solver that can **reason, generate solutions, run tests, analyze failures and teach**.

It aims to support:
- DSA and algorithm practice; browser code editor; submissions and explainable judge verdicts.
- C++17/C++20 and Python coding; test execution isolated from application infrastructure.
- Progressive AI hints, explanations, code review, counterexample debugging and personalized paths.
- Verified AI solver experiments with candidate generation and bounded repair.
- Virtual contests, ICPC team practice, scoreboards and post-contest analysis.
- Model-neutral inference, legally sourced training datasets, fine-tuning and rigorous evaluation.
- Independent hosting and extensibility for a future commercial product.

**These are goals, not already implemented features.**

## New contributor? Start here

1. Read [Start Here](docs/START_HERE.md) (orientation, how to contribute today).
2. Read [Vision](docs/PROJECT_VISION.md) and [Requirements](docs/PRODUCT_REQUIREMENTS.md).
3. Review the [Architecture](docs/ARCHITECTURE.md) and [Roadmap](docs/ROADMAP.md).
4. Find a scoped starter task in [Contributor Tasks](docs/CONTRIBUTOR_TASKS.md).
5. Check [Project Status](docs/PROJECT_STATUS.md) before assuming a feature exists.
6. Follow [Contributing](CONTRIBUTING.md), [Security](SECURITY.md), and [AGENTS.md](AGENTS.md) for agent-assisted work.

**All project documents:** [Documentation index](docs/INDEX.md).

## Proposed architecture (not built yet)

~~~text
Next.js + Monaco web app
        |
FastAPI + authentication + PostgreSQL
       /                       \
Submission queue            AI tutor / solver
       |                       |
Sandboxed judge            Model provider adapter
(C++ / Python)                |
       |                 API or self-hosted model
Verdicts + history              |
                           Test-and-repair feedback

Offline: dataset provenance -> evaluations -> LoRA/QLoRA on external GPU
~~~

We prefer **one modular monorepo** and verified third-party dependencies/services. Study [Open-source Strategy](docs/OPEN_SOURCE_STRATEGY.md) before choosing or importing upstream code.

## First milestone

An authorized seed problem can be opened in the browser, solved in a Monaco editor, submitted to a secure isolated judge, and graded with a real verdict. A later milestone adds an optional AI hint and debugging workflow. Each increment requires reproducible tests.

The proposed layout and API contracts are in [Architecture](docs/ARCHITECTURE.md). There is **no supported installation or run command yet**; the first coding contributions will introduce them.

## Expectations and guardrails

- Respect intellectual-property rights: no bulk copying third-party problem statements, hidden tests or editorials without appropriate permission.
- Do not train on evaluation data, or claim benchmark gains without held-out evidence.
- Generated code is untrusted; it must not run inside the API/web process.
- Contest-integrity controls must follow each event's AI-assistance policy.
- Keep proprietary secrets, training weights and large datasets out of Git.
- Third-party software remains subject to its own license obligations.
- The repository does not currently declare an outbound license for original code; see [Open Decisions](docs/OPEN_DECISIONS.md) and seek maintainer approval before reuse.

## How to help

Documentation reviews, reproducible architectural prototypes, security research, original problems, tests and well-scoped implementation PRs are welcome proposals. Before investing effort in a major feature, open an issue describing scope and acceptance criteria.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow and [docs/CONTRIBUTOR_TASKS.md](docs/CONTRIBUTOR_TASKS.md) for suggested starter work.

This project is not affiliated with LeetCode, Codeforces, AtCoder, ICPC or any referenced open-source project.
