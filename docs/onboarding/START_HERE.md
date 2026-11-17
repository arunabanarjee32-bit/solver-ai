# Start here — first-day contributor onboarding

Welcome. You do not need access to any previous private chats to contribute. This repository has a runnable local practice foundation with accounts, owned submission history and an optional gVisor-isolated Python/C++17 judge. Generated AI tutoring, contests and production operations remain proposed. Read the current status ledger before interpreting older plans as missing work.

## Understand the purpose in 10 minutes

- Mission: [PROJECT_VISION](../product/PROJECT_VISION.md).
- What users should be able to do: [PRODUCT_REQUIREMENTS](../product/PRODUCT_REQUIREMENTS.md).
- Where code should go: [ARCHITECTURE](../architecture/ARCHITECTURE.md).
- Current facts: [PROJECT_STATUS](../status/PROJECT_STATUS.md).
- Sequence of work: [ROADMAP](../product/ROADMAP.md).
- How to use upstream projects: [OPEN_SOURCE_STRATEGY](../governance/OPEN_SOURCE_STRATEGY.md).
- Contributor etiquette and PR workflow: [CONTRIBUTING](../../CONTRIBUTING.md).

## What should I work on next?

The local end-to-end capability already includes: choose an authorized sample problem -> edit C++17/Python -> submit -> receive real sandboxed verdict. Preserve and verify this workflow before extending it. Use [PROJECT_STATUS](../status/PROJECT_STATUS.md) to identify completed work and [CONTRIBUTOR_TASKS](../engineering/CONTRIBUTOR_TASKS.md) as a suggested backlog, rather than rebuilding the scaffold. The authenticated authored-hint browser integration is recovered and locally validated; it does not provide model-generated tutoring. Do not start by adding an AI chat widget that cannot verify code, or building a full contest platform first.

## Local development today

From the checkout root, run `npm ci`, `uv sync --project services/api --frozen`, then `npm run dev`. Open `http://127.0.0.1:3000` to browse original problems, edit Python/C++17 drafts, create a local account and view owned history. Drafts stay in the browser until an explicit run/submit. Set a writable uv cache as documented for managed clouds.

Follow [Development](DEVELOPMENT.md) for tests and Docker Compose. The optional full workflow builds a gVisor sandbox image and runs `npm run dev:judge`; it generates its own private local worker credential. No external account/model keys are required. Read the isolation/runtime limitations before changing execution. Do not execute learner code inside the API or web app, or call ordinary containers a fallback judge.

## Contribution expectations

Keep one reviewable objective per change; use the normal PR workflow unless the owner explicitly directs another workflow. The current repository recovery task authorizes checkpoint commits and pushes directly to `main`. Avoid unrequested frameworks or rewrites. Tests should demonstrate behavior, not only presence of files. Do not commit credentials or private datasets. Be explicit when functionality is authored, mocked or model-generated. Include docs and licenses as appropriate.

## Definition of ready for an implementation issue

User story, expected API/data contract, dependencies, security considerations, clear acceptance criteria, what to defer, and a small test plan.

## Definition of done

Reproducible implementation, tests, lint/build success where applicable, no unnecessary new dependencies, docs, and project-status update. Never mark a capability done on the basis of a design alone.
