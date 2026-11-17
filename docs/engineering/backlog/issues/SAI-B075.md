# [SAI-B075] Admit only reviewed differential and metamorphic test specifications

<!-- solver-ai-backlog:SAI-B075 -->
Order: 94 / Priority: P1 / Phase: AI-4 evaluation and research gates
Area: Authorized test generation / Suggested role: Problem author and judge evaluation engineer

Implementation status: planned

## Problem

More generated inputs do not establish correctness when the reference oracle or metamorphic relationship is wrong; model-produced expectations may share the candidate's error.

## Prerequisites

- SAI-B068 (confirm prerequisite state in the catalogue)
- SAI-B071 (confirm prerequisite state in the catalogue)
- SAI-B074 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- services/judge/solver_judge/grading/cases.py
- services/judge/solver_judge/sandbox/harness.py
- docs/research/MODEL_DATA_EVALUATION.md
- services/judge/tests/grading/test_cases.py

## Scope

- Define versioned reviewed oracle/relation manifests tied to original or permissioned tasks.
- Bound generated case counts, seed space and execution resources.
- Keep expected answers outside learner containers and forbid model assertions from becoming trusted oracles automatically.

## Acceptance criteria

- Invalid relation/oracle versions are refused before candidate scoring.
- Reference fixtures independently expose a deliberately wrong candidate.
- Run reports distinguish reviewed generated cases from public samples and private grading.

## Validation

- Future authorized check: uv run --project services/api --frozen pytest services/judge/tests/grading -q; approved isolated oracle integration fixtures.

## Out of scope

- Universal test adequacy guarantees
- Publishing private grader answers

## Risk and review

A faulty oracle can confidently reject correct programs or accept incorrect ones.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
