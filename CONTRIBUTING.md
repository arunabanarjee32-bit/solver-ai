# Contributing to Solver AI

Thanks for helping explore an AI-native DSA and competitive-programming platform. The repository is initially documentation-first; please check [current status](docs/PROJECT_STATUS.md) and [start here](docs/START_HERE.md) before submitting code.

## Before you begin

Read [vision](docs/PROJECT_VISION.md), [requirements](docs/PRODUCT_REQUIREMENTS.md), [architecture](docs/ARCHITECTURE.md), [roadmap](docs/ROADMAP.md), [security](SECURITY.md) and [open-source strategy](docs/OPEN_SOURCE_STRATEGY.md).

Pick one small task from [contributor tasks](docs/CONTRIBUTOR_TASKS.md); open an issue to confirm scope, particularly if changing security, licensing, architecture, data or model behavior. Existing pull requests should be reviewed before duplicating work.

## Contribution workflow

1. Discuss scoped work in an issue; include acceptance criteria.
2. Create your feature branch from main (e.g. `feat/first-scaffold`).
3. Make focused changes with tests, relevant documentation and license notices.
4. In PR description, provide purpose, changes, exact verification commands/results and risk.
5. Ask for review; address security/rights concerns before merging.
6. Update `docs/PROJECT_STATUS.md` only to reflect verified implementation.

No stable development/test commands have been committed yet; this will be part of the first scaffold PR.

## Code quality and review

- Prefer small, testable modules and interfaces.
- Avoid custom auth, code execution or crypto when vetted approaches exist.
- Never use downloaded problem statements/hidden tests without rights verification.
- Avoid new dependencies without assessing security, maintenance and licenses.
- No secrets, production datasets, huge artifacts or personal information in commits.
- Call out mocked functionality and unverifiable behaviors.
- Respect competition integrity rules.
- Security issues should use private reporting guidelines in SECURITY.md.

## Licensing and contributors

The owner has not selected an outbound license for this repository's original code. A publicly readable repository is **not automatically licensed for reuse**. Do not assume you can copy or redistribute source code or third-party artifacts. Maintainer must decide the license and inbound contribution policy before major external code contributions are accepted. See [open decisions](docs/OPEN_DECISIONS.md).

## AI-generated contributions

Agent-authored code must be reviewed by the contributor, tested, checked for unintended copyrighted copying and accompanied by accurate verification claims. See [AGENTS.md](AGENTS.md) and [Codex playbook](docs/CODEX_PLAYBOOK.md).
