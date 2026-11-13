# 0001 — Practice foundation

Date: 2026-11-13. Status: implemented first increment; larger product remains planned.

## Scope and boundaries

Adopt Next.js + TypeScript and FastAPI in the proposed modular monorepo. Implement a read-only public catalog of three original seed problems, statement/samples, Python/C++17 Monaco editing, drafts scoped by problem and language in browser localStorage, and authored progressive hints. Avoid a database until there is authenticated persistent data to store. Search/filter a complete three-item library in the client; the API independently supports bounded filtering and pagination for future clients.

No source code is submitted to or executed by the server. Run/Submit controls are disabled. No verdict, progress statistic or AI response is fabricated. Hints are authored text, not an offline AI mock. Auth, judge isolation, durable submissions, queueing, rate limits for writes, provider adapters and contests are deferred. The next execution milestone requires the review and hostile-code tests in [Judge security](../JUDGE_SECURITY.md).

## Adopted dependencies

Exact versions and transitive packages are in `package-lock.json` and `services/api/uv.lock`. Use frozen installs. These are dependencies, not imported upstream repositories.

| Component | Release | Upstream / license | Reason and exit path |
| --- | --- | --- | --- |
| Next.js | 16.4.6 | https://github.com/vercel/next.js / MIT | Maintained React routing/build tooling; replace the presentation/proxy layer independently of FastAPI |
| React / React DOM | 19.3.1 | https://github.com/facebook/react / MIT | UI state and accessible native controls |
| Monaco Editor | 0.57.0 | https://github.com/microsoft/monaco-editor / MIT | Mature code editing; locally hosted assets; draft text is independent of the editor |
| Monaco React wrapper | 4.7.0 | https://github.com/suren-atoyan/monaco-react / MIT | Small lifecycle adapter, replaceable by direct editor integration |
| DOMPurify | 3.4.17 | https://github.com/cure53/DOMPurify / Apache-2.0 OR MPL-2.0 | Replaces Monaco's vulnerable embedded sanitizer during bundling |
| esbuild | 0.28.2 | https://github.com/evanw/esbuild / MIT | Builds local Monaco and worker assets; build-time dependency only |
| FastAPI | 0.162.6 | https://github.com/fastapi/fastapi / MIT | Typed validation and OpenAPI; keep public problem contracts stable if replacing service |
| Uvicorn | 0.54.0 | https://github.com/Kludex/uvicorn / BSD-3-Clause | ASGI serving, replaceable by compatible server |
| Playwright | 1.65.0 | https://github.com/microsoft/playwright / Apache-2.0 | Actual browser verification of integrated behavior |

Development also uses TypeScript (Apache-2.0), pytest (MIT), HTTPX (BSD-3-Clause), and Ruff (MIT). Preserve installed package LICENSE/NOTICE files and review transitive dependencies before distributing. Initial release choices use current registry releases; run `npm audit` and revisit dependency advisories regularly. This is an initial component decision, not a comprehensive security or legal audit. No third-party problem statements, model weights or datasets are incorporated. Original seeds are tagged with their provenance in the catalog.

Monaco 0.57.0 vendors DOMPurify 3.4.15 inside its source, so an npm override alone does not patch the browser bundle. The editor build replaces that import with the pinned 3.4.17 package, asserts the installed version, and checks the bundle's input graph excludes the vendored sanitizer. Keep these checks when updating Monaco. `public/monaco/build-info.json` records the verified sanitizer version in generated assets. The root override also patches Monaco's separate npm dependency. The initial npm audit after a clean locked install reports no known advisories; this does not establish absence of vulnerabilities.

Decision owner: initial implementation for maintainer review. The original project code/content still has no selected outbound license. This change does not resolve that maintainer decision.

## Operational implications

The browser uses same-origin API URLs; Next.js rewrites to a server-configured upstream. Render statements as text instead of allowing embedded HTML. Public API models contain only public samples and authored hints. Stable errors include request IDs without exposing stack traces. Neither server needs secrets. The optional local Compose configuration is application development infrastructure, never a sandbox for arbitrary submitted programs.

Native setup and validation are documented in [Development](../DEVELOPMENT.md). CI is added as configuration; report hosted CI results only after an actual run. There is no public deployment in this increment.
