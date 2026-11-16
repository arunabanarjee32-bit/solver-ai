# Solver AI — Conversation continuity and decision history

**Last snapshot: 2026-11-16 (Asia/Kolkata)**

This is a **faithful continuity record of accessible project conversation excerpts, requests, decisions and verified actions**, *not* a full verbatim export of all previous ChatGPT messages. Chats outside the accessible context cannot be recovered by the assistant. Private reasoning, unprovided messages, passwords, tokens, confidential code and hidden grader details are deliberately excluded. The main repo is **public**, so do not commit private transcripts without reviewing them.

## Project conversation timeline

### 2026-11-13 — establish own software project

The project conversations titled **Build Solver AI**, **Review Project Feasibility**, and **Start Project Development** record the owner's intentions:
- Create independently owned software rather than merely install an external product.
- Use Codex/AI developers to build the existing repository: https://github.com/arunabanarjee32-bit/solver-ai.
- Research whether a modular monorepo using selected upstream dependencies and patterns is better than merging whole repositories.
- Study leading competitive-programming/DSA platforms, choose useful product capabilities and avoid wasting coding credits on features already available as secure maintained libraries.
- Analyze feasibility and architecture **before** expansive implementation.
- Make all research, referenced repository URLs, decisions and next steps discoverable in GitHub so contributors do not require previous chat access.
- Verify and handle open PRs safely, preserve a text file of study repositories and avoid merging unreviewed changes.

These are summaries of the older project context; unavailable exact message bodies are not invented.

### 2026-11-15 — baseline research and hint API

An earlier source audit, `docs/AUDIT_AND_AI_PLAN_2026-11-15.md`, documented the working web/API/auth/judge foundation, all 20 research references and exactly two principal AI solver research repos (CodeSIM / phi-code). The authenticated offline hint contract **SAI-010** was implemented and later merged into `main`. It returns author-written hints and does not invoke a model. Hosted CI for the SAI-010 work: https://github.com/arunabanarjee32-bit/solver-ai/actions/runs/43737836616.

### 2026-11-16 — user's comprehensive development brief

The user supplied **"MASTER DEVELOPMENT PROMPT — SOLVER AI"**, directing the assistant to act as architect/full-stack/AI/security engineer, keep existing code, deeply audit the main branch, inspect all relevant docs and source, compare 20 study repos, select exactly two AI research references, design the entire incremental platform, prioritize P0–P4, implement the smallest useful missing feature, actually verify tests and preserve findings on GitHub. See [MASTER_DEVELOPMENT_SPEC.md](MASTER_DEVELOPMENT_SPEC.md) for a structured preservation of the ten tasks, exact source/acceptance requirements and non-negotiable constraints.

**Key user requirement:** "This is an existing software project, not a new project. Do not start from zero."

**Key user requirement:** Verify that `services/api/solver_api/hints.py`, `services/api/tests/test_hints.py` and `POST /api/v1/hints` are already on `main` and add the frontend integration **instead of rebuilding the endpoint**.

**Key user requirement:** No unsafe model-generated code execution, no hidden-case disclosure, no false benchmark or fake-AI claims, no unapproved GPU/model spend, no merger of 20 research repositories.

### 2026-11-16 — engineering work actually performed

