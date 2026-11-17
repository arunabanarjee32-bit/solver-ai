# [SAI-B142] Accept bounded account-owned specifications for new authorized DSA problems

<!-- solver-ai-backlog:SAI-B142 -->
Order: 142 / Priority: P1 / Phase: AI-6 new-problem coverage
Area: New-problem solver input / Suggested role: API engineer with content/privacy and solver reviewer

Implementation status: planned

## Problem

Existing solver specifications project the seed catalog, while the main goal includes previously unseen user-supplied DSA statements. An explicit bounded input contract is needed without treating arbitrary text as trusted instructions or an independently verified grader.

## Prerequisites

- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)
- SAI-B026 (confirm prerequisite state in the catalogue)
- SAI-B049 (confirm prerequisite state in the catalogue)
- SAI-B064 (confirm prerequisite state in the catalogue)
- SAI-B068 (confirm prerequisite state in the catalogue)
- SAI-B128 (confirm prerequisite state in the catalogue)
- SAI-B018 (confirm prerequisite state in the catalogue)
- SAI-B022 (confirm prerequisite state in the catalogue)

## Current code ownership

- services/api/solver_api/features/solver/
- services/api/tests/solver/
- docs/product/DSA_SOLVER_READINESS.md

## Scope

- Extend the B068 public ProblemSpec contract with an account-owned bounded ingestion path for a complete pasted statement, constraints, input/output, public examples, language and user rights/assistance attestation. Use immutable source fingerprints and retain original/normalized provenance; do not create another canonical catalog/grader revision authority.
- Validate size, encoding, sample shape and supported formats; return missing-information, contradictory-input or unsupported-format states before generation. A user-supplied sample or attestation is not proof of source rights or a trustworthy hidden evaluator.
- Reuse identity, entitlement, source-sharing consent and retention/deletion controls. Do not fetch arbitrary URLs, execute uploaded validators/scripts, accept archive code or send private inputs to an unapproved provider. Distinguish public sample checking from independent verified evaluation.
- Register owned ProblemSpec source/version storage in the existing B018/B022 export, retention and deletion hooks, including derived provider/run references; do not create a separate data-lifecycle policy.

## Acceptance criteria

- A valid new authorized statement outside the three seeds produces an owned immutable specification; another account cannot read or modify it. Corrections create attributable new versions.
- Oversized, incomplete, maliciously embedded instructions and unsupported interactive/custom-checker formats cannot bypass policy, quotas or schema validation. The API does not claim an unreviewed problem is independently graded.
- Only explicitly approved public/consented context reaches the existing generation contract; credentials, private grader data and unrelated account history remain excluded. Deletion/retention removes the owned input under the established policy.

## Validation

- Use synthetic non-catalog statements and fixture identities to check ownership, limits, deterministic fingerprints, explicit unsupported/missing-information outcomes and injection boundaries.
- Inspect data-flow to provider/evaluator serializers and verify no arbitrary network fetch, executable import or alternate host executor is introduced.

## Out of scope

- Bulk scraping external problem banks or resolving their rights automatically
- Interactive/custom checker execution and unsupported languages
- Inventing hidden tests, a reference oracle or a correctness proof from user samples

## Risk and review

Arbitrary problem text is untrusted data. It can contain prompt injection, private material, contradictory constraints or false sample answers; account boundaries, bounded parsing and honest evidence labels must survive.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
