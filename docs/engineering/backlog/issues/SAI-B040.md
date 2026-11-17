# [SAI-B040] Add a focused automated accessibility regression gate

<!-- solver-ai-backlog:SAI-B040 -->
Order: 41 / Priority: P2 / Phase: 2-useful-practice
Area: accessibility-quality / Suggested role: accessibility/test engineer

Implementation status: planned

## Problem

Accessibility repairs need a repeatable regression signal. Existing functional Playwright assertions do not provide a dedicated scan of representative guest, signed-in, loading, error and result states.

## Prerequisites

- SAI-B037 (confirm prerequisite state in the catalogue)
- SAI-B038 (confirm prerequisite state in the catalogue)
- SAI-B039 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- apps/web/package.json
- package-lock.json
- tests/e2e/practice/practice.spec.ts
- tests/e2e/submissions/submissions.spec.ts
- tests/e2e/hints/hints.spec.ts
- .github/workflows/ci.yml
- docs/onboarding/DEVELOPMENT.md

## Scope

- Review and pin a browser accessibility scanner as a development-only dependency, retaining its license and lockfile integrity.
- Scan a small representative set of stable app states and fail on agreed actionable violations; keep explicit, justified exceptions narrow.
- Document which manual keyboard/screen-reader checks remain necessary and attach evidence to AI-authored PRs.

## Acceptance criteria

- A deliberate missing-label or contrast fixture is detected by the new gate and a clean repaired state passes.
- The gate covers guest practice, account form, authored hint result and owned submission result without scanning private production data.
- Exceptions identify a specific rule/node, reason and owner rather than globally disabling categories; scan output does not claim full conformance.

## Validation

- Run the scoped Playwright accessibility cases added to the existing practice/hints/submissions suites.
- When CI execution is authorized, observe the dedicated accessibility job/step on the exact PR commit.

## Out of scope

- Replacing manual accessibility review
- Adding a paid audit service by default
- Globally suppressing violations to obtain a green check

## Risk and review

Scanner version changes and noisy exceptions can erode trust; pin the tool and review exceptions like code.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
