# Contributor tasks — suggested starter backlog

**This is the suggested backlog, not a list of created GitHub issues.** Much of the local foundation is implemented; see progress below and PROJECT_STATUS.md for verification. Normally pick one scoped issue per PR and discuss major work first. Follow explicit owner instructions when they authorize a different workflow, as in the current recovery task's direct-to-main checkpoint commits.

| ID | Size | Suggested title | Acceptance criteria |
| --- | --- | --- | --- |
| SAI-001 | S | Select repository license / contributor policy | Maintainer decision; add appropriate LICENSE and policy docs; record ADR |
| SAI-002 | M | Scaffold web/API dev environment | Next.js and FastAPI start locally; health endpoint; reproducible documented commands |
| SAI-003 | S | Add quality gates | JS/Python lint/type checks, tests and GitHub Actions CI run on PR |
| SAI-004 | M | Define problem / submission schema | Versioned problems, language runtime and verdict contracts; unit tests |
| SAI-005 | M | Create original seed problem fixtures | Rights/provenance manifest; original tests; validator and examples |
| SAI-006 | M | Prototype sandboxed judge | Adapter, limits, isolated runtime, good/invalid/TLE/OOM tests; security review |
| SAI-007 | M | Build problem list and Monaco editor | Accessible page, sample view, code selection and editor state tests |
| SAI-008 | M | Submit-and-grade end-to-end path | Real code run, persisted submission, private test secrecy and verdict poll |
| SAI-009 | M | Add accounts and submission access control | Secure sessions, ownership checks, auth integration tests |
| SAI-010 | S | Define provider boundary and authored hint API | Authored output clearly labeled; bounded responses, privacy and auth tests; real provider deferred |
| SAI-011 | M | Connect authenticated graded hints to the browser | Typed authored-hint UI, no hidden-test leak, answer spoil controls; generated tutoring remains separate work |
| SAI-012 | M | Establish held-out benchmark | Provenance, split integrity, fixed baselines and test harness |
| SAI-013 | S | Build vs reuse ADR for judge choice | Upstream license, maintenance/security, operational comparison and recommendation |
| SAI-014 | S | Dependency inventory | Exact versions, notice/license compliance and vulnerability review process |

## Ready-made issue format

Current foundation progress: SAI-002 is implemented locally. SAI-007 has catalog/detail, Monaco, browser drafts and browser tests. SAI-003 has Python lint, TypeScript checking, API/auth/judge/browser tests and CI configuration, with historical hosted evidence recorded in PROJECT_STATUS.md; a full accessibility/lint policy remains future work. SAI-004/005/014 remain partial: public problem and submission contracts, original samples/generated grading cases, provenance and initial dependency decisions exist, while richer problem/test version management and a full compliance audit remain open. SAI-006/008/009 have a bounded local gVisor runner, actual authenticated run/submit and owned SQLite history with tests. SAI-010's authenticated authored hint API is implemented; it makes no model call. A prior SAI-011 browser integration is being recovered in the current task and awaits final integration validation. Production identity, host-wide resource accounting, independent isolation review, real model inference and contests remain open. These statements do not close GitHub issues or mark the full P0 release complete.

**Problem / user value:** Who benefits and what problem is solved?
**Scope:** Exact modules/components touched.
**Non-goals:** Features explicitly deferred.
**Acceptance:** Observable pass/fail criteria.
**Security and rights:** Data/IP/runner/auth implications.
**Evidence:** Reproduction, tests and docs.
**Dependencies:** Previous issue or ADR, if applicable.

## Recommended order

Resolve SAI-001's licensing/contributor policy, preserve the already implemented SAI-002/003 foundation and consult PROJECT_STATUS.md before choosing remaining contract, content, runtime or UI work. Review recovered SAI-011 behavior before adding another hint implementation. Real-provider and solver work should follow explicit budgets, privacy and a proven judge, not precede them.
