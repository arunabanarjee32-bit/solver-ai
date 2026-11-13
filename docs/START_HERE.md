# Start here — first-day contributor onboarding

Welcome. You do not need access to any previous private chats to contribute. This repository is currently a documented **proposal**, not a working app.

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

There is **no runnable development environment yet**. Don't invent `npm install`, `docker compose up`, environment variables, or a live URL. The first engineering PR should add real scripts, test commands, a working minimal scaffold and clear instructions to this file.

Until then:
1. Clone with `git clone https://github.com/arunabanarjee32-bit/solver-ai.git`.
2. Read these docs and identify a scoped gap or decision.
3. Open an issue with context, acceptance tests, license implications, and expected files.
4. Create a branch and PR; show evidence of checks you could actually run.
5. Update PROJECT_STATUS when code/CI exists.

## Contribution expectations

One reviewable objective per PR; avoid unrequested frameworks or rewrites. Tests should demonstrate behavior, not only presence of files. Do not commit credentials or private datasets. Be explicit when functionality is mocked. Include docs and licenses as appropriate.

## Definition of ready for an implementation issue

User story, expected API/data contract, dependencies, security considerations, clear acceptance criteria, what to defer, and a small test plan.

## Definition of done

Reproducible implementation, tests, lint/build success where applicable, no unnecessary new dependencies, docs, and project-status update. Never mark a capability done on the basis of a design alone.
