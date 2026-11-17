## What problem does this PR solve?

Link issue and describe the user-visible value.
Include the stable backlog ID (`SAI-Bnnn`), execution order and prerequisite status.

## Machine-readable review evidence

Fill every field in this single block using the [evidence contract](https://github.com/arunabanarjee32-bit/solver-ai/blob/main/docs/engineering/PR_EVIDENCE.md).
Use the actual PR head revision. Record honest failed, skipped or not-run results
with an explanation; this metadata does not prove a command ran or approve a merge.
Include every prerequisite from the current catalogue, each with `id`, `status`
and `evidence`. Do not put secrets or full private logs in the block.

```solver-ai-evidence
{
  "schema_version": 1,
  "backlog_id": "",
  "execution_order": 0,
  "head_revision": "",
  "prerequisites": [],
  "before": "",
  "after": "",
  "changed_paths": [],
  "checks": [
    {"command": "", "outcome": "", "evidence": ""}
  ],
  "security_data_impact": "",
  "rollback": "",
  "limitations": "",
  "review_requested": false
}
```

## Machine-readable evidence

Fill exactly one block below using the [evidence contract](../docs/engineering/PR_EVIDENCE.md).
The head revision is the PR head commit, not GitHub's synthetic merge SHA.
Use `not-run` with an honest reason when a check was not executed.

```solver-ai-evidence
{
  "schema_version": 1,
  "backlog_id": "",
  "execution_order": 0,
  "head_revision": "",
  "prerequisites": [],
  "before": "",
  "after": "",
  "changed_paths": [],
  "checks": [{"command": "", "outcome": "", "evidence": ""}],
  "security_data_impact": "",
  "rollback": "",
  "limitations": "",
  "review_requested": false
}
```

## Scope and implementation

Summarize code/docs changes; state what is intentionally deferred.

## Verification

List exact commands and observed results. If tests were not run, say why. Distinguish mocked from real components.
Include the tested head revision and passed, failed, skipped and unrun outcomes.

## Security / licenses / privacy

Describe any new dependencies, problem content, data handling, code execution or model integration. Confirm no secrets/private tests were committed.

## Documentation and project status

- [ ] README / docs updated as relevant
- [ ] docs/status/PROJECT_STATUS.md reflects actual verified state
- [ ] Tests and deployment notes included when behavior changes
- [ ] License/attribution requirements considered
- [ ] Scope matches one assigned backlog task; no competing implementation introduced
- [ ] Review requested; contributor has not self-merged
