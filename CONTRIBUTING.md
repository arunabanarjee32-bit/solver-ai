# Contributing to Solver AI

Thanks for helping develop an AI-native DSA and competitive-programming platform. The repository contains a working local web/API/account/submission foundation with an optional isolated judge. Its broader AI, contest and production ambitions remain proposed; check [current status](docs/status/PROJECT_STATUS.md) and [start here](docs/onboarding/START_HERE.md) before submitting code.

## Before you begin

Read [vision](docs/product/PROJECT_VISION.md), [requirements](docs/product/PRODUCT_REQUIREMENTS.md), [architecture](docs/architecture/ARCHITECTURE.md), [roadmap](docs/product/ROADMAP.md), [security](SECURITY.md) and [open-source strategy](docs/governance/OPEN_SOURCE_STRATEGY.md).

Pick one small task from [contributor tasks](docs/engineering/CONTRIBUTOR_TASKS.md); open an issue to confirm scope, particularly if changing security, licensing, architecture, data or model behavior. Existing pull requests should be reviewed before duplicating work.

## Contribution workflow

The steps below are the default contributor workflow. Explicit owner instructions can authorize a different process; the current recovery task requests checkpoint commits and pushes directly to `main`, without branches or PRs. Keep changes reviewable and verification claims accurate in either workflow.

1. Discuss scoped work in an issue; include acceptance criteria.
2. Create your feature branch from main (e.g. `feat/first-scaffold`).
3. Make focused changes with tests, relevant documentation and license notices.
4. In PR description, provide purpose, changes, exact verification commands/results and risk.
5. Ask for review; address security/rights concerns before merging.
6. Update `docs/status/PROJECT_STATUS.md` only to reflect verified implementation.

Use the setup and verification commands in [Development](docs/onboarding/DEVELOPMENT.md). The foundation has API, real-auth, judge and browser suites, lint, type checking and a web build. Actual gVisor and full-judge browser checks require their explicitly enabled commands; normal suites intentionally skip those paths. A passing check validates its executed scope, not an unrun AI service or production deployment.

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

The owner has not selected an outbound license for this repository's original code. A publicly readable repository is **not automatically licensed for reuse**. Do not assume you can copy or redistribute source code or third-party artifacts. Maintainer must decide the license and inbound contribution policy before major external code contributions are accepted. See [open decisions](docs/governance/OPEN_DECISIONS.md).

## AI-generated contributions

Agent-authored code must be reviewed by the contributor, tested, checked for unintended copyrighted copying and accompanied by accurate verification claims. See [AGENTS.md](AGENTS.md) and [Codex playbook](docs/engineering/CODEX_PLAYBOOK.md).
