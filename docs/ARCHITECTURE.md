# Architecture proposal

Status: target architecture with local implementation. `apps/web` implements Better Auth sessions, practice and history; `services/api` implements public catalog, JWT ownership and durable SQLite job leases; `services/judge` is a separate trusted control worker using the existing gVisor runtime. PostgreSQL, AI and contests remain proposed. See [foundation](adr/0001-practice-foundation.md) and [isolated submissions](adr/0002-authenticated-isolated-submissions.md). One modular monorepo with independently deployable services; local validation is not production certification.

## Data and control flow

~~~text
 Browser (Next.js + TypeScript + Monaco)
             |
        API gateway / FastAPI
       /      |         \
 users/auth  problems   submission & hint endpoints
    |          |              |
 PostgreSQL ---+          job queue
                           /    \
                    Judge worker  AI solver service
                        |           |       \
                 hardened sandbox   |   model provider (local / API / vLLM)
                                    |
                            test feedback from judge
 Separate offline ML pipeline ---> model registry / artifacts
~~~

All code, model output, embedded problem text and incoming user input are untrusted at relevant boundaries. Judge workers must not access database credentials, cloud instance metadata, production networks or other users' data.

## Proposed repository layout (create only as code is implemented)

~~~text
apps/web/                Next.js pages, practice UI, contest UI, Monaco
services/api/            FastAPI endpoints, auth integration, persistence
services/solver/         prompts, planning, provider adapters, test-and-repair
services/judge/          queue workers, runner/sandbox adapter, graders
packages/contracts/      versioned request/response schemas and types
ml/datasets/             ingestion, provenance, deduplication, splits
ml/training/             LoRA/QLoRA and experiments
ml/evaluation/           benchmarks, pass@k, latency, cost, contamination
infra/                   Docker for local, deployment, security config
tests/                   API, integration, sandbox, evaluation fixtures
docs/                    decisions, onboarding, specifications
.github/                 issue/PR templates and CI
~~~

## Technology candidates, not commitments

- Next.js, React, TypeScript and Monaco for web UI; shadcn/ui components.
- Better Auth (or reviewed equivalent) for identity; single authority for sessions across web and API.
- FastAPI and Python for service orchestration.
- PostgreSQL for users, problem metadata, attempts and contests.
- Redis-backed queue (or equivalent) for submission and solver jobs.
- Self-hosted Piston only if threat-model testing supports requirements; otherwise a purpose-built judge worker/service.
- Hugging Face Transformers/PEFT/TRL, Unsloth core and vLLM as optional separate ML capabilities.
- Docker Compose for reproducible development, plus independent deployable services.

## Conceptual domain entities

User, Identity, Session, Problem, ProblemVersion, TestCase, TestSet, Submission, ExecutionJob, Verdict, HintRequest, ModelRun, Contest, Team, Registration, RatingEvent, TopicSkill, DatasetSource, Experiment, ModelArtifact. Keep private test sets separate from public samples.

## Public API concepts (proposed, subject to versioning)

- GET /api/v1/problems — pagination/filtering.
- GET /api/v1/problems/{id} — authorized statement/samples.
- POST /api/v1/submissions — language, code, problem version; idempotency key.
- GET /api/v1/submissions/{id} — scoped status/verdict, no hidden test answers.
- POST /api/v1/hints — problem and hint-level selection; provider policy.
- GET /api/v1/me/progress — authorized user's skill/progress.
- Admin-only problem versioning and test-case ingestion endpoints.

Errors need stable codes and correlation IDs. Enforce input size limits. Consider polling before adding websockets.

## Security/operations

Submission API writes a queued job; a separate worker retrieves an authorized problem version/test set; sandbox compiles/runs with CPU/memory/process/output/time caps and no default network; worker emits a structured verdict; API checks ownership before returning results. Don't execute arbitrary code in API or frontend processes.

Resource costs per job, max AI retries and token budgets, job cancellation, submission quotas, audit logs and encrypted data storage are first-class requirements.

## Architecture decisions

See OPEN_SOURCE_STRATEGY.md, JUDGE_SECURITY.md and OPEN_DECISIONS.md. Architectural choices must be recorded before integrating major third-party services.
