# Implementation, review and merge workflow

The owner has assigned implementation tasks to other AI tools and requested
maintainer/assistant review before merging their work. The
[ordered backlog](backlog/README.md) contains 127 task cards with current feature
paths, prerequisites, bounded scope, acceptance criteria and validation commands.
Cards are plans; [publication.json](backlog/publication.json) records actual
GitHub issue links and any publishing blocker.

## Implement one ready task

1. Use the **Order** column and check every prerequisite. Stable `SAI-Bnnn` IDs
   identify tasks; the numeric suffix is not the execution order. Record the task
   assignment so two tools do not implement competing versions of the same work.
2. Inspect the current feature, tests, [structure guide](../../PROJECT_STRUCTURE.md)
   and [status ledger](../status/PROJECT_STATUS.md). Search for existing work first.
3. Create one implementation branch and a focused PR linked to the actual issue
   or stable local card if publication is blocked. Routine reversible work within
   the assigned issue does not need repeated permission requests.
4. Keep public contracts, private state and isolation boundaries intact. Put new
   modules and tests in their owning functional collection. Preserve superseded
   material with provenance; do not delete archives or change their byte hashes.
5. Run the relevant checks and report passed, failed, skipped and unrun outcomes.
   Never invent execution or weaken assertions/security to obtain a passing run.
6. Include the exact head revision, changed paths, dependencies, observed behavior,
   validation and remaining risks. Request review and respond with focused fixes.
   Do not self-merge or push implementation work directly to `main`.

Owner-only licensing, resource spending, production activation, data-use and
irreversible operations retain their explicit gates. A task card is not consent
to send private submissions to a provider, train a model or purchase compute.

## Reviewer responsibilities

The designated maintainer/assistant reviews the exact PR head and its relationship
to the issue and prerequisites. Review must inspect code, imports, authorization,
data ownership, execution boundaries, dependency changes and actual check results.
Green CI and a completed template alone do not establish a correct implementation.

The reviewer requests changes when evidence is missing or behavior is wrong. After
corrections, review the new head and relevant regression checks before an
owner-authorized merge. Preserve published history and follow the owner's chosen
merge policy; never force-push `main` or merge every PR automatically.

The [executable evidence contract](PR_EVIDENCE.md) now checks a single fenced JSON
record on PR creation, body edits and head changes. It runs trusted base code
with read-only access and never executes submitted commands or echoes PR-body
content. A complete record is not proof of execution, substantive approval or
permission to merge. Keep failed/skipped/not-run outcomes honest.

Bring a PR number or URL into an active assistant session for review. The assistant
cannot continuously monitor GitHub, assign work or merge future PRs after the
session ends. No unattended review bot or automatic merger is enabled here.

This maintenance session retains the owner's explicit direct-to-`main` checkpoint
authorization. The branch/PR workflow above governs contributions from other
implementation tools under the latest review-and-merge instruction.

## Enforcement and current access

Repository prose cannot enforce GitHub permissions. SAI-B001's executable
PR evidence gate is implemented locally; SAI-B127 requires owner-approved reviewed-merge rules and actual
reviewer identities. Effective branch settings have not been verified through the
currently blocked GitHub API. Do not claim those controls are already enforced.

The environment allows Git HTTPS operations but currently denies CONNECT to
`api.github.com`. An additive allowlist draft is saved in environment settings;
it requires review/save and publication to apply. Existing `gh` authentication
is reused; network denial prevents testing its API issue-write permissions.
Never paste credentials into chat, issue bodies, task cards or commits.

## Publishing the prepared issues

```sh
# Offline validation and card consistency, with no GitHub requests:
python3 scripts/github/publish_issues.py
python3 scripts/github/build_backlog.py --check

# After API access is available, create only missing issues:
python3 scripts/github/publish_issues.py --publish
python3 scripts/github/build_backlog.py --write
```

The publisher reconciles durable remote markers before posting, preserves
existing issues, paces writes, records each confirmed issue and stops on uncertain
mutations. Rerunning reconciles remote state first. It never blindly retries an
ambiguous POST, edits/closes issues or performs merges.
