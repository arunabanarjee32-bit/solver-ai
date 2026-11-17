# [SAI-B029] Validate trusted problem authoring inputs before catalog publication

<!-- solver-ai-backlog:SAI-B029 -->
Order: 30 / Priority: P2 / Phase: 2-useful-practice
Area: content-tooling / Suggested role: content tooling engineer

## Problem

Catalog exercises are hand-authored in Python source. Adding content lacks a focused author preflight for duplicate IDs/slugs, incomplete constraints, bad samples, missing provenance or revision mismatch.

## Prerequisites

- SAI-B026 (publish/complete prerequisite first)
- SAI-B027 (publish/complete prerequisite first)
- SAI-B028 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- scripts/verification
- services/api/solver_api/features/catalog/models.py
- services/api/solver_api/features/catalog/content.py
- services/judge/solver_judge/grading/cases.py
- docs/onboarding/DEVELOPMENT.md

## Scope

- Create an offline trusted-author validation command for the existing content format or a deliberately small versioned input format.
- Check identifier uniqueness, required statements/formats/constraints, sample shape, starter languages, hint levels, provenance and public/grader revision linkage.
- Report path/field errors without executing arbitrary uploaded scripts or ingesting external archives.

## Acceptance criteria

- The current seeds pass all documented checks, while fixtures for duplicate slug, missing rights, invalid sample and revision mismatch fail precisely.
- The command leaves input files unchanged and never imports a user-selected executable module.
- An author can follow one documented workflow to prepare a reviewed content PR with B001 evidence.

## Validation

- Run the new authoring command only on trusted committed seeds and intentionally invalid temporary data fixtures.
- uv run --project services/api --frozen pytest services/api/tests/catalog/test_api.py services/judge/tests/grading/test_cases.py

## Out of scope

- Web-based public problem uploads
- Bulk competitor dataset ingestion
- A generic plugin execution system

## Risk and review

An authoring validator must validate data rather than become an unrestricted code loader.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
