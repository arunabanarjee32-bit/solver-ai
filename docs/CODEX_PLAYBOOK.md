# Codex Cloud / AI agent development playbook

Purpose: maximize useful verified output and minimize repeated/credit-wasting code generation.

## Before editing

1. Read README, AGENTS.md, PROJECT_STATUS and the task's relevant docs.
2. Inspect actual files; do not assume a stack, app, test command or implementation exists.
3. Define user-visible behavior, scope, tests, dependencies and non-goals.
4. Search the repo for existing functionality before rebuilding it.
5. For third-party components, consult OPEN_SOURCE_STRATEGY; check exact upstream license, maintenance and security.
6. For high-risk components, propose an ADR and audit first.

## Implementation discipline

- One milestone / focused PR at a time, with a small diff.
- Prefer mature libraries or narrow service adapters for commodity features.
- Do not merge entire upstream Git repositories or copy their code automatically.
- Avoid UI-only fake implementations presented as real features.
- Do not add large placeholders that prevent typecheck or future builds.
- Never embed API keys, tokens, production user data, hidden tests or copyrighted problem sets.
- Don't run untrusted C++/Python directly on the application server.
- Don't train a model on Codex Cloud or perform paid GPU provisioning without approval.
- Pin dependency versions, isolate judge/model resources and observe cost budgets.
- Add tests for both happy path and failure cases; no invented test results.
- Update docs and PROJECT_STATUS with verified work.

## Required task report

- Scope and exact files modified.
- Before/after state, and reuse decisions.
- Commands run and outcomes (or explicitly not run).
- Security/licensing implications.
- Known limitations and proposed next independent task.

## Current next agent task — not the obsolete scaffold

The foundation, owned isolated submissions, and signed authored hint API exist on `main`; do **not** restart a skeleton or recreate `POST /api/v1/hints`. The SAI-011 typed signed-in frontend integration is on [PR #5](https://github.com/arunabanarjee32-bit/solver-ai/pull/5). Verify the current PR head and workflow, review it, and merge only after maintainer approval. Resume context, precise paths and tests are in [IMPLEMENTATION_PROGRESS](IMPLEMENTATION_PROGRESS.md) and [IMPLEMENTATION_BACKLOG](IMPLEMENTATION_BACKLOG.md).

After that, the next independent task is a narrowly scoped provider-threat-model ADR: fixed egress, quotas and hard cost limits, model/output provenance, public-only context, data retention and privacy, contest rules and a kill switch. Get explicit approval before paid providers or GPU spending. Read [AI_ARCHITECTURE_PLAN](AI_ARCHITECTURE_PLAN.md) and [PRIMARY_RESEARCH_REPOS](PRIMARY_RESEARCH_REPOS.md).

## Verification ladder

Read -> Plan -> Small change -> Focused unit tests -> Integration test -> Build/lint -> Docs -> PR. Do not run repeated expensive suites without cause. Report remaining gaps, not '100% done' from successful mocks.
