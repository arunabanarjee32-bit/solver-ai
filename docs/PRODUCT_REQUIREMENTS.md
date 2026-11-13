# Product requirements and feature inventory

Status: requirements proposal. Labels P0/P1/P2 indicate priority, not implementation status.

## Primary workflow

Learner opens problem -> reads statement/constraints/samples -> edits C++17/Python in Monaco -> runs samples -> submits to private grading tests -> reads CE/WA/RE/TLE/MLE/AC verdict -> requests optional graded hint or debugging -> reviews history -> receives next-topic suggestion.

## P0 — first working release

| ID | Capability | Acceptance criteria |
| --- | --- | --- |
| P0-01 | Project setup | Fresh developer can start frontend, API and safe judge using documented commands |
| P0-02 | Problem catalog | At least several original/licensed seed problems with provenance, tags, constraints and test cases |
| P0-03 | Problem page | Markdown/math where safe, input/output formats, samples and constraints |
| P0-04 | Editor | Monaco-based C++17 and Python editor, language selection, accessible controls |
| P0-05 | Run and submit | Asynchronous jobs with idempotency, resource limits and actual sandboxed execution |
| P0-06 | Results | Clear compilation, runtime, memory/time and output-mismatch feedback; private test data protected |
| P0-07 | Hint service | Provider-neutral model adapter; graded hints; transparent mock/offline mode |
| P0-08 | Submissions | Durable per-user history with ownership/access control |
| P0-09 | Quality | Unit/integration tests, CI, safe defaults, rate limits and documented failures |
| P0-10 | Deployability | Reproducible local environment and a documented deployment path |

## P1 — AI and contest differentiation

- Constraint-aware algorithm selection, multiple candidate generation, sandbox feedback, bounded repair loop.
- Differential and property/metamorphic testing where a valid oracle exists; minimal counterexample discovery.
- Progressive hints, Socratic tutoring, editorial-style explanations, complexity analysis and feedback.
- Topic-wise strengths and weaknesses, adaptive learning plan, practice sets, revision reminders.
- Virtual contests, ICPC team workflow, post-contest editorial review, scoreboard freeze.
- Evaluation dashboard with baseline versus tuned model, pass@1/pass@k, time/cost, test coverage.
- Trusted administrative problem/test authoring and review.

## P2 — scale and business

- Rated contests, community moderation/discussions, editorial contributor workflow.
- Coaching dashboards, institutional assessments, configurable contest integrity.
- Payments/subscriptions with usage accounting and abuse limits.
- Multi-region operations, localization, advanced accessibility and mobile polish.
- Dedicated model training, self-hosted inference where economics justify it.

## Modes

**Practice/tutor:** hint ladder, guided questions, optionally full solution by explicit user choice.
**Solver/research:** complete algorithm, proof idea, code, measured tests, known gaps.
**Debug:** user-supplied code, reproducible failure, targeted explanation and minimal fix.
**Contest:** enforce event-specific AI-assistance rules; hide restricted AI tools in rated contests.
**Admin:** curate approved problems, tests, users, contests, access and audit trails.

## Nonfunctional expectations

Security: untrusted code never runs on public API/app host, no secrets/network in sandbox, auth/rate limits.
Correctness: deterministic verdict schema; grader versions logged; do not claim tests prove universal correctness.
Privacy: submissions and user history scoped correctly, retention/deletion policy established.
Reliability: bounded jobs, cancellation, retries, monitoring, backups and incident playbooks.
Accessibility: keyboard navigation, semantic labeling, legible diagnostics.
Observability: metrics/traces with redacted sensitive data; token and GPU costs monitored.

## Done means

Implemented and tested, documented startup/operation, license/provenance reviewed, accessible UI, security controls reviewed, and PROJECT_STATUS.md updated. A mock or blank UI does not satisfy a production feature.
