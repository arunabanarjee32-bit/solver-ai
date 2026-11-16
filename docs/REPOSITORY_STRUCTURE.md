# Repository structure and preservation review

Reviewed: 2026-11-17 (Asia/Kolkata). Full-review baseline:
`a00894df45e5b451d3261ed374b36e8d2c208ad6` (238 tracked files), with
63 fetched commits and 253 historical paths. The earlier upload-preservation
baseline was `d4e1fc66e9cbf87bfa13d5e7bf4dd02ea4756e9e` (109 tracked files).
See the [complete recovery audit](../AnalyseFuture/REPOSITORY_AUDIT.txt).

## One product, with clear responsibilities

```text
solver-ai/
├── PROJECT_IDEA.txt              Detailed product vision and staged future work
├── README.md                    Orientation and working development commands
├── AGENTS.md                    Repository instructions
├── CONTRIBUTING.md / SECURITY.md
├── apps/
│   └── web/                     Next.js/TypeScript UI, accounts, Monaco, history
│       ├── app/                 Pages, layout and auth routes
│       ├── features/
│       │   ├── accounts/        Account form and browser/server auth adapters
│       │   ├── practice/        Catalog, editor, workspace and public API client
│       │   ├── hints/           Recovered authenticated authored-hint UI/client
│       │   └── submissions/     Submission panel, history and queue client
│       ├── components/          Shared navigation shell and icons
│       ├── scripts/             Auth migration and editor asset preparation
│       └── tests/               Actual Better Auth integration tests
├── services/
│   ├── api/                     Python/FastAPI catalog, hints, ownership, queue
│   │   ├── solver_api/          Application modules
│   │   └── tests/               API, hint, auth and submission tests
│   └── judge/                   Separate trusted controller and isolated runner
│       ├── solver_judge/        Worker, limits, cases, harness and diagnostics
│       └── tests/               Unit and explicitly enabled gVisor tests
├── scripts/                     Local startup and repository verification tools
├── tests/e2e/                   Browser flows across web/API/optional judge
├── docs/                        Requirements, decisions, status and development
│   └── adr/                     Recorded architecture decisions
├── .github/                     CI and contributor template
├── AnalyseFuture/
│   ├── README.md                Preservation rationale and integration boundaries
│   ├── manifest.json            Original file inventory and archive/member hashes
│   ├── archives/                Both original ZIPs, unchanged
│   ├── historical-implementations/ Original branch versions (23 files)
│   ├── repository-inventory/    Current/baseline paths, hashes and assessments
│   └── extracted/
│       ├── CodeGenerator-master/ 73 preserved files
│       └── phi-code-main/       49 preserved files
├── package.json / package-lock.json
├── compose.yaml / compose.cloud.yaml
└── toolchain, ignore and browser-test configuration
```

The Python API owns its `pyproject.toml`, `uv.lock` and Python version pin.
Each deployable component keeps its Dockerfile beside its source. Root Compose
files connect the services. Lockfiles and version pins are intentional, not
unwanted uploads. Generated dependencies, build artifacts, editor assets,
test reports and private `.local` state remain ignored local outputs.

The docs index groups the existing specifications. The detailed plain-text idea
extends those documents; it does not replace the implementation status ledger.
Future solver modules, contracts packages, ML pipelines or infrastructure folders
should be added when their implementation justifies them, rather than as empty
folders suggesting features already exist.

## What the review found

The earlier upload commit `d4e1fc6` added only `CodeGenerator-master.zip` and
`phi-code-main.zip`. Native scripts, npm workspaces, Python project configuration,
Docker builds, Compose and CI consistently reference the existing active paths.
Those paths were retained to preserve the already implemented workflow.

Fetching the other branches revealed the disconnected SAI-011 authored-hint
frontend and permanent-memory records. Five source/test versions were selectively
recovered, ten web modules moved to their feature owners, and 23 original branch
versions preserved. SAI-010 already matched main and was not applied again. The
[full path mapping](../AnalyseFuture/ORIGINAL_TO_NEW_PATH_MAPPING.txt) accounts
for every baseline path and all recovered branch inputs.

The maintainer reports unwanted changes and disruption. A file-tree/history
review cannot authenticate historical account activity or attribute a compromise.
No history was reset or force-pushed, and no existing tracked file was discarded.
Original tracked file paths and hashes are recorded in the preservation manifest.
Earlier versions of amended documentation remain in Git history.

Documentation did contain inconsistent status wording: a merged hint feature was
described as a branch, historical API counts were mixed with newer results, and
one paragraph contradicted the recorded hosted CI evidence. Those statements
were clarified while retaining the historical results and their limitations.

## Archive handling and reuse decisions

Both ZIPs were moved from the root into `AnalyseFuture/archives/`. Every regular
member was extracted into its upstream directory under `AnalyseFuture/extracted/`.
The manifest maps every original member name to its preserved path and hash.

Three upstream Git control files were renamed with an `.upstream` suffix. Their
contents remain intact; their broad ignore patterns and LFS filters are inactive.
The preservation folder explicitly includes all extracted files, including
Python source directories called `models` that the root ignore rules otherwise
exclude. Verification checks the staged blobs as well as working-tree bytes.

Five phi-code dataset entries are already LFS pointers in the supplied archive.
Their referenced large objects are not present and were not downloaded. No claim
is made that extraction recovered those datasets.

CodeGenerator's source license is MIT; phi-code's is Apache-2.0. Original notices
are preserved. Dataset, contest-content and model rights require their own review.
The archive-preservation request is not a decision to ingest their datasets or
adopt their execution frameworks. Their Python dependencies remain outside the
application's lockfiles and workspace.

Both research projects use Python. Keep the existing TypeScript frontend and
Python backend in this one modular project. Learner runtime languages are a
separate interface; Python/C++17 support does not require rewriting the product.
See the [detailed idea](../PROJECT_IDEA.txt) for possible later languages.

Archive execution helpers include host subprocesses, an external execution
client, model downloads and optional training. They were inspected as text, not
executed or installed. No common credential token, private-key or credential-URL
pattern was found by a limited static scan; this is not a complete security audit.
No claim of safety or production readiness follows from this review.

`AnalyseFuture` is excluded from the root Docker build context and Next.js
standalone tracing. The packaging guard rejects its accidental inclusion. CI
verifies preservation, while normal application tests continue to target the
active project only.

## Reproduce the preservation check

From the repository root:

```sh
python3 scripts/verify_preserved_archives.py
# After staging changes, or in a clean checkout, also check the Git index:
python3 scripts/verify_preserved_archives.py --git-index
```

Both checks must report two ZIPs, 122 members and 23 branch snapshots. A missing member, changed hash,
missing staged file or transformed staged blob fails the check. This verifies
preservation, not the correctness or licensing of archived research code.

The original uploads remain recoverable through the non-rewritten Git history.
Future displaced material should receive the same original-path inventory and
preservation treatment. Never put private runtime databases or credentials in
the future-analysis folder as a substitute for secure storage.

## Recovery and next work

The new organization gives the owner a reviewable revision, not an account
security recovery. The owner should separately review GitHub account access,
sessions, collaborator access, installed applications, deploy keys and unexpected
workflow changes; rotate any credential actually found exposed. This task did
not change account settings or establish that historical compromise is resolved.

Use `docs/PROJECT_STATUS.md` for tests and runtime limits, `docs/DEVELOPMENT.md`
for startup, and `PROJECT_IDEA.txt` for the proposed product and conditional
one-year, two-year and longer-term roadmap. No model provider, training job,
contest system or public deployment was introduced by this reorganization.
