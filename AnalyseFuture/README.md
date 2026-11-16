# Preserved material for future analysis

This folder preserves the two ZIPs supplied with Solver AI and every extracted
file, at the maintainer's request. It separates research/reference material from
the working product. Inclusion here is **not adoption, a working AI integration,
or an assertion that the material is malicious**.

## Contents and original locations

| Original root file | Preserved original | Extracted contents |
| --- | --- | --- |
| `CodeGenerator-master.zip` | `archives/CodeGenerator-master.zip` | `extracted/CodeGenerator-master/` (73 files) |
| `phi-code-main.zip` | `archives/phi-code-main.zip` | `extracted/phi-code-main/` (49 files) |

`manifest.json` records the baseline Git commit, all original tracked paths and
SHA-256 hashes, both archive hashes, and each extracted file's original member
name, destination, size and SHA-256. No archive contents were discarded. File
contents are preserved byte for byte. Three upstream Git control files were
renamed to `.gitignore.upstream` or `.gitattributes.upstream` so their ignore and
Git LFS rules do not affect this repository. The originals also remain unchanged
inside the ZIPs. These are filename changes, not content edits.

## How this relates to the project

- CodeGenerator/CodeSIM offers Python planning, generation and repair research.
- phi-code offers Python candidate generation and ranking research.
- Their license notices, dependency lists, example configuration, benchmark data,
  images and published results remain alongside their sources.
- Dependencies were not installed and archive code was not run. These projects
  are outside the root npm workspace, API dependency project and normal CI targets.
- Their code execution paths are not the application's isolated judge. Any later
  reuse must pass through Solver AI's reviewed execution and ownership boundaries.
- Dataset, contest-content and model rights remain separate from source-code
  licenses. Preservation does not authorize bulk ingestion, redistribution of
  derived datasets, training or claims that upstream benchmark results reproduce.
- Five `phi-code-main/datasets/*.jsonl` members are Git LFS pointers supplied in
  the ZIP, not the underlying datasets. The pointers are preserved exactly;
  extracting a ZIP cannot restore data it does not contain.

The existing research assessment is in
[`docs/AUDIT_AND_AI_PLAN_2026-11-15.md`](../docs/AUDIT_AND_AI_PLAN_2026-11-15.md).
The repository map and review findings are in
[`docs/REPOSITORY_STRUCTURE.md`](../docs/REPOSITORY_STRUCTURE.md).
The expanded product proposal is [`PROJECT_IDEA.txt`](../PROJECT_IDEA.txt).

Future displaced or uncertain files belong here with their source path and a
reason recorded in the inventory. Do not delete material merely because it
does not fit the current product. Keep runtime credentials and private user
data out of Git.
