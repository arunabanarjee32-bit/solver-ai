# Solver AI documentation index

New here? Read [START_HERE](onboarding/START_HERE.md), then [PROJECT_VISION](product/PROJECT_VISION.md).

## Functional groups

| Directory | Responsibility |
| --- | --- |
| `onboarding/` | Starting the project and contributing without prior chat context |
| `architecture/` | System boundaries, repository layout and architecture decisions |
| `product/` | Vision, requirements, roadmap, solver design and the retained plain-text idea |
| `research/` | Dated audits, study references, positioning and model evaluation proposals |
| `governance/` | Owner decisions, rights, licensing and build-versus-reuse policy |
| `engineering/` | Agent development practice and contributor backlog |
| `security/` | Judge threat model and release controls |
| `status/` | Named-revision implementation evidence and limitations |

The owner paused checks during the initial reorganization, then requested full
validation. The relocated application now passes the documented runtime suites;
see [current results](status/PROJECT_STATUS.md#post-relocation-validation-and-contributor-backlog-2026-11-17).

## Documents and preserved analysis

| Document | Purpose |
| --- | --- |
| [Complete project handoff](../PROJECT_HANDOFF.md) | Root guide: goal, implemented features, every file/folder and all detailed remaining tasks for other tools |
| [DSA solver readiness](product/DSA_SOLVER_READINESS.md) | Full supported-coverage, actual training, evaluation, artifact and release checklist |
| [Fine-tuning model research](research/FINETUNING_MODEL_RESEARCH.md) | Broad candidate comparison for a future decision; no selected checkpoint |
| [Start here](onboarding/START_HERE.md) | First-day orientation and workflow |
| [Ordered implementation backlog](engineering/backlog/README.md) | 141 scoped tasks, dependency order and actual GitHub publication status |
| [Implementation/review workflow](engineering/AI_CONTRIBUTION_WORKFLOW.md) | Other tools implement; designated reviewer inspects before authorized merge |
| [Detailed project idea (TXT)](product/PROJECT_IDEA.txt) | Product vision, AI-era features, staged horizons, responsibilities and limits |
| [Repository structure and review](architecture/REPOSITORY_STRUCTURE.md) | Active component map, preservation inventory and review findings |
| [Preserved future-analysis material](../AnalyseFuture/README.md) | Original uploads, complete extraction and reuse boundaries |
| [Current recovery audit](../AnalyseFuture/audits/REPOSITORY_AUDIT.txt) | Complete review scope, discovered branch work and repairs |
| [Complete feature inventory](../AnalyseFuture/repository-inventory/FEATURE_INVENTORY.txt) | Evidence and ownership for the recorded feature catalogue |
| [PR evidence contract](engineering/PR_EVIDENCE.md) | Offline metadata gate, schema, head matching and safe CI execution |
| [Security findings](../AnalyseFuture/audits/SECURITY_AUDIT.txt) | Confirmed cleanup weakness, remediation and unresolved risks |
| [Current validation report](../AnalyseFuture/validation/TEST_AND_VALIDATION_REPORT.txt) | Executed outcomes, expected failures and unrun checks |
| [Canonical future vision (TXT)](../AnalyseFuture/planning/PROJECT_VISION_AND_FUTURE_ROADMAP.txt) | Feasibility, priorities, resources and conditional future horizons |
| [Next developer instructions](../AnalyseFuture/continuation/NEXT_DEVELOPER_INSTRUCTIONS.txt) | Continuity, commands, evidence and next priorities |
| [Development](onboarding/DEVELOPMENT.md) | Tested setup, service commands and verification |
| [Foundation decision](architecture/adr/0001-practice-foundation.md) | Initial scope, dependencies and safety boundaries |
| [Accounts and isolated submissions](architecture/adr/0002-authenticated-isolated-submissions.md) | Upstream evaluation, identity boundary and gVisor integration |
| [Project vision](product/PROJECT_VISION.md) | Mission, users, differentiation and boundaries |
| [Product requirements](product/PRODUCT_REQUIREMENTS.md) | Feature inventory, user journeys and acceptance criteria |
| [Architecture](architecture/ARCHITECTURE.md) | Service/data boundaries and proposed monorepo layout |
| [Roadmap](product/ROADMAP.md) | Phased implementation and quality gates |
| [Project status](status/PROJECT_STATUS.md) | Honest implemented-versus-planned ledger |
| [Open-source strategy](governance/OPEN_SOURCE_STRATEGY.md) | Public repository candidates, licenses and integration logic |
| [Public repositories and resources (TXT)](research/PUBLIC_REPOSITORIES_AND_RESOURCES.txt) | All 20 previously suggested GitHub repositories plus models, datasets and benchmarks |
| [Audit and AI plan (2026-11-15)](research/AUDIT_AND_AI_PLAN_2026-11-15.md) | Source-based architecture review, 20 references, two AI research selections and implementation roadmap |
| [AI solver](product/AI_SOLVER.md) | Planning, testing, hints and agent workflow |
| [Judge security](security/JUDGE_SECURITY.md) | Threat model and untrusted code execution |
| [Model/data/evaluation](research/MODEL_DATA_EVALUATION.md) | Training plan, dataset rights and benchmarking |
| [Content and licenses](governance/DATA_AND_LICENSES.md) | Commercial-use boundaries and content sourcing |
| [Competitive landscape](research/COMPETITIVE_LANDSCAPE.md) | Markets and product differentiation |
| [Starter issues](engineering/CONTRIBUTOR_TASKS.md) | First testable contributions |
| [Open decisions](governance/OPEN_DECISIONS.md) | What requires maintainer sign-off |
| [Codex playbook](engineering/CODEX_PLAYBOOK.md) | Agent instructions and credit efficiency |

Also read [CONTRIBUTING](../CONTRIBUTING.md), [AGENTS](../AGENTS.md), and [SECURITY](../SECURITY.md).

**Truth convention:** Planned means not built. Candidate means not adopted. Implemented requires code, tests and reproducible instructions. Out-of-date documents should be corrected in the same PR that changes behavior.
