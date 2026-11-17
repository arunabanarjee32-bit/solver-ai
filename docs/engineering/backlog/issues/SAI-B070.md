# [SAI-B070] Normalize bounded source candidates without archive parser assumptions

<!-- solver-ai-backlog:SAI-B070 -->
Order: 89 / Priority: P1 / Phase: AI-3 bounded candidate solver
Area: Candidate generation / Suggested role: AI/backend engineer

## Problem

Archived fenced-code parsers assume matching blocks and can index an empty result. Candidate source must have a deterministic language, byte cap and provenance before execution.

## Prerequisites

- SAI-B046 (publish/complete prerequisite first)
- SAI-B068 (publish/complete prerequisite first)
- SAI-B069 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- services/api/solver_api/features/hints/service.py
- services/api/solver_api/features/submissions/store.py
- AnalyseFuture/extracted/CodeGenerator-master/src/utils/parse.py
- services/api/tests/hints/test_hints.py

## Scope

- Define a candidate artifact schema with exact source bytes/hash and supported runtime identity.
- Accept one reviewed response form; reject ambiguous multiple blocks, missing source and excess bytes.
- Count rejected generation against the run's recorded attempts/usage without executing it.

## Acceptance criteria

- Empty, mismatched-fence, multiple-code and oversized fixtures have deterministic outcomes.
- Source hash is stable over the exact bytes later sent to the judge.
- Unsupported languages never reach the execution queue.

## Validation

- Future authorized check: uv run --project services/api --frozen pytest services/api/tests/hints services/api/tests/submissions -q

## Out of scope

- Running source during extraction
- Repairing archived parsers in place

## Risk and review

Aggressive source cleanup can silently alter the program the learner thinks was tested.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
