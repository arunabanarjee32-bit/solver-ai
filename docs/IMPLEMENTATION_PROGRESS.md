# Implementation progress and Codex resume handoff

**Review date:** 2026-11-16. **Starting main:** `9952f8b5fa74f6900d57d1b48e3a26f3e962a358`. **Work branch:** `feat/sai-011-frontend-hint-api`. **Open PRs at start:** none. GitHub read/write identity was verified. No merge to `main` is implied.

## What exists and what was changed

On `main`: SAI-010 authenticated authored `POST /api/v1/hints` already exists with `solver_api/hints.py` and `tests/test_hints.py`. The existing unauthenticated authored ladder in `components/workspace.tsx` never called the API.

On this feature branch:
- NEW `apps/web/lib/hints.ts`: Zod strict input and response, matched problem/level, consistent authored/mock/model provenance, Better Auth short-lived JWT, 10-second timeout, AbortSignal cancellation, user-safe errors and retry.
- NEW `apps/web/components/account-hint.tsx`: optional signed-in level request (levels track existing ladder), guest sign-in link, explicitly authored/mock/AI result labels, loading/error/cancel/retry and account/logout change cancellation. Does not upload editor code.
- MODIFIED `apps/web/components/workspace.tsx`: integrates separate account hint without changing public authored hint reveal.
- MODIFIED `apps/web/app/globals.css`: responsive layout and safe long text.
- NEW `tests/e2e/hints.spec.ts`: guest pathway, token-backed request, authored/mock/model provenance, invalid/503 errors, retry and timeout.
- Research and backlog documents in `docs/` refreshed using live GitHub source and 20 upstream HEADs.

## Verification discipline

This session cannot clone GitHub into the local shell: `git ls-remote` failed with "Could not resolve host: github.com". No local `npm ci`, `uv sync`, Ruff, typecheck, build, or Playwright execution is claimed. GitHub Actions on branch push runs `uv sync --project services/api --frozen`, `npm ci`, `npm run test:api`, `npm run test:auth`, `npm run test:judge`, Ruff, `npm run typecheck`, `npm run build` and `npm run test:e2e`. See the latest branch CI run and record its **actual conclusion** before merge. The normal judge suite intentionally skips real gVisor integration, and the normal browser suite skips the judge-enabled case; those need a separately approved isolated environment if judge internals change.

The prior 2026-11-15 hosted evidence (GitHub Actions run 43737836616) passed SAI-010 but is not evidence that SAI-011 passed. No private runner, paid model, training, deployed service or new judge execution was used.

## Next task for any developer/Codex session

**Finish SAI-011 verification and review** — inspect branch head, run/check GitHub Actions with source-matching SHA, review auth and provenance tests, fix any red CI, open/maintain a focused PR to `main`. Do not auto-merge. If successful, update `PROJECT_STATUS.md` with exact CI URL/SHA/counts and verified browser behavior, then request reviewer approval.

**Next independent milestone after merge:** threat-modeled, budget-controlled real provider adapter. Start by writing ADR `docs/adr/0003-tutor-provider.md` covering approved provider, token/cost/user quotas, fixed safe egress, context/provenance validation, prompt injection, test fixtures, contest policy, access/retention, kill switch, and independent operational budget approval. Do not buy GPU or make paid API calls without explicit approval.

**Resume commands:** `git fetch origin`; `git checkout feat/sai-011-frontend-hint-api`; `npm ci`; `uv sync --project services/api --frozen`; `npm run test:api`; `npm run test:auth`; `npm run test:judge`; `uv run --project services/api --frozen ruff check services/api services/judge scripts`; `npm run typecheck`; `npm run build`; `npm run test:e2e`. Real gVisor suite only in supported isolated environment. Revert SAI-011 UI/client/test diff to roll back without changing existing hints, auth, queue, or judge.
