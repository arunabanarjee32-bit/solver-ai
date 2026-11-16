# Solver AI — prompt to paste at the start of any new ChatGPT/Codex session

**Continue the EXISTING Solver AI codebase; do not create a new project.**

Repository: https://github.com/arunabanarjee32-bit/solver-ai

Before planning or coding:
1. Read `docs/PROJECT_MEMORY.md` (primary permanent context), `docs/MASTER_DEVELOPMENT_SPEC.md` (full task requirements), `docs/CHAT_CONTINUITY_LOG.md` (project history), `AGENTS.md`, `README.md`, `docs/PROJECT_STATUS.md` and `docs/INDEX.md`.
2. Check latest main SHA, open PRs, latest CI and source code. On 2026-11-16 the authored signed hint API was already merged into main and the frontend integration was in **green but unmerged** [PR #5](https://github.com/arunabanarjee32-bit/solver-ai/pull/5). Its state may have changed, so verify before editing.
3. Treat source code and real CI as final authority, not old chat/roadmap statements. Do not reimplement existing APIs, auth, submission queue or judge.
4. Preserve Next.js/Monaco + Better Auth EdDSA JWT + FastAPI + owned SQLite queue + gVisor fail-closed judge. Use exactly **two primary AI solving research references**, CodeSIM/MapCoder and phi-code, for *patterns only*. No host `exec`, `eval`, private grading cases or copied competitor content.
5. Choose one smallest incomplete high-value milestone. After the frontend hint PR is reviewed/merged with maintainer approval, the proposed next task is a threat-modeled, budget-controlled real provider adapter **ADR first**, with deterministic fake-provider tests. Do not spend on model API, GPUs or new infrastructure without explicit approval.
6. Make focused changes on an authorized feature branch; run actual tests, record pass/fail/skip and what could not be run, submit PR and **never auto-merge unreviewed code**.
7. At the end, update `docs/PROJECT_MEMORY.md`, append to `docs/CHAT_CONTINUITY_LOG.md` and update `docs/PROJECT_STATUS.md` with exact branch, SHA, CI URL, files, risks and **single next action**. Keep these documents free of tokens, hidden tests, private user code and sensitive chat content; the repository is public.

**Deliverable:** real verified progress, not a placeholder. Show current status, prior work reused, 20-repository research references when relevant, exactly two primary solver research references, code touched, tests and skipped checks, licensing/security/cost, PR and next task.

For the canonical design decision, docs inventory and command list, follow the links in `docs/PROJECT_MEMORY.md`. Never assume a historical PR or provider remains in the same state without checking GitHub.