1. Connected to GitHub with authorized read/write permission. Inspected `main` at `9952f8b5fa74f6900d57d1b48e3a26f3e962a358`; no open PRs at initial inspection.
2. Confirmed original Next.js/Monaco, Better Auth JWT, FastAPI catalog/submissions, gVisor judge and existing authored hint backend.
3. Revisited all 20 upstream default branch HEADs. Continued to select exactly two AI architecture research references: [CodeSIM/MapCoder](https://github.com/kagnlp/CodeGenerator) and [phi-code](https://github.com/Nan-Do/phi-code). Rejected their unsafe host execution approaches.
4. Created branch `feat/sai-011-frontend-hint-api`; implemented `apps/web/lib/hints.ts` with a strict Zod contract and bounded authenticated client; `apps/web/components/account-hint.tsx` with signed-in request, provenance labeling, cancellation, loading/retry/error; narrow workspace/CSS integration and `tests/e2e/hints.spec.ts`. Guest authored hints remain.
5. Initial GitHub Actions caught two browser test failures from a broad `role=alert` selector also matching Next.js route announcer. Commit `7b42e676` corrected the test selector; later CI passed.
6. Documented current source audit, two-repo research choices, AI architecture, P0–P4 backlog and Codex resume steps in five added docs plus updates to status/index/playbook and study inventory on the same feature branch.
7. Created [PR #5](https://github.com/arunabanarjee32-bit/solver-ai/pull/5) and marked ready for review, **not merged**. Head `b591db142d7b65c306769a59251ed4129f42118a`. Latest branch-head [GitHub Actions run 43837980897](https://github.com/arunabanarjee32-bit/solver-ai/actions/runs/43837980897) passed: **137 API passed, 91 judge unit passed (15 skipped), 22 browser passed (1 skipped)**, plus Better Auth, Ruff, typecheck, build and packaging checks.
8. Production model inference, debugger, solver, contest engine and GPU training remain **not implemented**. Real gVisor integration was **not rerun** in the SAI-011 hosted workflow.

### 2026-11-16 — user's request for permanent context preservation

The user requested (excerpt from this conversation):

> "Can you push all the detail, all the document, all the chart, all the link as a doc file in our GitHub repo? Reason is that when long chat, ChatGPT giving problem, and ChatGPT can't load our chat."

**Response:** A separate documentation feature branch was created from verified `main` so it can be reviewed independently of PR #5. The continuity package includes this file, [PROJECT_MEMORY.md](PROJECT_MEMORY.md), [MASTER_DEVELOPMENT_SPEC.md](MASTER_DEVELOPMENT_SPEC.md), [RESUME_PROMPT.md](RESUME_PROMPT.md), diagrams, complete 20-repo links, verified CI and source/PR references. This preserves accessible information **without claiming to have exported inaccessible chats**.

## Decisions retained across chats

| Domain | Stable decision / constraint | Still open? |
| --- | --- | --- |
| Repository | Original modular Solver AI monorepo; do not restart | Settled |
| Frontend/API | Preserve Next.js/Monaco and FastAPI | Settled for current foundation |
| Identity/queue | Reuse Better Auth/JWT and owner-scoped submission state | Local implementation, production review remains |
| Execution | Existing gVisor boundary, fail-closed | Public deployment review required |
| Hints | Author-written text is not model-generated | Settled |
| Primary AI research | Exactly CodeSIM + phi-code; **patterns** only | Re-evaluate only on new evidence |
| Model integration | Provider-neutral, offline first, bounded cost | Provider and budget unapproved |
| Training | Benchmark approved licensed data before optional LoRA/GPU | Unapproved |
| Contest integrity | No prohibited AI assistance in restricted events | Policy details unapproved |
| Licensing/privacy | Original-code license, inbound IP and data retention require owner | **Blocked decisions** |
| Git | Focused branch, real tests, PR and approval before main merge | Standard workflow |

## How to append future entries (do not overwrite prior facts)

### YYYY-MM-DD — Milestone title
- **User goal / short request:**
- **Main branch and pre-edit SHA:**
- **Open PRs / branch conflicts:**
- **Verified source findings:**
- **Important architecture/security decisions:**
- **Files changed:**
- **GitHub branch/commits/PR links:**
- **Executed tests (exact command and pass/fail/skip):**
- **Not run / environment limitations:**
- **Licensing/data/model costs and rollback:**
- **One next task for a new session:**

**Missing chats:** Future agents cannot conjure the full private ChatGPT history from GitHub; this file explicitly distinguishes direct accessible quotes, faithful historical summaries and verified GitHub source. To preserve older chat text verbatim, the owner must export it separately and review it for suitability before publication in the public repository.
