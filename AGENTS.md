# Instructions for Codex and all coding agents

**Source of truth:** README.md, docs/INDEX.md, docs/status/PROJECT_STATUS.md. Read them and the relevant specification before making changes.

## Mission

Build Solver AI: an independently controlled, AI-native DSA/competitive programming/ICPC practice platform with a secure online judge, robust tutoring and eventually measured AI solution generation/fine-tuning. Compete through product quality, not copied proprietary content.

## Reality check

This repository has a local practice workflow: web/API catalog, Monaco drafts, Better Auth accounts, owned submission history and an optional gVisor-isolated control worker. AI, contests and production deployment remain unimplemented. Read PROJECT_STATUS.md for executed checks and runtime limits; never fabricate benchmarks, hosted CI outcomes or release readiness.

## Priority order

1. Agree licensing/contributor policy with maintainer.
2. Set up a reproducible monorepo scaffold with tests/CI.
3. Secure judge and authorized seed problems.
4. Working practice UI and submit/grade flow.
5. AI tutoring and verified solver.
6. Contest/ICPC features.
7. Model fine-tuning on licensed data and external GPUs.
8. Business/scale features.

## Engineering constraints

- One modular monorepo; services may run independently.
- Evaluate instead of blindly copying third-party GitHub projects.
- Reuse libraries for Monaco/editor, auth, UI, model inference and training when appropriate, after license/security review.
- Never merge entire upstream repositories without a documented rationale.
- Sandbox all untrusted compiled/interpreted code away from app services and credentials.
- No user secrets, hidden tests, copyrighted bulk problem data, large model weights or private datasets committed.
- No GPU training, paid infrastructure or expensive automated loops without approval.
- Maintain provider-neutral inference, bounded token/test budgets, and strict auth for submissions and contests.
- Treat model output as untrusted; don't disclose hidden tests or enable cheating in restricted contests.
- Prefer small patches, real tests and docs over broad speculative scaffolding.

## PR report format

Summary; files; decisions/reuse; tests actually run with results; open risks; deployment impacts; docs/PROJECT_STATUS changes. Don't say "done" for placeholders.

## Next implementation work

Follow docs/engineering/CODEX_PLAYBOOK.md and docs/onboarding/DEVELOPMENT.md. Preserve the tested identity, ownership, queue and sandbox boundaries. Maintain actual sandbox/hostile-program tests when changing execution; never fall back to host or ordinary-container execution. Production identity/runtime/operations hardening and provider-neutral AI tutoring remain future work. Do not present authored hints as AI inference or finite grading as proof of universal correctness.
