# Decisions requiring maintainer approval

These are not silently settled by an AI coding agent.

This register began before the local identity and judge implementation. ADR 0001 and ADR 0002 record the adopted development choices; they do not resolve original-code licensing, production deployment or provider spending. Read technical rows as production/review decisions where a local choice already exists, rather than instructions to rebuild working services.

| ID | Decision | Initial proposed default | Why it matters |
| --- | --- | --- | --- |
| D-01 | Original code outbound license | Undecided | Public repo without a LICENSE is not automatically open source |
| D-02 | Contributor inbound IP policy | Undecided | Ownership/permissions for future commercial product |
| D-03 | First launch audience | DSA learners + early contest programmers | Narrows scope |
| D-04 | First languages | C++17, Python 3; C++20 next | Runtime/test burden |
| D-05 | Production identity operations and review | Retain adopted Better Auth + API verification; review recovery, trusted ingress and deployment policy | Avoid split auth; local adoption is recorded in ADR 0002 |
| D-06 | Production judge infrastructure | Retain local gVisor boundary; choose maintained dedicated production runtime/operations after review | ADR 0002 adopted local gVisor and deferred stock Piston; public isolation/resource review remains open |
| D-07 | Allowed initial problem sources | Original seed problems and explicit permissions | Copyright and trust |
| D-08 | First real AI provider | Existing provider-neutral authored backend, then owner-approved API/model and budget | Authored hints are implemented, not model inference; cost and privacy need approval |
| D-09 | Training data / model | Unselected; research multiple families, compare matched baselines, then decide checkpoint/data/external training budget | See model research catalogue; no assumed model, licensed data and compute decision required |
| D-10 | Hosting/budget | Local dev first; vendor later | Operational ownership |
| D-11 | Brand/name | Working title 'Solver AI' | Avoid trademark conflicts |
| D-12 | Contest AI rules | AI disabled for restricted/live competitions | Integrity |
| D-13 | Privacy, data retention and training consent | Explicit opt-in and minimal collection | User trust and compliance |

## Decision records

For major choices add a short `docs/architecture/adr/NNNN-title.md` with Context, Options, Decision, Tradeoffs, Date and Owner. Avoid implying the suggested defaults above have been authorized.

The [fine-tuning model research catalogue](../research/FINETUNING_MODEL_RESEARCH.md)
records candidates and questions for D-09. The
[solver readiness plan](../product/DSA_SOLVER_READINESS.md) describes the future
training, evaluation and release evidence; neither document selects a checkpoint
or authorizes model training or spending.
