# Contributor tasks — suggested starter backlog

**These are proposed tasks, not yet GitHub issues or implemented features.** New contributors should first read START_HERE.md and PROJECT_STATUS.md. Pick one scoped issue per PR. Create a GitHub issue before major work.

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
| SAI-010 | S | Define model provider and mock hint API | Mock clearly labeled; budget, privacy and auth tests |
| SAI-011 | M | Implement graded tutor hints | Conceptual hints, no hidden-test leak, answer spoil controls |
| SAI-012 | M | Establish held-out benchmark | Provenance, split integrity, fixed baselines and test harness |
| SAI-013 | S | Build vs reuse ADR for judge choice | Upstream license, maintenance/security, operational comparison and recommendation |
| SAI-014 | S | Dependency inventory | Exact versions, notice/license compliance and vulnerability review process |

## Ready-made issue format

**Problem / user value:** Who benefits and what problem is solved?
**Scope:** Exact modules/components touched.
**Non-goals:** Features explicitly deferred.
**Acceptance:** Observable pass/fail criteria.
**Security and rights:** Data/IP/runner/auth implications.
**Evidence:** Reproduction, tests and docs.
**Dependencies:** Previous issue or ADR, if applicable.

## Recommended order

Begin with SAI-001 to establish policy and SAI-002/003 for project skeleton, then SAI-004/005/013/006 before SAI-007/008. AI work should follow a proven judge, not precede it.
