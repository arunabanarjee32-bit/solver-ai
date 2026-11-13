# Decisions requiring maintainer approval

These are not silently settled by an AI coding agent.

| ID | Decision | Initial proposed default | Why it matters |
| --- | --- | --- | --- |
| D-01 | Original code outbound license | Undecided | Public repo without a LICENSE is not automatically open source |
| D-02 | Contributor inbound IP policy | Undecided | Ownership/permissions for future commercial product |
| D-03 | First launch audience | DSA learners + early contest programmers | Narrows scope |
| D-04 | First languages | C++17, Python 3; C++20 next | Runtime/test burden |
| D-05 | Backend identity architecture | Better Auth + API verification, subject to audit | Avoid split auth |
| D-06 | Judge service | Piston self-hosted versus hardened alternate | Most important security decision |
| D-07 | Allowed initial problem sources | Original seed problems and explicit permissions | Copyright and trust |
| D-08 | First AI provider | Provider-neutral mocked adapter, then chosen API/model | Cost and flexibility |
| D-09 | Training data / model | Benchmark first; external-GPU LoRA later | Legal rights/compute budget |
| D-10 | Hosting/budget | Local dev first; vendor later | Operational ownership |
| D-11 | Brand/name | Working title 'Solver AI' | Avoid trademark conflicts |
| D-12 | Contest AI rules | AI disabled for restricted/live competitions | Integrity |
| D-13 | Privacy, data retention and training consent | Explicit opt-in and minimal collection | User trust and compliance |

## Decision records

For major choices add a short `docs/adr/NNNN-title.md` with Context, Options, Decision, Tradeoffs, Date and Owner. Avoid implying the suggested defaults above have been authorized.
