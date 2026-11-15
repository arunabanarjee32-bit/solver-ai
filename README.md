# Solver AI

**An open-development project aiming to build an AI-native platform for DSA, competitive programming and ICPC preparation.**

> **Current status:** Local practice development includes a Next.js library, FastAPI catalog, Monaco drafts, Better Auth accounts, owned submission history and optional gVisor-isolated Python/C++17 judging. AI, contests and production deployment remain planned. See [Project status](docs/PROJECT_STATUS.md) for executed validation and limitations.

## Run locally

Requirements: Node.js24 (see `.node-version`), Python3.12 and [uv](https://docs.astral.sh/uv/). No external API keys, database server or paid service is needed. Local account/submission data uses ignored SQLite files.

```sh
export UV_CACHE_DIR="${UV_CACHE_DIR:-/tmp/solver-ai-uv-cache}"
npm ci
uv sync --project services/api --frozen
npm run dev
```

Open `http://127.0.0.1:3000`. The API listens on `http://127.0.0.1:8000`; its interactive documentation is at `/docs`. Stop both services with Ctrl-C. The browser calls the API through the web server, so no CORS configuration is required.

```sh
npm run test:api
npm run test:auth
npm run test:judge
npm run typecheck
npm run build
npx playwright install chromium
npm run test:e2e
```

Browser tests start their own services; stop `npm run dev` before running them. On Linux, Playwright may need `npx playwright install --with-deps chromium`. See [Development](docs/DEVELOPMENT.md) for independent services, production builds, Docker Compose and troubleshooting.

For actual run/submit, this cloud image provides rootless Docker with gVisor. Build the sandbox with `npm run judge:build:cloud`, then start `npm run dev:judge` and create a local account. Other machines use `npm run judge:build` after installing a supported gVisor runtime. Missing isolation fails closed; learner code is never executed by the API/web process. [Full workflow and tests](docs/DEVELOPMENT.md#real-isolated-judging).

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

**The full product above remains a roadmap.** The local implementation supports browsing, editing, accounts, finite isolated grading and authored hints. It does not provide AI-generated results or a production judge certification.

## New contributor? Start here

1. Read [Start Here](docs/START_HERE.md) (orientation, how to contribute today).
2. Read [Vision](docs/PROJECT_VISION.md) and [Requirements](docs/PRODUCT_REQUIREMENTS.md).
3. Review the [Architecture](docs/ARCHITECTURE.md) and [Roadmap](docs/ROADMAP.md).
4. Find a scoped starter task in [Contributor Tasks](docs/CONTRIBUTOR_TASKS.md).
5. Check [Project Status](docs/PROJECT_STATUS.md) before assuming a feature exists.
6. Follow [Contributing](CONTRIBUTING.md), [Security](SECURITY.md), and [AGENTS.md](AGENTS.md) for agent-assisted work.

**All project documents:** [Documentation index](docs/INDEX.md). **Previously suggested public repositories:** [complete TXT reference list](docs/PUBLIC_REPOSITORIES_AND_RESOURCES.txt).

## Target architecture

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

The proposed layout and API contracts are in [Architecture](docs/ARCHITECTURE.md). The current [foundation decision](docs/adr/0001-practice-foundation.md) records what is implemented and deferred.

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
