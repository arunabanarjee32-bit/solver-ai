# Start here — first-day contributor onboarding

Welcome. You do not need access to any previous private chats to contribute. This repository now has a runnable practice foundation. The larger judge, AI and contest platform remains a proposal.

## New ChatGPT/Codex session? Read this first

Start with [Permanent Project Memory](PROJECT_MEMORY.md) for the authoritative continuity snapshot and [Resume Prompt](RESUME_PROMPT.md) for the short startup script. Use [Conversation Continuity](CHAT_CONTINUITY_LOG.md) and [Master Development Specification](MASTER_DEVELOPMENT_SPEC.md) to recover prior decisions without the old chat. Re-verify current `main`, PRs and CI; the project memory records a dated snapshot, not live status. For a consolidated Microsoft Word-compatible file use [Complete Handbook (RTF)](SOLVER_AI_COMPLETE_HANDBOOK.rtf).

## Understand the purpose in 10 minutes

- Mission: [PROJECT_VISION](PROJECT_VISION.md).
- What users should be able to do: [PRODUCT_REQUIREMENTS](PRODUCT_REQUIREMENTS.md).
- Where code should go: [ARCHITECTURE](ARCHITECTURE.md).
- Current facts: [PROJECT_STATUS](PROJECT_STATUS.md).
- Sequence of work: [ROADMAP](ROADMAP.md).
- How to use upstream projects: [OPEN_SOURCE_STRATEGY](OPEN_SOURCE_STRATEGY.md).
- Contributor etiquette and PR workflow: [CONTRIBUTING](../CONTRIBUTING.md).

## What should I build first?

The first end-to-end capability is: choose an authorized sample problem -> edit C++17/Python -> submit -> receive real sandboxed verdict. Use [CONTRIBUTOR_TASKS](CONTRIBUTOR_TASKS.md) as the ordered backlog. Do not start by adding an AI chat widget that cannot verify code, or building a full contest platform first.

## Local development today

From the checkout root, run `npm ci`, `uv sync --project services/api --frozen`, then `npm run dev`. Open `http://127.0.0.1:3000` to browse original problems, edit Python/C++17 drafts, create a local account and view owned history. Drafts stay in the browser until an explicit run/submit. Set a writable uv cache as documented for managed clouds.

Follow [Development](DEVELOPMENT.md) for tests and Docker Compose. The optional full workflow builds a gVisor sandbox image and runs `npm run dev:judge`; it generates its own private local worker credential. No external account/model keys are required. Read the isolation/runtime limitations before changing execution. Do not execute learner code inside the API or web app, or call ordinary containers a fallback judge.

## Contribution expectations

One reviewable objective per PR; avoid unrequested frameworks or rewrites. Tests should demonstrate behavior, not only presence of files. Do not commit credentials or private datasets. Be explicit when functionality is mocked. Include docs and licenses as appropriate.

## Definition of ready for an implementation issue

User story, expected API/data contract, dependencies, security considerations, clear acceptance criteria, what to defer, and a small test plan.

## Definition of done

Reproducible implementation, tests, lint/build success where applicable, no unnecessary new dependencies, docs, and project-status update. Never mark a capability done on the basis of a design alone.
