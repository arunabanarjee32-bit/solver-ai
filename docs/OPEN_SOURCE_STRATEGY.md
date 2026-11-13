# Build versus reuse: public repository evaluation

**Status: candidate inventory, NOT audited dependencies or selected integrations.** Assess upstream HEAD, dependencies, vulnerabilities, licenses, support and API compatibility before adoption. Public access is not permission to copy problem content or proprietary code.

## Guiding policy

One original modular monorepo, external libraries/services behind narrow adapters, rather than merging entire upstream repositories. Reuse mature commodity building blocks; build the differentiated tutor, solver orchestration, learning experience and product integration ourselves.

| Product area | Candidate upstream | Proposed approach | License / caution to verify |
| --- | --- | --- | --- |
| Web code editor | [Monaco Editor](https://github.com/microsoft/monaco-editor) | Reuse as dependency | MIT; browser integration and editor safety |
| Component UI | [shadcn/ui](https://github.com/shadcn-ui/ui) | Select components when frontend exists | MIT; audit transitive deps |
| Authentication | [Better Auth](https://github.com/better-auth/better-auth) | Consider rather than custom auth | MIT; session integration must be reviewed |
| Code execution | [Piston](https://github.com/engineer-man/piston) | Evaluate **self-hosted** sandbox adapter | MIT; sandbox hardening, resource isolation; don't rely on public API |
| Alternate judge foundation | [QingdaoU OnlineJudge](https://github.com/QingdaoU/OnlineJudge) | Study APIs and contest design; audit maintenance | MIT reported; check latest, security |
| Rich judge foundation | [DMOJ](https://github.com/DMOJ/online-judge), [judge server](https://github.com/DMOJ/judge-server) | Consider if advanced grading drives scope | AGPL-family obligations and integration cost |
| AI competitive solver | [phi-code](https://github.com/Nan-Do/phi-code) | Research candidate generation/ranking approach | Apache 2.0; research project, not full product |
| Multi-agent solving | [CodeSIM / CodeGenerator](https://github.com/kagnlp/CodeGenerator) | Study planning/feedback approach | MIT reported; reproduce evaluations |
| Fine-tuning | [Transformers](https://github.com/huggingface/transformers), [PEFT](https://github.com/huggingface/peft), [TRL](https://github.com/huggingface/trl) | Use libraries on external GPUs | Check exact release/model licenses |
| Efficient fine-tuning | [Unsloth](https://github.com/unslothai/unsloth) | Optional accelerator | Core Apache-2.0; some optional components have different licenses |
| Self-hosted inference | [vLLM](https://github.com/vllm-project/vllm) | Optional serving backend | Apache 2.0; requires suitable compute |
| Search | [Meilisearch](https://github.com/meilisearch/meilisearch) | Defer; PostgreSQL search first | Community/enterprise editions differ |
| Telemetry | [OpenTelemetry JS](https://github.com/open-telemetry/opentelemetry-js) | Integrate once runtime exists | Verify version and privacy settings |
| DSA tutoring reference | [dsa-gpt-tutor](https://github.com/0xmetaschool/dsa-gpt-tutor) | UX reference only | Evaluate own product and licenses |
| Contest platform reference | [MOJ](https://github.com/MonashAPS/MOJ) | Optional contest UX/architecture reference | AGPL-3.0-or-later; network-use obligations |

## Which code to prioritize?

**Now:** Monaco; proven web UI/auth libraries; robust code execution *after* security audit; basic Postgres; simple provider adapter.

**Soon:** AI tutor; phi-code/CodeSIM research; multiple candidate verification; problem metadata and difficulty tags.

**Later:** large contest frameworks; Meilisearch, enterprise auth, complex observability, GPU serving, model fine-tuning once benchmark/data evidence exists.

## Decision process (required for each upstream)

Record: exact upstream URL and commit/release; license and attribution obligations (including dependencies); release/maintenance activity; known security issues and patch policy; operational burden; implementation-vs-integration estimate; compatibility; exit/migration plan; decision owner and date.

Options: DEPENDENCY, SERVICE, REFERENCE ONLY, ORIGINAL IMPLEMENTATION, DEFER, REJECT. Do not conflate references with installed components.

## Licensing cautions

The project has no chosen original-code license yet. Do not assume this repository's public visibility grants an open-source license. MIT/Apache components can often be used in commercial software while preserving notices and other obligations, but consult counsel as needed. GPL/AGPL, source distribution and network-use obligations require particular review. Dataset licenses, model licenses, platform terms and problem copyright are separate issues. Do not paste competitor source code merely because it appears online.

## Codex cost controls

Audit existing work before rewriting. Prefer documentation/prototypes for high-risk unknowns. Choose one dependency at a time, add focused tests, avoid entire-repo source imports, pin versions, and write an ADR when changing foundations. See CODEX_PLAYBOOK.
