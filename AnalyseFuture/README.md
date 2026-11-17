# Preserved material for future analysis

This folder preserves the two ZIPs supplied with Solver AI and every extracted
file, at the maintainer's request. It separates research/reference material from
the working product. Inclusion here is **not adoption, a working AI integration,
or an assertion that the material is malicious**.

## Contents and original locations

Current recovery records are grouped by responsibility:

| Collection | Recovery records |
| --- | --- |
| `audits/` | [Repository audit](audits/REPOSITORY_AUDIT.txt), [security audit](audits/SECURITY_AUDIT.txt) |
| `repository-inventory/` | [Complete file inventory](repository-inventory/COMPLETE_FILE_INVENTORY.txt), [feature inventory](repository-inventory/FEATURE_INVENTORY.txt), [duplicate analysis](repository-inventory/DUPLICATE_ANALYSIS.txt), [archived-files manifest](repository-inventory/ARCHIVED_FILES_MANIFEST.txt), [dependency map](repository-inventory/DEPENDENCY_MAP.txt) |
| `migration-records/` | [Original-to-new path mapping](migration-records/ORIGINAL_TO_NEW_PATH_MAPPING.txt), [consolidation report](migration-records/CONSOLIDATION_REPORT.txt), [migration summary](migration-records/MIGRATION_SUMMARY.txt) |
| `planning/` | [Project vision and future roadmap](planning/PROJECT_VISION_AND_FUTURE_ROADMAP.txt), [technical debt](planning/TECHNICAL_DEBT.txt) |
| `validation/` | [Test and validation report](validation/TEST_AND_VALIDATION_REPORT.txt) |
| `continuation/` | [Work progress](continuation/WORK_PROGRESS.txt), [next-developer instructions](continuation/NEXT_DEVELOPER_INSTRUCTIONS.txt) |

The dependency map describes actual cross-service calls. `repository-inventory/`
also contains machine-readable baseline/current ledgers and independent
assessments. Moving these records changes their locations, not their evidence or
the status of any earlier test result.

`historical-implementations/` preserves 23 changed file versions from the SAI-011
and permanent-memory branches. Their source commits and byte hashes are in
`repository-inventory/historical-branches.json`. Five SAI-011 runtime/test inputs
were selectively recovered into the active frontend; these snapshots retain the
original branch versions. Archived `AGENTS.md` is renamed `AGENTS.md.upstream`
so obsolete instructions remain a record. No snapshot is installed or imported.

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
[`docs/research/AUDIT_AND_AI_PLAN_2026-11-15.md`](../docs/research/AUDIT_AND_AI_PLAN_2026-11-15.md).
The repository map and review findings are in
[`docs/architecture/REPOSITORY_STRUCTURE.md`](../docs/architecture/REPOSITORY_STRUCTURE.md).
The canonical future proposal is
[`planning/PROJECT_VISION_AND_FUTURE_ROADMAP.txt`](planning/PROJECT_VISION_AND_FUTURE_ROADMAP.txt);
the earlier [`docs/product/PROJECT_IDEA.txt`](../docs/product/PROJECT_IDEA.txt)
remains available.

Future displaced or uncertain files belong here with their source path and a
reason recorded in the inventory. Do not delete material merely because it
does not fit the current product. Keep runtime credentials and private user
data out of Git.
