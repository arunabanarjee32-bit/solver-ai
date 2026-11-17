# [SAI-B005] Pin web and API container bases and align intended Python patch versions

<!-- solver-ai-backlog:SAI-B005 -->
Order: 6 / Priority: P1 / Phase: 1-safe-pilot
Area: supply-chain / Suggested role: release engineer

## Problem

The judge base is already digest-pinned, while web/API image tags remain mutable and the API Python pin is broader than the root patch pin. Rebuilding can silently select different toolchains.

## Prerequisites

- SAI-B004 (publish/complete prerequisite first)
- SAI-B001 (publish/complete prerequisite first)

## Current code ownership

- apps/web/Dockerfile
- services/api/Dockerfile
- services/api/.python-version
- .python-version
- .node-version
- docs/onboarding/DEVELOPMENT.md

## Scope

- Select supported official web/API base-image identities and pin immutable digests while preserving their current nonroot and read-only runtime assumptions.
- Reconcile the intended root and API Python patch policy with actual documented supported versions; do not silently widen dependency compatibility.
- Document how digest/patch updates are reviewed and refreshed.

## Acceptance criteria

- Web/API base-image references include reviewed digests and readable versions.
- Root/API Python pins express one intentional policy and frozen dependency installation remains enabled.
- A later authorized build produces artifacts without runtime keys, databases or AnalyseFuture content; no TLS or checksum verification is disabled.

## Validation

- Statically review Docker stages, image origins and version pins.
- When builds are authorized: npm run build; docker build --secret id=proxy_ca,src=/etc/ssl/certs/ca-certificates.crt -t solver-ai-api:pin-check services/api.

## Out of scope

- Replacing the sandbox runtime
- Automatic latest-version upgrades
- Installing GPU tooling

## Risk and review

Image updates may change OS libraries or runtime behavior; preserve rollback digests and verify supported architecture.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
