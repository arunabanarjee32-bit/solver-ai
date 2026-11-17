# [SAI-B137] Qualify inference export and quantization at the deployed precision

<!-- solver-ai-backlog:SAI-B137 -->
Order: 137 / Priority: P1 / Phase: ML-4 evaluation and delivery
Area: inference-qualification / Suggested role: ML inference engineer

Implementation status: planned

## Problem

The trained adapter and the intended serving artifact may differ through merging, quantization, tokenizer handling or engine support. A training-precision score cannot be assumed to survive the deployment format.

## Prerequisites

- [SAI-B001 (completed locally)](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/backlog/issues/SAI-B001.md)
- SAI-B079 (confirm prerequisite state in the catalogue)
- SAI-B128 (confirm prerequisite state in the catalogue)
- SAI-B135 (confirm prerequisite state in the catalogue)
- SAI-B136 (confirm prerequisite state in the catalogue)

## Current code ownership

- docs/research/MODEL_DATA_EVALUATION.md
- docs/product/DSA_SOLVER_READINESS.md
- docs/architecture/ARCHITECTURE.md
- tests/tooling

## Scope

- Implement a reproducible export recipe for one approved serving engine/precision with exact base/adapter/tokenizer/config identities and safe serialization.
- Compare the exported artifact with the qualified training/reference representation using bounded tokenization/generation parity fixtures and the preregistered regression subset.
- Measure supported context, throughput/latency, actual peak memory and constrained concurrency on approved hardware; document unsupported operations and fallback to the retained qualified artifact.

## Acceptance criteria

- Export artifacts carry reconstructible lineage and cannot load with an incompatible tokenizer or unapproved remote-code path.
- Actual inference-precision evaluation meets B128 thresholds or produces an explicit narrower/rejected decision; no assumption of lossless quantization substitutes for measurement.
- A repeat export from the recorded recipe yields the stated deterministic identities or documented tool nondeterminism, and resources stay inside the approved envelope.

## Validation

- Future approved execution: run the exact export/qualification recipe on the authorized inference host and replay token/template plus held-out regression checks.
- Verify malformed/mismatched export manifests fail in the CPU synthetic tooling fixtures.

## Out of scope

- Quantizing every available format
- Assuming a specific model/engine is selected now
- Public deployment or unrestricted benchmark tuning

## Risk and review

Merging/quantization can silently degrade quality or exceed memory; qualify the artifact actually deployed, not only its training checkpoint.

Implement this issue on a dedicated branch and submit a PR linked here. Include the exact tests run and remaining limitations. Do not self-merge. A maintainer/assistant review must inspect the diff, dependencies, security and actual check results before a maintainer-authorized merge. Do not enable paid services, training or new production infrastructure without the owner's explicit approval.
