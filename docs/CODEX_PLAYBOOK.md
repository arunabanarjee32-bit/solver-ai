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

## Suggested first agent task

"Inspect repo. Implement only the smallest reproducible full-stack skeleton: Next.js frontend, FastAPI health endpoint, scripts, Docker Compose local setup, basic API integration test and CI. Add clear run instructions. Do not implement auth, contest, AI or sandbox until foundations are tested. Keep repo working and update PROJECT_STATUS."

Next agent task: design and threat-model judge adapter, integrate self-hosted sandbox, run malicious-program tests before public deployment. Then problem catalog and editor.

## Verification ladder

Read -> Plan -> Small change -> Focused unit tests -> Integration test -> Build/lint -> Docs -> PR. Do not run repeated expensive suites without cause. Report remaining gaps, not '100% done' from successful mocks.
