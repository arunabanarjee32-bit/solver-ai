# [SAI-B039] Repair contrast, reduced-motion and zoom reflow gaps

<!-- solver-ai-backlog:SAI-B039 -->
Order: 40 / Priority: P2 / Phase: 2-useful-practice
Area: accessibility / Suggested role: accessibility/UI engineer

Implementation status: planned

## Problem

Responsive styles exist, but the repository has no demonstrated review of text/control contrast, reduced-motion behavior and high-zoom reflow. Decorative motion and narrow result surfaces can block access.

## Prerequisites

- SAI-B037 (confirm prerequisite state in the catalogue)
- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)

## Current code ownership

- apps/web/app/globals.css
- apps/web/components/shell.tsx
- apps/web/features/practice/catalog.tsx
- apps/web/features/practice/workspace.tsx
- tests/e2e/practice/practice.spec.ts

## Scope

- Measure contrast of actual text/control/focus states and repair specific failures without redesigning the product.
- Respect prefers-reduced-motion for decorative animation and smooth scrolling.
- Check 200%/400% zoom and a narrow viewport for catalog, problem/editor controls and result text; preserve necessary code scrolling without page-wide loss of controls.

## Acceptance criteria

- Changed text/control combinations meet the chosen documented WCAG AA contrast criterion with recorded measurements.
- Reduced-motion emulation removes nonessential animation while all controls remain usable.
- At reviewed zoom/viewports, content and actions are reachable with no clipped critical labels or horizontal page scrolling caused by layout controls.

## Validation

- PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e -- tests/e2e/practice/practice.spec.ts --workers=2
- Record manual contrast and zoom findings for changed states and limitations.

## Out of scope

- A new brand/theme system
- Marketing a complete accessibility certification
- Reformatting user code to eliminate editor horizontal scrolling

## Risk and review

Visual fixes can hide controls or alter editor sizing; preserve responsive behavior and clear focus states.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
