# Solver AI project structure

This is the complete functional organization of
[`arunabanarjee32-bit/solver-ai`](https://github.com/arunabanarjee32-bit/solver-ai).
The product is a DSA/competitive-programming practice platform with accounts,
authored hints, submission history and an optional isolated judge. AI inference
and the longer-term solver remain proposed work. Files are grouped by their
responsibility and dependencies, not by extension.

The owner initially paused runtime checks during reorganization, then explicitly
requested testing and fixes. Post-relocation checks now passed: 137 API, 7 auth,
118 judge and 25 browser cases, plus 11 issue-publisher safety cases, type checks,
lint, optimized build and local production smoke. The only application-layout
fix needed was import formatting in a moved judge test. Full evidence and the
separate GitHub publication blocker are recorded in
[the validation report](AnalyseFuture/validation/TEST_AND_VALIDATION_REPORT.txt).

## The complete map

```text
solver-ai/
├── README.md                       Product and development entry point
├── PROJECT_STRUCTURE.md            This ownership/location guide
├── AGENTS.md                       Instructions applying to the whole project
├── CONTRIBUTING.md                 Contributor workflow and safeguards
├── SECURITY.md                     Reporting and security boundaries
├── package.json                    Root workspace and developer commands
├── package-lock.json               Frozen npm dependency graph
├── compose.yaml                    Standard local web/API deployment entry point
├── compose.cloud.yaml              Managed-cloud build trust override
├── playwright.config.ts            Cross-service browser discovery/lifecycle
├── .github/                        Hosted checks and contributor template
├── .node-version / .python-version Toolchain pins
├── .npmrc / .gitignore / .dockerignore
│
├── apps/web/
│   ├── app/                        Next.js framework routes/layout/global CSS
│   │   ├── account/                Account route
│   │   ├── api/auth/[...all]/       Session/JWT/JWKS route adapter
│   │   ├── problems/[slug]/         Problem route
│   │   └── submissions/            Submission history route
│   ├── features/
│   │   ├── accounts/               Account form, browser client, server authority
│   │   ├── practice/               Catalog, code editor, workspace, catalog client
│   │   ├── hints/                  Account hints and provenance-validating client
│   │   └── submissions/            Run/submit UI, saved history, queue client
│   ├── components/                 Shared shell/navigation and icons
│   ├── scripts/                    Web-owned auth migration and Monaco preparation
│   ├── tests/                      Web-owned Better Auth integration cases
│   ├── public/monaco/              Ignored generated editor assets
│   └── Dockerfile, package.json, tsconfig.json, next.config.ts, AGENTS.md
│
├── services/api/
│   ├── solver_api/
│   │   ├── main.py                 Stable FastAPI composition/entry point
│   │   ├── features/
│   │   │   ├── catalog/            Original content and catalog response models
│   │   │   ├── identity/           Fixed-issuer/JWKS bearer-token verification
│   │   │   ├── hints/              Authored hint backend/future-provider contract
│   │   │   └── submissions/        Owned SQLite queue, leases, quotas and history
│   │   └── http/                   Body limits, correlated errors and HTTP helpers
│   ├── tests/
│   │   ├── catalog/                Catalog and shared HTTP behavior cases
│   │   ├── identity/               JWT/JWKS and authentication cases
│   │   ├── hints/                  Authored/provider-contract cases
│   │   └── submissions/            Ownership, queue and completion cases
│   └── Dockerfile, pyproject.toml, uv.lock, .python-version, .dockerignore
│
├── services/judge/
│   ├── solver_judge/
│   │   ├── control/                Trusted host runner, worker and diagnostics
│   │   ├── grading/                Generated cases and expected-answer computation
│   │   ├── sandbox/                Restricted learner-program harness
│   │   └── bounded.py              Deliberately shared bounded process transport
│   ├── tests/
│   │   ├── control/                Runner protocol/worker/cleanup cases
│   │   ├── grading/                Original grading-case cases
│   │   └── sandbox/                Bounded transport and real isolation cases
│   └── Dockerfile, pytest.ini, UPSTREAM_REVIEW.md, .dockerignore
│
├── tests/e2e/
│   ├── hints/                      Account hint/provenance/cancellation flows
│   ├── practice/                   Catalog, editor, drafts and outage/retry flows
│   └── submissions/                Accounts, run/submit and cross-user history
├── tests/tooling/github/           Fake-client issue-publication safety cases
│
├── scripts/
│   ├── development/                Web/API/worker launch and local token selection
│   ├── github/                     Offline backlog cards and explicit issue publication
│   └── verification/               Packaging guard and static inventory/preservation
│
├── docs/
│   ├── INDEX.md                    Navigation for all active documentation
│   ├── onboarding/                Start-here and development commands
│   ├── architecture/              Current/target boundaries, layout and ADRs
│   ├── product/                   Vision, requirements, roadmap, solver proposal
│   ├── research/                  Algorithm/model/reference/comparison research
│   ├── governance/                Content rights, reuse and maintainer decisions
│   ├── engineering/               Contributor tasks and coding playbook
│   │   └── backlog/               Canonical issue catalogue, 127 cards and receipts
│   ├── security/                  Judge threat model and release requirements
│   └── status/                    Current implementation and evidence ledger
│
└── AnalyseFuture/
    ├── README.md                   Preservation and recovery navigation
    ├── manifest.json               Original ZIP/member provenance and hashes
    ├── archives/                   Both original uploaded ZIPs, unchanged
    ├── extracted/                  Complete inactive upstream research projects
    ├── historical-implementations/ Original branch snapshots and dated prose
    ├── audits/                     Repository/security findings
    ├── repository-inventory/       Complete file/feature/dependency ledgers
    │   ├── reviews/                Frozen source-review records with scope limits
    │   ├── functional-baseline.json Published baseline before these moves
    │   ├── functional-moves.json    Exact current relocation map
    │   └── current-files.json      Current indexed paths, ownership and hashes
    ├── migration-records/          Consolidation, origin mapping and archive record
    ├── planning/                   Detailed future vision and technical debt
    ├── validation/                 Historical check results; no current test claim
    └── continuation/               Work progress and next-developer instructions
```

The [complete per-file ledger](AnalyseFuture/repository-inventory/COMPLETE_FILE_INVENTORY.txt)
accounts for deeply nested paths. The
[functional move map](AnalyseFuture/repository-inventory/functional-moves.json)
records every relocation from the published baseline. Framework/dependency
files which remain in place have intentional owners, as described below.

## Feature ownership across processes

| Responsibility | Browser owner | API/control owner | Related material |
| --- | --- | --- | --- |
| Accounts and identity | `apps/web/features/accounts/` | `services/api/solver_api/features/identity/` | Web auth tests; API identity cases |
| Catalog and practice | `apps/web/features/practice/` | `services/api/solver_api/features/catalog/` | Practice browser cases; original content |
| Authored account hints | `apps/web/features/hints/` | `services/api/solver_api/features/hints/` | Hint browser and API cases |
| Submissions and history | `apps/web/features/submissions/` | `services/api/solver_api/features/submissions/` | Submission browser/API cases |
| Judging and verdicts | Submission UI | `services/judge/solver_judge/{control,grading,sandbox}/` | Separate trust-boundary cases |
| Shared HTTP behavior | Validating feature clients | `services/api/solver_api/http/` | Catalog/HTTP and failure cases |
| Launch and repository tools | Root npm commands | `scripts/{development,verification}/` | CI, containers, onboarding docs |

Related browser and service code shares a feature owner without being merged into
one process or dependency package. This keeps credentials, grading answers and
untrusted execution separated. Public authored hints and authenticated authored
hints serve different access workflows; neither is presented as real inference.

## Why some files stay at their framework entry points

- Root npm manifests, lockfile, version pins and ignore rules govern the entire
  workspace. Moving them would change tool discovery rather than improve ownership.
- Root Compose files and Playwright configuration are standard command entry
  points; their paths now reference the functional collections.
- Next.js `app/`, global CSS, web configuration and the auth route retain framework
  conventions. Feature code is outside route adapters; shell/icons are shared.
- Each service keeps its own manifest, tests, Dockerfile and local configuration
  because it can be developed/deployed independently.
- `solver_api.main:app` remains the stable API entry point. The trusted judge
  launcher now uses `solver_judge.control.worker`; documented diagnostics use
  `solver_judge.control.diagnostics`.
- `bounded.py` is shared intentionally across the host controller and sandbox
  image. The image copies only it and the harness into its flat `/opt/solver_judge`
  runtime. Expected answers and host credentials stay outside the image.
- `.local`, `.venv`, `node_modules`, `.next`, editor assets and transient reports
  retain their required ignored runtime/cache locations. They were not erased or
  published as source. Generated and private files are not unrelated user work.

## Preservation and uncertain material

Both original research ZIPs, all 122 extracted members and 23 branch snapshots
retain their bytes and existing organization inside their named reference
collections. Their internal structure is part of the evidence, not a second
active application. No upstream executor, model download, training job or
dependency installation was enabled by these moves.

Duplicate-looking package markers, logging helpers, benchmark variants and
historical documents remain preserved. Five supplied dataset members are LFS
pointers; the missing data were not silently invented or downloaded. License and
dataset rights records remain with their original materials. Private runtime
credentials and account data stay outside this public analysis collection.

Future uncertain material belongs under a named `AnalyseFuture` collection with
its original path, purpose, reason and replacement recorded. Do not move a file
there solely because it is unfamiliar, and do not copy live credentials into it.

## How to place the next file

1. Identify the owning feature and runtime before choosing a directory.
2. Use its existing collection; put cross-feature UI in shared components only
   when it is actually shared. Keep trusted control and sandbox code separate.
3. Put test source beside the corresponding service/feature test collection.
   Cross-service browser cases belong in the matching `tests/e2e/` collection.
4. Put commands in the owning app/service, or use `scripts/development` for
   cross-service startup and `scripts/verification` for repository integrity.
5. Put active guidance in the matching `docs/` group. Record past/uncertain
   evidence and future analysis in the named `AnalyseFuture/` groups.
6. Update imports, command paths, local links, inventory and relocation records.
   Preserve earlier versions through ordinary Git history and recorded moves.

The next developer should begin with [docs/INDEX.md](docs/INDEX.md),
[current status](docs/status/PROJECT_STATUS.md), and the
[continuation guide](AnalyseFuture/continuation/NEXT_DEVELOPER_INSTRUCTIONS.txt).
Runtime checks were resumed and completed at the owner's request. The new issue
cards describe future work; they do not indicate that their proposed features
are already implemented. Actual remote issue links exist only when confirmed in
the publication receipt.
